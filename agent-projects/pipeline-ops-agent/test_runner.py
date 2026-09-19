import json
import tempfile
import unittest
from pathlib import Path

from runner import load_plugins, run_tool


class RunnerTests(unittest.TestCase):
    def test_failed_run_has_quality_evidence(self):
        status = run_tool("run_status", {"run_id": "R-002"})
        checks = run_tool("quality_checks", {"run_id": "R-002"})
        self.assertEqual(status["result"]["status"], "FAILED")
        self.assertEqual(checks["result"]["failed"], 2)

    def test_unknown_tool_and_arguments_rejected(self):
        with self.assertRaises(ValueError):
            run_tool("delete_files", {"path": "/"})
        with self.assertRaises(ValueError):
            run_tool("run_status", {"run_id": "R-002", "path": "/"})

    def test_invalid_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / "invalid"
            folder.mkdir()
            (folder / "manifest.json").write_text(json.dumps({"name": "bad-name", "inputs": []}))
            with self.assertRaises(ValueError):
                load_plugins(Path(temporary))


if __name__ == "__main__":
    unittest.main()
