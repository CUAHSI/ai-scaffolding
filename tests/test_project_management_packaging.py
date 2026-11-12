"""Check the public packaging contract of the project-management skill."""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_DIRECTORY = Path(__file__).resolve().parents[1] / "cuahsi-project-management"


class ProjectManagementPackagingTests(unittest.TestCase):
    def test_skill_is_named_and_available_for_explicit_invocation(self):
        document = (SKILL_DIRECTORY / "SKILL.md").read_text()
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", document, re.DOTALL)
        self.assertIsNotNone(frontmatter, "Publish Agent Skills frontmatter")
        metadata = frontmatter.group(1)
        self.assertRegex(metadata, r"(?m)^name: cuahsi-project-management$")
        self.assertRegex(metadata, r"(?m)^disable-model-invocation: true$")
        description = re.search(r"(?m)^description: (.+)$", metadata)
        self.assertIsNotNone(description, "Provide a human-facing description")
        self.assertTrue(1 <= len(description.group(1).strip('\"')) <= 1024)

    def test_installed_skill_can_reach_all_bundled_references(self):
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
