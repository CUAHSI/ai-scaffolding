---
name: cuahsi-project-setup
description: "Configure this repo for the engineering skills in accordance with CUAHSI project guidelines: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

# Setup CUAHSI Project

Configure this repo so the engineering skills track work in Jira (project `CAM`) and keep code and pull requests on GitHub. The Jira playbook is the template [`assets/issue-tracking-guidelines.md`](assets/issue-tracking-guidelines.md); this skill fills in its `{{...}}` placeholders and writes the result to `docs/agents/issue-tracker.md`.

| Placeholder | Value | Example |
| --- | --- | --- |
| `{{OBJECTIVE_KEY}}` | The Jira Objective this repo's work rolls up to | `CAM-209` |
| `{{LABELS}}` | Project labels applied to every work item, comma-separated | `COMSES,OMF-Skills` |
| `{{LABEL_FILTER}}` | `{{LABELS}}` as JQL, one clause per label joined by `AND` | `labels = "COMSES" AND labels = "OMF-Skills"` |
| `{{BASE_BRANCH}}` | Branch that Story branches start from and PRs target | `develop` |
| `{{GITHUB_REPO}}` | The GitHub repo, `owner/name` | `CUAHSI/ai-scaffolding` |

`<...>` placeholders in the template (`<KEY>`, `<EPIC-KEY>`, ...) are filled in per command at run time; leave them as written.

If `docs/agents/issue-tracker.md` already exists, this is a re-run: read its **Project** table and offer those values as the defaults in step 2.

## 1. Check prerequisites

Run each check. Done when every one passes.

| Check | Command | Pass |
| --- | --- | --- |
| GitHub CLI signed in | `gh auth status` | Logged in to `github.com` |
| Write access to the repo | `gh repo view --json nameWithOwner,viewerPermission` | `viewerPermission` is `WRITE`, `MAINTAIN`, or `ADMIN` |
| Atlassian CLI signed in | `acli jira auth status` | Authenticated to `cuahsi.atlassian.net` |
| Jira netrc permissions | `ls -l ~/.jira/netrc` | Starts with `-rw-------` |
| Jira REST login | `curl -sS -o /dev/null -w "%{http_code}\n" --netrc-file ~/.jira/netrc https://cuahsi.atlassian.net/rest/api/3/myself` | `200` |
| Parent skill installed | `setup-matt-pocock-skills` is in your available skills | Present |

For each failure, give the user setup steps for their operating system and wait for them to fix it:

- `gh`: install from <https://cli.github.com/>, then `gh auth login`.
- `acli`: install from <https://developer.atlassian.com/cloud/acli/guides/install-acli/>, then `acli jira auth login --web`.
- netrc: walk them through **Credentials** in the guidelines template. The netrc file holds an API token; check it only with the two commands above, and keep its contents out of the conversation.
- Parent skill: `npx skills add mattpocock/skills`, then restart the agent session so the skill loads.

## 2. Gather project values

Done when the user has confirmed a value for every placeholder in the table above.

1. **Objective.** Ask for the Jira Objective ID. Confirm it with `PAGER=cat acli jira workitem view <KEY> --fields "summary,issuetype,status" --json | cat`: `issuetype` must be `Objective`. Show the user its summary.
2. **Labels.** List the Objective's Epics with `acli jira workitem search --jql "parent = <OBJECTIVE-KEY>" --fields "key,issuetype,summary,labels" --csv`, then their Stories with the same command and `--jql "parent in (<EPIC-KEYS>)"`. Propose the labels shared across those items as `{{LABELS}}`, leaving out triage labels (`needs-triage`, `ready-for-agent`, ...) and `wayfinder:*` labels. The user confirms or edits the list. Derive `{{LABEL_FILTER}}` from it.
3. **Base branch.** Run `git ls-remote --heads origin develop`. If `develop` exists, propose it; otherwise propose the default branch from `gh repo view --json defaultBranchRef`. The user confirms.
4. **GitHub repo.** Take `nameWithOwner` from step 1.

## 3. Run `setup-matt-pocock-skills`

Invoke `setup-matt-pocock-skills` and answer its sections as follows:

- **Section A (issue tracker):** choose **Other**. For `docs/agents/issue-tracker.md`, use the guidelines template with every `{{...}}` placeholder replaced by the values from step 2 (in place of a freeform description).
- **Section B (triage labels):** keep the defaults unless the user says otherwise. Triage labels are Jira labels, created on first use, so skip `gh label create`. `docs/agents/triage-labels.md` holds only the triage roles; the project labels live in the **Project** table of `docs/agents/issue-tracker.md`.
- **Section C (domain docs):** follow its defaults.

On a re-run, show the user a diff of each file that would change and write only what they approve.

Done when `docs/agents/issue-tracker.md` exists and `grep -n "{{" docs/agents/issue-tracker.md` prints nothing.

## 4. Add a pull request template

If `.github/pull_request_template.md` is missing, copy [`assets/pull_request_template.md`](assets/pull_request_template.md) there. If one exists, show the user its contents and propose adding the template's **Jira** section at the top.

Done when `.github/pull_request_template.md` contains a Jira link section.

## 5. Report

Tell the user setup is complete and list:

- The values recorded: Objective (with summary), project labels, base branch, GitHub repo.
- Every file created or changed.
- The engineering skills that now read from `docs/agents/`.

Mention that they can edit `docs/agents/*.md` directly later; re-running this skill is only needed to switch issue trackers or start over.
