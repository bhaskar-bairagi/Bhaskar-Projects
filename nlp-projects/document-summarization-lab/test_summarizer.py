import unittest

from summarizer import evaluate, summarize


class SummarizerTests(unittest.TestCase):
    def test_extracts_only_original_sentences(self):
        source = "Alpha was delayed. Beta was loaded. Gamma was checked."
        for method in ("lead", "frequency"):
            result = summarize(source, method, 2)
            self.assertTrue(evaluate(source, result, ["loaded"])["source_sentence_support"])

    def test_coverage_and_unsupported_claim(self):
        metrics = evaluate("Five rows failed. The report paused.", "Five rows failed.", ["five", "paused"])
        self.assertEqual(metrics["key_term_coverage"], 0.5)
        self.assertFalse(evaluate("Five rows failed.", "Everything succeeded.", [])["source_sentence_support"])

    def test_invalid_method_and_empty_source(self):
        with self.assertRaises(ValueError):
            summarize("One sentence.", "unknown")
        with self.assertRaises(ValueError):
            summarize("", "lead")


if __name__ == "__main__":
    unittest.main()
