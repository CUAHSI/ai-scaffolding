"""Collect paginated, read-only Jira evidence for the project-report agent skill.

This produces source data, not a report. The agent must assess historical claims,
uncertainty, citations, and delivery using SKILL.md and evidence.md.
"""

import argparse
import json
import re
import stat
import subprocess
import sys
from collections import deque
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ISSUE_FIELDS = (
    "summary,issuetype,parent,created,status,resolution,resolutiondate,assignee,"
    "duedate,customfield_10504,description,updated"
)
PAGE_SIZE = 100


def timestamp(instant):
    precision = "microseconds" if instant.microsecond else "seconds"
    return instant.astimezone(timezone.utc).isoformat(timespec=precision).replace("+00:00", "Z")


def parse_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Expected an ISO calendar date (YYYY-MM-DD): {value}")
    return date.fromisoformat(value)


class JiraReader:
    def __init__(self, site, netrc_file):
        if not re.fullmatch(r"[a-zA-Z0-9.-]+", site):
            raise ValueError("--site must be a Jira hostname, without a scheme or path")
        mode = netrc_file.stat().st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            raise ValueError("Jira netrc file must be private (chmod 600)")
        self.base = f"https://{site}/rest/api/3"
        self.netrc_file = netrc_file

    def get(self, path, **params):
        args = ["curl", "-fsS", "--get", "--netrc-file", str(self.netrc_file)]
        for name, value in params.items():
            args.extend(("--data-urlencode", f"{name}={value}"))
        args.append(f"{self.base}/{path}")
        result = subprocess.run(args, text=True, capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f"GET {path} failed: {result.stderr.strip()}")
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"GET {path} returned invalid JSON") from error

    def issue(self, key):
        return self.get(f"issue/{quote(key, safe='')}", fields=ISSUE_FIELDS)

    def children(self, key):
        token = None
        seen_tokens = set()
        children = []
        while True:
            params = {"jql": f"parent = {key} ORDER BY key", "fields": "key", "maxResults": PAGE_SIZE}
            if token is not None:
                params["nextPageToken"] = token
            page = self.get("search/jql", **params)
            if not isinstance(page.get("issues"), list) or not isinstance(page.get("isLast"), bool):
                raise RuntimeError(f"Search for children of {key} returned an incomplete page")
            children.extend(issue["key"] for issue in page["issues"])
            if page["isLast"]:
                return children
            token = page.get("nextPageToken")
            if not token or token in seen_tokens:
                raise RuntimeError(f"Search for children of {key} has no usable nextPageToken")
            seen_tokens.add(token)

    def pages(self, key, kind):
        path = f"issue/{quote(key, safe='')}/{kind}"
        item_key = "comments" if kind == "comment" else "values"
        offset = 0
        results = []
        while True:
            page = self.get(path, startAt=offset, maxResults=PAGE_SIZE)
            values = page.get(item_key)
            total = page.get("total")
            if not isinstance(values, list) or not isinstance(total, int) or page.get("startAt") != offset:
                raise RuntimeError(f"Incomplete {kind} page for {key} at {offset}")
            results.extend(values)
            offset += len(values)
            if offset >= total:
                return results
            if not values:
                raise RuntimeError(f"Incomplete {kind} page for {key} at {offset}")


def collect(reader, root_key, start, end, zone):
    retrieved_at = datetime.now(timezone.utc)
    today = retrieved_at.astimezone(zone).date()
    if start > end:
        raise ValueError("Reporting start date is after end date")
    if end > today:
        raise ValueError("Reporting end date is later than today in the reporting timezone")
    start_utc = datetime.combine(start, time.min, zone).astimezone(timezone.utc)
    end_exclusive_utc = datetime.combine(end + timedelta(days=1), time.min, zone).astimezone(timezone.utc)
    provisional = end == today
    cutoff = retrieved_at if provisional else end_exclusive_utc

    root = reader.issue(root_key)
    if root.get("fields", {}).get("issuetype", {}).get("name") not in {"Research Project", "Objective", "Epic"}:
        raise ValueError("Reporting root must be a Research Project, Objective, or Epic")

    queue = deque([root_key])
    seen = {root_key}
    items = []
    while queue:
        parent = queue.popleft()
        for key in reader.children(parent):
            if key in seen:
                raise RuntimeError(f"Duplicate or cyclic descendant: {key}")
            seen.add(key)
            issue = reader.issue(key)
            if issue.get("fields", {}).get("parent", {}).get("key") != parent:
                raise RuntimeError(f"Parent of {key} differs from search result; scope is uncertain")
            items.append({
                "issue": issue,
                "comments": reader.pages(key, "comment"),
                "changelog": reader.pages(key, "changelog"),
            })
            queue.append(key)

    return {
        "root": root,
        "period": {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "timezone": zone.key,
            "start_utc": timestamp(start_utc),
            "end_exclusive_utc": timestamp(end_exclusive_utc),
            "cutoff_utc": timestamp(cutoff),
            "retrieved_at_utc": timestamp(retrieved_at),
            "provisional": provisional,
        },
        "items": items,
        "coverage": "Current descendant discovery does not establish historical membership; moved-out, deleted, or inaccessible work may be absent.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Jira key of the reporting root")
    parser.add_argument("start", help="inclusive local YYYY-MM-DD")
    parser.add_argument("end", help="inclusive local YYYY-MM-DD")
    parser.add_argument("--site", required=True, help="Jira hostname from the invoking project's guidance")
    parser.add_argument("--timezone", help="IANA timezone (defaults to the authenticated Jira user's timezone)")
    parser.add_argument("--netrc-file", type=Path, default=Path.home() / ".jira/netrc")
    args = parser.parse_args()
    try:
        start, end = parse_date(args.start), parse_date(args.end)
        reader = JiraReader(args.site, args.netrc_file)
        zone_name = args.timezone or reader.get("myself").get("timeZone")
        if not zone_name:
            raise ValueError("Jira has no reporting timezone; specify --timezone")
        zone = ZoneInfo(zone_name)
        result = collect(reader, args.root, start, end, zone)
    except (OSError, ValueError, ZoneInfoNotFoundError, RuntimeError, KeyError) as error:
        print(f"Evidence collection failed: {error}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
