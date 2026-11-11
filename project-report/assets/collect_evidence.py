"""Collect paginated, read-only Jira evidence for the project-report agent skill.

This produces source data, not a report. Comment bodies lacking cutoff-valid
creation and edit timestamps are withheld, with their IDs and reasons retained.
The agent must assess historical claims, uncertainty, citations, and delivery
using SKILL.md and evidence.md.
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
REQUESTED_FIELDS = ISSUE_FIELDS.split(",")


class PartialRetrieval(RuntimeError):
    """A paginated request failed after zero or more usable records."""

    def __init__(self, message, records, page):
        super().__init__(message)
        self.records = records
        self.page = page


def timestamp(instant):
    """Format an instant as a UTC timestamp without losing cutoff precision.

    Parameters
    ----------
    instant : datetime
        Timezone-aware instant to format.

    Returns
    -------
    str
        ISO 8601 UTC timestamp ending in ``Z``.
    """
    precision = "microseconds" if instant.microsecond else "seconds"
    return instant.astimezone(timezone.utc).isoformat(timespec=precision).replace("+00:00", "Z")


def recorded_before_cutoff(value, cutoff):
    """Whether a Jira timestamp proves a record existed before the cutoff."""
    if not isinstance(value, str):
        return False
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return instant.tzinfo is not None and instant < cutoff
    except ValueError:
        return False


def parse_date(value):
    """Parse a reporting date in the required ISO calendar format.

    Parameters
    ----------
    value : str
        Calendar date in ``YYYY-MM-DD`` form.

    Returns
    -------
    date
        Parsed calendar date.

    Raises
    ------
    ValueError
        If the date is invalid or not in the required format.
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Expected an ISO calendar date (YYYY-MM-DD): {value}")
    return date.fromisoformat(value)


class JiraReader:
    """Read Jira issues and complete paginated records using GET requests."""

    def __init__(self, site, netrc_file):
        """Configure the Jira host and check that REST credentials are private.

        Parameters
        ----------
        site : str
            Jira hostname, without a scheme or path.
        netrc_file : Path
            Private netrc file supplied only to curl.

        Raises
        ------
        ValueError
            If the host is invalid or the credential file is not private.
        OSError
            If the credential file cannot be inspected.
        """
        if not re.fullmatch(r"[a-zA-Z0-9.-]+", site):
            raise ValueError("--site must be a Jira hostname, without a scheme or path")
        mode = netrc_file.stat().st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            raise ValueError("Jira netrc file must be private (chmod 600)")
        self.base = f"https://{site}/rest/api/3"
        self.netrc_file = netrc_file

    def get(self, path, **params):
        """Fetch JSON from a Jira REST path with URL-encoded query parameters.

        Parameters
        ----------
        path : str
            Path relative to Jira's REST API v3 endpoint.
        **params : object
            Query parameters to encode for a GET request.

        Returns
        -------
        dict
            Decoded Jira response.

        Raises
        ------
        RuntimeError
            If the GET fails or Jira returns invalid JSON.
        """
        args = ["curl", "-fsS", "--get", "--netrc-file", str(self.netrc_file)]
        for name, value in params.items():
            args.extend(("--data-urlencode", f"{name}={value}"))
        args.append(f"{self.base}/{path}")
        result = subprocess.run(args, text=True, capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f"GET {path} failed: {result.stderr.strip()}")
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"GET {path} returned invalid JSON") from error
        if not isinstance(response, dict):
            raise RuntimeError(f"GET {path} returned a non-object response")
        return response

    def issue(self, key):
        """Fetch the fields needed to assess one Jira work item.

        Parameters
        ----------
        key : str
            Jira issue key.

        Returns
        -------
        dict
            Issue response, including its requested fields.
        """
        return self.get(f"issue/{quote(key, safe='')}", fields=ISSUE_FIELDS)

    def children(self, key):
        """Find every current direct child of an issue across search pages.

        Parameters
        ----------
        key : str
            Parent Jira issue key.

        Returns
        -------
        list[str]
            Direct child keys in search order.

        Raises
        ------
        PartialRetrieval
            If a search page fails; carries all previously returned child keys.
        """
        token = None
        seen_tokens = set()
        children = []
        page_number = 1
        while True:
            params = {"jql": f"parent = {key} ORDER BY key", "fields": "key", "maxResults": PAGE_SIZE}
            if token is not None:
                params["nextPageToken"] = token
            try:
                page = self.get("search/jql", **params)
                if not isinstance(page.get("issues"), list) or not isinstance(page.get("isLast"), bool):
                    raise RuntimeError(f"Search for children of {key} returned an incomplete page")
                keys = [issue["key"] for issue in page["issues"]]
                if not all(isinstance(child_key, str) for child_key in keys):
                    raise RuntimeError(f"Search for children of {key} returned an invalid key")
                children.extend(keys)
                if page["isLast"]:
                    return children
                next_token = page.get("nextPageToken")
                if not isinstance(next_token, str) or not next_token or next_token in seen_tokens:
                    raise RuntimeError(f"Search for children of {key} has no usable nextPageToken")
            except (RuntimeError, KeyError, TypeError) as error:
                raise PartialRetrieval(str(error), children, page_number) from error
            token = next_token
            seen_tokens.add(token)
            page_number += 1

    def pages(self, key, kind):
        """Retrieve every comment or changelog entry for one issue.

        Parameters
        ----------
        key : str
            Jira issue key.
        kind : str
            Jira endpoint name: ``comment`` or ``changelog``.

        Returns
        -------
        list[dict]
            All entries returned by the paginated endpoint.

        Raises
        ------
        PartialRetrieval
            If a page fails; carries all previously returned entries.
        """
        path = f"issue/{quote(key, safe='')}/{kind}"
        item_key = "comments" if kind == "comment" else "values"
        offset = 0
        results = []
        page_number = 1
        while True:
            try:
                page = self.get(path, startAt=offset, maxResults=PAGE_SIZE)
                values = page.get(item_key)
                total = page.get("total")
                if (not isinstance(values, list) or not isinstance(total, int)
                        or page.get("startAt") != offset or total < offset + len(values)):
                    raise RuntimeError(f"Incomplete {kind} page for {key} at {offset}")
                results.extend(values)
                offset += len(values)
                if offset >= total:
                    return results
                if not values:
                    raise RuntimeError(f"Incomplete {kind} page for {key} at {offset}")
            except RuntimeError as error:
                raise PartialRetrieval(str(error), results, page_number) from error
            page_number += 1


