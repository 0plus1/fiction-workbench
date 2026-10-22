# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Download the model slop profiles displayed on EQBench Creative Writing v3.

Run: uv run download_eqbench_slop.py
Source: https://eqbench.com/creative_writing.html
Uses only the Python standard library; never evaluates upstream JavaScript.
"""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


PAGE_URL = "https://eqbench.com/creative_writing.html"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "slop_profiles"
SECTIONS = {
    "Top Repetitive Words": "top_repetitive_words",
    "Top Repetitive Phrases": "top_repetitive_phrases",
    "Top Bigrams": "top_bigrams",
    "Top Trigrams": "top_trigrams",
}


class ScriptSources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            source = dict(attrs).get("src")
            if source:
                self.sources.append(source)


def discover_data_url(page_html, page_url=PAGE_URL):
    parser = ScriptSources()
    parser.feed(page_html)
    matches = [urljoin(page_url, source) for source in parser.sources
               if Path(urlsplit(source).path).name == "creative_writing.js"]
    if len(matches) != 1:
        raise ValueError("Expected exactly one creative_writing.js script on the source page.")
    return matches[0]


def template_literal(javascript, name):
    match = re.search(
        r"\b(?:const|let|var)\s+" + re.escape(name)
        + r"\s*=\s*`((?:\\.|[^`\\])*)`", javascript, re.DOTALL,
    )
    if not match:
        raise ValueError(f"Missing upstream JavaScript template: {name}")
    value = match[1]
    # Current upstream data is literal HTML/CSV. Fail visibly if this changes,
    # rather than executing code or silently misinterpreting JS string escapes.
    if "\\" in value or "${" in value:
        raise ValueError(f"Unsupported escapes/interpolation in upstream template: {name}")
    return value


class ProfileParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = {}
        self.section = None
        self.heading = None
        self.item = None

    def handle_starttag(self, tag, attrs):
        if tag == "h4":
            self.heading = []
        elif tag == "span":
            classes = set((dict(attrs).get("class") or "").split())
            if classes & {"slop-word-item", "slop-ngram-item"}:
                if self.section is None:
                    raise ValueError("Profile item appeared outside a recognised section.")
                self.item = []

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
        if self.item is not None:
            self.item.append(data)

    def handle_endtag(self, tag):
        if tag == "h4" and self.heading is not None:
            title = "".join(self.heading).strip()
            self.heading = None
            self.section = SECTIONS.get(title)
            if self.section:
                if self.section in self.sections:
                    raise ValueError(f"Duplicate profile section: {title}")
                self.sections[self.section] = []
        elif tag == "span" and self.item is not None:
            displayed = "".join(self.item).strip()
            self.item = None
            if not displayed:
                raise ValueError("Empty profile item.")
            count = None
            text = displayed
            if self.section != "top_repetitive_words":
                match = re.fullmatch(r"(.+)\s+\((\d+)\)", displayed, re.DOTALL)
                if not match:
                    raise ValueError(f"Missing count in profile item: {displayed}")
                text, count = match[1], int(match[2])
            self.sections[self.section].append({"text": text, "count": count})


def parse_profiles(javascript):
    leaderboard = template_literal(javascript, "leaderboardDataCreativeWritingV3")
    rows = list(csv.DictReader(io.StringIO(leaderboard.strip())))
    # A leading asterisk is a display marker, not part of a model identifier.
    models = [row["model_name"].strip().lstrip("*") for row in rows]
    if not models or any(not name for name in models) or len(set(models)) != len(models):
        raise ValueError("Missing or duplicate leaderboard model identifiers.")

    slop = template_literal(javascript, "slopData")
    headings = list(re.finditer(r"^#####\s+([^\r\n]+)\s*$", slop, re.MULTILINE))
    profiles = {}
    for index, heading in enumerate(headings):
        name = heading[1].strip()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(slop)
        parser = ProfileParser()
        parser.feed(slop[heading.end():end])
        parser.close()
        if name in profiles:
            raise ValueError(f"Duplicate model profile: {name}")
        if set(parser.sections) != set(SECTIONS.values()):
            raise ValueError(f"Incomplete profile sections for {name}")
        profiles[name] = parser.sections
    missing = set(models) - profiles.keys()
    extra = profiles.keys() - set(models)
    if missing or extra:
        raise ValueError(f"Leaderboard/profile mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    return {name: profiles[name] for name in models}


def profile_filename(model_name):
    slug = re.sub(r"[^a-z0-9]+", "-", model_name.lower()).strip("-")[:100] or "model"
    digest = hashlib.sha256(model_name.encode()).hexdigest()[:12]
    return f"{slug}--{digest}.json"


def fetch(url, timeout):
    request = Request(url, headers={"User-Agent": "fiction-workbench-eqbench-downloader/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read(), response.geturl()


def write_json(path, value):
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def save_profiles(output, profiles, source):
    # Only prune files recorded by an earlier run of this downloader. Never
    # delete unrelated files, even when a model vanishes from the leaderboard.
    previous_files = set()
    manifest_path = output / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if previous.get("schema_version") != 1:
            raise ValueError("Unsupported existing output manifest; choose a new output directory.")
        for entry in previous["models"]:
            if entry["file"] != profile_filename(entry["model_name"]):
                raise ValueError("Unexpected filename in existing output manifest.")
            previous_files.add(entry["file"])

    output.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, sections in profiles.items():
        filename = profile_filename(name)
        write_json(output / filename, {
            "schema_version": 1, "model_name": name, "source": source, **sections,
        })
        entries.append({"model_name": name, "file": filename})
    current_files = {entry["file"] for entry in entries}
    for stale in previous_files - current_files:
        (output / stale).unlink(missing_ok=True)
    write_json(manifest_path, {
        "schema_version": 1, "source": source, "model_count": len(entries), "models": entries,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT,
                        help="Destination directory (default: slop_profiles/ beside this script)")
    parser.add_argument("--timeout", type=float, default=30, help="HTTP timeout in seconds (default: 30)")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        page_bytes, page_url = fetch(PAGE_URL, args.timeout)
        data_url = discover_data_url(page_bytes.decode("utf-8"), page_url)
        javascript, resolved_data_url = fetch(data_url, args.timeout)
        profiles = parse_profiles(javascript.decode("utf-8"))
        source = {
            "page_url": page_url,
            "data_url": data_url,
            "resolved_data_url": resolved_data_url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "data_sha256": hashlib.sha256(javascript).hexdigest(),
        }
        save_profiles(args.output_dir, profiles, source)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1
    print(f"Downloaded {len(profiles)} model profiles to {args.output_dir.resolve()}")
    print(f"Source: {data_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
