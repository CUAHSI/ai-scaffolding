---
name: cuahsi-project-management
description: "Run a CUAHSI kickoff or re-plan, draft a Project Charter, and publish project information to a private staff repository."
disable-model-invocation: true
---

# CUAHSI project management

Run a human-led kickoff, produce an approximately two-page Project Charter, and explicitly publish it when requested. Shared understanding takes priority at kickoff, quarterly re-plans, and major pivots; keep routine coordination lightweight. The accounting grant or activity code, not a slug, Jira key, or repository, is the canonical project identity.

This skill implements **kickoff**, **revise**, and **publish**. Publication includes approved charters on `main`, in-progress charters on `develop`, adjacent append-only logs, repository policy/access checks, and navigation links. Automated transcript processing and decision extraction, email sending, reporting, scheduling, exports, and staff-site provisioning remain later work; explain those limits rather than simulating success. The existing `project-report` skill remains Jira-only and read-only.

## 1. Establish the session

Accept `/cuahsi-project-management kickoff` for a new charter, `/cuahsi-project-management revise` for changes to an existing charter, or `/cuahsi-project-management publish` for explicitly requested central-repository publication; equivalent natural-language requests are fine. Ask which workflow applies if unclear.

For **publish**, read and execute [Publication](assets/publication.md) instead of the kickoff steps below. This covers repository setup/access checks, approved publication, and in-progress storage. An unchanged signed-off charter does not require another kickoff; requested charter changes still use the revision/sign-off rules. A plan-only request authorizes no live writes.

Collect the project/activity title and type, lifecycle checkpoint, named PI or owning activity co-PI, accounting code, supplied source documents, meeting participants/absentees, and any existing charter. Sources may be supplied text or explicitly authorized documents; linked material that was not read remains an unverified reference. A local conversation and supplied documents suffice; external service credentials are not prerequisites.

Read the [charter template](assets/charter-template.md) before drafting. For a project already under way, a Core Award Activity, or any existing charter, read the matching branch in [Lifecycle cases](assets/lifecycle.md) before proceeding. An existing charter always takes the revision branch, even if the request says kickoff.

**Done when:** the workflow, project identity, and approval role are established, or their missing values are explicitly recorded for clarification. A missing accounting code remains pending, never replaced with a Jira key or invented code.

## 2. Run the kickoff discussion

Hold the kickoff at award for a new project; for work already under way use its next quarterly re-plan, major pivot, or reporting deadline. Invite staff with deliverables when possible. Meeting transcripts are on by default: ask the organizer to confirm recording and record its actual state or an explicit exception. Do not claim to have enabled recording.

Work through the template with the participants: preserve objectives as written alongside the agreed interpretation, name owners and target dates for deliverables, and ask for rough S/M/L sizes or person-weeks. Surface scope exclusions, risks, assumptions, and disagreements. Ask focused questions where evidence is missing or conflicting; record unresolved points instead of deciding them for the team. Gather all confirmed Jira keys and GitHub repositories without treating a multi-repository project as multiple projects.

Link proposals, plans, budgets, and other source documents. Budgets and HR are linked, not copied. Keep actual time-spent figures, credentials, and raw transcripts out of the charter and source control. Use only necessary, non-sensitive conclusions from authorized discussion.

**Done when:** every required template field has an evidence-backed value, an explicit pending question, or a confirmed not-applicable explanation. Missing fields are visible blockers, not plausible guesses. Distinguish an open risk the approver can accept from an unresolved required field. Risk/assumption follow-up owners or dates are optional unless the team makes them commitments; an organizer can remain the role-based next actor without a supplied personal name.

## 3. Draft the charter

Fill the fixed schema in the template. Aim for two pages without dropping required fields or material uncertainty. Use confirmed names/handles for decision-PR tags; if missing, ask and keep them pending. Include source references close enough to distinguish source wording, team interpretation, and unresolved contradictions. Retain the AI-drafted marker and reviewed-by field on the charter and any generated notices or handoffs; record a human reviewer only when review is actually supplied.

For revisions, follow the lifecycle guide before drafting a separate candidate version. Optional work breakdown into epics/stories/dates is a separate, explicitly requested step, not a prerequisite or an automatic side effect of this workflow. Model-tier choice is a recommendation rather than a required tool configuration.

**Done when:** the complete charter is reviewable, its version is identifiable, and its status is `Draft` while required fields, disagreements, or kickoff participation steps remain unresolved.

## 4. Honor the absentee reopening window

Give absentees the written plan and a 20-minute window to reopen it. If anyone was absent, prepare a ready-to-send notice naming the charter version and the right to reopen it; ask the organizer to deliver it and confirm delivery, the window times, and timezone. This slice drafts the notice but does not send email or start a timer. Unknown delivery, elapsed time, or objections remain pending; a generated notice is not evidence that the window happened.

If a request to reopen arrives, return to discussion, reconcile the affected fields, and seek approval for the resulting version. Record not applicable only when the organizer confirms nobody was absent.

**Done when:** delivery/window evidence and any reopened questions are resolved, or are explicitly listed as blockers. A draft can be delivered before these steps finish, but not represented as a completed kickoff or signed-off charter.

## 5. Obtain explicit sign-off

A complete charter with resolved participation steps is `Awaiting sign-off`. Only the named PI signs off a funded-project charter; only the owning activity co-PI signs off a Core Award Activity charter. A team consensus, repository merge, or statement by an unidentified participant does not establish that approval.

Set `Signed off` only when an explicit approval statement or attributable approval record identifies the correct approver and exact candidate version, with no unresolved required fields or reopening blockers. Record the supplied approval evidence and date; if identity, date, scope, or approval is uncertain, ask and leave approval pending. Human review and approver sign-off are distinct. Changes after approval require a new candidate and new sign-off, never carried-forward approval.

**Done when:** the charter records actual version-specific approval or clearly says sign-off is pending. Never write an approval on behalf of the PI/co-PI or invent a reviewer, approval date, or source verification.

## 6. Deliver and hand off

Display the complete charter, approval status, remaining questions/next owners, and any absentee notice in chat. Save only when the user explicitly chooses a private destination outside the source checkout and installed skill; state whether privacy is user-confirmed rather than independently verified. Preserve existing files and approved versions: choose a new destination or ask instead of overwriting. If saving fails, display the charter, identify the failure, and say no file was saved.

Do not create tickets, PRs, central repositories, or external messages as an implicit kickoff side effect. An explicit request to publish follows [Publication](assets/publication.md); privacy, approval, and write-authorization gates still apply. For an approved charter revision, deliver the candidate and approval evidence alongside its baseline reference; preserve the baseline.

**Done when:** the user has the full charter and an honest account of pending decisions, participation, sign-off, and any file delivery. Completion of drafting is not completion of human approvals.

## Verification

Exercise [Charter scenarios](assets/charter-scenarios.md) at the invocation-to-charter seam with synthetic inputs. Packaging checks run with `python3 -m unittest discover -s tests -p test_project_management_packaging.py`; the isolated installation test uses the cached Skills CLI offline and explicitly skips if Node/npx or that cache is unavailable. Use `npx skills add . --list` from this source repository to verify discovery and populate the installer cache before retrying a skipped installation check. For publication, exercise [Publication scenarios](assets/publication-scenarios.md) at the invocation-to-publication seam with synthetic observations and no live writes. Scenario checks evaluate agent behavior; packaging checks alone do not prove that the workflow was followed, and neither establishes live operational acceptance.
