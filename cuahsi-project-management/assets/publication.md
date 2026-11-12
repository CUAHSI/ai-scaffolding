# Publish project information (CAM-1634)

Use this procedure only for an explicit `cuahsi-project-management publish` request, including a request to store an in-progress charter. Publication is a separate branch of the skill, not a kickoff side effect. Every generated policy, log, PR, notice, and handoff carries an AI-drafted marker and a reviewed-by field, with human review recorded only from actual evidence. Use GitHub CLI and Git already available in the environment; no separate application, hosting, transcript ingestion, or email service is introduced.

## 1. Establish destination and authority

Confirm the private central repository, responsible practice owner, access administrator, canonical accounting code, charter/version, intended draft or approved publication, and all related project/activity repositories. Read the existing central policy or start a candidate from the [repository policy template](repository-policy-template.md). Tony approves tooling changes; credential/hosting work has a named, explicitly delegated owner. Ask for missing administrative authority instead of choosing a staff team or changing permissions unilaterally.

Inspect repository visibility, contents, branches, and current project files with authenticated read-only operations. An empty repository has no charter and may have no branches even when its configured default branch is `main`. A failed request is not evidence of absence. Keep live project documents and audit data outside this source checkout and the installed skill. Use an explicitly authorized private workspace; retain existing files and user changes.

**Done when:** the destination and requested writes are explicit, and missing identity, policy, credentials, or approval information is listed. Without a canonical code, offer a plan but store neither a draft nor an approved charter under an invented identity.

## 2. Audit effective access

Complete the policy's access configuration and verification record before committing project content, including drafts. Compare all effective access paths against an authorized employee roster, not organization membership. Check private visibility, organization base permission, organization owners, all direct collaborators, teams and inherited/nested membership, pending invitations, apps, deploy keys, and automation. Employees need write permission to propose and merge decisions; external collaborators receive exports through the separate export workflow. Authorized machine access must have a named accountable owner.

For the confirmed repository, representative read operations are:

```sh
gh repo view <owner/repository> --json isPrivate,defaultBranchRef,viewerPermission
gh api repos/<owner/repository>/collaborators --paginate
gh api 'repos/<owner/repository>/collaborators?affiliation=outside' --paginate
gh api repos/<owner/repository>/teams --paginate
gh api repos/<owner/repository>/invitations --paginate
gh api repos/<owner/repository>/keys --paginate
gh api repos/<owner/repository>/rulesets --paginate
gh api repos/<owner/repository>/rules/branches/main
gh api repos/<owner/repository>/rules/branches/develop
```

Also inspect organization permissions/owners, each team's members and children, applicable branch protections including inherited rules, and installed GitHub Apps using appropriately authorized administration APIs. Resolve actual account/team names from read results before generating commands. Keep roster and audit details private; record references rather than HR contents or credentials. An inaccessible API is `unverified`, not an empty access list.

Test staff read and nonstaff denial using explicitly authorized test identities with adequate credentials/SSO authorization. For a new repository, first audit access configuration, then perform the explicitly approved non-sensitive bootstrap in step 3 so read/merge probes have a real target. Complete those probes before committing any charter content; repeat read checks against the approved charter after publication. Record bootstrap probes as such, not as an approved-charter read. A 404 from a narrowly scoped token or an unauthenticated request alone cannot distinguish an access restriction from inadequate credentials. Record identities, adequate scope, timestamp, observation, and result without tokens. Confirm employee decision-PR review, merge, and self-merge through a harmless synthetic PR. Review counts, author-approval restrictions, CODEOWNERS requirements, push restrictions, or inherited rules must not effectively prohibit the agreed employee self-merge policy. Do not weaken organization rules or remove collaborators without the owner's explicit approval; hand off the exact conflict to the access administrator.

**Done when:** each access check is `verified`, `failed`, or `unverified` with evidence. Publish project content only when the complete audit and staff/nonstaff/merge checks are verified. If blocked, provide templates and a delegated checklist; only the separately authorized non-sensitive bootstrap may proceed before branch-dependent probes pass. Do not claim staff-only access or operational acceptance. Synthetic checks establish scenario behavior, not live permissions.

## 3. Establish repository layout and branches

Under the confirmed policy, `main` contains approved charters and their decision logs; `develop` contains visibly in-progress charters. Both use:

```text
POLICY.md
.github/pull_request_template.md
projects/<accounting-code>/charter.md
projects/<accounting-code>/decision-log.md
```

The adjacent decision log is required for an approved charter. A draft does not invent approved-charter metadata or decision entries. Use one project directory per accounting code, including multi-repository projects. If a code is not safe as a single path segment, agree and record a reversible encoding; reject traversal, absolute paths, and ambiguous collisions. Preserve the original code in charter identity. Build canonical navigation URLs using `blob/main`, never the changing default branch or `develop`.

For an empty repository, obtain approval for a bootstrap commit containing only non-sensitive policy/navigation and the [decision PR template](decision-pr-template.md) at `.github/pull_request_template.md`. Create `main` and then `develop` from that bootstrap, make `main` the default, and read back both refs/configuration. The bootstrap has no approved charter. For existing repositories, propose focused configuration PRs; preserve contents and policy. Adding branches, publishing charter content, granting access, and merging PRs are distinct authorized actions. Confirm the intended changes rather than treating a read/plan request as permission to write. Never force-push, replace history, or merge a whole draft branch into the approved branch.

**Done when:** branches/layout are read back as configured, or their exact remaining setup/delegation is reported. Record Tony's actual tooling approval and the responsible administrator; drafting policy is not approval of it.

