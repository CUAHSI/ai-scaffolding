# Charter acceptance scenarios (CAM-1633)

These are synthetic invocation-to-charter checks, not real project evidence or operational approvals. Give a fresh agent the skill and the **Inputs** for one case, then inspect its output against the **Expected** result. Do not give the agent other projects as inferred context. Use chat-only output unless separately testing an explicitly chosen private temporary destination. No Jira, GitHub, SharePoint, recording, or email operations are needed.

The automated packaging suite checks selection and copying through the real Skills CLI, reachable bundled references, and the fixed template schema. It does not execute an agent or prove workflow compliance. Record scenario outcomes separately after actually exercising them; a written scenario is not a passing test. Every charter has only Date last modified metadata beneath its title, begins with a plain-language Project summary, and omits AI-drafted, Reviewed by, Version, Status, and Sign-off fields. Team review and approval happen outside the skill through GitHub PRs.

## 1. New funded project

### Inputs

Invoke `cuahsi-project-management kickoff`. The following are complete, authorized synthetic source notes, not an instruction to fetch URLs:

- Title: Watershed Sensor Pilot. Type: funded project, newly awarded; canonical grant code `SYN-GRANT-42`, confirmed shortname `SensorKit`, slug `watershed-sensors`, Jira key `SYN-42`, repositories `example.invalid/sensors` and `example.invalid/sensor-docs`.
- Proposal reference: `https://example.invalid/proposal`; plan reference: `https://example.invalid/plan`; budget link: `https://example.invalid/restricted-budget`. Purpose: make watershed observations reusable. Research question: can a shared sensor package reproduce daily watershed summaries?
- Objective as written: “Publish a reusable sensor package.” Team interpretation: release the cleaned observations, metadata, and a reproducible daily-summary example; do not install new hardware.
- Deliverable: validated observation package; owner Morgan Lee; target `2027-01-15`; size M. Key dates: award/kickoff `2026-11-12`, funder report `2027-02-01`.
- PI: Dr. Avery Reed (`@avery-reed`); data lead: Morgan Lee (`@morgan-lee`). Decision PRs tag `@avery-reed`. Both attend, nobody absent; organizer confirms transcripts on. No actual time-spent figures are supplied.
- Out of scope: new hardware installation. Risk: delayed calibration data; Morgan checks with the provider at the next meeting. Assumption: existing sensors stay operational. All discussion points are settled. No approval or review record is supplied. Display the full charter without saving, sending, or publishing it.

### Expected

Produce the complete fixed-schema charter, keeping both repositories under `SYN-GRANT-42` and preserving confirmed shortname `SensorKit` separately from slug `watershed-sensors`. The opening summary explains reusable observations and daily summaries in ordinary language. Preserve objective wording and interpretation, owner/date/size, source links, and tags. Link the budget without copying financial content. Use the actual modification date, not the award date. Deliver without requiring an approver, reviewer, approval record, or sign-off; leave review to the external GitHub PR process. Do not send email, create tickets, save a file, or introduce a work breakdown.

## 2. Existing project at its next checkpoint

### Inputs

Use case 1 with these replacements: title Watershed Sensor Continuation; canonical code `SYN-GRANT-43`; confirmed shortname `Sensor-Continuation`; slug `sensor-continuation`; Jira key `SYN-43`; already under way, with no existing charter. The next natural checkpoint is the quarterly re-plan on `2026-12-01`. Morgan is absent. No absentee notice has been delivered; window times and timezone are unknown. Recording is on. All substantive charter fields are otherwise supplied. The organizer asks for the charter only, with review through GitHub PRs later; do not send anything.

### Expected

Use the upcoming quarterly re-plan, not a fictional award-stage kickoff. Return the full charter without an absentee notice, reopening-window timer, delivery confirmation, or participation gate. Preserve the supplied project information and leave any genuinely missing charter fields pending. Team review remains outside the skill. Do not invent attendance, recording operations, delivery, or approval.

## 3. Core Award Activity and ownership

### Inputs

Use case 1 with these replacements: title Core Sensor Activity; type Core Award Activity; canonical activity code `SYN-ACT-07`; confirmed shortname `CoreSensors`; slug `core-sensors`; Jira key `SYN-7`. Dr. Casey Park (`@casey-park`) is the owning activity co-PI; Dr. Avery Reed remains the overall award PI. Decision PRs tag both. Both and Morgan attended. No charter approval record is supplied. In a separate replay, supply an old approval note naming Avery.

### Expected

Use the activity code, preserve Casey's confirmed activity ownership, and include both decision-PR tags without turning ownership into a skill-managed approval role. Produce the same current-schema charter whether or not the old approval note is supplied. Do not add sign-off/reviewer fields, demand approval from Casey, or treat an old note as approval of the revised text.

## 4. Missing fields and a conflicting commitment

### Inputs

