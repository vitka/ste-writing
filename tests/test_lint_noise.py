"""Regression checks for false positives and silently skipped edit targets."""

import json
from pathlib import Path
import runpy
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ste-lint.py"
lint = runpy.run_path(str(SCRIPT))["lint"]


class NoiseTests(unittest.TestCase):
    def test_filler_is_counted_once(self):
        result = lint("It is important to note that the service runs.")
        self.assertEqual(result["house_style"]["filler"], 1)
        self.assertEqual(sum(result["house_style"].values()), 1)

    def test_nominalization_is_counted_once_without_flagging_plain_nouns(self):
        for text, count in (
            ("Perform an inspection of the filter.", 1),
            ("Perform an analysis of the log.", 1),
            ("The configuration of the server is correct.", 0),
            ("The workers perform well.", 0),
        ):
            with self.subTest(text=text):
                self.assertEqual(lint(text)["review"]["nominalization"], count)

    def test_link_destinations_do_not_trigger_language_findings(self):
        for text in (
            "Read [the guide](https://example.com/provide/robust).",
            'Read [the guide](docs/provide_(robust).md "A seamless guide").',
            'Read [the guide](<docs/provide/robust> "Title with ) punctuation").',
            "Read [the guide][robust].\n\n[robust]: https://example.com/provide/robust",
            "Read <https://example.com/provide/robust>.",
            "Read https://example.com/provide/robust.",
        ):
            with self.subTest(text=text):
                result = lint(text)
                self.assertEqual(result["total"], 0)
                self.assertEqual(sum(result["house_style"].values()), 0)

    def test_visible_link_labels_still_get_checked(self):
        result = lint("Read [the robust guide](https://example.com/seamless).")
        self.assertEqual(result["house_style"]["marketing_adjective"], 1)
        self.assertEqual(result["sample_marketing"], ["robust"])

    def test_quoted_edit_targets_are_checked_by_default(self):
        for left, right in (("\"", "\""), ("“", "”"), ("'", "'"), ("‘", "’")):
            with self.subTest(left=left):
                text = left + "This robust tool runs; it is seamless." + right
                result = lint(text)
                self.assertFalse(result["quotes_excluded"])
                self.assertEqual(result["violations"]["semicolon"], 1)
                self.assertEqual(result["house_style"]["marketing_adjective"], 2)
                protected = lint(text, exclude_quotes=True)
                self.assertTrue(protected["quotes_excluded"])
                self.assertEqual(protected["words"], 0)
                self.assertEqual(protected["total"], 0)
                self.assertEqual(sum(protected["house_style"].values()), 0)

    def test_quote_exclusion_preserves_surrounding_prose_and_contractions(self):
        result = lint('The robust tool says "provide; seamless". It can\'t retry.', exclude_quotes=True)
        self.assertEqual(result["violations"]["semicolon"], 0)
        self.assertEqual(result["violations"]["contraction"], 1)
        self.assertEqual(result["sample_marketing"], ["robust"])

    def test_quoted_sentences_and_table_cells_are_separate(self):
        thirteen = "one two three four five six seven eight nine ten eleven twelve thirteen"
        for text in (
            f"| Left | Right |\n|---|---|\n| {thirteen} | {thirteen} |",
            f'"{thirteen.capitalize()}." "{thirteen.capitalize()}."',
        ):
            with self.subTest(text=text):
                self.assertEqual(lint(text)["violations"]["long_sentence(>25w)"], 0)
        long_cell = f"| Text |\n|---|\n| {thirteen} {thirteen} |"
        self.assertEqual(lint(long_cell)["violations"]["long_sentence(>25w)"], 1)

    def test_code_remains_excluded(self):
        for text in (
            "    provide();",
            "````text\n```\nprovide();\n```\n````",
            "Read `provide(robust);`.",
        ):
            with self.subTest(text=text):
                result = lint(text)
                self.assertEqual(result["total"], 0)
                self.assertEqual(sum(result["house_style"].values()), 0)

    def test_cli_quote_exclusion_is_explicit(self):
        for flags, expected_exit, excluded in (([], 1, False), (["--exclude-quotes"], 0, True)):
            with self.subTest(flags=flags):
                run = subprocess.run(
                    [sys.executable, str(SCRIPT), "--json", "--fail-over", "0", *flags],
                    input='"Read the file; then retry."', text=True, capture_output=True,
                )
                self.assertEqual(run.returncode, expected_exit, run.stderr)
                self.assertEqual(json.loads(run.stdout)["quotes_excluded"], excluded)


if __name__ == "__main__":
    unittest.main()
