---
name: project-report
description: "Generate a cited, historical Jira progress report for a specified hierarchy and date range. Invoke explicitly with a reporting root and inclusive dates."
disable-model-invocation: true
---

# Project report

Produce a leadership-facing account of delivered outcomes, significance, and outstanding work, grounded only in Jira evidence available at the reporting cutoff. Jira access is **read-only**. The report is both a local Markdown file and text in chat. Read [assets/evidence.md](assets/evidence.md) before classifying work; apply its rules to every item, including items with no period activity.

## 1. Establish the request

Require exactly one Jira Research Project, Objective, or Epic as root and two unambiguous inclusive calendar dates (start and end). Accept unambiguous natural-language dates; echo the resolved ISO dates. Accept an optional timezone, a person or list of people, a destination directory, and a format: `summary` (default), `by-contributor`, or `brief`. Ask about missing or ambiguous inputs; do not infer a root or period. Reject reversed ranges. If the end date is later than today **in the reporting timezone**, ask for a historical end date.

Use the authenticated Jira user's timezone from Jira's `/rest/api/3/myself` unless explicitly overridden; ask if no reliable timezone is available. Record the retrieval timestamp in UTC and the stated timezone. Calculate the window as `[local midnight at start, local midnight on the day after end)` using the named timezone (including daylight-saving changes), not a fixed UTC offset. For past end dates the cutoff is the exclusive end of that window; for an end date of today, use the retrieval time as cutoff and label the report **provisional through that time**. Apply the same cutoff to every evidence and state query. Confirm the root is accessible and has the requested issue type; stop with an actionable explanation if not.

## 2. Collect the bounded Jira evidence

Check the invoking repository's Jira and credential guidance (for example `docs/agents/issue-tracker.md`), including its access boundaries. This reusable skill does not assume a CAM root or expand access to other projects. Use `acli` for ordinary discovery/reads where possible; use authenticated, **GET-only** Jira REST requests for complete pagination and history. Reuse existing authentication; never print or copy credentials. If the repository uses `~/.jira/netrc`, check its permissions without reading it and send it only to `curl --netrc-file`. Never use Jira writes, even if another workflow normally assigns or transitions a ticket.

Discover direct children of the root, then recursively the children of each child (including Sub-tasks), by `parent` relationship. Collect **all accessible pages** at each level, not just the first search page. Jira Cloud's `/rest/api/3/search/jql` uses `nextPageToken`; continue until `isLast` is true. If `isLast` is false with no next token, treat retrieval as incomplete, not as an empty page. If using `acli jira workitem search --jql 'parent = KEY'`, verify whether its output is complete and fall back to paginated REST when it is not. Retrieve each item's details, comments from `/rest/api/3/issue/KEY/comment` (paginate `startAt`/`maxResults` until `total`), and history from `/rest/api/3/issue/KEY/changelog` (same pagination rule). Request fields needed for identity, issue type, parent, created, status, resolution, assignee, schedule, description, and updated time. Fetch every page even when embedded issue comments or expanded changelogs are present. Use the root as organizational context; reportable work is its descendants, with related parent and child outcomes deduplicated. Ordinary issue links are context only, never additional members. Never fetch linked repositories, PRs, or documents to verify claims.

Record which pages/items failed, which fields cannot be reconstructed, and when information was retrieved. Current descendants are not a complete historical membership snapshot: disclose that moved-out, deleted, or inaccessible work may be absent. Exclude items created after the cutoff from period-end evidence. Stop if the accessible evidence cannot support a meaningful account; otherwise mark the result **partial**, naming affected scope and unsupported claims. A retrieval error is not evidence that no work occurred.

## 3. Reconstruct and assess

Apply [assets/evidence.md](assets/evidence.md) to each item before synthesis. Reconstruct status, resolution, assignment, and dated commitments as of the cutoff using retained change history; do not silently substitute today's values. Restrict accomplishment evidence to records whose text was reliably available by the cutoff. Evaluate both period activity and period-end outstanding work, including untouched outstanding items; exclude previously completed/abandoned items unless context or a distinct period outcome requires them. Separate lifecycle state from planning assessment, deduplicate parent/child outcomes and reopenings, and preserve contradictions and unknowns. An explicit delivered outcome may be reported from an unfinished item without calling that item completed.

For person filters, resolve stable Jira account identities; ask if the intended identities cannot be distinguished. Filter **which work is presented**, not just headings: keep documented contributions and distinctly labeled assignment-based attribution for selected people, plus necessary collaborator context. Without a filter include all contributors and unknown-contributor work. Never infer contribution from the assignee, comment author, reporter, mentions, or a status-transition author.

## 4. Write and deliver

Prepare one of the following; length is a soft target, never a reason to drop a material caveat or citation:

- `summary`: roughly one page, grouped by outcome, with significance, outstanding/abandoned work, and material planning results.
- `by-contributor`: typically one to three concise bullets per contributor, distinguishing documented contribution from assignment-based attribution; retain shared credit and unknown attribution.
- `brief`: usually at most five accomplishment bullets, followed by compact outstanding/abandoned work and qualifications.

Include root and link, inclusive dates, timezone, cutoff/retrieval time, format, people filter (or all), coverage/partial/provisional notes, ticket links for described work, and nearby Jira citations for every accomplishment and individual attribution. Link directly to a supporting comment when possible; otherwise cite the ticket and dated history event. Differentiate achieved dates from when statements were recorded. Label recorded claims as Jira evidence, not independently verified outcomes. Describe lifecycle and planning separately; omit default completion percentages, productivity rankings, and summed parent/child counts. If an unfiltered report has no qualifying findings, say **no qualifying evidence was found**; for an empty people-filtered report, say **no matching evidence was found**. Retain coverage limitations, not a claim of inactivity.

Save the **complete report** as Markdown under the invoking project's `reports/` by default, or the requested destination. Name it `<root>_<start>_<end>_<format>_<generated-UTC>.md` with a filesystem-safe UTC timestamp; add a numeric collision suffix if needed. Create the directory if needed, and create the file without overwriting an existing file. Put the people filter in report metadata, not the filename. Display the full report text in chat and the created path for ordinary, partial, and empty reports. If writing fails, display the available text, name the failure, mark delivery incomplete, and request a writable destination; do not claim a file was saved. The local artifact may contain internal Jira information: leave it unstaged and uncommitted; do not change ignore rules or publish it to Jira or elsewhere.
