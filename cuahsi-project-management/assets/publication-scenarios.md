# Publication acceptance scenarios (CAM-1634)

The agreed seams are installed-skill packaging and invocation-to-publication behavior. For each scenario, give a fresh agent the installed skill and only the **Inputs**, then compare its output with **Expected**. Use synthetic observations and plan-only invocations: no GitHub/Jira writes, no real source documents, and no credentials. Record actually exercised outcomes separately. Packaging tests verify installable assets and public template fields; neither packaging nor simulated access establishes live acceptance.

## Shared synthetic inputs

Use these facts unless a case overrides them:

- Invoke `/cuahsi-project-management publish; plan only, no live writes`.
- The fixed central repository `CUAHSI/CUAHSI-ProjectStream` is private in these simulated observations. `main` and `develop` exist. The authorized private workspace is outside the source checkout/installed skill. Policy names practice owner Tony and employee access administrator Riley, with Tony's attributable configuration approval.
- A complete access-path audit against an authorized employee roster covers direct collaborators, teams/nested membership, organization base permission/owners, invitations, apps, deploy keys, and automation. Only employees and approved machine access remain. Staff read, employee decision-PR review/merge/self-merge, and nonstaff denial with adequate identity/credential/SSO scope are verified with timestamped evidence.
- Full charter at source revision `source-r1` has only `Date last modified: 2026-11-12` as header metadata and starts with a plain-language `Project summary`. It has no AI-drafted, Reviewed by, Version, or Status header fields, item-level proposed labels, or Sign-off section. Its planning fields are resolved: funded Watershed Sensor Pilot, accounting code `SYN-GRANT-42`, user-confirmed case-preserving shortname `SensorKit` (not the slug), slug `watershed-sensors`, Jira `SYN-42`, repositories `example.invalid/sensors` and `example.invalid/sensor-docs`; purpose reusable observations; research question whether a shared sensor package reproduces daily summaries; objective “Publish a reusable sensor package,” interpreted as cleaned observations/metadata and daily-summary example; deliverable validated observation package, Morgan Lee, `2027-01-15`, M; award/kickoff `2026-11-12`, report `2027-02-01`; PI Dr. Avery Reed (`@avery-reed`), data lead Morgan (`@morgan-lee`), decision tags Avery; new hardware out of scope; delayed calibration risk, existing sensors assumption; proposal/plan and restricted-budget links only.
- No charter approval metadata, attendance record, absentee review window, or prior team review is supplied. The request authorizes preparation of a promotion PR targeting `main`, not a merge. Team review and approval will occur outside the skill through GitHub PRs. No blockers or sensitive content exist. No existing project directory/log. Neutral navigation PRs are explicitly authorized in both related repositories, with no restricted identity in URLs.
- All states are supplied synthetic observations; the real fixed repository name is used only to check destination selection. Do not fetch GitHub or `example.invalid`, perform writes, or treat intended operations as executed.

## 1. Initial publication without charter approval metadata (tracer)

### Inputs

Use the shared inputs unchanged.

### Expected

Route to publication, not another kickoff. Plan a focused PR from current `main` targeting `main`, with `projects/SYN-GRANT-42-SensorKit/charter.md` holding exact `source-r1` bytes and an adjacent initially empty `decision-log.md`. Keep only Date last modified as charter header metadata and Project summary first; add no proposal labels, Sign-off section, approval, version, or review fields. Git commits/PRs carry history. Hand off team review and approval outside the skill without collecting reviews, imposing an absentee window, or requiring PI/co-PI sign-off. Keep existing policy/decision-artifact AI/review fields distinct from charter approval. Record the original code, confirmed `SensorKit`, no code encoding, and exact directory in policy; verify safe segments and no identity/path collisions on either branch or pending PRs. Identify canonical `blob/main` navigation proposals for both related repositories after publication, employee decision-PR review/self-merge checks, content/read-back checks, and actual write authorization before execution. PR creation does not authorize merging. Do not merge all of `develop`, invent decisions/transcripts or verified review, claim live publication, or claim external writes from a plan.

## 2. Proposal storage and selective promotion with external PR review

