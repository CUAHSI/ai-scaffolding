"""Check the public packaging contract of the project-management skill."""

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL_DIRECTORY = Path(__file__).resolve().parents[1] / "cuahsi-project-management"


class ProjectManagementPackagingTests(unittest.TestCase):
    """Verify the installable skill and its user-facing charter assets."""

    @unittest.skipUnless(shutil.which("npx"), "Node/npx is needed for the installer check")
    def test_skill_can_be_selected_and_installed_by_name(self):
        """Use the real loader without depending on YAML serialization."""
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                ["npx", "--offline", "--yes", "skills", "add", str(SKILL_DIRECTORY),
                 "--skill", "cuahsi-project-management", "--agent", "claude-code",
                 "--yes", "--copy", "--json"],
                cwd=temporary, capture_output=True, text=True, check=False, timeout=60,
            )
            if result.returncode and "ENOTCACHED" in result.stderr:
                self.skipTest("Cache the installer with npx skills add . --list, then retry")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            records = json.loads(result.stdout)
            self.assertEqual(len(records), 1)
            installed = records[0]
            for field, value in {
                "name": "cuahsi-project-management", "status": "installed",
                "scope": "project", "mode": "copy",
            }.items():
                with self.subTest(field=field):
                    self.assertEqual(installed[field], value)
            destination = Path(installed["path"]).resolve()
            self.assertTrue(destination.is_relative_to(Path(temporary).resolve()))
            for source in SKILL_DIRECTORY.rglob("*"):
                if source.is_file():
                    with self.subTest(asset=source.name):
                        copied = destination / source.relative_to(SKILL_DIRECTORY)
                        self.assertEqual(copied.read_bytes(), source.read_bytes())

    def test_installed_skill_can_reach_all_bundled_references(self):
        """Ensure relative references remain within the distributed skill."""
        pending = [SKILL_DIRECTORY / "SKILL.md"]
        visited = set()
        references = set()
        while pending:
            document = pending.pop().resolve()
            if document in visited:
                continue
            visited.add(document)
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (document.parent / unquote(url.path)).resolve()
                with self.subTest(reference=link, document=document.name):
                    self.assertTrue(target.is_relative_to(SKILL_DIRECTORY.resolve()))
                    self.assertTrue(target.is_file(), f"Missing bundled reference: {link}")
                if not target.is_file() or not target.is_relative_to(SKILL_DIRECTORY.resolve()):
                    continue
                references.add(target)
                if target.suffix == ".md":
                    pending.append(target)
        self.assertTrue(references, "Bundle the charter assets with the skill")

    def test_publication_policy_records_branch_policy_and_access_evidence(self):
        """Expose the configuration and evidence needed for safe publication."""
        template = (SKILL_DIRECTORY / "assets" / "repository-policy-template.md").read_text()
        for field in (
            "Central repository:", "Responsible owner:", "Access administrator:",
            "Tooling approval:", "Approved-charter branch: main",
            "In-progress-charter branch: develop", "Staff roster reference:",
            "Staff team(s):", "Organization base permission:",
            "Outside collaborators:", "Organization owners:",
            "Apps, deploy keys, and automation:", "Branch rules and merge policy:",
            "| Check | Expected | Observed | Evidence and checked at | Result |",
            "| Project/activity repository | Canonical charter URL | Link verification |",
            "AI-drafted:", "Reviewed by:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, template)

    def test_publication_uses_the_fixed_projectstream_destination(self):
        """Keep destination selection, commands, policy, and examples consistent."""
        repository = "CUAHSI/CUAHSI-ProjectStream"
        documents = [
            SKILL_DIRECTORY / "SKILL.md",
            SKILL_DIRECTORY / "assets" / "publication.md",
            SKILL_DIRECTORY / "assets" / "repository-policy-template.md",
            SKILL_DIRECTORY.parent / "README.md",
        ]
        for document in documents:
            with self.subTest(document=document.name):
                content = document.read_text()
                self.assertIn(f"https://github.com/{repository}", content)
                self.assertNotIn("<owner/repository>", content)
                self.assertNotIn("<owner>/<repository>", content)
        skill = documents[0].read_text()
        self.assertIn("Fixed publication destination:", skill)
        self.assertIn("do not ask the user to select a central repository", skill)
        self.assertIn("A fixed destination neither authorizes writes", skill)
        publication = documents[1].read_text()
        self.assertIn(f"gh repo view {repository}", publication)
        self.assertIn(f"gh api repos/{repository}/collaborators", publication)
        self.assertIn("a different current repository or Git remote is not the central destination", publication)
        self.assertIn("report the blocker rather than create or use a replacement", publication)
        self.assertIn(
            f"https://github.com/{repository}/blob/main/projects/<accounting-code>-<shortname>/charter.md",
            publication,
        )
        scenarios = (SKILL_DIRECTORY / "assets" / "publication-scenarios.md").read_text()
        case = scenarios.split(
            "## 12. Fixed central destination without a repository prompt\n", 1,
        )[1].split("\n## ", 1)[0]
        for expectation in (
            "### Inputs", "### Expected", f"Select `{repository}` automatically",
            "Do not ask the user to choose the central repository",
            "no live fetches or writes",
        ):
            with self.subTest(expectation=expectation):
                self.assertIn(expectation, case)

    def test_readme_documents_fimbox_kickoff_with_three_attachments(self):
        """Name the supplied documents and show the screenshot beneath the table."""
        readme = (SKILL_DIRECTORY.parent / "README.md").read_text()
        example = readme.split(
            "#### Example: FIMBox kickoff from attached materials\n", 1,
        )[1].split("\n#### ", 1)[0]
        self.assertEqual(
            set(re.findall(r"`([^`]+\.docx)`", example)),
            {"Project Narrative FY25 Cohen FIMBox.docx", "CUAHSI-Research-Plan-FIMBox.docx"},
        )
        for requirement in (
            "two Word documents and a screenshot", "Grant-information screenshot",
            "Use the ./cuahsi-project-management skill to kick off the FIMBox project.",
            "/cuahsi-project-management kickoff FIMBox",
            "not files bundled with this repository",
            "link rather than transcribe financial details",
            "kickoff does not automatically publish a charter",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, example)
        self.assertNotIn("file:///Users/", example)
        image_link = "docs/images/fimbox-dashboard-screenshot.png"
        self.assertEqual(
            re.findall(r"!\[[^\]]+\]\(([^)]+)\)", example), [image_link],
        )
        self.assertGreater(example.index(image_link), example.index("| Grant-information screenshot |"))
        self.assertLess(example.index(image_link), example.index("Then use the same style of input"))
        image = SKILL_DIRECTORY.parent / image_link
        self.assertTrue(image.is_file(), "Bundle the screenshot referenced by the README")
        with image.open("rb") as screenshot:
            self.assertEqual(screenshot.read(8), b"\x89PNG\r\n\x1a\n")
        self.assertIn("the screenshot is reproduced above for reference", example)

    def test_project_directory_examples_use_the_confirmed_shortname_contract(self):
        """Keep orchestration, publication, policy, and README paths synchronized."""
        documents = [
            SKILL_DIRECTORY / "SKILL.md",
            SKILL_DIRECTORY / "assets" / "publication.md",
            SKILL_DIRECTORY / "assets" / "repository-policy-template.md",
            SKILL_DIRECTORY.parent / "README.md",
        ]
        for document in documents:
            with self.subTest(document=document.name):
                content = document.read_text()
                self.assertIn("projects/<accounting-code>-<shortname>/", content)
                self.assertNotIn("projects/<accounting-code>/", content)
                self.assertNotIn("projects/<encoded-code>/", content)
        publication = documents[1].read_text()
        self.assertIn("projects/A250366S013-FIMBox/", publication)
        self.assertIn("URL-escaping the actual segment", publication)

    def test_publication_collects_shortname_without_redefining_identity(self):
        """Make shortname confirmation explicit rather than deriving it from a slug."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        for requirement in (
            "Collect or explicitly confirm the shortname with the user",
            "preserving its case", "not a new identity",
            "keep a missing shortname pending",
            "Without a canonical code or confirmed shortname",
            "create or rename no project directory on either branch",
            "Never infer identity by splitting on hyphens",
            "An absent or historical Shortname field in an existing charter",
            "is not silently backfilled or rewritten",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, publication)
        template = (SKILL_DIRECTORY / "assets" / "charter-template.md").read_text()
        self.assertIn(
            "Shortname: <confirmed case-preserving human-readable folder suffix / pending; "
            "not an identity>", template,
        )

    def test_directory_contract_requires_safety_mapping_and_uniqueness(self):
        """Expose path/identity guards without pretending to execute an agent."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        for requirement in (
            "validate the confirmed shortname, code component, and complete",
            "safe single path segments before writes", "Require nonempty values",
            "reject `.`/`..`, traversal, absolute paths", "control/NUL characters",
            "filesystem-reserved names/characters", "trailing spaces/dots",
            "filesystem limits", "without symlink redirection",
            "rather than silently stripping characters, lowercasing, or slugifying",
            "reversible accounting-code encoding", "encoding/decoding rule",
            "Preserve the original code in charter identity",
            "URL escaping", "including legacy names", "pending publication PRs",
            "one project directory per accounting code per branch",
            "a different requested suffix requires an explicit path-only rename",
            "Block an occupied destination", "case-folding/filesystem-equivalent collision",
            "ambiguous encoding", "duplicate directories for the same accounting code",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, publication)
        policy = (SKILL_DIRECTORY / "assets" / "repository-policy-template.md").read_text()
        for field in (
            "## Project directory mapping", "Accounting code (canonical key)",
            "Confirmed shortname", "Code component", "Reversible encoding/decoding rule",
            "Exact project directory", "Confirmation evidence", "Path-only rename record:",
            "old/new paths", "byte-comparison and navigation evidence",
        ):
            with self.subTest(policy_field=field):
                self.assertIn(field, policy)

    def test_path_only_rename_preserves_bytes_history_and_external_review_boundary(self):
        """Keep directory moves separate from charter revision and log creation."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        rename = publication.split("### Path-only rename\n", 1)[1].split("\n## 4.", 1)[0]
        for requirement in (
            "only when the user explicitly requests a path-only rename",
            "including the unchanged access audit",
            "same write/merge authorization and repository-rule requirements",
            "Preserve charter/log bytes exactly", "Move other existing project files unchanged",
            "initialize no new charter, log, or decision", "Keep Git history",
            "immutable commit links", "Preserve each branch's own snapshot/proposal contents",
            "case-only rename", "Update the policy mapping", "central README/index navigation",
            "every affected related-repository link", "Historical immutable references",
            "Compare source and destination charter/log bytes before and after merge",
            "old directory is absent", "only one directory maps to the code",
            "read back active navigation URLs", "Recheck destination occupancy",
            "already completed identical rename needs no duplicate PR",
            "Report partial moves and link gaps explicitly",
            "not a new project or charter-content revision",
            "needs no new kickoff or Wayfinder/grilling session",
            "including all historical metadata", "Existing history remains attached to unchanged bytes",
            "it does not authorize content changes", "separate that candidate from the move",
            "hand off its review and approval through an external GitHub PR",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, rename)
        for document in ("SKILL.md", "assets/lifecycle.md"):
            with self.subTest(route=document):
                content = (SKILL_DIRECTORY / document).read_text()
                self.assertIn("path-only rename", content)
                self.assertIn("publication", content.lower())
                self.assertRegex(content.lower(), r"\bpreserves? charter/log bytes and history\b")

    def test_publication_scenarios_cover_directory_and_rename_failures(self):
        """Keep synthetic behavior checks available independently of packaging."""
        scenarios = (SKILL_DIRECTORY / "assets" / "publication-scenarios.md").read_text()
        for heading in (
            "7. Missing or unconfirmed shortname",
            "8. Unsafe segments and reversible code encoding",
            "9. Occupied paths, duplicate codes, and hyphen ambiguity",
            "10. Explicit path-only rename with unchanged commitments",
            "11. Rename authorization, partial migration, and content-change boundary",
        ):
            with self.subTest(scenario=heading):
                case = scenarios.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn("### Inputs", case)
                self.assertIn("### Expected", case)
        for example in (
            "user-confirmed case-preserving shortname `SensorKit` (not the slug)",
            "projects/SYN-GRANT-42-SensorKit/charter.md",
            "../SensorKit", "Sensor/Kit", "Sensor\\Kit", "NUL/control",
            "SYN%2FGRANT%2F42-SensorKit", "SYN%252FGRANT%252F42-SensorKit",
            "`SYN-GRANT` with confirmed shortname `42-SensorKit`",
            "projects/syn-grant-42-sensorkit/", "projects/SYN-GRANT-42-OldKit/",
            "projects/SYN-GRANT-42-Sensor-Kit/", "projects/SYN-GRANT-42-ReUseBox/",
            "baseline predates the Shortname field", "quietly move delivery",
        ):
            with self.subTest(example=example):
                self.assertIn(example, scenarios)

    def test_decision_assets_expose_attribution_source_and_review_fields(self):
        """Keep decision evidence and human review visible in public templates."""
        log = (SKILL_DIRECTORY / "assets" / "decision-log-template.md").read_text()
        for field in (
            "Accounting grant or activity code (canonical key):",
            "Approved charter:", "## Entries", "Entry ID:", "Decision date:",
            "Source transcript:", "Decision:", "Charter impact:",
            "Supersedes:", "AI-drafted:", "Reviewed by:",
        ):
            with self.subTest(log_field=field):
                self.assertIn(field, log)
        self.assertIn("source/publication revision <immutable Git commit URL / pending>", log)
        self.assertIn("publication PR <GitHub PR URL / pending>", log)
        self.assertIn("no in-document version field", log)
        self.assertNotIn("<approved version>", log)
        pull_request = (SKILL_DIRECTORY / "assets" / "decision-pr-template.md").read_text()
        self.assertIn("immutable Git commit or PR reference; no in-document version field", pull_request)
        self.assertNotIn("<main charter URL and version>", pull_request)
        for field in (
            "Canonical key:", "Charter/version:", "PI/co-PI tags:",
            "AI-drafted:", "Reviewed by:", "## Decisions and sources",
            "## Charter impact", "## Checks",
            "- [ ] Withheld items reviewed",
            "- [ ] Existing decision-log entries are unchanged",
        ):
            with self.subTest(pr_field=field):
                self.assertIn(field, pull_request)

    def test_charter_template_exposes_the_required_fixed_schema(self):
        """Keep the complete public charter schema available to the caller."""
        template = (SKILL_DIRECTORY / "assets" / "charter-template.md").read_text()
        required_sections = [
            "Project summary", "Identity", "Purpose and research question", "Objectives",
            "Deliverables", "Key dates", "Team and roles", "Out of scope",
            "Risks and assumptions", "Source documents",
        ]
        sections = re.findall(r"(?m)^## (.+)$", template)
        self.assertEqual(sections, required_sections)
        for field in (
            "Accounting grant or activity code (canonical key):",
            "Shortname:", "Slug:", "Jira keys:", "GitHub repositories:",
            "Decision-PR tags:", "Date last modified: <YYYY-MM-DD>",
            "| Objective as written | What we mean |",
            "| Deliverable | Owner | Target date | Rough size (S/M/L or person-weeks) |",
        ):
            with self.subTest(field=field):
                self.assertIn(field, template)

    def test_charter_template_header_contains_only_date_last_modified(self):
        """Check template metadata, not an agent's choice of modification date."""
        template = (SKILL_DIRECTORY / "assets" / "charter-template.md").read_text()
        header = template.split("\n## ", 1)[0]
        self.assertEqual(
            [line for line in header.splitlines() if line.strip()],
            ["# Project Charter: <project or activity title>",
             "Date last modified: <YYYY-MM-DD>"],
        )
        self.assertEqual(template.count("Date last modified:"), 1)

    def test_charter_template_summary_guides_non_specialist_explanation(self):
        """Require instructions for problem, work, and beneficiaries in the opener."""
        template = (SKILL_DIRECTORY / "assets" / "charter-template.md").read_text()
        summary = template.split("## Project summary\n", 1)[1].split("\n## ", 1)[0]
        for requirement in (
            "One short paragraph for a non-specialist",
            "what problem the project addresses", "what the team will do",
            "who benefits", "Explain necessary terms and acronyms",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, summary)

    def test_charter_template_omits_review_approval_and_proposal_fields(self):
        """Scope removed fields to the charter, not policy or decision artifacts."""
        template = (SKILL_DIRECTORY / "assets" / "charter-template.md").read_text()
        self.assertNotRegex(
            template,
            r"(?im)^\s*(?:-\s+)?(?:AI-drafted|Reviewed by|Version|Status|Approver|"
            r"Reviewer|Approval(?: evidence| date)?|Approved by|Sign[- ]off)\s*:",
        )
        self.assertNotRegex(template, r"(?im)^#{1,6}\s+.*\b(?:sign[- ]off|approval|review)\b")
        self.assertNotRegex(template, r"(?i)\bproposed\b")
        self.assertIn("<named owner / pending>", template)
        self.assertIn("<agreed interpretation or unresolved question>", template)

    def test_guides_document_current_charter_presentation(self):
        """Keep packaged drafting guidance aligned without evaluating generated prose."""
        requirements = {
            SKILL_DIRECTORY / "SKILL.md": (
                "plain-language Project summary explaining the problem, planned work, and who benefits",
                "without assuming specialist knowledge; explain necessary terms and acronyms",
                "header contains only Date last modified: YYYY-MM-DD beneath the title",
                "use the actual modification date and update it when the charter changes",
                "Omit AI-drafted, Reviewed by, Version, and Status fields and any Sign-off section",
                "Everything on develop is a proposal",
                "rather than adding proposed labels to individual items",
                "Preserve genuine uncertainty as specific pending values or open questions",
                "Git commits and PRs carry revision and review history",
            ),
            SKILL_DIRECTORY / "assets" / "publication.md": (
                "For new or revised charter content, the header contains only Date last modified",
                "first section is a plain-language Project summary",
                "Omit AI-drafted, Reviewed by, Version, and Status header fields, "
                "item-level proposed labels, and the Sign-off section",
                "branch placement makes the whole charter a proposal without document labels",
                "retain unresolved planning values honestly",
                "A pure path-only rename preserves existing bytes",
            ),
            SKILL_DIRECTORY / "assets" / "repository-policy-template.md": (
                "only header metadata is Date last modified",
                "plain-language Project summary as the first section",
                "Charter headers omit AI-drafted, Reviewed by, Version, and Status fields",
                "charters have no Sign-off section",
                "develop holds proposals without document-level or item-level proposal labels",
                "Existing policy and decision-artifact AI/review fields are separate",
            ),
            SKILL_DIRECTORY.parent / "README.md": (
                "plain-language project summary first, then identity",
                "header contains only Date last modified: YYYY-MM-DD beneath the title",
                "no AI-drafted, Reviewed by, Version, or Status fields, and no Sign-off section",
                "Everything on develop is a proposal",
                "individual items need no proposed labels",
                "specific unknowns still remain pending",
                "PRs, which also carry revision history",
            ),
        }
        for document, expected in requirements.items():
            content = " ".join(document.read_text().replace("**", "").replace("`", "").split())
            for requirement in expected:
                with self.subTest(document=document.name, requirement=requirement):
                    self.assertIn(requirement, content)

    def test_guides_leave_charter_review_external_without_managed_gates(self):
        """Check explicit review boundaries; access and repository rules still apply."""
        requirements = {
            SKILL_DIRECTORY / "SKILL.md": (
                "Team review and approval happen outside this skill through GitHub PRs",
                "does not solicit, record, or gate team approval of the charter",
                "Participation and recording observations inform the discussion, "
                "not charter review or approval gates",
                "Human review and approval are not completion criteria for drafting",
            ),
            SKILL_DIRECTORY / "assets" / "lifecycle.md": (
                "Team review and approval remain outside the skill through GitHub PRs",
                "ownership is not a skill-managed charter approval role",
                "This establishes revision scope, not team review or approval of the charter",
            ),
            SKILL_DIRECTORY / "assets" / "publication.md": (
                "Team review and approval take place wholly outside the skill through GitHub PRs",
                "without collecting reviews, imposing a participation or absentee window, "
                "requiring PI/co-PI sign-off, or using a skill-managed human-review gate",
                "External review is a PR handoff, not a prerequisite imposed by the skill",
                "does not solicit or certify PI/co-PI sign-off or collect team reviews",
                "do not impose an additional human-review gate or claim review you have not verified",
            ),
            SKILL_DIRECTORY / "assets" / "repository-policy-template.md": (
                "Team review and approval are wholly outside the skill",
                "does not collect charter reviews or require PI/co-PI sign-off",
                "without an additional skill-managed charter review gate",
            ),
            SKILL_DIRECTORY.parent / "README.md": (
                "Team review and approval happen outside the skill through GitHub PRs",
                "not charter fields or a skill-managed sign-off gate",
            ),
        }
        for document, expected in requirements.items():
            content = " ".join(document.read_text().replace("**", "").replace("`", "").split())
            for requirement in expected:
                with self.subTest(document=document.name, requirement=requirement):
                    self.assertIn(requirement, content)
        for document in ("SKILL.md", "assets/lifecycle.md"):
            with self.subTest(gate_sections=document):
                content = (SKILL_DIRECTORY / document).read_text()
                self.assertNotRegex(
                    content, r"(?im)^#{2,3}\s+.*\b(?:absentee|reopening|sign[- ]off|approval)\b",
                )
                self.assertNotIn("20-minute", content)
                self.assertNotIn("Awaiting sign-off", content)
                self.assertNotIn("Set `Signed off`", content)

    def test_lifecycle_distinguishes_formatting_edits_from_commitment_changes(self):
        """Retain substantive-session and history rules without review gates."""
        lifecycle = (SKILL_DIRECTORY / "assets" / "lifecycle.md").read_text()
        revision = lifecycle.split("## Existing charter or requested revision\n", 1)[1]
        scope = revision.split("2. ", 1)[1].split("\n3. ", 1)[0]
        for requirement in (
            "explicitly requested formatting, metadata, or explanatory-summary edits",
            "without requiring a new kickoff or grilling session",
            "preserving commitments and factual meaning",
            "For changes to scope, ownership, deliverables, or dates",
            "Wayfinder or grilling session",
            "supplied, attributable session record naming participants and agreed changes",
            "explicitly conduct the session in this conversation",
            "ask before altering commitments",
            "Merely labeling a routine edit a re-grill is not a session",
        ):
            with self.subTest(scope_requirement=requirement):
                self.assertIn(requirement, scope)
        for requirement in (
            "file or immutable commit reference", "Preserve baseline history",
            "Change only what the user or session authorizes",
            "preserving unaffected commitments and source wording",
            "Apply the current charter schema and update Date last modified",
            "summarize the diff in the handoff rather than adding version, approval, or proposal labels",
            "specific pending values or open questions",
            "Git history for an explicitly requested in-place revision",
            "an existing baseline cannot be bypassed by choosing a different mode label",
        ):
            with self.subTest(revision_requirement=requirement):
                self.assertIn(requirement, revision)

    def test_publication_guidance_separates_review_handoff_from_merge_authority(self):
        """No charter-review gate does not mean unrestricted writes or merges."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        screening = publication.split("## 4. Select and screen the exact charter\n", 1)[1].split(
            "\n## 5.", 1,
        )[0]
        for requirement in (
            "Missing planning fields are called out in the PR/handoff for external resolution",
            "Missing canonical identity or an unsafe/unconfirmed directory still blocks writes",
            "Both paths require verified access and content screening",
            "A changed source requires reselection and a refreshed diff",
            "never claim it was reviewed based on an earlier revision",
        ):
            with self.subTest(screening_requirement=requirement):
                self.assertIn(requirement, screening)
        promotion = publication.split("## 5. Propose, merge, and verify publication\n", 1)[1].split(
            "\n## 6.", 1,
        )[0]
        for requirement in (
            "opening a PR does not authorize a merge",
            "Merge only on an explicit merge request, obeying observed repository rules",
            "verifying any checks those rules require without bypassing them",
            "Record reviewers and checked boxes only from verified evidence",
            "existing AI/review fields remain for decisions, not as charter approval requirements",
            "an open promotion PR is not a published `main` snapshot",
        ):
            with self.subTest(promotion_requirement=requirement):
                self.assertIn(requirement, promotion)

    def test_charter_scenarios_document_external_review_and_revision_scope(self):
        """Verify synthetic cases are packaged, not that their behaviors passed."""
        scenarios = (SKILL_DIRECTORY / "assets" / "charter-scenarios.md").read_text()
        requirements = {
            "1. New funded project": (
                "opening summary", "ordinary language", "actual modification date, not the award date",
                "without requiring an approver, reviewer, approval record, or sign-off",
                "external GitHub PR process",
            ),
            "2. Existing project at its next checkpoint": (
                "upcoming quarterly re-plan",
                "without an absentee notice, reopening-window timer, delivery confirmation, or participation gate",
                "Team review remains outside the skill",
            ),
            "3. Core Award Activity and ownership": (
                "confirmed activity ownership", "without turning ownership into a skill-managed approval role",
                "whether or not the old approval note is supplied",
                "Do not add sign-off/reviewer fields, demand approval from Casey",
            ),
            "4. Missing fields and a conflicting commitment": (
                "every schema section with explicit pending values",
                "without adding a Status field, approval blockers, or per-item proposal labels",
            ),
            "5. Commitment revision authorization and baseline history": (
                "ask for a real grilling/Wayfinder session", "only the authorized delivery-date change",
                "No approval reset, approver request, or version/status label is needed",
                "leave team review and approval to GitHub PRs", "Preserve baseline history",
            ),
            "6. Formatting revision and branch-based proposal semantics": (
                "without demanding a kickoff, grilling session, reviewer, or approval",
                "Remove the obsolete fields/section rather than relocating them",
                "Project summary is the first section", "problem, work, and beneficiaries",
                "proposal by branch placement", "preserving actual pending values and source wording",
                "Preserve owners, dates, rough sizes, scope, canonical identity",
                "Update Date last modified and deliver a focused diff",
                "outside the skill through GitHub PRs",
            ),
        }
        for heading, expected in requirements.items():
            case = scenarios.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
            self.assertIn("### Inputs", case)
            outcome = case.split("### Expected\n", 1)[1]
            for requirement in expected:
                with self.subTest(scenario=heading, requirement=requirement):
                    self.assertIn(requirement, outcome)
        self.assertIn("does not execute an agent or prove workflow compliance", scenarios)
        self.assertIn("a written scenario is not a passing test", scenarios)

    def test_publication_scenarios_document_external_review_and_merge_limits(self):
        """Keep no-review-gate cases separate from actual GitHub rule verification."""
        scenarios = (SKILL_DIRECTORY / "assets" / "publication-scenarios.md").read_text()
        requirements = {
            "1. Initial publication without charter approval metadata (tracer)": (
                "Date last modified as charter header metadata and Project summary first",
                "without collecting reviews, imposing an absentee window, or requiring PI/co-PI sign-off",
                "existing policy/decision-artifact AI/review fields distinct from charter approval",
                "PR creation does not authorize merging",
            ),
            "2. Proposal storage and selective promotion with external PR review": (
                "branch makes the whole charter a proposal without labels or Status metadata",
                "Open-PR preparation is not blocked by absent PI/co-PI sign-off or uncollected team reviews",
                "Do not transfer review from `source-r1`, certify approval",
            ),
            "4. Restricted content and changed source require an external review handoff": (
                "stop before committing it to either branch/history",
                "Do not silently sanitize, invent approval, or treat earlier review as covering changed bytes",
                "identify/reselect `source-r2`, refresh the focused PR diff and source reference",
                "external review without collecting reviews or requiring PI/co-PI sign-off",
            ),
            "13. Missing planning fields without invented approval": (
                "Retain pending planning values without guessing",
                "Do not collect reviews, create an absentee window, require PI/co-PI sign-off",
                "block safe authorized PR preparation solely for absent approval metadata",
                "missing identity, unsafe paths, or unverified access would still block content writes",
            ),
            "14. PR creation and explicit merge requests are distinct": (
                "Do not treat PR creation as merge authorization",
                "obey observed repository rules without bypassing required checks or claiming unverified review",
                "do not collect team reviews or add a separate skill-managed gate",
                "without claiming a live operation",
            ),
        }
        for heading, expected in requirements.items():
            case = scenarios.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
            self.assertIn("### Inputs", case)
            outcome = case.split("### Expected\n", 1)[1]
            for requirement in expected:
                with self.subTest(scenario=heading, requirement=requirement):
                    self.assertIn(requirement, outcome)
        self.assertIn("neither packaging nor simulated access establishes live acceptance", scenarios)

    def test_post_kickoff_approval_authorizes_exact_develop_pr_submission(self):
        """Check the packaged trigger and bounds, not a live publication run."""
        skill = (SKILL_DIRECTORY / "SKILL.md").read_text()
        self.assertIn('direct follow-up **"this is approved"**', skill)
        step = skill.split("## 5. Publish kickoff documents\n", 1)[1].split(
            "\n## Verification", 1,
        )[0]
        content = " ".join(step.replace("**", "").replace("`", "").split())
        for requirement in (
            'after kickoff has delivered charter documents',
            '"this is approved" (case-insensitive, with optional final punctuation)',
            "authorizes saving, committing, pushing, and opening its PR",
            "No additional publish, push, PR request, or confirmation is needed",
            "CUAHSI/CUAHSI-ProjectStream as the destination and develop as the PR base",
            "topic branch from the latest remote develop",
            "verify the exact staged file set and diff",
            "Keep approved document bytes unchanged",
            "obtain fresh user approval before submitting them",
            "Commit and push the topic branch to ProjectStream",
            "open a PR explicitly targeting develop",
            "never push the documents directly to develop for this trigger",
            "leave the PR open, make no changes to main, and do not merge or promote",
            "ask which set before writing", "Without a delivered kickoff document set",
            "Quoted phrases and instructions to change the skill do not trigger",
            "approval phrase does not waive safety checks",
            "Read back the pushed files and PR repository, base, head, file set, and open state",
            "reuse an identical open PR", "no new diff rather than invent an empty PR",
            "Report partial push/PR failures accurately",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, content)
        self.assertIn("[Publication](assets/publication.md)", step)
        self.assertIn('replying **"this is approved"**', skill)

    def test_approval_submission_route_and_synthetic_cases_are_bundled(self):
        """Keep follow-up discovery and retry/safety scenarios reachable."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        readme = (SKILL_DIRECTORY.parent / "README.md").read_text()
        self.assertIn(
            "[Publish kickoff documents](../SKILL.md#5-publish-kickoff-documents)",
            publication,
        )
        self.assertIn(
            "[Publish kickoff documents](cuahsi-project-management/SKILL.md#5-publish-kickoff-documents)",
            readme,
        )
        for document in (publication, readme):
            self.assertIn('**"this is approved"**', document)
            self.assertIn("PR targeting `develop`", document.replace("**", ""))
        cases = {
            "charter-scenarios.md": (
                "7. Post-kickoff approval routes to publication",
                "without asking for another publish/push/PR request",
                "Quoted approval in a skill-edit request is not a live publication trigger",
            ),
            "publication-scenarios.md": (
                "15. Post-kickoff approval submits an exact document set to develop",
                "without another authorization request",
                "missing access verification blocks writes",
                "a required content change needs fresh user approval",
                "Reuse an identical open PR on retry",
                "report no new diff", "report partial results honestly",
            ),
        }
        for filename, (heading, *requirements) in cases.items():
            scenarios = (SKILL_DIRECTORY / "assets" / filename).read_text()
            case = scenarios.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
            self.assertIn("### Inputs", case)
            expected = case.split("### Expected\n", 1)[1]
            for requirement in requirements:
                with self.subTest(scenario=heading, requirement=requirement):
                    self.assertIn(requirement, expected)

    def test_kickoff_creates_only_charter_without_review_handoff_document(self):
        """Check the output and submission contract without deleting legacy files."""
        skill = (SKILL_DIRECTORY / "SKILL.md").read_text()
        drafting = skill.split("## 3. Draft the charter\n", 1)[1].split("\n## 4.", 1)[0]
        for requirement in (
            "create one project document, `charter.md`",
            "review guidance in chat and the eventual PR description",
            "Do not create `team-review.md` or an equivalent separate review/handoff document",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, drafting)
        self.assertIn("save only the approved `charter.md` and necessary project navigation/mapping changes", skill)
        self.assertIn("Leave pre-existing review/handoff files unchanged and out of this submission", skill)
        self.assertIn("removing an existing file requires an explicit removal request", skill)
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        self.assertIn("[kickoff output contract](../SKILL.md#3-draft-the-charter)", publication)
        readme = (SKILL_DIRECTORY.parent / "README.md").read_text()
        self.assertIn("`kickoff` creates only `charter.md`, not `team-review.md`", readme)
        scenarios = (SKILL_DIRECTORY / "assets" / "charter-scenarios.md").read_text()
        self.assertIn("No `team-review.md` or substitute review/handoff document is created or included", scenarios)
        self.assertIn("Preserve any pre-existing review file unchanged unless removal is explicitly requested", scenarios)
        publication_scenarios = (SKILL_DIRECTORY / "assets" / "publication-scenarios.md").read_text()
        self.assertIn("excluding `team-review.md` and any separate review/handoff document", publication_scenarios)


    def test_projectstream_changes_go_through_named_develop_prs(self):
        """Check that the PR-only rule and branch naming are bundled."""
        skill = (SKILL_DIRECTORY / "SKILL.md").read_text()
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        rule = publication.split("## ProjectStream submission rule\n", 1)[1].split("\n## 1.", 1)[0]
        content = " ".join(rule.replace("**", "").replace("`", "").split())
        for requirement in (
            "reaches the repository only through a pull request",
            "Never push directly to develop, main, or any other ProjectStream branch",
            "topic branch from the latest remote develop",
            "open a PR whose base is develop",
            "<action>-<ShortName>-<summary>",
            "kickoff-FIMBox-project-initiation",
            "revise-FIMBox-simplify-charter-header",
            "kickoff - FIMBox project initiation",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, content)
        flat_skill = " ".join(skill.replace("**", "").replace("`", "").split())
        self.assertIn("kickoff-<ShortName>-<summary>", flat_skill)
        self.assertIn("every ProjectStream change, including a later revise", flat_skill)
        self.assertIn("assets/publication.md#projectstream-submission-rule", skill)
        readme = (SKILL_DIRECTORY.parent / "README.md").read_text()
        self.assertIn("the branch is named for the action", readme)
        scenarios = (SKILL_DIRECTORY / "assets" / "publication-scenarios.md").read_text()
        self.assertIn("## 16. Every ProjectStream change goes through a named topic-branch PR", scenarios)
        self.assertIn("Refuse any direct push to `develop`, `main`", scenarios)


if __name__ == "__main__":
    unittest.main()
