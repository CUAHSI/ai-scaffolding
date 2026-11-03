# Issue tracker: Jira (CAM)

Tickets and specs live in Jira, project `CAM`, on `cuahsi.atlassian.net`. Use the Atlassian CLI (`acli`) for all operations. GitHub is used **only for source code and pull requests**; never create GitHub issues.

`CAM` is shared by every Compute and Modeling team project, and the tree for this repo's work is defined by the Objective `{{OBJECTIVE_KEY}}`. Only touch work items under that Objective, plus new items you create under the rules below.

Prefix every `acli` command with `PAGER=cat` (or `export PAGER=cat`), otherwise output opens in an interactive pager and hangs. In a chain like `a; b`, the prefix applies only to `a`: use `export PAGER=cat;` first. `acli jira workitem view` ignores `PAGER` and still opens a pager; pipe it through `| cat` instead (e.g. `acli jira workitem view <KEY> --json | cat`).

## Project

| Item | Value |
| --- | --- |
| Objective | `{{OBJECTIVE_KEY}}` |
| Project labels | `{{LABELS}}` |
| Base branch | `{{BASE_BRANCH}}` |
| GitHub repo | `{{GITHUB_REPO}}` |

**Project labels** mark work items as belonging to this repo. Apply all of them to every work item you create. They are separate from the triage labels in `docs/agents/triage-labels.md`, which track an item's triage state. Both kinds are Jira labels and are created on first use.

## Hierarchy

Project hierarchy follows this format:

```text
CAM-1021  Research Project   A specific research project
└── {{OBJECTIVE_KEY}}  Objective   The objective that the work will contribute to
    └── Epic                 bundles related Stories; 1 week to 3 months of work
        └── Story            smallest unit agents create
            └── Sub-task     (created by humans; agents don't create these)
```

List the current set with `acli jira workitem search --jql "parent = {{OBJECTIVE_KEY}} AND statusCategory != Done ORDER BY cf[10116] ASC" --fields "key,issuetype,summary,status" --csv`.

- **Story** is the smallest unit to create. Every Story has an Epic as its parent.
- Create an **Epic** only when bundling several related Stories that together take 1 week to 3 months. Every Epic has `{{OBJECTIVE_KEY}}` as its parent.
- Never create Research Projects, Objectives, or Sub-tasks.
- Every work item gets the project labels `{{LABELS}}`.
- Order backlogs by Rank: `ORDER BY cf[10116] ASC` (`customfield_10116`).
- Statuses: `To Do`, `Up Next`, `In Progress`, `In Review`, `Done`, `Won't Do`.

## Conventions

- **Create a Story**: `acli jira workitem create --project CAM --type Story --parent <EPIC-KEY> --label "{{LABELS}}" --summary "..." --description-file <file>`. Write the body to a temp file for multi-line descriptions. Plain text only: Jira does not render Markdown (use ADF JSON if rich formatting matters).

- **Create an Epic**: same as above with `--type Epic --parent {{OBJECTIVE_KEY}}`.

- **Read a work item**: `acli jira workitem view <KEY> --fields "summary,issuetype,status,parent,labels,description,comment" --json`.

- **Read comments**: `acli jira workitem comment list --key <KEY>`.

- **List this repo's work**: `acli jira workitem search --jql "project = CAM AND {{LABEL_FILTER}} AND statusCategory != Done ORDER BY cf[10116] ASC" --fields "key,issuetype,summary,status,labels" --csv`. Narrow with `AND parent = <EPIC-KEY>`, `AND labels = ready-for-agent`, `AND issuetype = Story`, etc.

- **Comment**: `acli jira workitem comment create --key <KEY> --body "..."` (or `--body-file <file>`).

- **Apply / remove labels**: `acli jira workitem edit --key <KEY> --labels "..." --yes` / `--remove-labels "..." --yes`. Labels are created on first use, so there is no separate create step.

- **Change status**: `acli jira workitem transition --key <KEY> --status "In Progress" --yes`.

- **Close**: comment with the reason, then transition to `Done` (resolved) or `Won't Do` (declined).

