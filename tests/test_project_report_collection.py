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
    if os.environ.get("FAIL_SEARCH_PARENT", "never-a-parent") in jql and os.environ.get("FAIL_SEARCH_PAGE", "1") == ("2" if "nextPageToken" in params else "1"):
        sys.exit(22)
    if os.environ.get("EMPTY_SCOPE"):
        result = {"issues": [], "isLast": True}
    elif "CAM-900" in jql:
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
    if suffix == os.environ.get("FAIL_ISSUE"):
        sys.exit(22)
    if suffix.endswith("/comment") or suffix.endswith("/changelog"):
        is_comment = suffix.endswith("/comment")
        if suffix == os.environ.get("FAIL_ENDPOINT") and params.get("startAt") == os.environ.get("FAIL_OFFSET", "0"):
            sys.exit(22)
        entry = ({"id": "100", "created": "2026-03-08T12:00:00.000+0000", "updated": "2026-03-08T12:00:00.000+0000", "body": {"type": "doc", "version": 1, "content": []}} if is_comment
                 else {"id": "100", "created": "2026-03-08T12:00:00.000+0000", "items": [{"field": "status", "fromString": "To Do", "toString": "Done"}]})
        if os.environ.get("POST_CUTOFF_ISSUES"):
            entry["created"] = "2026-03-10T12:00:00.000+0000"
            if is_comment:
                entry["updated"] = entry["created"]
        item_key = "comments" if is_comment else "values"
        start = int(params.get("startAt", 0))
        if is_comment and start == 0 and key == "CAM-901":
            if os.environ.get("LATER_COMMENT"):
                entry["created"] = "2026-03-10T12:00:00.000+0000"
                entry["updated"] = entry["created"]
            if os.environ.get("EDITED_COMMENT"):
                entry["updated"] = "2026-03-10T12:00:00.000+0000"
        result = {item_key: [dict(entry, id=str(100 + start))] if start < 2 else [], "startAt": start, "maxResults": 100, "total": 2}
    else:
        fields = {"summary": key, "issuetype": {"name": "Epic" if key == "CAM-900" else "Sub-task" if key == "CAM-903" else "Story"},
                  "parent": None if key == "CAM-900" else {"key": "CAM-901" if key == "CAM-903" else "CAM-900"},
                  "created": "2026-03-01T10:00:00.000+0000", "status": {"name": "Done"}, "resolution": None,
                                    "resolutiondate": None, "assignee": None, "duedate": None, "customfield_10504": None,
                                    "description": None, "updated": "2026-03-08T12:00:00.000+0000",
                                    "issuelinks": [{"outwardIssue": {"key": "CAM-999"}}]}
        if key == os.environ.get("MISSING_FIELD_ISSUE"):
            fields.pop("created")
        if os.environ.get("POST_CUTOFF_ISSUES"):
            fields["created"] = "2026-03-10T10:00:00.000+0000"
        if key == os.environ.get("MOVED_ISSUE"):
            fields["parent"] = {"key": "CAM-999"}
        result = {"key": key, "fields": fields}
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
        self.assertEqual(evidence["items"][0]["excluded_comments"], [])
        self.assertEqual(len(evidence["items"][0]["changelog"]), 2)
        self.assertFalse(evidence["partial"])
        self.assertEqual(evidence["failures"], [])
        self.assertTrue(evidence["items"][0]["comments_complete"])
        self.assertTrue(evidence["items"][0]["changelog_complete"])
        self.assertIn("moved-out, deleted, or inaccessible work may be absent", evidence["coverage"])
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

    def test_post_cutoff_or_later_edited_comment_text_is_not_usable(self):
        for case in ("LATER_COMMENT", "EDITED_COMMENT"):
            with self.subTest(case=case):
                self.env[case] = "1"
                result = self.run_collector()
                self.assertEqual(result.returncode, 0, result.stderr)
                item = json.loads(result.stdout)["items"][0]
                self.assertEqual([comment["id"] for comment in item["comments"]], ["101"])
                self.assertEqual(item["excluded_comments"][0]["id"], "100")
                self.assertIn("cutoff", item["excluded_comments"][0]["reason"])
                self.assertNotIn("body", item["excluded_comments"][0])
                self.env.pop(case)

    def test_incomplete_cursor_keeps_known_children_and_marks_scope_partial(self):
        self.env["BROKEN_PAGE"] = "1"
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]], ["CAM-901", "CAM-903"])
        self.assertTrue(evidence["partial"])
        self.assertEqual(evidence["failures"][0]["key"], "CAM-900")
        self.assertEqual(evidence["failures"][0]["endpoint"], "children")
        self.assertEqual(evidence["failures"][0]["page"], 1)
        self.assertIn("nextPageToken", evidence["failures"][0]["reason"])

    def test_root_failure_and_first_search_failure_with_no_items_stop(self):
        self.env["FAIL_ISSUE"] = "CAM-900"
        root = self.run_collector()
        self.assertNotEqual(root.returncode, 0)
        self.assertFalse(root.stdout)
        self.assertIn("CAM-900", root.stderr)
        self.env.pop("FAIL_ISSUE")
        self.env["FAIL_SEARCH_PARENT"] = "CAM-900"
        no_descendants = self.run_collector()
        self.assertNotEqual(no_descendants.returncode, 0)
        self.assertFalse(no_descendants.stdout)
        self.assertIn("no usable cutoff evidence", no_descendants.stderr)

    def test_later_search_page_failure_keeps_first_page_and_names_gap(self):
        self.env.update(FAIL_SEARCH_PARENT="CAM-900", FAIL_SEARCH_PAGE="2")
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]], ["CAM-901", "CAM-903"])
        self.assertEqual(evidence["failures"][0]["page"], 2)
        self.assertTrue(evidence["partial"])

    def test_only_post_cutoff_issues_with_failed_discovery_cannot_support_a_report(self):
        self.env.update(POST_CUTOFF_ISSUES="1", FAIL_SEARCH_PARENT="CAM-900", FAIL_SEARCH_PAGE="2")
        result = self.run_collector()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(result.stdout)
        self.assertIn("no usable cutoff evidence", result.stderr)
        self.assertIn("CAM-900 children page 2", result.stderr)

    def test_inaccessible_issue_and_failed_comment_or_history_page_are_identified(self):
        self.env.update(FAIL_ISSUE="CAM-902", FAIL_ENDPOINT="CAM-901/changelog", FAIL_OFFSET="1")
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]], ["CAM-901", "CAM-903"])
        self.assertEqual(len(evidence["items"][0]["changelog"]), 1)
        self.assertFalse(evidence["items"][0]["changelog_complete"])
        self.assertTrue(evidence["items"][0]["comments_complete"])
        self.assertEqual([(gap["key"], gap["endpoint"], gap["page"]) for gap in evidence["failures"]],
                         [("CAM-901", "changelog", 2), ("CAM-902", "issue", None)])
        self.env.update(FAIL_ENDPOINT="CAM-901/comment", FAIL_OFFSET="0")
        comments = json.loads(self.run_collector().stdout)
        self.assertEqual(comments["items"][0]["comments"], [])
        self.assertFalse(comments["items"][0]["comments_complete"])

    def test_missing_historical_field_is_recorded_without_substitution(self):
        self.env["MISSING_FIELD_ISSUE"] = "CAM-901"
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertTrue(evidence["partial"])
        self.assertIn({"key": "CAM-901", "endpoint": "issue", "field": "created", "page": None,
                       "reason": "Requested field not returned; historical value unknown"}, evidence["failures"])
        self.assertNotIn("created", evidence["items"][0]["issue"]["fields"])

    def test_parent_changed_during_collection_is_not_reported_as_a_descendant(self):
        self.env["MOVED_ISSUE"] = "CAM-902"
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]], ["CAM-901", "CAM-903"])
        self.assertTrue(evidence["partial"])
        self.assertEqual(evidence["failures"][0]["key"], "CAM-902")
        self.assertEqual(evidence["failures"][0]["field"], "parent")
        self.assertIn("moved-out", evidence["coverage"])

    def test_successful_empty_scope_is_not_a_retrieval_failure(self):
        self.env["EMPTY_SCOPE"] = "1"
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual(evidence["items"], [])
        self.assertFalse(evidence["partial"])
        self.assertEqual(evidence["failures"], [])
        self.assertIn("moved-out, deleted", evidence["coverage"])


if __name__ == "__main__":
    unittest.main()