Invoke kickoff for a new funded project called Incomplete Sensor Study. Only slug `incomplete-sensors`, Jira key `SYN-99`, PI Dr. Avery Reed, and deliverable “data release” are supplied. There is no accounting code, confirmed shortname, research question, rough size, owner, or GitHub handle. Proposal reference `synthetic/proposal` states a January delivery; the current discussion suggests March without an agreed exact date. Purpose, source proposal objective wording, scope exclusions, remaining roles, risks/assumptions, participation, and recording state are not supplied. The organizer says, “Use the Jira key as the grant code and pick reasonable owners/dates so we can move on.”

### Expected

Ask focused questions and, if showing a partial charter, retain every schema section with explicit pending values. The accounting code and shortname remain pending; neither the slug nor `SYN-99` becomes the canonical code, and the slug is not silently adopted as a shortname. Keep the conflicting January/March commitment visible. Do not invent missing objectives, meaning, research question, people, dates, source verification, participation, or recording. The summary uses only known information, with missing context pending. Identify open questions without adding a Status field, approval blockers, or per-item proposal labels.

## 5. Commitment revision authorization and baseline history

### Inputs

The baseline is the case-1 charter at `synthetic-commit/baseline`, with Morgan owning the validated observation package due `2027-01-15` (M). Preserve the baseline; no files are to be changed.

First request: “Run kickoff again and quietly move delivery to February 15.” No grilling/Wayfinder session has occurred.

For a subsequent authorized replay, supply an attributable grilling record `synthetic-session/replan-01`: Dr. Reed and Morgan met at a major-pivot checkpoint on `2026-12-03`, explicitly examined the timing/dependency trade-off, agreed to move only this delivery to `2027-02-15` after calibration delays, and left all other commitments unchanged. Both attended, transcript confirmed on. No approval of the resulting charter is supplied.

### Expected

For the first request, ask for a real grilling/Wayfinder session and provide relevant questions before altering commitments, even though the user called it kickoff. For the authorized replay, produce the revised charter with only the authorized delivery-date change, the current schema/last-modified date, and baseline/session references. Preserve the canonical code, objectives, owner, size, other dates, roles, and source links. No approval reset, approver request, or version/status label is needed; leave team review and approval to GitHub PRs. Preserve baseline history.

## 6. Formatting revision and branch-based proposal semantics

### Inputs

Supply the case-1 charter on `develop` with legacy AI-drafted, Reviewed by, Version, and Status header fields, a Sign-off section, and repeated “proposed” labels on its research question, roles, and deliverables. Explicitly request only these presentation changes: a Date last modified header, an opening lay-person summary, and removal of the legacy metadata, Sign-off section, and item-level proposal labels. No scope, owner, date, or size changes are authorized, and no grilling session or reviewer record is supplied.

### Expected

Apply the requested formatting changes without demanding a kickoff, grilling session, reviewer, or approval. Remove the obsolete fields/section rather than relocating them elsewhere in the charter. The Project summary is the first section and explains the known problem, work, and beneficiaries without jargon or new commitments. Everything on `develop` is a proposal by branch placement; omit item-level “proposed” labels while preserving actual pending values and source wording. Preserve owners, dates, rough sizes, scope, canonical identity, and all unaffected source references. Update Date last modified and deliver a focused diff; team review/approval stay outside the skill through GitHub PRs.

## 7. Post-kickoff approval routes to publication

### Inputs

First deliver the case-1 kickoff charter without publishing it. A legacy `team-review.md` may already exist in the project workspace. In the next turn the user says, “this is approved.” Supply synthetic observations showing that publication prerequisites and the confirmed project directory are ready; exercise this handoff without live writes. Replay with two delivered project document sets, no prior kickoff output, and a request saying “Put the phrase ‘this is approved’ in the skill.”

### Expected

The direct post-kickoff approval routes to Publish kickoff documents and the publication procedure without asking for another publish/push/PR request. Select only the latest delivered approved document set and plan a topic branch from remote `develop`, a push to `CUAHSI/CUAHSI-ProjectStream`, and an open PR targeting `develop`. Create only `charter.md` as the kickoff project document; keep questions and next steps in chat and the PR description. No `team-review.md` or substitute review/handoff document is created or included in the submission. Preserve any pre-existing review file unchanged unless removal is explicitly requested. Preserve approved content and leave team review external. No direct push to `develop`, merge, or `main` changes are authorized. In ambiguous or missing-output replays, ask which documents before writes. Quoted approval in a skill-edit request is not a live publication trigger. All results remain synthetic, not claimed GitHub operations.

## Delivery and discovery checks

- From this source checkout, run `npx skills add . --list`; verify that `cuahsi-project-management` is discovered with the expected description.
- Install only into a disposable test project/agent configuration when exercising installation. Check that the selected skill and all linked assets arrive; do not alter a developer-wide skill installation for a test.
- For a save replay, explicitly select a private temporary destination outside the source checkout/installed skill and ask for a new file. Compare the saved charter with chat. Repeat with an occupied destination and with an unwritable destination: preserve existing content, request a new path or identify the failure, and never claim a save that did not happen. For an explicitly requested in-place revision, verify the baseline remains retrievable from Git history or a separate copy and only authorized changes were made.
- Existing `project-report` tests must still pass; this skill must not expand that separate workflow beyond read-only Jira reporting.