- **Link**: `acli jira workitem link create --out <BLOCKED> --in <BLOCKER> --type Blocks --yes` creates "`<BLOCKER>` blocks `<BLOCKED>`". The flag names are the reverse of what they suggest, and acli's success message (`<BLOCKED> Blocks <BLOCKER>`) describes the opposite of what Jira stores, so read the link back after creating it (see **Read links** below). Other types: `Relates`, `Duplicate`. The REST equivalent is `POST /rest/api/3/issueLink` with `{"type":{"name":"Blocks"},"inwardIssue":{"key":"<BLOCKER>"},"outwardIssue":{"key":"<BLOCKED>"}}`; delete a link with `DELETE /rest/api/3/issueLink/<LINK-ID>`. Credentials for REST calls are described under **Sprints, start dates, and due dates** below.

- **Read links**: `curl -sS --netrc-file ~/.jira/netrc "https://cuahsi.atlassian.net/rest/api/3/issue/<KEY>?fields=issuelinks"`. For a `Blocks` link, an `inwardIssue` entry means `<KEY>` is blocked by that item, and an `outwardIssue` entry means `<KEY>` blocks it. Do not rely on `acli jira workitem link list`: it omits the other item's key for half of the links, so it cannot show direction.

- **Read any field**: `acli jira workitem view <KEY> --fields "duedate,customfield_10115" --json | cat`. `view` reads any system or custom field, but `edit` can only write the fields listed below.

## Sprints, start dates, and due dates (Jira REST API)

`acli` (checked at 1.3.39) cannot set start dates, due dates, sprints, or any custom field on an existing work item. `acli jira workitem edit` only accepts `summary`, `description`, `assignee`, `type`, and labels; `--from-json` rejects other keys (`unknown field "duedate"`, `unknown field "fields"`) and there is no `--field` flag. Use the Jira REST API with `curl` for these instead.

| Item          | Value                                                               |
| ------------- | ------------------------------------------------------------------- |
| Board         | `CAM board`, id `18` (scrum)                                        |
| Sprint field  | `customfield_10115`                                                 |
| Start date    | `customfield_10504` (not `Target start`, which CAM does not use)    |
| Rank field    | `customfield_10116`                                                 |
| Active sprint | `acli jira board list-sprints --id 18 --state active --json \| cat` |
| Credentials   | `~/.jira/netrc` (see **Credentials** below)                         |

### Credentials

Credentials live in a netrc file so the API token never appears in commands, shell history, or agent output. Never print, read into context, or copy this file. If it is missing, give the user the setup steps below and wait; do not ask them to paste the token.

One-time setup, done by the user:

1. Create a classic API token at <https://id.atlassian.com/manage-profile/security/api-tokens> with **Create API token**, not **Create API token with scopes** (scoped tokens need a different base URL and separate sprint permissions).
2. Create a private folder and an empty file only the user can read:

   ```sh
   mkdir -p ~/.jira && chmod 700 ~/.jira
   touch ~/.jira/netrc && chmod 600 ~/.jira/netrc
   open -e ~/.jira/netrc
   ```

   Use an editor (`open -e`, `nano`, `vim`), not `echo`, so the token stays out of shell history.

3. Add the following, replacing the email and token:

   ```text
   machine cuahsi.atlassian.net
     login <atlassian-email>
     password <api-token>
   ```

   `machine` is the bare host (no `https://`, no trailing `/`), `login` is the Atlassian sign-in email, and `password` is the token exactly as issued, with no quotes. End the file with a newline.

Before the first REST call, check the file without reading it:

- **Permissions**: `ls -l ~/.jira/netrc` must start with `-rw-------`. If it doesn't, ask the user to run `chmod 600 ~/.jira/netrc`.

- **Login** (read-only): `curl -sS --netrc-file ~/.jira/netrc https://cuahsi.atlassian.net/rest/api/3/myself`. Expect HTTP 200 and print only `displayName`. HTTP 401 means the email, token, or `machine` host is wrong.

### Requests

- **Set a due date**: `curl -sS -w "HTTP %{http_code}\n" --netrc-file ~/.jira/netrc -X PUT -H "Content-Type: application/json" -d '{"fields":{"duedate":"2026-11-06"}}' https://cuahsi.atlassian.net/rest/api/3/issue/<KEY>`. Success is HTTP 204. Send `"duedate":null` to clear it.

