#!/usr/bin/env python3
"""Tests for validate_pack.py: the real pack must pass; broken packs must fail."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_pack as vp  # noqa: E402

STUB_BANNER = "> **STUB — implement as needed by this project.**\n"


def write(root: Path, rel: str, text: str = "x\n") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_pack(root: Path) -> None:
    """Smallest pack that satisfies every check."""
    skill = ".qualityai/skills/demo-skill"
    write(root, f"{skill}/SKILL.md", "---\nname: demo-skill\n---\n# Demo\n")
    for name in ("PLAYBOOK.md", "coverage/COVERAGE.md", "coverage/GAPS.md", "playbook/review/PLAYBOOK.md"):
        write(root, f"{skill}/{name}")
    write(root, f"{skill}/examples/good-pattern.md")
    write(root, f"{skill}/examples/bad-pattern.md")
    write(root, f"{skill}/references/notes.md")
    write(root, ".qualityai/agents/qa.demo.agent.md", "# Agent\n\n## Skills\n\n- `demo-skill` → `.qualityai/skills/demo-skill/SKILL.md`\n")
    write(root, ".qualityai/agents/gates/demo-gate.md", "- Skill: `demo-skill`\n")
    write(root, ".qualityai/instructions/WORKFLOWS.md", "Use `demo-skill` / `review`.\n")
    write(root, ".qualityai/instructions/FINDING-SCHEMA.md", '"skill_applied": "demo-skill#review"\n')
    write(root, ".qualityai/context/stub.md", f"{STUB_BANNER}\n<!--\nstatus: stub\n-->\n")
    write(root, ".qualityai/context/filled.md", "<!--\nstatus: active\n-->\n")
    write(root, "README.md", "[pack](.qualityai/README.md)\n")
    write(root, ".qualityai/README.md", "# Pack\n")


def codes(root: Path) -> set[str]:
    return {issue.code for issue in vp.validate(root)}


class RealPackTest(unittest.TestCase):
    def test_repository_pack_is_valid(self) -> None:
        self.assertEqual([str(i) for i in vp.validate(vp.REPO)], [])


class BrokenPackTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        make_pack(self.root)

    def skill(self, rel: str = "") -> Path:
        return self.root / ".qualityai/skills/demo-skill" / rel

    def test_good_pack_passes(self) -> None:
        self.assertEqual(vp.validate(self.root), [])

    def test_missing_required_files(self) -> None:
        for rel in ("PLAYBOOK.md", "coverage/COVERAGE.md", "coverage/GAPS.md"):
            with self.subTest(rel=rel):
                make_pack(self.root)
                self.skill(rel).unlink()
                self.assertIn("SKILL_FILE", codes(self.root))

    def test_missing_skill_md(self) -> None:
        self.skill("SKILL.md").unlink()
        self.assertIn("SKILL_FILE", codes(self.root))

    def test_missing_phase_playbook(self) -> None:
        self.skill("playbook/review/PLAYBOOK.md").unlink()
        self.assertIn("SKILL_PHASE", codes(self.root))

    def test_missing_good_or_bad_example(self) -> None:
        for name in ("good-pattern.md", "bad-pattern.md"):
            with self.subTest(name=name):
                make_pack(self.root)
                self.skill(f"examples/{name}").unlink()
                self.assertIn("SKILL_EXAMPLES", codes(self.root))

    def test_missing_references(self) -> None:
        self.skill("references/notes.md").unlink()
        self.assertIn("SKILL_REFERENCES", codes(self.root))

    def test_frontmatter_mismatch_or_missing(self) -> None:
        write(self.root, ".qualityai/skills/demo-skill/SKILL.md", "---\nname: other\n---\n")
        self.assertIn("SKILL_FRONTMATTER", codes(self.root))
        write(self.root, ".qualityai/skills/demo-skill/SKILL.md", "---\nid: demo-skill\n---\n")
        self.assertEqual(vp.validate(self.root), [])
        write(self.root, ".qualityai/skills/demo-skill/SKILL.md", "# no frontmatter\n")
        self.assertIn("SKILL_FRONTMATTER", codes(self.root))

    def test_broken_link(self) -> None:
        write(self.root, "README.md", "[gone](missing.md)\n")
        self.assertIn("LINK", codes(self.root))

    def test_links_ignored_when_not_real(self) -> None:
        text = (
            "```\n[x](nope.md)\n```\n"
            "`[y](nope.md)`\n"
            "[web](https://example.com/nope) [mail](mailto:a@b.c) "
            "[agent](cursor.agent://x) [anchor](#top) [tpl](<skill-id>/SKILL.md) "
            "[ok](.qualityai/README.md#section)\n"
        )
        write(self.root, "README.md", text)
        self.assertEqual(vp.validate(self.root), [])

    def test_reference_style_link(self) -> None:
        write(self.root, "README.md", "[a][1]\n\n[1]: gone.md\n")
        self.assertIn("LINK", codes(self.root))

    def test_unknown_skill_references(self) -> None:
        cases = {
            ".qualityai/agents/qa.demo.agent.md": "## Skills\n\n- `ghost-skill` → x\n",
            ".qualityai/agents/gates/demo-gate.md": "- Skill: `ghost-skill`\n",
            ".qualityai/instructions/WORKFLOWS.md": "see `.qualityai/skills/ghost-skill/SKILL.md`\n",
            ".qualityai/instructions/FINDING-SCHEMA.md": '"skill_applied": "ghost-skill#x"\n',
        }
        for rel, text in cases.items():
            with self.subTest(rel=rel):
                make_pack(self.root)
                write(self.root, rel, text)
                self.assertIn("SKILL_REF", codes(self.root))

    def test_unknown_playbook_phase(self) -> None:
        write(self.root, ".qualityai/instructions/WORKFLOWS.md", "`demo-skill` / `nope`\n")
        self.assertIn("SKILL_REF", codes(self.root))
        write(self.root, ".qualityai/agents/qa.demo.agent.md", "skills/demo-skill/playbook/review|nope\n")
        self.assertIn("SKILL_REF", codes(self.root))

    def test_checklist_only_flagged_in_agent_files(self) -> None:
        write(self.root, ".qualityai/agents/qa.demo.agent.md", "- [ ] do a thing\n")
        self.assertIn("CHECKLIST", codes(self.root))
        make_pack(self.root)
        write(self.root, ".qualityai/agents/qa.demo.agent.feedback.md", "- [ ] ok\n")
        write(self.root, ".qualityai/agents/gates/demo-gate.md", "- [x] ok\n")
        write(self.root, ".qualityai/agents/qa.demo.agent.md", "```\n- [ ] sample\n```\n")
        self.assertEqual(vp.validate(self.root), [])

    def test_stub_banner_and_status_must_agree(self) -> None:
        write(self.root, ".qualityai/context/stub.md", "<!--\nstatus: stub\n-->\n")
        self.assertIn("STUB", codes(self.root))
        write(self.root, ".qualityai/context/stub.md", STUB_BANNER)
        self.assertIn("STUB", codes(self.root))
        write(self.root, ".qualityai/context/stub.md", "Mentions `status: stub` and the STUB banner in prose.\n")
        self.assertEqual(vp.validate(self.root), [])


class CliTest(unittest.TestCase):
    def test_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_pack(root)
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(vp.main(["--root", str(root)]), 0)
                write(root, "README.md", "[gone](missing.md)\n")
                self.assertEqual(vp.main(["--root", str(root)]), 1)
            self.assertIn("LINK README.md:1", out.getvalue())


if __name__ == "__main__":
    unittest.main()