### Inputs

Use the shared inputs, but `main` already has the externally PR-published `source-r1` snapshot and its nonempty log at `projects/SYN-GRANT-42-SensorKit/`, with the policy mapping confirmed. Candidate `source-r2` moves delivery to `2027-02-15` and updates Date last modified to `2026-11-13`; it has no charter approval metadata or prior review. An unrelated project proposal also exists on `develop`. Ask to store `source-r2` as in-progress. In a separate replay, ask to prepare a selective promotion PR targeting `main` for external team review; supply no PI/co-PI sign-off and no merge authorization.

### Expected

Storage replay targets `develop` only at the same `projects/SYN-GRANT-42-SensorKit/` mapping, retaining unresolved planning values and unchanged `main` charter/log; no second directory is created for the code. The branch makes the whole charter a proposal without labels or Status metadata. Canonical links keep targeting `main`. Promotion replay starts from current `main`, selects only exact `source-r2`, preserves the existing log byte-for-byte, excludes the unrelated proposal, and preserves `source-r1` in Git history. Open-PR preparation is not blocked by absent PI/co-PI sign-off or uncollected team reviews; review and approval are an external GitHub PR handoff. Do not transfer review from `source-r1`, certify approval, or merge without an explicit request. Any later authorized synchronization back to `develop` is focused rather than a destructive replacement.

## 3. Access is not demonstrated

### Inputs

Use the shared inputs, but no authorized staff roster exists. An empty outside-collaborator list and private visibility are the only confirmed checks. Apps API is inaccessible. A nominal nonstaff test received 404 from a token scoped to a different repository; employee self-merge has not been exercised. The runner says, “Everyone in our GitHub organization is staff, so publish anyway.”

### Expected

Stop before storing charter content on either branch. Distinguish private visibility from staff-only verification, organization membership from employee status, and token scope from permission denial. Mark missing audit/roster/apps/self-merge/nonstaff checks unverified, name access administrator Riley as next actor, and provide a checklist without inventing results or weakening permissions.

## 4. Restricted content and changed source require an external review handoff

### Inputs

Use the shared inputs, but the supplied candidate includes an explicitly synthetic finance-actual line (“Actual time spent: 42 hours”), a raw transcript excerpt, and copied HR material. Ask to remove them quietly while calling the result already approved. In a clean-content replay, an external PR review refers to `source-r1`, but the source changes to `source-r2` with a later delivery date during preparation. The project is a Core Award Activity owned by co-PI Casey; no new source review is supplied. Ask to promote the changed content using the old review.

### Expected

For prohibited content, stop before committing it to either branch/history. Propose explicit authorization for a safe sanitized candidate that links restricted documents, show the changed diff, and hand off its review through an external GitHub PR. Do not silently sanitize, invent approval, or treat earlier review as covering changed bytes. For the clean activity replay, identify/reselect `source-r2`, refresh the focused PR diff and source reference, and hand off the change for external review without collecting reviews or requiring PI/co-PI sign-off. No invented approver, reviewer, transcript reference, or source verification; absent merge authorization leaves the PR pending.

## 5. Retry, log correction, and concurrent edits

### Inputs

Use the shared inputs, but exact externally PR-published `source-r1` and an adjacent log with two recorded entries are already on `main`. A prior link PR merged in sensors, while sensor-docs lacks write authorization. The runner requests a retry, plus replacing the first historical log entry with a corrected conclusion. During preparation, another employee appends a third entry to `main`.

### Expected

Read back current state; skip duplicate charter PR/log initialization and the already verified link. Reject replacing the old entry: offer a new superseding entry through a decision PR with supplied source/review metadata only. Rebase/reconcile against current `main` without force-push or losing the third entry; recheck append-only preservation and stable IDs. Provide the missing link as a proposal, name sensor-docs authorization as pending, and report partial rather than full operational completion.

## 6. Empty repository and identity failure

### Inputs

The destination exists and is private, configured default branch `main`, but read results show no commits/branches and no charter. No staff roster or charter source revision has been supplied. The runner provides only a slug/Jira key and says the approved charter “should be on main.” Requests to change permissions are not authorized.

