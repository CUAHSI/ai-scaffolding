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
            "An absent or historical Shortname field in a signed-off charter",
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

    def test_path_only_rename_preserves_bytes_history_and_approval_boundary(self):
        """Keep directory moves separate from charter revision and log creation."""
        publication = (SKILL_DIRECTORY / "assets" / "publication.md").read_text()
        rename = publication.split("### Path-only rename\n", 1)[1].split("\n## 4.", 1)[0]
        for requirement in (
            "only when the user explicitly requests a path-only rename",
            "including the unchanged access audit",
            "same write/review/merge authorization requirements",
            "Preserve charter/log bytes exactly", "Move other existing project files unchanged",
            "initialize no new charter, log, or decision", "Keep Git history",
            "immutable commit links", "Preserve each branch's own approved/draft contents",
            "case-only rename", "Update the policy mapping", "central README/index navigation",
            "every affected related-repository link", "Historical immutable references",
            "Compare source and destination charter/log bytes before and after merge",
            "old directory is absent", "only one directory maps to the code",
            "read back active navigation URLs", "Recheck destination occupancy",
            "already completed identical rename needs no duplicate PR",
            "Report partial moves and link gaps explicitly",
            "not a new project or charter-content revision",
            "needs no new kickoff, Wayfinder/grilling session, charter version, or PI/co-PI sign-off",
            "Existing approval remains evidence for the unchanged bytes",
            "separate that candidate and apply the existing lifecycle/sign-off rules",
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
        pull_request = (SKILL_DIRECTORY / "assets" / "decision-pr-template.md").read_text()
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
        required_sections = {
            "Identity", "Purpose and research question", "Objectives", "Deliverables",
            "Key dates", "Team and roles", "Out of scope", "Risks and assumptions",
            "Source documents", "Sign-off",
        }
        sections = set(re.findall(r"(?m)^## (.+)$", template))
        self.assertTrue(required_sections <= sections, required_sections - sections)
        for field in (
            "Accounting grant or activity code (canonical key):",
            "Shortname:", "Slug:", "Jira keys:", "GitHub repositories:",
            "Decision-PR tags:", "AI-drafted:", "Reviewed by:",
            "| Objective as written | What we mean |",
            "| Deliverable | Owner | Target date | Rough size (S/M/L or person-weeks) |",
            "Approver:", "Approval evidence:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, template)


if __name__ == "__main__":
    unittest.main()
