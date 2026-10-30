"""Regression checks for preservation-aware scoring and CLI behavior."""

import json
from pathlib import Path
import runpy
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ste-lint.py"
lint = runpy.run_path(str(SCRIPT))["lint"]


class PreservationTests(unittest.TestCase):
    def test_modal_meaning_has_no_score_penalty(self):
        for strict in (False, True):
            for text in (
                "The request may have failed.",
                "The request MIGHT NOT HAVE FAILED.",
                "The job could\n  have run.",
                "The job will have completed by then.",
                "You should restart the service.",
                "The client shall send the header.",
            ):
                with self.subTest(strict=strict, text=text):
                    result = lint(text, strict)
                    self.assertEqual(result["total"], 0)
                    self.assertEqual(result["review"]["complex_tense"], 0)
                    self.assertEqual(sum(result["house_style"].values()), 0)

    def test_contracted_modals_only_need_contraction_expansion(self):
        for modal in ("couldn't", "can’t", "won't", "shouldn't"):
            with self.subTest(modal=modal):
                result = lint(f"The task {modal} have failed.", strict=True)
                self.assertEqual(result["total"], 1)
                self.assertEqual(result["violations"]["contraction"], 1)
                self.assertEqual(result["review"]["complex_tense"], 0)

    def test_tense_and_passive_need_context_not_score_penalties(self):
        result = lint("The job has completed. The file was deleted.")
        self.assertGreater(result["review"]["complex_tense"], 0)
        self.assertGreater(result["review"]["passive_voice"], 0)
        self.assertEqual(result["total"], 0)

    def test_house_style_and_strict_vocabulary_are_separate(self):
        text = "However, we provide robust tools—use them."
        for strict in (False, True):
            with self.subTest(strict=strict):
                result = lint(text, strict)
                self.assertEqual(result["total"], 0)
                self.assertEqual(result["house_style"]["word_choice"], 1)
                self.assertEqual(result["house_style"]["marketing_adjective"], 1)
                self.assertEqual(result["house_style"]["em_dash"], 1)
                self.assertEqual(result["review"].get("strict_word_choice", 0), int(strict))

    def test_preservation_does_not_hide_mechanical_findings(self):
        result = lint("The request may have failed; retry it.", strict=True)
        self.assertEqual(result["violations"]["semicolon"], 1)
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["review"]["complex_tense"], 0)

    def test_cli_threshold_uses_only_mechanical_score(self):
        for text, expected_exit in (
            ("The request may have failed. You should retry.", 0),
            ("However, we provide robust tools—use them.", 0),
            ("The request may have failed; retry it.", 1),
        ):
            with self.subTest(text=text):
                run = subprocess.run(
                    [sys.executable, str(SCRIPT), "--strict", "--json", "--fail-over", "0"],
                    input=text, text=True, capture_output=True,
                )
                self.assertEqual(run.returncode, expected_exit, run.stderr)
                result = json.loads(run.stdout)
                self.assertEqual(result["score_version"], 3)
                self.assertEqual(result["total"], sum(result["violations"].values()))
                self.assertIn("review", result)
                self.assertIn("house_style", result)


if __name__ == "__main__":
    unittest.main()