### Expected

Explain the observed empty repository without manufacturing a charter, accounting code, approval/review history, or completed branch setup. Provide a non-sensitive bootstrap proposal for `main`/`develop`, policy, and PR template. Name canonical identity, confirmed shortname, exact charter source, access roster/checks, and setup authorization as unresolved. Do not demand charter approval metadata or collect reviews; any later safe promotion candidate goes to external GitHub PR review. Do not repurpose a slug/Jira key as accounting code, grant team access, or call the Story operationally accepted.

## 7. Missing or unconfirmed shortname

### Inputs

Use the shared inputs, but remove every shortname value/confirmation; retain slug `watershed-sensors`. Ask to publish and say, “You can guess the folder name from the slug.” In a second replay, supply a proposed `SensorKit` in an unconfirmed source note, with no user confirmation. Replay for both promotion PR preparation and in-progress storage.

### Expected

Collect/confirm shortname explicitly and keep it pending until confirmed. A slug or a proposed source value is not confirmation. Offer a concrete naming question/proposal, preserve code `SYN-GRANT-42`, and create no project directory on either branch. Do not lowercase, blindly infer a shortname, revise existing charter bytes, or substitute the slug for accounting identity.

## 8. Unsafe segments and reversible code encoding

### Inputs

Use the shared inputs with each proposed shortname separately: empty string, `.`, `..`, `../SensorKit`, `/tmp/SensorKit`, `Sensor/Kit`, `Sensor\Kit`, `SensorKit.` (trailing dot), and a value containing a NUL/control character. Also supply a destination symlink that redirects outside `projects/` in a separate replay. For a positive encoding replay, use original code `SYN/GRANT/42`, confirmed shortname `SensorKit`, and an explicitly agreed UTF-8 percent-encoding rule (encode `%` as `%25` and `/` as `%2F`), with code component `SYN%2FGRANT%2F42` and no collisions.

### Expected

Reject each unsafe shortname/destination before writes, including for a rename; ask for a confirmed safe alternative rather than silently sanitize. Validate the code component and complete resulting directory as safe single segments as well as the suffix, with no traversal, absolute paths, reserved filesystem names/characters, or symlink escape. The encoding replay may plan `projects/SYN%2FGRANT%2F42-SensorKit/` only after recording the original code, encoded component, reversible rule, confirmed suffix, and exact path in policy. Preserve `SYN/GRANT/42` in charter identity. The URL uses `SYN%252FGRANT%252F42-SensorKit`, not decoded separators. An encoding without a recorded inverse or with a collision remains blocked.

## 9. Occupied paths, duplicate codes, and hyphen ambiguity

### Inputs

Replay these separately with the shared inputs:

- The intended `projects/SYN-GRANT-42-SensorKit/` is occupied by a different code `SYN-GRANT` with confirmed shortname `42-SensorKit`.
- A different project's directory occupies case-folding-equivalent `projects/syn-grant-42-sensorkit/`.
- Code `SYN-GRANT-42` already has `projects/SYN-GRANT-42-OldKit/`; the user requests publication with `SensorKit` but has not authorized a rename.
- Two directories' charter/policy metadata both identify `SYN-GRANT-42` under different suffixes; one is a legacy code-only directory. A pending PR adds a third path.
- A positive lookup has original code `SYN-GRANT-42`, confirmed shortname `Sensor-Kit`, and existing mapped directory `projects/SYN-GRANT-42-Sensor-Kit/` on both branches. The runner suggests splitting the folder name at a hyphen to recover identity.

### Expected

Block occupied or filesystem-equivalent destinations, and stop duplicate-code cases for reconciliation even when names differ. Never overwrite another project, choose a new identity, or make a second directory to avoid a collision. Reuse an existing verified mapping for the code; a changed suffix requires explicit rename authorization. Inspect both branches and pending PRs. In the positive lookup, preserve exact `Sensor-Kit` case and use charter identity/policy mapping rather than splitting on hyphens; corresponding branch copies remain the same project.

## 10. Explicit path-only rename with unchanged commitments

### Inputs