## 4. Select and screen the exact charter

Read the complete [charter template](charter-template.md) and apply the main skill's sign-off and lifecycle rules. For approved publication, require the exact candidate version, all required fields and participation/reopening steps resolved, and attributable dated approval by the named PI or owning activity co-PI. Team consensus, a repository merge, a filename, and a user's description of the branch as approved do not substitute for that evidence. An unchanged previously approved charter may be published without a new kickoff. A changed charter requires its authorized Wayfinder/grilling session and new version-specific sign-off; approval never transfers from its baseline.

For draft publication, retain `Draft` or `Awaiting sign-off`, all pending values, and absent approval honestly. Save only to `develop`; do not create or replace an approved charter on `main` or link project repositories to an unapproved version as canonical. Existing approved `main` content and logs remain intact. Draft publication still requires verified access and content screening.

Inspect the exact proposed content, including metadata, URLs, filenames, PR body, and the staged diff. Budgets and HR are linked rather than copied. Keep actual time-spent figures, raw transcripts, credentials, and restricted source material out of both branches and Git history. If a signed-off candidate contains prohibited content, stop and ask for a sanitized, reapproved candidate; do not silently edit the approved text or first commit then delete it. Retain AI-drafted markers and actual review metadata. A rough deliverable size is planning information, not a finance actual.

**Done when:** the precise content/version, branch, safety check, approval evidence or draft status, and permitted diff are established. Missing evidence blocks approved publication, not a properly authorized safe draft on `develop`.

## 5. Propose, merge, and verify publication

For a draft, create a focused candidate branch/PR targeting `develop` in the authorized workspace. For an approved initial publication or update, start a fresh branch from current `main` and copy only the exact signed-off candidate's charter bytes from the identified source revision. Do not use a whole `develop` merge: other projects' or versions' unapproved content must remain absent from `main`. Confirm the canonical code, candidate version, and source commit/diff in the PR.

For an initial approved charter, place an empty [decision log](decision-log-template.md) next to it, filling only established identity and approval references. Remove the unused commented entry schema from the published empty log; it is a template, not a recorded decision. Keep the adjacent charter link relative and the approval evidence immutable. Do not fabricate a first decision or transcript reference merely to initialize the log. Existing logs are preserved byte-for-byte, including their historical baseline reference; later decisions cite newer charter versions in appended entries. Corrections append an entry identifying what it supersedes. Compare the proposed log against `main` and reject deletions, edits, reorderings, or duplicate entry IDs. Resolve a concurrent update against the latest `main`, recheck the signed-off charter and log, and request review again if the candidate changes.

Use the standard central PR template; a charter-publication PR also names its version, source revision, approver, dated approval evidence, and content diff. Use confirmed PI/co-PI handles as tags. Every AI-drafted decision entry goes through a PR with [the decision template](decision-pr-template.md); any employee may review/merge, self-merge included. Initializing an empty log is not transcript processing and generates no decisions. Automated extraction, conflict detection, and digests remain later Stories. Human review and charter sign-off are separate; record reviewers and checked boxes only from actual evidence.

Show the exact intended files, base branch, and metadata before writes. Push/open a PR only under the requested publication authorization; merge only when explicitly authorized and required actual human review is established. Use existing credentials without reading or printing secrets. If a PR cannot merge, report it as proposed/pending rather than published. Keep the baseline approved version retrievable by commit link, and synchronize only this project's approved state back to `develop` through a focused reviewed change, preserving unrelated drafts.

Read back merged files from the destination branch. Compare charter bytes/version/approval to the selected candidate, check the adjacent log and append-only invariants, confirm the merged PR and commit, and verify no unrelated draft content reached `main`. On retry, inspect existing branches, PRs, and files first; an identical already-published version needs no duplicate PR or log reset. Partial or failed operations remain explicit; never substitute an intended write for read-back evidence.

**Done when:** the exact content is verified on its destination branch or the PR/failure is clearly pending. Draft storage is not approved publication. A merged decision PR alone is not PI/co-PI charter approval.

## 6. Link every project/activity repository and hand off

For an approved charter, produce the canonical `https://github.com/<owner>/<repository>/blob/main/projects/<encoded-code>/charter.md` URL and list every related repository recorded in the charter. With explicit authorization, add a neutral charter link to each repository's README or existing project-navigation document through its normal PR process. Do not copy the charter or restricted source content. For public/nonstaff repositories, confirm that even the path/URL discloses no restricted identity before proposing it. If identity disclosure is restricted, obtain an approved neutral redirect/export handoff instead of posting the revealing URL. Missing permissions or authorization produce ready-to-review link proposals, not claimed edits.

Read back every merged link on its actual target branch and record URL/commit evidence in the central policy's navigation table. A multi-repository project is complete only when all relevant repositories have verified links, or the gaps are individually named. Do not edit the signed-off charter just to record operational link checks. Re-run access checks after configuration changes and keep private evidence in the authorized central policy/audit location.

Return branch/commit/PR URLs, canonical identity and version, approval status, decision-log location, owner/delegations, access results, and per-repository link results. Display remaining blockers and next actors. Keep live project content and access rosters out of the ai-scaffolding checkout and Jira completion comments. The independent `project-report` workflow stays Jira-only and read-only; this workflow introduces no reporting, hosted MkDocs site, exports, transcript fetching, or email sending.

**Done when:** actual publication, access, and link outcomes are distinguishable from proposals and assumptions. Live acceptance needs an approved charter on `main`, adjacent log, verified staff/nonstaff and employee merge checks, and verified links for every related repository; a tested reusable skill alone does not fulfill those operational checks.
