# Lifecycle cases

Load the branch matching the request. The main skill owns the common schema, confidentiality, and drafting rules; these cases specialize timing, ownership, and revision scope. Team review and approval remain outside the skill through GitHub PRs.

## Existing project without a charter

Use the main workflow's checkpoint rule rather than backdating a kickoff to the award or requiring a second award-stage meeting. Ask which checkpoint applies if unclear. Use current authorized plans and discussion, keeping historical proposal wording distinct from the current interpretation.

## Core Award Activity

Confirm which co-PI owns this activity separately from the overall award's PI role. A change of owning co-PI requires explicit confirmation, not inference from who attends or reviews. Decision-PR tags can include both roles without changing activity ownership. Apply the common workflow using that confirmed ownership; ownership is not a skill-managed charter approval role.

## Existing charter or requested revision

For an explicitly requested path-only rename, use [Publication's rename branch](publication.md#path-only-rename): preserve charter/log bytes and history and update navigation. This is not a charter revision or a new project; the content-revision rules below do not apply to a directory move.

1. Identify the baseline charter, its file or immutable commit reference, canonical code, and requested changes. Preserve baseline history. A routine update, decision, or generic request to tidy the charter is not permission to change its commitments.
2. Apply explicitly requested formatting, metadata, or explanatory-summary edits without requiring a new kickoff or grilling session, preserving commitments and factual meaning. For changes to scope, ownership, deliverables, or dates, establish a **Wayfinder or grilling session**: accept a supplied, attributable session record naming participants and agreed changes, or explicitly conduct the session in this conversation. If its scope is unclear or no substantive session has happened, show the relevant questions and ask before altering commitments. Merely labeling a routine edit a re-grill is not a session.
3. If running a substantive session here, identify the human participants, challenge the reasons, scope, dependencies, and trade-offs of the change, and obtain an explicit account of the requested changes and unresolved points. This establishes revision scope, not team review or approval of the charter.
4. Change only what the user or session authorizes, preserving unaffected commitments and source wording. A changed canonical accounting code requires explicit confirmation, not derivation from a slug or repository. Apply the current charter schema and update Date last modified. Identify baseline/session references in source documents when they support a substantive change; summarize the diff in the handoff rather than adding version, approval, or proposal labels to the charter.
5. Deliver the revised charter with specific pending values or open questions wherever information remains unresolved. Preserve the baseline separately or through Git history for an explicitly requested in-place revision. Leave team review and approval to GitHub PRs outside this skill.

When a request contains both a charter and a new kickoff, this branch still applies: an existing baseline cannot be bypassed by choosing a different mode label. Automatic conflict detection against accumulated decision logs is later work; this slice handles the revision that the user presents.
