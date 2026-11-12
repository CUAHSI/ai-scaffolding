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
if os.environ.get("REQUIRE_SIBLING_OVERLAP"):
    from time import monotonic, sleep
    sibling = None
    for key in ("CAM-901", "CAM-902"):
        if path.endswith(f"/issue/{key}"):
            sibling = ("issue", key)
        elif path.endswith("/search/jql") and params.get("jql") == f"parent = {key} ORDER BY key":
            sibling = ("children", key)
    if sibling:
        phase, key = sibling
        directory = Path(os.environ["CALL_LOG"]).parent
        (directory / f"{phase}-{key}").touch()
        other = "CAM-902" if key == "CAM-901" else "CAM-901"
        peer = directory / f"{phase}-{other}"
        deadline = monotonic() + 5
        while not peer.exists() and monotonic() < deadline:
            sleep(0.01)
        if not peer.exists():
            print(f"{phase} {key} did not overlap sibling", file=sys.stderr)
            sys.exit(22)
if path.endswith("/myself"):
    result = {"timeZone": "America/New_York"}
elif path.endswith("/search/jql"):
    jql = params["jql"]
    if os.environ.get("FAIL_SEARCH_PARENT", "never-a-parent") in jql and os.environ.get("FAIL_SEARCH_PAGE", "1") == ("2" if "nextPageToken" in params else "1"):
        sys.exit(22)
    if "labels =" in jql and os.environ.get("FAIL_LABEL_SEARCH_PAGE") == ("2" if "nextPageToken" in params else "1"):
        sys.exit(22)
    if os.environ.get("EMPTY_SCOPE"):
        result = {"issues": [], "isLast": True}
    elif "labels =" in jql:
        if os.environ.get("LABEL_NO_MATCH"):
            result = {"issues": [], "isLast": True}
        elif (os.environ.get("LABEL_TWO_PROJECTS") or os.environ.get("LABEL_AMBIGUOUS") or os.environ.get("LABEL_CROSS_PROJECTS") or os.environ.get("LABEL_DUPLICATE")) and "nextPageToken" in params:
            variant = "hydrofabric" if os.environ.get("LABEL_AMBIGUOUS") else "HydroFabric"
            key = "CAM-800" if os.environ.get("LABEL_DUPLICATE") else "HYDRO-20" if os.environ.get("LABEL_CROSS_PROJECTS") else "CAM-810"
            result = {"issues": [{"key": key, "fields": {"summary": "Second HydroFabric project", "labels": [variant], "issuetype": {"name": "Research Project"}}}], "isLast": True}
        else:
            result = {"issues": [{"key": "CAM-800", "fields": {"summary": "HydroFabric project", "labels": ["HydroFabric"], "issuetype": {"name": "Research Project"}}}],
                      "isLast": not bool(os.environ.get("LABEL_TWO_PROJECTS") or os.environ.get("LABEL_AMBIGUOUS") or os.environ.get("LABEL_CROSS_PROJECTS") or os.environ.get("LABEL_DUPLICATE"))}
            if os.environ.get("LABEL_AMBIGUOUS_FIRST"):
                result["issues"].append({"key": "CAM-810", "fields": {"summary": "Second HydroFabric project",
                                         "labels": ["hydrofabric"], "issuetype": {"name": "Research Project"}}})
                result["isLast"] = False
            if not result["isLast"]:
                result["nextPageToken"] = "next"
    elif os.environ.get("EMPTY_DESCENDANTS") and "parent =" in jql:
        result = {"issues": [], "isLast": True}
    elif "CAM-800" in jql:
        result = {"issues": [{"key": "CAM-801"}], "isLast": True}
    elif "HYDRO-20" in jql:
        result = {"issues": [{"key": "HYDRO-21"}], "isLast": True}
    elif "CAM-810" in jql:
        result = {"issues": [{"key": "CAM-811"}], "isLast": True}
    elif "CAM-811" in jql:
        result = {"issues": [{"key": "CAM-812"}], "isLast": True}
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
        issue_types = {"CAM-800": "Research Project", "CAM-810": "Research Project", "HYDRO-20": "Research Project",
                       "CAM-900": "Epic", "CAM-903": "Sub-task", "CAM-812": "Sub-task"}
        parents = {"CAM-801": "CAM-800", "HYDRO-21": "HYDRO-20", "CAM-811": "CAM-810",
                   "CAM-812": "CAM-811", "CAM-903": "CAM-901"}
        fields = {"summary": "HydroFabric project" if key == "CAM-800" else key,
                  "issuetype": {"name": issue_types.get(key, "Story")},
                  "parent": {"key": parents.get(key, "CAM-900")} if key not in ("CAM-800", "CAM-810", "CAM-900", "HYDRO-20") else None,
                  "created": "2026-03-01T10:00:00.000+0000", "status": {"name": "Done"}, "resolution": None,
                                    "resolutiondate": None, "assignee": None, "duedate": None, "customfield_10504": None,
                                    "description": None, "updated": "2026-03-08T12:00:00.000+0000",
                                    "labels": ["hydrofabric" if key == "CAM-810" and os.environ.get("LABEL_AMBIGUOUS") else "HydroFabric"] if key in ("CAM-800", "CAM-810", "HYDRO-20") else [],
                                    "issuelinks": [{"outwardIssue": {"key": "CAM-999"}}]}
        if key == os.environ.get("MISSING_FIELD_ISSUE"):
            fields.pop("created")
        if os.environ.get("POST_CUTOFF_ISSUES"):
            fields["created"] = "2026-03-10T10:00:00.000+0000"
        if key == os.environ.get("MOVED_ISSUE"):
            fields["parent"] = {"key": "CAM-999"}
        if key == os.environ.get("ROOT_LABEL_REMOVED"):
            fields["labels"] = []
        if "labels" not in params.get("fields", "").split(","):
            fields.pop("labels", None)
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

    def run_collector(self, start="2026-03-07", end="2026-03-08", *extra, selector="CAM-900"):
        return subprocess.run(
            [sys.executable, str(COLLECTOR), selector, start, end,
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

    def test_sibling_issue_and_child_search_gets_overlap_without_changing_evidence(self):
        self.env["REQUIRE_SIBLING_OVERLAP"] = "1"
        result = self.run_collector()
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(result.stdout)
        self.assertEqual([item["issue"]["key"] for item in evidence["items"]],
                         ["CAM-901", "CAM-902", "CAM-903"])
        self.assertFalse(evidence["partial"], evidence["failures"])
        for phase in ("issue", "children"):
            for key in ("CAM-901", "CAM-902"):
                self.assertTrue((self.directory / f"{phase}-{key}").exists())

    def test_label_selects_matching_research_project_and_retains_explicit_root_mode(self):
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="hydrofabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual(bundle["project_label"], "HydroFabric")
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertEqual([(item["issue"]["key"], item["reporting_root"]) for item in bundle["items"]],
                         [("CAM-801", "CAM-800")])
        self.assertFalse(bundle["partial"])
        self.assertIn("current label membership", bundle["coverage"].lower())
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        label_queries = [arg for call in calls for arg in call if arg.startswith("jql=") and "labels =" in arg]
        self.assertEqual(len(label_queries), 1)
        self.assertIn('project = CAM', label_queries[0])
        self.assertIn('issuetype = "Research Project"', label_queries[0])
        explicit = self.run_collector()
        self.assertEqual(explicit.returncode, 0)
        self.assertNotIn("labels", json.loads(explicit.stdout)["root"]["fields"])
        self.assertNotIn("labels", json.loads(explicit.stdout)["items"][0]["issue"]["fields"])

    def test_label_collects_all_project_search_pages_and_nested_descendants(self):
        self.env["LABEL_TWO_PROJECTS"] = "1"
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800", "CAM-810"])
        self.assertEqual([(item["issue"]["key"], item["reporting_root"]) for item in bundle["items"]],
                         [("CAM-801", "CAM-800"), ("CAM-811", "CAM-810"), ("CAM-812", "CAM-810")])
        self.assertEqual([project["key"] for project in bundle["matched_projects"]], ["CAM-800", "CAM-810"])
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        label_queries = [call for call in calls if any("labels =" in arg for arg in call)]
        self.assertEqual(len(label_queries), 2)
        self.assertTrue(any("nextPageToken=next" in call for call in label_queries))
        self.assertTrue(all("--get" in call for call in calls))

    def test_inaccessible_labeled_project_is_named_without_losing_accessible_project(self):
        self.env.update(LABEL_TWO_PROJECTS="1", FAIL_ISSUE="CAM-810")
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertEqual([project["key"] for project in bundle["matched_projects"]], ["CAM-800", "CAM-810"])
        self.assertEqual([item["issue"]["key"] for item in bundle["items"]], ["CAM-801"])
        self.assertTrue(bundle["partial"])
        self.assertEqual(bundle["failures"][0]["key"], "CAM-810")
        self.assertIn("inaccessible", bundle["failures"][0]["reason"])

    def test_failed_later_label_search_page_marks_partial_without_dropping_first_project(self):
        self.env.update(LABEL_TWO_PROJECTS="1", FAIL_LABEL_SEARCH_PAGE="2")
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertTrue(bundle["partial"])
        self.assertEqual(bundle["failures"][0]["endpoint"], "projects")
        self.assertEqual(bundle["failures"][0]["page"], 2)
        self.assertIn("unseen", bundle["coverage"].lower())

    def test_failed_first_label_search_page_cannot_be_called_no_matches(self):
        self.env["FAIL_LABEL_SEARCH_PAGE"] = "1"
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertNotEqual(labeled.returncode, 0)
        self.assertFalse(labeled.stdout)
        self.assertIn("page 1", labeled.stderr)
        self.assertNotIn("No Research Projects match", labeled.stderr)

    def test_no_match_and_ambiguous_label_require_clarification_without_report(self):
        for flag, expected in (("LABEL_NO_MATCH", "No Research Projects match"),
                               ("LABEL_AMBIGUOUS", "Ambiguous Research Project label")):
            with self.subTest(flag=flag):
                self.env[flag] = "1"
                labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                             selector="HydroFabric")
                self.assertNotEqual(labeled.returncode, 0)
                self.assertFalse(labeled.stdout)
                self.assertIn(expected, labeled.stderr)
                self.env.pop(flag)

    def test_unscoped_label_includes_research_projects_across_jira_projects(self):
        self.env["LABEL_CROSS_PROJECTS"] = "1"
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800", "HYDRO-20"])
        self.assertEqual([item["reporting_root"] for item in bundle["items"]], ["CAM-800", "HYDRO-20"])
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        label_queries = [arg for call in calls for arg in call if arg.startswith("jql=") and "labels =" in arg]
        self.assertTrue(label_queries)
        self.assertTrue(all("project = " not in query for query in label_queries))

    def test_label_removed_during_collection_excludes_that_project_and_marks_partial(self):
        self.env.update(LABEL_TWO_PROJECTS="1", ROOT_LABEL_REMOVED="CAM-810")
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertTrue(bundle["partial"])
        self.assertEqual(bundle["failures"][0]["key"], "CAM-810")
        self.assertIn("label", bundle["failures"][0]["reason"])

    def test_empty_labeled_scope_is_valid_only_when_discovery_completed(self):
        self.env["EMPTY_DESCENDANTS"] = "1"
        empty = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                   selector="HydroFabric")
        self.assertEqual(empty.returncode, 0, empty.stderr)
        bundle = json.loads(empty.stdout)
        self.assertEqual(bundle["items"], [])
        self.assertFalse(bundle["partial"])
        self.assertIn("current label membership", bundle["coverage"].lower())
        self.env.update(LABEL_TWO_PROJECTS="1", FAIL_LABEL_SEARCH_PAGE="2")
        insufficient = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                          selector="HydroFabric")
        self.assertNotEqual(insufficient.returncode, 0)
        self.assertFalse(insufficient.stdout)
        self.assertIn("usable cutoff evidence", insufficient.stderr)

    def test_duplicate_project_across_search_pages_cannot_duplicate_reported_work(self):
        self.env["LABEL_DUPLICATE"] = "1"
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertEqual([item["issue"]["key"] for item in bundle["items"]], ["CAM-801"])
        self.assertTrue(bundle["partial"])
        self.assertIn("duplicate", bundle["failures"][0]["reason"].lower())

    def test_ambiguous_label_on_retained_page_still_requires_clarification(self):
        self.env.update(LABEL_AMBIGUOUS_FIRST="1", FAIL_LABEL_SEARCH_PAGE="2")
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     selector="HydroFabric")
        self.assertNotEqual(labeled.returncode, 0)
        self.assertFalse(labeled.stdout)
        self.assertIn("Ambiguous Research Project label", labeled.stderr)

    def test_label_scope_limits_collection_to_permitted_research_project_roots(self):
        self.env["LABEL_TWO_PROJECTS"] = "1"
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     "--allowed-project-root", "CAM-800", selector="HydroFabric")
        self.assertEqual(labeled.returncode, 0, labeled.stderr)
        bundle = json.loads(labeled.stdout)
        self.assertEqual([root["key"] for root in bundle["roots"]], ["CAM-800"])
        self.assertEqual([project["key"] for project in bundle["matched_projects"]], ["CAM-800"])
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertFalse(any("/issue/CAM-810" in str(call) for call in calls))
        outside = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     "--allowed-project-root", "CAM-999", selector="HydroFabric")
        self.assertNotEqual(outside.returncode, 0)
        self.assertFalse(outside.stdout)
        self.assertIn("permitted", outside.stderr)

    def test_incomplete_allowed_root_search_is_not_a_definitive_no_match(self):
        self.env.update(LABEL_TWO_PROJECTS="1", FAIL_LABEL_SEARCH_PAGE="2")
        labeled = self.run_collector("2026-03-07", "2026-03-08", "--project-label", "--project", "CAM",
                                     "--allowed-project-root", "CAM-810", selector="HydroFabric")
        self.assertNotEqual(labeled.returncode, 0)
        self.assertFalse(labeled.stdout)
        self.assertIn("incomplete", labeled.stderr.lower())
        self.assertNotIn("No matching Research Projects within permitted", labeled.stderr)

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