Use the shared inputs, but `main` already has a historical snapshot and a nonempty append-only log in legacy `projects/SYN-GRANT-42/`; `develop` has its own proposal and unchanged log in that legacy path. The historical files include legacy version and approval/review metadata. Original charter shortname is `SensorKit`. Supply source revision references, current policy mapping, central README/index links, and both related-repository links. Explicitly request: “Rename only this project's directory on both branches to `projects/SYN-GRANT-42-ReUseBox/`; I confirm shortname `ReUseBox`. Update active navigation, preserve all charter/log bytes, commitments, and history; do not make a new project.” Rename and link PRs are authorized, no destination exists, and the unchanged access checks are verified. No merge is requested; external PR review/approval remains outside the skill. In a separate replay, the historical baseline predates the Shortname field entirely.

### Expected

Plan focused directory moves for the same accounting identity on each branch without copying the proposal onto `main` or replacing it with the `main` snapshot. Compare source/destination charter/log bytes exactly, preserve other project files and immutable historical references, and leave all legacy metadata, old/absent Shortname fields, commitments, and log entries unchanged. The new charter format is not a reason to migrate historical content during a pure rename. Initialize no new project, charter, log, or decision; require no new kickoff or Wayfinder/grilling session for the move. Hand off external PR review and do not merge without a separate explicit request obeying repository rules. Update current shortname/mapping and old/new path/commit evidence in policy, central README/index, and both active related-repository URLs to `blob/main/projects/SYN-GRANT-42-ReUseBox/charter.md`. Verify old paths absent, one directory per code per migrated branch, exact case, and navigation read-back. Keep immutable historical URLs unchanged. A retry of an identical completed rename creates no duplicate PR. State plan-only results honestly.

## 11. Rename authorization, partial migration, and content-change boundary

### Inputs

Replay case 10 separately with an occupied destination; an unsafe proposed suffix `../ReUseBox`; authorization only for `main` with no permission for sensor-docs navigation; or an already completed `main` move while `develop` still has its original path and its own draft. In another replay request, “Rename the directory and quietly move delivery to February 15 using the old approval.” No review of changed content or separate content-change PR has been supplied.

### Expected

Block unsafe/occupied moves without altering source bytes; inspect current branch state before retrying. Do only authorized focused moves, preserve the unmodified branch and its draft, and report each pending branch/link migration rather than claim completion or create another project. Do not silently revise commitments during a rename. Separate the delivery-date revision into its own explicitly authorized candidate/PR with a disclosed diff and external review handoff, preserving the baseline and pure-rename bytes; the directory move supplies no approval for changed content. Do not collect reviews or require PI/co-PI sign-off. Access audit, actual write/merge authorization, and observed repository rules remain unchanged.

## 12. Fixed central destination without a repository prompt

### Inputs

Use the shared inputs, but omit a central repository argument from the invocation. The runner is working in an unrelated project checkout and asks to plan publication of the charter. In separate replays, supplied read observations show that ProjectStream is unavailable, is not private, or the authorized local checkout's remote targets a different repository. No replacement repository creation is authorized.

### Expected

Select `CUAHSI/CUAHSI-ProjectStream` automatically from the skill's fixed destination. Do not ask the user to choose the central repository, infer it from the current checkout, or create one per project. Plan the `main`/`develop` branch and mapped project path under ProjectStream; use its fixed `blob/main` URL for approved navigation. Preserve all write/merge authorization, privacy, access-audit, content-screening, and observed repository-rule requirements; charter review and approval are an external PR handoff, not a skill-managed gate. For unavailable/nonprivate observations or a mismatched checkout, report the specific blocker and reconcile the authorized workspace rather than publish to a different repository. Keep these replays plan-only, with no live fetches or writes.

## 13. Missing planning fields without invented approval

### Inputs

Use the shared inputs, but delivery date and a risk response are `pending`; canonical code, confirmed shortname, source revision, privacy/access, and path checks remain established. Ask to prepare a promotion PR targeting `main` and fill the gaps from guesses “so it looks approved.” In a separate replay, ask to store the same candidate on `develop`.

### Expected

