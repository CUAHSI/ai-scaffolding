---
name: cuahsi-project-management
description: "Run a CUAHSI kickoff or re-plan, draft a Project Charter, and publish project information to a private staff repository."
disable-model-invocation: true
---

# CUAHSI project management

Run a human-led kickoff, produce an approximately two-page Project Charter, and explicitly publish it when requested. Shared understanding takes priority at kickoff, quarterly re-plans, and major pivots; keep routine coordination lightweight. The accounting grant or activity code, not a slug, Jira key, or repository, is the canonical project identity.

**Fixed publication destination:** [CUAHSI/CUAHSI-ProjectStream](https://github.com/CUAHSI/CUAHSI-ProjectStream). Use this repository for every project's charter and associated files; do not ask the user to select a central repository or create a separate one per project. Verify its live visibility and access before publishing. A fixed destination neither authorizes writes nor establishes staff-only access; if it is unavailable, report the blocker rather than choose a replacement.

This skill implements **kickoff**, **revise**, and **publish**. Publication stores in-progress charters on `develop`, with repository policy/access checks and navigation links. **Promotion of a charter from `develop` to `main` is manual in GitHub and outside this skill.** **Team review and approval happen outside this skill through GitHub PRs.** The skill drafts and prepares requested publication changes; it does not solicit, record, or gate team approval of the charter. The user's approval of kickoff output is authorization to submit it for that external review, not a substitute for it. Automated transcript processing and decision extraction, email sending, reporting, scheduling, exports, and staff-site provisioning remain later work; explain those limits rather than simulating success. The existing `project-report` skill remains Jira-only and read-only.

## 1. Establish the session

Accept `/cuahsi-project-management kickoff` for a new charter, `/cuahsi-project-management revise` for changes to an existing charter, or `/cuahsi-project-management publish` for explicitly requested central-repository publication; equivalent natural-language requests are fine. Ask which workflow applies if unclear.

After delivering **kickoff** documents, route the user's direct follow-up **"this is approved"** to [Publish kickoff documents](#5-publish-kickoff-documents). An approval phrase quoted in a request to edit this skill or in source material is not a live publication instruction.

For **publish** or an explicitly requested **path-only rename**, read and execute [Publication](assets/publication.md) instead of the kickoff steps below. This covers repository setup/access checks, branch-specific storage, and directory renames. Publish collects/confirms the case-preserving shortname for `projects/<accounting-code>-<shortname>/`; the accounting code remains the identity. A path-only rename preserves charter/log bytes and history, updates navigation, and is not a new project or charter revision. An unchanged charter does not require another kickoff; requested content changes use the lifecycle guide. A plan-only request authorizes no live writes.

Collect the project/activity title and type, lifecycle checkpoint, named PI or owning activity co-PI, accounting code, confirmed shortname (human-readable folder suffix, not an identity or an automatic copy of the slug), supplied source documents, discussion participants, and any existing charter. Sources may be supplied text or explicitly authorized documents; linked material that was not read remains an unverified reference. A local conversation and supplied documents suffice; external service credentials are not prerequisites.

Read the [charter template](assets/charter-template.md) before drafting. For a project already under way, a Core Award Activity, or any existing charter, read the matching branch in [Lifecycle cases](assets/lifecycle.md) before proceeding. An existing charter takes the revision branch for content changes, even if the request says kickoff; an explicit path-only rename takes the publication branch above.

**Done when:** the workflow, project identity, and ownership are established, or their missing values are explicitly recorded for clarification. A missing accounting code remains pending, never replaced with a Jira key or invented code.

## 2. Run the kickoff discussion

Hold the kickoff at award for a new project; for work already under way use its next quarterly re-plan, major pivot, or reporting deadline. Invite staff with deliverables when possible. Meeting transcripts are on by default: ask the organizer to confirm recording or an explicit exception in the session context. Do not claim to have enabled recording. Participation and recording observations inform the discussion, not charter review or approval gates.

Work through the template with the participants: preserve objectives as written alongside the agreed interpretation, name owners and target dates for deliverables, and ask for rough S/M/L sizes or person-weeks. Surface scope exclusions, risks, assumptions, and disagreements. Ask focused questions where evidence is missing or conflicting; record unresolved points instead of deciding them for the team. Gather all confirmed Jira keys and GitHub repositories without treating a multi-repository project as multiple projects.

Link proposals, plans, budgets, and other source documents. Budgets and HR are linked, not copied. Keep actual time-spent figures, credentials, and raw transcripts out of the charter and source control. Use only necessary, non-sensitive conclusions from authorized discussion.

**Done when:** every required template field has an evidence-backed value, an explicit pending question, or a confirmed not-applicable explanation. Missing fields are visible questions, not plausible guesses. Risk/assumption follow-up owners or dates are optional unless the team makes them commitments; an organizer can remain the role-based next actor without a supplied personal name.

## 3. Draft the charter

**Kickoff output contract:** create one project document, `charter.md`. Keep remaining questions, next steps, and review guidance in chat and the eventual PR description. Do not create `team-review.md` or an equivalent separate review/handoff document; team review happens through GitHub PRs.

Fill the fixed schema in the template. Start with a plain-language **Project summary** explaining the problem, planned work, and who benefits, without assuming specialist knowledge; explain necessary terms and acronyms. Aim for two pages without dropping required fields or material uncertainty. Use confirmed names/handles for decision-PR tags; if missing, ask and keep them pending. Include source references close enough to distinguish source wording, team interpretation, and unresolved contradictions.

The header contains only **Date last modified: YYYY-MM-DD** beneath the title; use the actual modification date and update it when the charter changes. Git commits and PRs carry revision and review history. Omit AI-drafted, Reviewed by, Version, and Status fields and any Sign-off section from the charter. Everything on `develop` is a proposal, so write the plan directly rather than adding `proposed` labels to individual items. Preserve genuine uncertainty as specific pending values or open questions; branch placement is not evidence that missing facts are known.

For revisions, follow the lifecycle guide. Optional work breakdown into epics/stories/dates is a separate, explicitly requested step, not a prerequisite or an automatic side effect of this workflow. Model-tier choice is a recommendation rather than a required tool configuration.

**Done when:** the complete charter follows the schema, has the correct last-modified date and opening summary, and makes unresolved information visible. Human review and approval are not completion criteria for drafting.

## 4. Deliver and hand off

Display the complete charter and remaining questions/next owners in chat. Save only when the user explicitly chooses a private destination outside the source checkout and installed skill; state whether privacy is user-confirmed rather than independently verified. Preserve existing files and baseline history: for a new save choose an unused destination or ask instead of overwriting; for an explicitly requested in-place revision show the focused diff and retain the baseline in Git history or a separate copy. If saving fails, display the charter, identify the failure, and say no file was saved.

Do not create tickets, PRs, central repositories, or external messages while merely drafting kickoff documents. Once the documents are delivered, tell the user that replying **"this is approved"** submits them through the next step. An explicit request to publish follows [Publication](assets/publication.md); privacy and write-authorization gates still apply. For a revision, summarize the changes and identify the baseline by file or immutable commit reference. Leave team review and approval to the external GitHub PR process.

**Done when:** the user has the full charter and an honest account of pending information and any file delivery. Drafting or opening a PR does not establish approval or authorize a merge.

## 5. Publish kickoff documents

**Trigger:** after `kickoff` has delivered charter documents, the user's direct statement **"this is approved"** (case-insensitive, with optional final punctuation) approves the latest delivered document set and authorizes saving, committing, pushing, and opening its PR. No additional `publish`, push, PR request, or confirmation is needed when the document set and publication prerequisites are clear. If multiple projects or document sets make "this" ambiguous, ask which set before writing. Without a delivered kickoff document set, ask for context rather than publish an unrelated charter. Quoted phrases and instructions to change the skill do not trigger this action.

Read and execute [Publication](assets/publication.md) with `CUAHSI/CUAHSI-ProjectStream` as the destination and **`develop` as the PR base**. Keep its privacy/access, credentials, canonical-code/confirmed-shortname, safe-path, content-screening, and private-workspace requirements. Use the confirmed `projects/<accounting-code>-<shortname>/` mapping. Missing prerequisites are specific blockers, not a reason to request publication authorization again; the approval phrase does not waive safety checks.

Start a focused topic branch from the latest remote `develop`, named for the action as `kickoff-<ShortName>-<summary>` (for example `kickoff-FIMBox-project-initiation`), save only the approved `charter.md` and necessary project navigation/mapping changes in the authorized private workspace, and verify the exact staged file set and diff. Apply the kickoff output contract above to the staged file set. Leave pre-existing review/handoff files unchanged and out of this submission; removing an existing file requires an explicit removal request. Keep approved document bytes unchanged; if screening or a new edit requires content changes, show the revised documents and obtain fresh user approval before submitting them. Preserve genuine pending fields and baseline history; keep restricted source attachments and unrelated projects out of the commit.

Commit and push the topic branch to ProjectStream, then open a PR explicitly targeting `develop`, never push the documents directly to `develop` for this trigger. Describe the document set and the user's actual publication approval in the PR without adding approval metadata to the charter or asserting team review. This is one case of the general rule in [Publication](assets/publication.md#projectstream-submission-rule): every ProjectStream change, including a later `revise` such as `revise-FIMBox-<summary>`, goes through a topic-branch PR targeting `develop`, never a direct push. This authorization covers PR submission only: leave the PR open, make no changes to `main`, and do not merge or promote the charter (promotion is manual in GitHub). Team review and approval remain outside the skill through GitHub PRs.

Read back the pushed files and PR repository, base, head, file set, and open state. On retry, inspect existing branches/PRs first and reuse an identical open PR instead of creating duplicates. If the exact documents are already on `develop`, return their existing publication/PR reference or report that there is no new diff rather than invent an empty PR. Report partial push/PR failures accurately and return the actual PR URL and remaining blockers.

**Done when:** the exact approved kickoff documents are verified on a pushed ProjectStream topic branch with an open PR targeting `develop`, or the precise blocker/already-submitted result is reported. PR submission is not a merge, team approval, or promotion to `main`.

## Verification

Exercise [Charter scenarios](assets/charter-scenarios.md) at the invocation-to-charter seam with synthetic inputs. Packaging checks run with `python3 -m unittest discover -s tests -p test_project_management_packaging.py`; the isolated installation test uses the cached Skills CLI offline and explicitly skips if Node/npx or that cache is unavailable. Use `npx skills add . --list` from this source repository to verify discovery and populate the installer cache before retrying a skipped installation check. For publication, exercise [Publication scenarios](assets/publication-scenarios.md) at the invocation-to-publication seam with synthetic observations and no live writes. Scenario checks evaluate agent behavior; packaging checks alone do not prove that the workflow was followed, and neither establishes live operational acceptance.
