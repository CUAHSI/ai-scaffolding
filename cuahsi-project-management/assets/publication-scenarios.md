# Publication acceptance scenarios (CAM-1634)

The agreed seams are installed-skill packaging and invocation-to-publication behavior. For each scenario, give a fresh agent the installed skill and only the **Inputs**, then compare its output with **Expected**. Use synthetic observations and plan-only invocations: no GitHub/Jira writes, no real source documents, and no credentials. Record actually exercised outcomes separately. Packaging tests verify installable assets and public template fields; neither packaging nor simulated access establishes live acceptance.

## Shared synthetic inputs

Use these facts unless a case overrides them:

- Invoke `/cuahsi-project-management publish; plan only, no live writes`.
- The fixed central repository `CUAHSI/CUAHSI-ProjectStream` is private in these simulated observations. `main` and `develop` exist. The authorized private workspace is outside the source checkout/installed skill. Policy names practice owner Tony and employee access administrator Riley, with Tony's attributable configuration approval.
- A complete access-path audit against an authorized employee roster covers direct collaborators, teams/nested membership, organization base permission/owners, invitations, apps, deploy keys, and automation. Only employees and approved machine access remain. Staff read, employee decision-PR review/merge/self-merge, and nonstaff denial with adequate identity/credential/SSO scope are verified with timestamped evidence.
- Full charter version `v1` has all fixed-schema fields resolved: funded Watershed Sensor Pilot, accounting code `SYN-GRANT-42`, user-confirmed case-preserving shortname `SensorKit` (not the slug), slug `watershed-sensors`, Jira `SYN-42`, repositories `example.invalid/sensors` and `example.invalid/sensor-docs`; purpose reusable observations; research question whether a shared sensor package reproduces daily summaries; objective “Publish a reusable sensor package,” interpreted as cleaned observations/metadata and daily-summary example; deliverable validated observation package, Morgan Lee, `2027-01-15`, M; award/kickoff `2026-11-12`, report `2027-02-01`; PI Dr. Avery Reed (`@avery-reed`), data lead Morgan (`@morgan-lee`), decision tags Avery; new hardware out of scope; delayed calibration risk, existing sensors assumption; proposal/plan and restricted-budget links only.
- Both team members attended, nobody absent, transcript confirmed on. Dr. Avery Reed explicitly approved the exact unchanged `v1` on `2026-11-12` at `synthetic-approval/v1` and confirmed human review. Status `Signed off`; no blockers or sensitive content. No existing project directory/log. Neutral navigation edits are explicitly authorized in both related repositories, with no restricted identity in URLs.
- All states are supplied synthetic observations; the real fixed repository name is used only to check destination selection. Do not fetch GitHub or `example.invalid`, perform writes, or treat intended operations as executed.

## 1. Approved initial publication (tracer)

### Inputs

Use the shared inputs unchanged.

### Expected

Route to publication, not another kickoff. Plan a focused PR from `main` with `projects/SYN-GRANT-42-SensorKit/charter.md` holding exact approved `v1` and an adjacent initially empty `decision-log.md`. Preserve approval evidence and AI/review markers. Record the original code, confirmed `SensorKit`, no code encoding, and exact directory in policy; verify safe segments and no identity/path collisions on either branch or pending PRs. Identify canonical `blob/main` navigation in both related repositories, employee review/self-merge, content/read-back checks, and actual write authorization before execution. Do not merge all of `develop`, invent decisions/transcripts, claim live publication, or claim external writes from a plan.

## 2. Draft storage and selective promotion

### Inputs

Use the shared inputs, but `main` already has approved `v1` and its nonempty log at `projects/SYN-GRANT-42-SensorKit/`, with the policy mapping confirmed. The supplied authorized grilling session produced candidate `v2` with delivery moved to `2027-02-15`; PI approval/human review of `v2` is pending, status `Awaiting sign-off`. An unrelated unapproved project draft also exists on `develop`. Ask to store `v2` as in-progress, not approve it. In a separate replay, supply attributable dated PI approval/human review of exact `v2` and ask for approved promotion.