- **Set a start date**: same request with `-d '{"fields":{"customfield_10504":"2026-10-29"}}'`. Every scheduled work item needs both a start date and a due date; set them together.

- **Before overwriting** an existing start or due date, check the item's changelog (`GET /rest/api/3/issue/<KEY>/changelog`) and tell the user if a person set it.

- **Add work items to a sprint**: `curl -sS -w "HTTP %{http_code}\n" --netrc-file ~/.jira/netrc -X POST -H "Content-Type: application/json" -d '{"issues":["<KEY>","<KEY>"]}' https://cuahsi.atlassian.net/rest/agile/1.0/sprint/<SPRINT-ID>/issue`. Success is HTTP 204. Add Stories, not Epics.

- **Verify** every write by reading it back with `acli jira workitem view <KEY> --fields "customfield_10504,duedate,customfield_10115" --json | cat`.
- When setting due dates for dependent Stories, keep them consistent with `Blocks` links: a blocker's due date comes on or before the start date of every item it blocks.

## Branches

Work on a Story in its own branch off the latest `{{BASE_BRANCH}}`, named `<KEY>-<short-description>`: the Jira key, then a few lowercase, hyphenated words summarising the change (e.g. `CAM-1500-hydroshare-codemeta-collector`). The key ties the branch, and the PR opened from it, back to the Story.

```sh
git checkout {{BASE_BRANCH}} && git pull && git checkout -b CAM-1500-hydroshare-codemeta-collector
```

## Commits

Start every commit message with the Story key and a colon (e.g. `CAM-1500: Parse HydroShare resource metadata`), so each commit traces back to its Story.

## Pull requests (GitHub)

The Story moves through these steps alongside its PR:

1. **Open**: `gh pr create --base {{BASE_BRANCH}}` from a branch named as in **Branches** above. Put the Jira key in the PR title (e.g. `CAM-1500: Add maintained HydroShare metadata collector`) and fill in the repo's PR template, including the Jira link `https://cuahsi.atlassian.net/browse/<KEY>`.
2. **Link back**: comment the PR URL on the Story (`acli jira workitem comment create --key <KEY> --body "PR: <url>"`), then transition the Story to `In Review`.
3. **Merged**: when `gh pr view <n> --json state` reports `MERGED`, transition the Story to `Done`. Whenever you come across a Story in `In Review`, check its PR this way and transition it if it has merged.
4. **Closed without merging**: comment the reason on the Story and move it back to `In Progress`, or to `Won't Do` if the work is abandoned.

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_ When `yes`, triage external PRs with `gh pr view <n> --comments`, `gh pr diff <n>`, `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, and `gh pr close`.

## When a skill says "publish to the issue tracker"

Create a Jira Story under the relevant Epic of `{{OBJECTIVE_KEY}}`, labelled `{{LABELS}}` (or an Epic under `{{OBJECTIVE_KEY}}`, if it's a multi-Story body of work). If no Epic clearly fits, ask the user which one to use rather than guessing.

## When a skill says "fetch the relevant ticket"

Read it as in **Read a work item** above. A bare `#42` refers to a GitHub PR (or a closed, pre-Jira GitHub issue); a `CAM-123` key refers to Jira.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single Epic with **child** Stories as tickets.

- **Map**: an Epic under `{{OBJECTIVE_KEY}}`, labelled `{{LABELS}},wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.

- **Child ticket**: a Story with `--parent <map-epic>`, labelled `{{LABELS}},wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, it's assigned to the driving dev.

- **Blocking**: a `Blocks` link, created as in **Link** above. A ticket is unblocked when every item it is blocked by (each `inwardIssue` on its `Blocks` links) is in `Done` or `Won't Do`.

- **Frontier query**: `acli jira workitem search --jql "parent = <map> AND statusCategory != Done AND assignee is EMPTY ORDER BY cf[10116] ASC" --csv`, then drop any with an open blocker (check as in **Read links** above); first in Rank order wins.

- **Claim**: `acli jira workitem assign --key <KEY> --assignee @me --yes`, the session's first write. Then transition to `In Progress`.

- **Resolve**: comment with the answer, transition to `Done`, then append a context pointer (gist + key) to the map Epic's Decisions-so-far.