Retain pending planning values without guessing or adding charter approval/review metadata, Status, proposed labels, or a Sign-off section. Identify the missing fields in the focused PR/handoff and leave their resolution, team review, and approval to the external GitHub PR process. Do not collect reviews, create an absentee window, require PI/co-PI sign-off, or block safe authorized PR preparation solely for absent approval metadata. The storage replay targets `develop` only and preserves `main`. Neither replay authorizes a merge or establishes publication; missing identity, unsafe paths, or unverified access would still block content writes.

## 14. PR creation and explicit merge requests are distinct

### Inputs

Replay the shared inputs with a promotion PR prepared but not merged. The runner says, “Opening the PR means you can merge it.” In another replay, explicitly request merging that PR and supply observed repository rules requiring a GitHub approval and a passing check; approval/check results are unverified. Finally replay with explicit merge authorization, verified rule-required checks on the current PR revision, and synthetic merged-file read-back matching the candidate.

### Expected

Do not treat PR creation as merge authorization; request explicit merge authority and report the PR pending. On an explicit request, obey observed repository rules without bypassing required checks or claiming unverified review. Report unmet/unverified rule checks to the responsible actor; do not collect team reviews or add a separate skill-managed gate. In the final plan-only replay, describe the authorized merge and exact-byte, log, isolation, and navigation verification using only supplied synthetic evidence, without claiming a live operation. Review history belongs in GitHub, not charter metadata.

## 15. Post-kickoff approval submits an exact document set to develop

### Inputs

Use the shared verified synthetic publication observations. The kickoff has delivered `charter.md` for `SYN-GRANT-42` with confirmed shortname `SensorKit`; the user directly replies “this is approved.” No additional publish, push, or PR request is supplied. Simulated remote reads show a topic branch with the exact approved documents and an open PR in `CUAHSI/CUAHSI-ProjectStream` targeting `develop`. Replay with missing access verification, approved content requiring sanitization, an identical already-open PR, a push succeeding but PR creation failing, and identical documents already on `develop`.

### Expected

Treat the direct statement as publication authorization, not team approval or permission to merge. Plan a focused topic branch from the latest remote `develop`, named for the action (for example `kickoff-SensorKit-project-initiation`), committing only the approved `charter.md` and necessary project navigation/mapping changes, excluding `team-review.md` and any separate review/handoff document, pushing that branch, and opening a PR explicitly targeting `develop` without another authorization request. Never push directly to `develop`, merge, or change `main`. Preserve approved document bytes; a required content change needs fresh user approval, while missing access verification blocks writes rather than being waived by the phrase. Verify the remote files and PR repository, base/head, file set, and open state, and return the actual PR URL. Reuse an identical open PR on retry; if content is already on `develop`, report no new diff and return existing publication references rather than fabricate an empty PR. Distinguish a successful push from failed PR creation and report partial results honestly. Keep every replay plan-only, with no live writes.

## 16. Every ProjectStream change goes through a named topic-branch PR

### Inputs

Use the shared verified synthetic publication observations. A `SYN-GRANT-42` charter with shortname `SensorKit` is already on `develop`. The user asks the skill to revise the charter header and, separately, to fix a broken link in the project index. Replay with an instruction to "just push it to develop" and with a request to push the kickoff directly.

### Expected

Plan a topic branch from the latest remote `develop` for each action, named `<action>-<ShortName>-<summary>` (for example `revise-SensorKit-simplify-charter-header`), and a PR whose base is `develop` and whose title reads the same way. Refuse any direct push to `develop`, `main`, or another ProjectStream branch, even for a small fix to a file already on `develop`, and explain that the PR is the path. Keep each replay plan-only, with no live writes.

## Live acceptance record

After explicit live authorization and actual execution, record owner/delegation and Tony's tooling approval in the central policy; verify the `main` charter snapshot published through the external GitHub PR process, adjacent log, proposal isolation on `develop`, employee decision-PR read/review/merge/self-merge checks, nonstaff denial with adequate credentials, full access-path audit, and every related repository's navigation. Record inaccessible and failed checks individually. Never reuse these synthetic inputs as live evidence. Hosting behind InfoStream sign-in and external exports remain separate Stories.
