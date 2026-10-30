---
name: setup-project-setup
description: "Configure this repo for the engineering skills in accordance with CUAHSI project guidelines: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

### 1 Setup CUAHSI Project

* Call the the "setup-matt-pocock-skills" using GitHub for tracking code and PRs, and JIRA for tracking issues. If this skill does not exist, the user should install it before proceeding using: `npx skills add https://github.com/mattpocock/skills`

* You will need to gather the JIRA Objective ID assocated with this project. Use assets/issue-tracking-guidelines.md to configure the issue tracking for this project. Issues will contain labels, which should be inferred from existing child items of the Objective and by asking the user.

* Verify that the user has `acli`, `gh`, and `netrc` configured properly. If not, provide instructions for setting these up based on thier operating system. 

### 2. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