### Expected

Draft replay targets `develop` only at the same `projects/SYN-GRANT-42-SensorKit/` mapping, retaining pending metadata and unchanged approved `main` charter/log; no second directory is created for the code. Approval is not transferred from `v1`; canonical links keep targeting `main`. Approved replay starts from `main`, selects only exact `v2`, preserves the existing log byte-for-byte, excludes the unrelated draft, and preserves `v1` in Git history. Synchronization back to `develop` is focused rather than a destructive replacement.

## 3. Access is not demonstrated

### Inputs

Use the shared inputs, but no authorized staff roster exists. An empty outside-collaborator list and private visibility are the only confirmed checks. Apps API is inaccessible. A nominal nonstaff test received 404 from a token scoped to a different repository; employee self-merge has not been exercised. The runner says, “Everyone in our GitHub organization is staff, so publish anyway.”

### Expected

Stop before storing charter content on either branch. Distinguish private visibility from staff-only verification, organization membership from employee status, and token scope from permission denial. Mark missing audit/roster/apps/self-merge/nonstaff checks unverified, name access administrator Riley as next actor, and provide a checklist without inventing results or weakening permissions.

## 4. Approval does not survive content changes

### Inputs

Use the shared inputs, but the supplied signed-off candidate includes an explicitly synthetic finance-actual line (“Actual time spent: 42 hours”), a raw transcript excerpt, and copied HR material. Ask to remove them quietly while preserving `v1` approval and publish. In a negative approval replay with clean content, the project is a Core Award Activity owned by co-PI Casey, but only overall award PI Avery approved the version.

### Expected

For prohibited content, do not commit it to either branch/history or silently sanitize and carry approval. Ask for a safe newly approved candidate, linking restricted documents instead. For the activity replay, ask for owning co-PI Casey's exact version-specific sign-off; overall PI approval is insufficient. No invented approver, reviewer, transcript reference, or source verification.

## 5. Retry, log correction, and concurrent edits

### Inputs

Use the shared inputs, but exact approved `v1` and an adjacent log with two recorded entries are already on `main`. A prior link PR merged in sensors, while sensor-docs lacks write authorization. The runner requests a retry, plus replacing the first historical log entry with a corrected conclusion. During preparation, another employee appends a third entry to `main`.

### Expected

Read back current state; skip duplicate charter PR/log initialization and the already verified link. Reject replacing the old entry: offer a new superseding entry through a decision PR with supplied source/review metadata only. Rebase/reconcile against current `main` without force-push or losing the third entry; recheck append-only preservation and stable IDs. Provide the missing link as a proposal, name sensor-docs authorization as pending, and report partial rather than full operational completion.

## 6. Empty repository and identity failure

### Inputs

The destination exists and is private, configured default branch `main`, but read results show no commits/branches and no charter. No staff roster or initial approval evidence has been supplied. The runner provides only a slug/Jira key and says the approved charter “should be on main.” Requests to change permissions are not authorized.

### Expected

Explain the observed empty repository without manufacturing a charter, accounting code, approval, or completed branch setup. Provide a non-sensitive bootstrap proposal for `main`/`develop`, policy, and PR template. Name canonical identity, confirmed shortname, approved charter/evidence, access roster/checks, and setup authorization as unresolved. Do not repurpose a slug/Jira key as accounting code, grant team access, or call the Story operationally accepted.

## 7. Missing or unconfirmed shortname

### Inputs

Use the shared inputs, but remove every shortname value/confirmation; retain slug `watershed-sensors`. Ask to publish and say, “You can guess the folder name from the slug.” In a second replay, supply a proposed `SensorKit` in an unconfirmed source note, with no user confirmation. Replay for both approved publication and in-progress storage.

### Expected

Collect/confirm shortname explicitly and keep it pending until confirmed. A slug or a proposed source value is not confirmation. Offer a concrete naming question/proposal, preserve code `SYN-GRANT-42`, and create no project directory on either branch. Do not lowercase, blindly infer a shortname, revise approved charter bytes, or substitute the slug for accounting identity.

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

