"""Local-only delivery checks for the project-report artifact helper."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SAVER = Path(__file__).resolve().parents[1] / "project-report" / "assets" / "save_report.py"
spec = importlib.util.spec_from_file_location("save_report", SAVER)
assert spec is not None and spec.loader is not None
save_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(save_report)


class ReportDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.source = self.directory / "private-draft.md"
        self.source.write_text("# Report\n\nNo qualifying evidence was found. [CAM-900](https://example.atlassian.net/browse/CAM-900)\n")
        self.generated = datetime(2026, 11, 11, 15, 0, tzinfo=timezone.utc)

    def test_repeat_runs_preserve_existing_files_and_write_complete_text(self):
        destination = self.directory / "reports"
        args = (self.source, destination, "CAM-900", "2026-10-01", "2026-10-31", "summary", self.generated)
        first = save_report.save_report(*args)
        second = save_report.save_report(*args)
        self.assertEqual(first.name, "CAM-900_2026-10-01_2026-10-31_summary_20261111T150000Z.md")
        self.assertEqual(second.name, "CAM-900_2026-10-01_2026-10-31_summary_20261111T150000Z_1.md")
        self.assertEqual(first.read_text(), self.source.read_text())
        self.assertEqual(second.read_text(), self.source.read_text())

    def test_unwritable_destination_fails_without_losing_report_text_or_existing_file(self):
        destination = self.directory / "already-a-file"
        destination.write_text("preserve me")
        result = subprocess.run(
            [sys.executable, str(SAVER), "CAM-900", "2026-10-01", "2026-10-31", "brief",
             "--source", str(self.source), "--destination", str(destination)],
            capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(result.stdout)
        self.assertIn("Report not saved", result.stderr)
        self.assertEqual(destination.read_text(), "preserve me")
        self.assertIn("No qualifying evidence was found", self.source.read_text())


if __name__ == "__main__":
    unittest.main()
