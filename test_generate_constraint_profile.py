"""Offline aggregation and checker compatibility tests."""

from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from download_eqbench_slop import save_profiles
from generate_constraint_profile import CATEGORIES, generate_profile, load_downloads, main


SOURCE = {"page_url": "https://eqbench.com/creative_writing.html", "data_sha256": "fixture"}
CHECKER = Path(__file__).resolve().parent / "skills/fiction-workbench/scripts/constraint_check.py"


def model(name, words=(), phrases=(), bigrams=(), trigrams=()):
    return {
        "model_name": name,
        "top_repetitive_words": [{"text": text, "count": None} for text in words],
        **{category: [{"text": text, "count": count} for text, count in entries]
           for category, entries in zip(CATEGORIES[1:], (phrases, bigrams, trigrams))},
    }


class GeneratorTests(unittest.TestCase):
    def test_prevalence_outweighs_occurrences_and_uses_ceiling(self):
        profiles = [model(str(i), words=("shared",) if i < 2 else (),
                          phrases=(("rare phrase", 100000),) if i == 0 else ())
                    for i in range(11)]
        result = generate_profile(profiles, SOURCE)
        self.assertEqual(result["hard"], ["shared"])
        self.assertEqual(result["metadata"]["selection"]["min_model_count"], 2)
        self.assertEqual(result["metadata"]["categories"][CATEGORIES[0]][0]["model_count"], 2)

    def test_case_apostrophe_whitespace_variants_get_one_vote_per_model(self):
        profiles = [model("first", phrases=(("Couldn’t   wait", 2), ("couldn't wait", 3))),
                    model("second", phrases=(("COULDN'T WAIT", 1),))]
        result = generate_profile(profiles, SOURCE, 1)
        evidence = result["metadata"]["categories"]["top_repetitive_phrases"][0]
        self.assertEqual(result["hard"], ["couldn't wait"])
        self.assertEqual(evidence["model_count"], 2)
        self.assertEqual(evidence["reported_count_total"], 6)

    def test_exact_percentage_boundary_is_not_rounded_up_twice(self):
        profiles = [model(str(i), words=("shared",) if i < 7 else ()) for i in range(100)]
        result = generate_profile(profiles, SOURCE, 0.07)
        self.assertEqual(result["hard"], ["shared"])
        self.assertEqual(result["metadata"]["selection"]["min_model_count"], 7)

    def test_all_categories_contribute_and_cross_category_terms_are_deduplicated(self):
        profiles = [model("one", words=("flickered",), phrases=(("one last time", 2),),
                          bigrams=(("said nothing", 4),), trigrams=(("one last time", 3),))]
        result = generate_profile(profiles, SOURCE)
        self.assertEqual(set(result["hard"]), {"flickered", "one last time", "said nothing"})
        self.assertEqual(len(result["hard"]), 3)
        self.assertTrue(all(result["metadata"]["categories"].values()))
        self.assertEqual(result["review"], [])

    def test_support_cannot_be_added_across_categories_to_reach_threshold(self):
        profiles = [model("one", words=("shared",), phrases=(("cross list term", 1),)),
                    model("two", words=("shared",), trigrams=(("cross list term", 1),)),
                    model("three", words=("shared",))]
        self.assertEqual(generate_profile(profiles, SOURCE, 0.5)["hard"], ["shared"])

    def test_model_order_does_not_change_output_and_punctuation_is_preserved(self):
        profiles = [model("a", phrases=(("something else, something", 1),)),
                    model("b", phrases=(("something else something", 1),))]
        first = generate_profile(profiles, SOURCE)
        second = generate_profile(list(reversed(profiles)), SOURCE)
        self.assertEqual(json.dumps(first), json.dumps(second))
        self.assertEqual(set(first["hard"]), {"something else, something", "something else something"})

    def test_rejects_invalid_thresholds_empty_results_and_duplicate_models(self):
        profiles = [model("a", words=("shared",))]
        for fraction in (0, -1, 1.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                generate_profile(profiles, SOURCE, fraction)
        for inputs in ([], profiles * 2, [model("empty")]):
            with self.assertRaises(ValueError):
                generate_profile(inputs, SOURCE)

    def test_reads_manifest_models_only_and_rejects_incomplete_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = model("a", words=("flickered",))
            save_profiles(root, {"a": {key: profile[key] for key in CATEGORIES}}, SOURCE)
            (root / "unlisted.json").write_text("invalid json")
            profiles, source = load_downloads(root)
            self.assertEqual(profiles[0]["model_name"], "a")
            self.assertEqual(source, SOURCE)
            manifest = json.loads((root / "manifest.json").read_text())
            (root / manifest["models"][0]["file"]).unlink()
            with self.assertRaises(OSError):
                load_downloads(root)

    def test_cli_preserves_existing_output_when_input_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "profile.json"
            output.write_text("previous profile")
            args = ["generate_constraint_profile.py", "--input-dir", str(Path(directory) / "missing"),
                    "--output", str(output)]
            with patch.object(sys, "argv", args), redirect_stderr(io.StringIO()):
                self.assertEqual(main(), 1)
            self.assertEqual(output.read_text(), "previous profile")

    def test_generated_metadata_and_legacy_profiles_work_with_checker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "candidate.md"
            target.write_text("The light flickered.\n")
            path = root / "profile.json"
            generated = generate_profile([model("a", words=("flickered",))], SOURCE)
            legacy = {key: generated[key] for key in ("name", "hard", "review")}
            for profile in (generated, legacy):
                path.write_text(json.dumps(profile))
                result = subprocess.run([sys.executable, "-B", str(CHECKER), str(target),
                                         "--profile", str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(json.loads(result.stdout)["hard_matches"], 1)
            generated["metadata"] = "invalid"
            path.write_text(json.dumps(generated))
            result = subprocess.run([sys.executable, "-B", str(CHECKER), str(target),
                                     "--profile", str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