def collect(reader, root_key, start, end, zone):
    """Collect a dated evidence bundle for every current descendant.

    The bundle retains raw Jira records for the reporting agent to assess;
    it does not infer historical outcomes or produce a report.

    Parameters
    ----------
    reader : JiraReader
        Authenticated, read-only Jira client.
    root_key : str
        Key of a Research Project, Objective, or Epic.
    start : date
        First included local calendar day.
    end : date
        Last included local calendar day.
    zone : ZoneInfo
        IANA reporting timezone used for calendar boundaries.

    Returns
    -------
    dict
        Root, UTC period boundaries, accessible descendants, and retrieval gaps.

    Raises
    ------
    ValueError
        If the dates or root issue type are invalid.
    RuntimeError
        If the root or all descendants are inaccessible after a retrieval failure.
    """
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
    if root.get("key") != root_key or not isinstance(root.get("fields"), dict):
        raise RuntimeError(f"Reporting root {root_key} is inaccessible or incomplete")
    if (root["fields"].get("issuetype") or {}).get("name") not in {"Research Project", "Objective", "Epic"}:
        raise ValueError("Reporting root must be a Research Project, Objective, or Epic")

    queue = deque([root_key])
    seen = {root_key}
    items = []
    failures = []
    while queue:
        parent = queue.popleft()
        try:
            child_keys = reader.children(parent)
        except PartialRetrieval as error:
            child_keys = error.records
            failures.append({"key": parent, "endpoint": "children", "page": error.page,
                             "reason": str(error)})
        for key in child_keys:
            if key in seen:
                failures.append({"key": key, "endpoint": "children", "page": None,
                                 "reason": f"Duplicate or cyclic descendant beneath {parent}"})
                continue
            seen.add(key)
            try:
                issue = reader.issue(key)
            except RuntimeError as error:
                failures.append({"key": key, "endpoint": "issue", "page": None,
                                 "reason": str(error) + "; descendants cannot be discovered"})
                continue
            if issue.get("key") != key or not isinstance(issue.get("fields"), dict):
                failures.append({"key": key, "endpoint": "issue", "page": None,
                                 "reason": "Issue identity or fields unavailable; descendants cannot be discovered"})
                continue
            if (issue["fields"].get("parent") or {}).get("key") != parent:
                failures.append({"key": key, "endpoint": "issue", "field": "parent", "page": None,
                                 "reason": f"Parent differs from search result ({parent}); scope is uncertain"})
                continue
            for field in REQUESTED_FIELDS:
                if field not in issue["fields"]:
                    failures.append({"key": key, "endpoint": "issue", "field": field, "page": None,
                                     "reason": "Requested field not returned; historical value unknown"})
            record = {"issue": issue}
            for kind, name in (("comment", "comments"), ("changelog", "changelog")):
                try:
                    record[name] = reader.pages(key, kind)
                    record[f"{name}_complete"] = True
                except PartialRetrieval as error:
                    record[name] = error.records
                    record[f"{name}_complete"] = False
                    failures.append({"key": key, "endpoint": kind, "page": error.page,
                                     "reason": str(error)})
            valid_comments = []
            excluded_comments = []
            for comment in record["comments"]:
                created = comment.get("created") if isinstance(comment, dict) else None
                updated = comment.get("updated") if isinstance(comment, dict) else None
                if recorded_before_cutoff(created, cutoff) and recorded_before_cutoff(updated, cutoff):
                    valid_comments.append(comment)
                else:
                    reason = ("creation time unavailable or after cutoff"
                              if not recorded_before_cutoff(created, cutoff)
                              else "edit time unavailable or after cutoff; earlier text cannot be verified")
                    excluded_comments.append({"id": comment.get("id") if isinstance(comment, dict) else None,
                                              "created": created, "updated": updated, "reason": reason})
            record["comments"] = valid_comments
            record["excluded_comments"] = excluded_comments
            items.append(record)
            queue.append(key)

    if failures and not any(
        recorded_before_cutoff(record["issue"]["fields"].get("created"), cutoff)
        or bool(record["comments"])
        or any(recorded_before_cutoff(change.get("created"), cutoff)
               for change in record["changelog"])
        for record in items
    ):
        raise RuntimeError("Descendant retrieval failed and no usable cutoff evidence was found: "
                           + "; ".join(f"{gap['key']} {gap['endpoint']} page {gap['page']}: {gap['reason']}"
                                       for gap in failures))

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
        "partial": bool(failures),
        "failures": failures,
        "coverage": "Current descendant discovery does not establish historical membership; moved-out, deleted, or inaccessible work may be absent.",
    }


def main():
    """Parse CLI inputs and print a complete read-only Jira evidence bundle.

    Returns
    -------
    int
        Exit status: zero on success, one on a collection error.
    """
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
