# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build the committed constraint profile from downloaded EQBench model profiles.

Run: uv run generate_constraint_profile.py
Refresh inputs first with: uv run download_eqbench_slop.py
"""

import argparse
from collections import defaultdict
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
import math
from pathlib import Path
import sys

from download_eqbench_slop import DEFAULT_OUTPUT, SECTIONS, profile_filename, write_json


DEFAULT_PROFILE = (Path(__file__).resolve().parent / "skills" / "fiction-workbench"
                   / "references" / "constraint-profile.json")
CATEGORIES = tuple(SECTIONS.values())


def normalize(text):
    """Use the same duplicate key as the skill's literal constraint checker."""
    return " ".join(text.casefold().replace("’", "'").split())


def load_downloads(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported download manifest schema.")
    entries = manifest["models"]
    if not entries or manifest["model_count"] != len(entries):
        raise ValueError("Download manifest must list every model exactly once.")
    profiles = []
    seen = set()
    for entry in entries:
        name = entry["model_name"]
        if name in seen or entry["file"] != profile_filename(name):
            raise ValueError(f"Duplicate model or unexpected profile filename: {name}")
        seen.add(name)
        profile = json.loads((directory / entry["file"]).read_text(encoding="utf-8"))
        if (profile["schema_version"] != 1 or profile["model_name"] != name
                or profile["source"] != manifest["source"]):
            raise ValueError(f"Model profile does not match its manifest: {name}")
        for category in CATEGORIES:
            if not isinstance(profile[category], list):
                raise ValueError(f"Invalid list for {name}: {category}")
            for item in profile[category]:
                if not isinstance(item["text"], str) or not normalize(item["text"]):
                    raise ValueError(f"Empty or invalid entry for {name}: {category}")
                count = item["count"]
                if category == "top_repetitive_words":
                    valid_count = count is None
                else:
                    valid_count = type(count) is int and count >= 0
                if not valid_count:
                    raise ValueError(f"Invalid reported count for {name}: {category}")
        profiles.append(profile)
    return profiles, manifest["source"]


def generate_profile(profiles, source, min_model_fraction=0.1):
    if not math.isfinite(min_model_fraction) or not 0 < min_model_fraction <= 1:
        raise ValueError("Minimum model fraction must be greater than 0 and at most 1.")
    names = [profile["model_name"] for profile in profiles]
    if not names or len(set(names)) != len(names):
        raise ValueError("Input must contain distinct model profiles.")
    model_count = len(profiles)
    # Decimal avoids rounding 7% of 100 to 7.000000000000001 and then 8.
    minimum = int((Decimal(str(min_model_fraction)) * model_count).to_integral_value(rounding=ROUND_CEILING))
    categories = {}
    selected_models = defaultdict(set)
    for category in CATEGORIES:
        models_by_term = defaultdict(set)
        totals = defaultdict(int)
        for profile in profiles:
            for item in profile[category]:
                term = normalize(item["text"])
                models_by_term[term].add(profile["model_name"])
                if item["count"] is not None:
                    totals[term] += item["count"]
        selected = [term for term, models in models_by_term.items() if len(models) >= minimum]
        selected.sort(key=lambda term: (-len(models_by_term[term]), term))
        categories[category] = []
        for term in selected:
            models = models_by_term[term]
            selected_models[term].update(models)
            categories[category].append({
                "text": term,
                "model_count": len(models),
                "model_fraction": round(len(models) / model_count, 6),
                "reported_count_total": None if category == "top_repetitive_words" else totals[term],
            })
    hard = sorted(selected_models, key=lambda term: (-len(selected_models[term]), term))
    if not hard:
        raise ValueError("No entries meet the threshold; the existing profile was not replaced.")
    # Hash the semantic input in model order independent of the leaderboard.
    inputs = [{"model_name": profile["model_name"],
               **{category: profile[category] for category in CATEGORIES}}
              for profile in sorted(profiles, key=lambda profile: profile["model_name"])]
    fingerprint = hashlib.sha256(json.dumps(
        inputs, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
    ).encode()).hexdigest()
    return {
        "name": "eqbench-cross-model-slop",
        "hard": hard,
        "review": [],
        "metadata": {
            "generator": "generate_constraint_profile.py",
            "source": source,
            "input_profiles_sha256": fingerprint,
            "model_count": model_count,
            "selection": {
                "min_model_fraction": min_model_fraction,
                "min_model_count": minimum,
                "rule": "Include entries meeting the threshold in any one source category.",
                "ranking": "Distinct model count descending, then text alphabetically; each model has equal weight.",
                "normalization": "Casefold, convert curly apostrophes to straight, collapse whitespace; preserve punctuation and n-gram wording.",
                "deduplication": "One vote per model per entry; merge selected entries across categories into hard.",
            },
            "hard_entry_count": len(hard),
            "categories": categories,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_OUTPUT,
                        help="Downloaded EQBench profiles (default: repository slop_profiles/)")
    parser.add_argument("--output", type=Path, default=DEFAULT_PROFILE,
                        help="Profile JSON to replace (default: skill references/constraint-profile.json)")
    parser.add_argument("--min-model-fraction", type=float, default=0.1,
                        help="Minimum share of models listing an entry in a category (default: 0.1)")
    args = parser.parse_args()
    try:
        profiles, source = load_downloads(args.input_dir)
        result = generate_profile(profiles, source, args.min_model_fraction)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.output, result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {len(result['hard'])} hard bans from {len(profiles)} models to {args.output.resolve()}")
    for category, entries in result["metadata"]["categories"].items():
        print(f"  {category}: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
