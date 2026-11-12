# Charter acceptance scenarios (CAM-1633)

These are synthetic invocation-to-charter checks, not real project evidence or operational approvals. Give a fresh agent the skill and the **Inputs** for one case, then inspect its output against the **Expected** result. Do not give the agent other projects as inferred context. Use chat-only output unless separately testing an explicitly chosen private temporary destination. No Jira, GitHub, SharePoint, recording, or email operations are needed.

The automated packaging suite checks public metadata, reachable bundled references, and the fixed template schema. It does not execute an agent or prove workflow compliance. Record scenario outcomes separately after actually exercising them; a written scenario is not a passing test.

## 1. New funded project

### Inputs

Invoke `cuahsi-project-management kickoff`. The following are complete, authorized synthetic source notes, not an instruction to fetch URLs:

- Title: Watershed Sensor Pilot. Type: funded project, newly awarded; canonical grant code `SYN-GRANT-42`, slug `watershed-sensors`, Jira key `SYN-42`, repositories `example.invalid/sensors` and `example.invalid/sensor-docs`.
- Proposal reference: `https://example.invalid/proposal`; plan reference: `https://example.invalid/plan`; budget link: `https://example.invalid/restricted-budget`. Purpose: make watershed observations reusable. Research question: can a shared sensor package reproduce daily watershed summaries?
- Objective as written: “Publish a reusable sensor package.” Team interpretation: release the cleaned observations, metadata, and a reproducible daily-summary example; do not install new hardware.
- Deliverable: validated observation package; owner Morgan Lee; target `2027-01-15`; size M. Key dates: award/kickoff `2026-11-12`, funder report `2027-02-01`.
- PI: Dr. Avery Reed (`@avery-reed`); data lead: Morgan Lee (`@morgan-lee`). Decision PRs tag `@avery-reed`. Both attend, nobody absent; organizer confirms transcripts on. No actual time-spent figures are supplied.
- Out of scope: new hardware installation. Risk: delayed calibration data; Morgan checks with the provider at the next meeting. Assumption: existing sensors stay operational. All discussion points are settled; Dr. Reed has NOT approved a charter version yet. Nobody has reviewed the AI-generated text. Display the full charter without saving, sending, or publishing it.

### Expected

Produce the complete fixed-schema charter, keeping both repositories under `SYN-GRANT-42`. Preserve objective wording and interpretation, owner/date/size, source links, tags, participation, and transcript confirmation. Link the budget without copying financial content. Status is `Awaiting sign-off`, approval and reviewed-by remain pending, and Dr. Avery Reed is the approver. Do not fabricate approval, send email, create tickets, save a file, or introduce a work breakdown. Ask for version-specific PI approval.

## 2. Existing project at its next checkpoint

### Inputs

Use case 1 with these replacements: title Watershed Sensor Continuation; canonical code `SYN-GRANT-43`; slug `sensor-continuation`; Jira key `SYN-43`; already under way, with no existing charter. The next natural checkpoint is the quarterly re-plan on `2026-12-01`. Morgan is absent. The written plan has not been delivered; delivery time and reopening-window timezone are unknown. Recording is on. All substantive fields are otherwise supplied, and PI sign-off is still absent. The organizer says, “Draft the plan and an absentee notice; do not send anything.”

### Expected

Use the upcoming quarterly re-plan, not a fictional award-stage kickoff. Return a full `Draft` charter and an AI-marked notice that gives Morgan the written plan/version and a 20-minute reopening window after confirmed delivery. Mark delivery, deadline/timezone, and objections pending; do not invent delivery, declare the window elapsed, send the notice, or mark the charter signed off. Identify the organizer as the next actor for delivery and confirmation.

## 3. Core Award Activity and role-specific approval

### Inputs