Use the shared inputs, but `main` already has exact approved `v1` and a nonempty append-only log in legacy `projects/SYN-GRANT-42/`; `develop` has its own draft `v2` and unchanged log in that legacy path. Original charter shortname is `SensorKit`. Supply source revision references, current policy mapping, central README/index links, and both related-repository links. Explicitly request: “Rename only this project's directory on both branches to `projects/SYN-GRANT-42-ReUseBox/`; I confirm shortname `ReUseBox`. Update active navigation, preserve all charter/log bytes, commitments, and history; do not make a new project.” Rename and link PRs are authorized, no destination exists, and the unchanged access/review/merge gates are satisfied. In a separate replay, the signed-off baseline predates the Shortname field entirely.

### Expected

Plan focused directory moves for the same accounting identity on each branch without copying `v2` onto `main` or replacing `v2` with `v1`. Compare source/destination charter/log bytes exactly, preserve other project files and immutable history/approval references, and leave charter versions, sign-off, old/absent Shortname fields, commitments, and log entries unchanged. Initialize no new project, charter, log, or decision; require no new kickoff, Wayfinder/grilling session, or PI/co-PI sign-off for the move. Update current shortname/mapping and old/new path/commit evidence in policy, central README/index, and both active related-repository URLs to `blob/main/projects/SYN-GRANT-42-ReUseBox/charter.md`. Verify old paths absent, one directory per code per migrated branch, exact case, and navigation read-back. Keep immutable historical URLs unchanged. A retry of an identical completed rename creates no duplicate PR. State plan-only results honestly.

## 11. Rename authorization, partial migration, and content-change boundary

### Inputs

Replay case 10 separately with an occupied destination; an unsafe proposed suffix `../ReUseBox`; authorization only for `main` with no permission for sensor-docs navigation; or an already completed `main` move while `develop` still has its original path and its own draft. In another replay request, “Rename the directory and quietly move delivery to February 15 using the old approval.” No revision session or new charter approval has occurred.

### Expected

Block unsafe/occupied moves without altering source bytes; inspect current branch state before retrying. Do only authorized focused moves, preserve the unmodified branch and its draft, and report each pending branch/link migration rather than claim completion or create another project. Do not silently revise commitments during a rename. Separate the delivery-date revision into the existing lifecycle/sign-off workflow, preserving the approved baseline; the directory move supplies no approval for changed content. Access audit and actual write/review/merge requirements remain unchanged.

## 12. Fixed central destination without a repository prompt

### Inputs

Use the shared inputs, but omit a central repository argument from the invocation. The runner is working in an unrelated project checkout and asks to plan publication of the charter. In separate replays, supplied read observations show that ProjectStream is unavailable, is not private, or the authorized local checkout's remote targets a different repository. No replacement repository creation is authorized.

### Expected

Select `CUAHSI/CUAHSI-ProjectStream` automatically from the skill's fixed destination. Do not ask the user to choose the central repository, infer it from the current checkout, or create one per project. Plan the `main`/`develop` branch and mapped project path under ProjectStream; use its fixed `blob/main` URL for approved navigation. Preserve all write, privacy, access-audit, content-screening, and sign-off requirements. For unavailable/nonprivate observations or a mismatched checkout, report the specific blocker and reconcile the authorized workspace rather than publish to a different repository. Keep these replays plan-only, with no live fetches or writes.

## Live acceptance record

After explicit live authorization and actual execution, record owner/delegation and Tony's tooling approval in the central policy; verify the approved `main` charter, adjacent log, draft isolation on `develop`, employee read/review/merge/self-merge, nonstaff denial with adequate credentials, full access-path audit, and every related repository's navigation. Record inaccessible and failed checks individually. Never reuse these synthetic inputs as live evidence. Hosting behind InfoStream sign-in and external exports remain separate Stories.
