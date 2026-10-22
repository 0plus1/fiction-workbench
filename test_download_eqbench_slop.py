"""Offline regression checks: uv run --no-project python -m unittest -v test_download_eqbench_slop.py"""

import json
from pathlib import Path
import tempfile
import unittest

from download_eqbench_slop import (
    discover_data_url, parse_profiles, profile_filename, save_profiles, template_literal,
)


def profile_html():
    return """<h4>Most Similar To:</h4><div>Another model</div>
<h4>Top Repetitive Words</h4>
<span class='slop-word-item'>needn&#x27;t</span>
<span class='slop-word-item'>Mara</span>
<h4>Top Repetitive Phrases</h4>
<span class='slop-word-item'>Twelve years ago (2)</span>
<span class='slop-word-item'>twelve years ago (1)</span>
<h4>Top Bigrams</h4>
<span class='slop-ngram-item'>asked whether (22)</span>
<h4>Top Trigrams</h4>
<span class='slop-ngram-item'>could decide whether (3)</span>
"""


def javascript(names=("vendor/model", "other-model")):
    leaderboard = "model_name,slop_score\n" + "\n".join(f"*{name},8.4" for name in names)
    slop = "\n".join(f"##### {name}\n{profile_html()}" for name in names)
    return (f"let leaderboardDataCreativeWritingV3 = `{leaderboard}`;\n"
            f"const slopData = `{slop}`;")


class DownloaderTests(unittest.TestCase):
    def test_discovers_versioned_script_from_page(self):
        page = '<script src="utils.js"></script><script src="creative_writing.js?v=next&amp;x=1"></script>'
        self.assertEqual(discover_data_url(page), "https://eqbench.com/creative_writing.js?v=next&x=1")
        for page in ("", '<script src="creative_writing.js"></script>' * 2):
            with self.assertRaises(ValueError):
                discover_data_url(page)

    def test_preserves_all_four_lists_order_case_entities_and_counts(self):
        profiles = parse_profiles(javascript())
        self.assertEqual(list(profiles), ["vendor/model", "other-model"])
        profile = profiles["vendor/model"]
        self.assertEqual(profile["top_repetitive_words"], [
            {"text": "needn't", "count": None}, {"text": "Mara", "count": None},
        ])
        self.assertEqual(profile["top_repetitive_phrases"], [
            {"text": "Twelve years ago", "count": 2},
            {"text": "twelve years ago", "count": 1},
        ])
        self.assertEqual(profile["top_bigrams"], [{"text": "asked whether", "count": 22}])
        self.assertEqual(profile["top_trigrams"], [{"text": "could decide whether", "count": 3}])

    def test_empty_list_is_valid_but_missing_section_is_not(self):
        source = javascript().replace("<span class='slop-ngram-item'>could decide whether (3)</span>", "")
        self.assertEqual(parse_profiles(source)["vendor/model"]["top_trigrams"], [])
        with self.assertRaises(ValueError):
            parse_profiles(source.replace("<h4>Top Trigrams</h4>", ""))

    def test_rejects_missing_counts_and_duplicate_models(self):
        for source in (javascript().replace("asked whether (22)", "asked whether"),
                       javascript(("same", "same"))):
            with self.assertRaises(ValueError):
                parse_profiles(source)

    def test_rejects_leaderboard_profile_mismatch(self):
        source = javascript().replace("##### other-model", "##### unexpected-model")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            parse_profiles(source)

    def test_does_not_execute_or_guess_dynamic_javascript(self):
        for source in ('const slopData = `${danger()}`;', r'const slopData = `a\nb`;'):
            with self.assertRaises(ValueError):
                template_literal(source, "slopData")

    def test_safe_distinct_filenames(self):
        names = ["vendor/model", "vendor-model", "Vendor/Model", "../../outside", "x" * 500]
        filenames = [profile_filename(name) for name in names]
        self.assertEqual(len(set(filenames)), len(names))
        for filename in filenames:
            self.assertEqual(Path(filename).name, filename)
            self.assertLess(len(filename), 255)

    def test_refresh_prunes_only_previously_recorded_models(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "profiles"
            source = {"page_url": "https://eqbench.com/creative_writing.html"}
            save_profiles(output, parse_profiles(javascript()), source)
            unrelated = output / "my-notes.json"
            unrelated.write_text("{}")
            save_profiles(output, parse_profiles(javascript(("other-model",))), source)
            self.assertFalse((output / profile_filename("vendor/model")).exists())
            self.assertTrue(unrelated.exists())
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["model_count"], 1)
            saved = json.loads((output / manifest["models"][0]["file"]).read_text())
            self.assertEqual(saved["source"], source)
            self.assertEqual(saved["model_name"], "other-model")


if __name__ == "__main__":
    unittest.main()