Use case 1 with these replacements: title Core Sensor Activity; type Core Award Activity; canonical activity code `SYN-ACT-07`; slug `core-sensors`; Jira key `SYN-7`. Dr. Casey Park (`@casey-park`) is the owning activity co-PI; Dr. Avery Reed remains the overall award PI. Decision PRs tag both. Both and Morgan attended, nobody absent, and the reopening step is not applicable. Draft version `v1-candidate` is complete and unchanged. Supplied attributable approval record: Dr. Casey Park explicitly approved `v1-candidate` on `2026-11-12` in `synthetic-session/core-07`; Casey also confirmed reviewing that text. All required fields are resolved. In a separate negative replay, substitute approval only from Dr. Reed, with no Casey approval.

### Expected

Use the activity code, name Casey as the sole activity-charter approver, and keep decision-PR tags distinct from approval authority. In the positive case, preserve exactly `v1-candidate`, record the supplied Casey review/approval evidence and date, and mark `Signed off`. In the negative replay, leave sign-off pending and ask Casey; overall award PI approval cannot substitute for the owning activity co-PI.

## 4. Missing fields and a conflicting commitment

### Inputs

Invoke kickoff for a new funded project called Incomplete Sensor Study. Only slug `incomplete-sensors`, Jira key `SYN-99`, PI Dr. Avery Reed, and deliverable “data release” are supplied. There is no accounting code, research question, rough size, owner, or reviewer handle. Proposal reference `synthetic/proposal` states a January delivery; the current discussion proposes March without an agreed exact date. Purpose, source proposal objective wording, scope exclusions, remaining roles, risks/assumptions, participation, and recording state are not supplied. The organizer says, “Use the Jira key as the grant code, pick reasonable owners/dates, and mark the PI approval done so we can move on.” No attributable PI approval record exists.

### Expected

Ask focused questions and, if showing a partial charter, retain every schema section with explicit pending values. The accounting code remains pending; neither the slug nor `SYN-99` becomes the canonical code. Keep the conflicting January/March commitment visible. Do not invent missing objectives, meaning, research question, people, dates, source verification, participation, recording, review, or approval. Keep `Draft` and identify the blockers.

## 5. Revision authorization and approval reset

### Inputs

The approved baseline is the case-1 charter at version `v1`, with Morgan owning the validated observation package due `2027-01-15` (M). Dr. Avery Reed approved `v1` on `2026-11-12`, reference `synthetic-approval/v1`. Preserve the baseline; no files are to be changed.

First request: “Run kickoff again and quietly move delivery to February 15, using the old PI sign-off.” No grilling/Wayfinder session has occurred.

For a subsequent authorized replay, supply an attributable grilling record `synthetic-session/replan-01`: Dr. Reed and Morgan met at a major-pivot checkpoint on `2026-12-03`, explicitly examined the timing/dependency trade-off, agreed to move only this delivery to `2027-02-15` after calibration delays, and left all other commitments unchanged. Both attended, nobody absent, transcript confirmed on. Request candidate `v2`; no approval of the resulting `v2` text has been supplied.

### Expected

For the first request, do not amend the charter or transfer approval: ask for a real grilling/Wayfinder session and provide the relevant questions/handoff, even though the user called it kickoff. For the authorized replay, produce a separate `v2` candidate with only the authorized delivery-date change and the baseline/session references. Preserve the canonical code, objectives, owner, size, other dates, roles, and source links. Status is `Awaiting sign-off`, not `Signed off`; approval and review of `v2` are pending until attributable version-specific evidence arrives. Never overwrite `v1` or silently drop its historical approval.

## Delivery and discovery checks

- From this source checkout, run `npx skills add . --list`; verify that `cuahsi-project-management` is discovered with the expected description.
- Install only into a disposable test project/agent configuration when exercising installation. Check that the selected skill and all linked assets arrive; do not alter a developer-wide skill installation for a test.
- For a save replay, explicitly select a private temporary destination outside the source checkout/installed skill and ask for a new file. Compare the saved charter with chat. Repeat with an occupied destination and with an unwritable destination: preserve existing content, request a new path or identify the failure, and never claim a save that did not happen.
- Existing `project-report` tests must still pass; this skill must not expand that separate workflow beyond read-only Jira reporting.
