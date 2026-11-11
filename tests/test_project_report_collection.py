"""Black-box checks for the project-report evidence collector CLI."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


COLLECTOR = Path(__file__).resolve().parents[1] / "project-report" / "assets" / "collect_evidence.py"
FAKE_CURL = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit

args = sys.argv[1:]
with Path(os.environ["CALL_LOG"]).open("a") as log:
    log.write(json.dumps(args) + "\n")
params = dict(arg.split("=", 1) for i, arg in enumerate(args) if i and args[i - 1] == "--data-urlencode")
path = urlsplit(args[-1]).path
if path.endswith("/myself"):
    result = {"timeZone": "America/New_York"}
elif path.endswith("/search/jql"):
    jql = params["jql"]
    if "CAM-900" in jql:
        if "nextPageToken" not in params:
            result = {"issues": [{"key": "CAM-901"}], "isLast": False}
            if not os.environ.get("BROKEN_PAGE"):
                result["nextPageToken"] = "next"
        else:
            result = {"issues": [{"key": "CAM-902"}], "isLast": True}
    elif "CAM-901" in jql:
        result = {"issues": [{"key": "CAM-903"}], "isLast": True}
    else:
        result = {"issues": [], "isLast": True}
elif "/issue/" in path:
    suffix = path.split("/issue/", 1)[1]
    key = suffix.split("/", 1)[0]
    if suffix.endswith("/comment") or suffix.endswith("/changelog"):
        is_comment = suffix.endswith("/comment")
        entry = ({"id": "100", "created": "2026-03-08T12:00:00.000+0000", "body": {"type": "doc", "version": 1, "content": []}} if is_comment
                 else {"id": "100", "created": "2026-03-08T12:00:00.000+0000", "items": [{"field": "status", "fromString": "To Do", "toString": "Done"}]})
        item_key = "comments" if is_comment else "values"
        start = int(params.get("startAt", 0))
        result = {item_key: [dict(entry, id=str(100 + start))] if start < 2 else [], "startAt": start, "maxResults": 100, "total": 2}
    else:
        result = {"key": key, "fields": {"summary": key, "issuetype": {"name": "Epic" if key == "CAM-900" else "Sub-task" if key == "CAM-903" else "Story"},
                  "parent": None if key == "CAM-900" else {"key": "CAM-901" if key == "CAM-903" else "CAM-900"},
                  "created": "2026-03-01T10:00:00.000+0000", "status": {"name": "Done"}, "issuelinks": [{"outwardIssue": {"key": "CAM-999"}}]}}
else:
    sys.exit(7)
print(json.dumps(result))
'''


class CollectorCLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        curl = self.directory / "curl"
        curl.write_text(FAKE_CURL)
        curl.chmod(0o700)
        self.netrc = self.directory / "netrc"
        self.netrc.write_text("machine example.atlassian.net login test password dummy\n")
        self.netrc.chmod(0o600)
        self.log = self.directory / "calls.jsonl"
        self.env = dict(os.environ, PATH=f"{self.directory}{os.pathsep}{os.environ['PATH']}", CALL_LOG=str(self.log))

    def run_collector(self, start="2026-03-07", end="2026-03-08", *extra):
        return subprocess.run(
            [sys.executable, str(COLLECTOR), "CAM-900", start, end,
             "--site", "example.atlassian.net", "--netrc-file", str(self.netrc), *extra],
            env=self.env, text=True, capture_output=True, check=False,
        )

    def test_paginates_nested_descendants_comments_and_changes_without_following_links(self):
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]], ["CAM-901", "CAM-902", "CAM-903"])
        self.assertEqual(len(evidence["items"][0]["comments"]), 2)
        self.assertEqual(len(evidence["items"][0]["changelog"]), 2)
        self.assertNotIn("dummy", result.stdout)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertTrue(all("--netrc-file" in call and "--get" in call for call in calls))
        self.assertFalse(any("CAM-999" in str(call) for call in calls))
        self.assertTrue(any("nextPageToken=next" in call for call in calls))
        self.assertTrue(any("startAt=1" in call for call in calls))

    def test_calendar_boundaries_use_timezone_offsets_not_fixed_utc_days(self):
        result = self.run_collector("2026-03-07", "2026-03-08", "--timezone", "America/New_York")
        self.assertEqual(result.returncode, 0, result.stderr)
        period = json.loads(result.stdout)["period"]
        self.assertEqual(period["start_utc"], "2026-03-07T05:00:00Z")
        self.assertEqual(period["end_exclusive_utc"], "2026-03-09T04:00:00Z")
        self.assertEqual(period["cutoff_utc"], "2026-03-09T04:00:00Z")
        self.assertFalse(period["provisional"])

    def test_today_is_provisional_and_future_or_reversed_periods_are_rejected(self):
        today = datetime.now(ZoneInfo("America/New_York")).date()
        result = self.run_collector(today.isoformat(), today.isoformat())
        self.assertEqual(result.returncode, 0, result.stderr)
        period = json.loads(result.stdout)["period"]
        self.assertTrue(period["provisional"])
        self.assertEqual(period["cutoff_utc"], period["retrieved_at_utc"])
        self.assertRegex(period["cutoff_utc"], r"\.\d{6}Z$")
        future = self.run_collector(today.isoformat(), (today + timedelta(days=1)).isoformat())
        self.assertNotEqual(future.returncode, 0)
        self.assertFalse(future.stdout)
        reversed_dates = self.run_collector("2026-03-08", "2026-03-07")
        self.assertNotEqual(reversed_dates.returncode, 0)
        self.assertFalse(reversed_dates.stdout)

    def test_incomplete_cursor_does_not_claim_complete_retrieval(self):
        self.env["BROKEN_PAGE"] = "1"
        result = self.run_collector()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(result.stdout)
        self.assertIn("nextPageToken", result.stderr)


if __name__ == "__main__":
    unittest.main()
