# Project-information repository policy

AI-drafted: yes

Reviewed by: pending human review

## Responsibility and branches

- Central repository: https://github.com/CUAHSI/CUAHSI-ProjectStream (fixed destination; verify live privacy and access before publishing)
- Responsible owner: <named practice owner / pending>
- Access administrator: <named employee; explicit credentials/hosting delegation / pending>
- Tooling approval: <Tony's approval evidence for this configuration/version / pending>
- Approved-charter branch: main
- In-progress-charter branch: develop
- Canonical project path: `projects/<accounting-code>-<shortname>/charter.md`
- Adjacent append-only log: `projects/<accounting-code>-<shortname>/decision-log.md`
- Branch rules and merge policy: <observed rules for main/develop and decision branches; employee review/merge and self-merge check / pending>

The accounting code identifies one project across all its repositories; a confirmed, case-preserving shortname is a human-readable folder suffix, not an identity or an inferred slug. Apply the installed skill's publication guide (§3, directory contract) for safe single-segment validation, reversible code encoding, and collision/duplicate checks. Read identity from charter metadata and this mapping, never by splitting directory names on hyphens. Approved snapshots live on `main`; candidates on `develop` are visibly drafts. Promote only the exact signed-off candidate, not unrelated drafts from `develop`. Historical approved versions remain retrievable through Git commit links. Decision-log corrections append superseding entries rather than edit or remove existing entries.

## Project directory mapping

| Accounting code (canonical key) | Confirmed shortname | Code component | Reversible encoding/decoding rule | Exact project directory | Confirmation evidence |
| --- | --- | --- | --- | --- | --- |
| <original code, unchanged> | <user-confirmed case-preserving suffix / pending> | <original safe code or agreed encoded component> | <none, or reversible rule> | `projects/<accounting-code>-<shortname>/` | <user confirmation / pending> |

Use one directory per accounting code per branch and the same mapping across `main`/`develop`; inspect charter identities and existing/pending paths before writes. An occupied or filesystem-equivalent destination, ambiguous encoding, or duplicate code under another shortname blocks creation/rename until reconciled. A different suffix for an existing code is a rename request, not a new project.

- Path-only rename record: <original code; old/new paths and shortname; encoding rule; affected branches; source and rename commit/PR links; byte-comparison and navigation evidence; pending gaps / not applicable>

For an explicitly requested path-only rename, follow the installed skill's publication guide (Path-only rename): preserve charter/log bytes and Git history, and update this mapping and active navigation. The charter's absent or historical Shortname field remains unchanged; current folder metadata lives here. A directory move does not revise commitments or require a new charter approval. Content revisions still use the existing lifecycle/sign-off rules.

## Access configuration

- Staff roster reference: <authorized employee roster, reference/date only; no HR contents>
- Staff team(s): <confirmed team slug(s), permission, roster comparison, nested teams / pending>
- Organization base permission: <observed value and who it grants access to / pending>
- Direct collaborators: <employee status and effective permission; reference only where sensitive>
- Outside collaborators: <observed list and exclusion evidence / pending>
- Organization owners: <review against staff roster; owners retain administrative access / pending>
- Pending invitations: <observed list and roster comparison / pending>
- Apps, deploy keys, and automation: <authorized access paths and responsible owners / pending>
- Last complete access review: <checker and timestamp with timezone / pending>

A private repository, organization membership, or an empty outside-collaborator list does not prove staff-only access. Compare every access path to the confirmed roster; inaccessible API results remain unverified. External collaborators receive an approved export through a separate workflow, not repository access.

## Verification record

| Check | Expected | Observed | Evidence and checked at | Result |
| --- | --- | --- | --- | --- |
| Repository visibility | Private | pending | pending | pending |
| Complete access-path audit | Employees plus explicitly authorized automation only | pending | pending | pending |
| Staff read | Confirmed employee can read approved charter on main | pending | pending | pending |
| Staff decision PR | Employee can open, review, merge, and self-merge a synthetic decision PR | pending | pending | pending |
| Nonstaff read | Confirmed nonemployee cannot read approved charter | pending | pending | pending |
| Approved publication | Exact signed-off version on main with adjacent log | pending | pending | pending |
| Draft separation | Candidate on develop absent from main until sign-off | pending | pending | pending |
| Content screening | Restricted sources are linked; no actuals, raw transcripts, or credentials | pending | pending | pending |

Use `verified`, `failed`, or `unverified` for each result, with an attributable observation rather than an assumption. A scoped token's 404 is not proof that its account lacks access. Record account identity and adequate credential/SSO scope without recording tokens. Keep sensitive audit evidence in an authorized private location, linked here rather than copied.

## Project and activity navigation

| Project/activity repository | Canonical charter URL | Link verification |
| --- | --- | --- |
| <every relevant repository, or confirmed none> | <https://github.com/CUAHSI/CUAHSI-ProjectStream/blob/main/projects/accounting-code-shortname/charter.md; exact mapped segment, URL-escaped> | <commit/read-back evidence or pending> |

When a linking repository is public or shared with nonstaff, use neutral link text and confirm that its path/URL discloses no restricted identity. Keep charter content in the central repository. After a path-only rename, update active central and related-repository navigation to the mapped path, preserving historical immutable commit URLs and recording any unauthorized/unverified link changes as gaps.

## Repeatable procedure

Run `cuahsi-project-management publish` using the installed skill's publication procedure. Repeat the access audit before publishing and after changes to staff, teams, collaborators, owners, invitations, automation, or branch rules. Record publication commit/PR URLs and each incomplete check; a partial run does not establish operational acceptance.
