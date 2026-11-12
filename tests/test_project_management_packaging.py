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
            "Slug:", "Jira keys:", "GitHub repositories:",
            "Decision-PR tags:", "AI-drafted:", "Reviewed by:",
            "| Objective as written | What we mean |",
            "| Deliverable | Owner | Target date | Rough size (S/M/L or person-weeks) |",
            "Approver:", "Approval evidence:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, template)


if __name__ == "__main__":
    unittest.main()
