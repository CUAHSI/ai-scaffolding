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
