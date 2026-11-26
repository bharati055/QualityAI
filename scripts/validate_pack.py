#!/usr/bin/env python3
"""Validate the QualityAI pack contract (stdlib only).

Usage:
    validate_pack.py [--root DIR]    check one repo/pack root (default: this repo)
    validate_pack.py --self-check    unit tests + every pack checker + this repo

Checks (each issue is printed as `CODE path: message`):
    SKILL_*   skill folder has the required files and matching frontmatter
    LINK      relative Markdown link points at a missing file
    SKILL_REF skill id or phase referenced by agents, gates, WORKFLOWS or
              FINDING-SCHEMA does not exist
    CHECKLIST `- [ ]` / `- [x]` task list inside a `*.agent.md` file
    STUB      `status: stub` and the STUB banner disagree in a context file
    QUAR_*    quarantine metadata incomplete, expired without escalation, or a
              muted test without a ticket (flaky-quarantine/tooling/validate_quarantine.py)
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import unittest
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SKILL_FILES = ("SKILL.md", "PLAYBOOK.md", "coverage/COVERAGE.md", "coverage/GAPS.md")
GOOD_TOKENS = {"good", "better", "well", "clear", "readable", "secure", "aligned", "reviewed"}
BAD_TOKENS = {"bad", "anti", "unreadable", "insecure", "drifted", "vague", "regression", "missing"}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
INLINE_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]*)\)")
REF_LINK_RE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
PLACEHOLDER_RE = re.compile(r"[<>{}$*]|\.\.\.|YYYY|\bTODO\b")
CHECKLIST_RE = re.compile(r"^\s*[-*+]\s+\[[ xX]\]\s")
STATUS_STUB_RE = re.compile(r"^status:\s*stub\s*$", re.M)
STUB_BANNER_RE = re.compile(r"^>\s*\*\*STUB — implement as needed", re.M)

SKILL_PATH_RE = re.compile(r"skills/([A-Za-z0-9][A-Za-z0-9_-]*)(?![A-Za-z0-9_-])(?!\.[A-Za-z])(?:/playbook/([A-Za-z0-9_|-]+))?")
SKILL_APPLIED_RE = re.compile(r"skill_applied[`\"']?\s*[:=]\s*[`\"']?([a-z][a-z0-9-]*)")
SKILL_LABEL_RE = re.compile(r"^\s*[-*]\s*Skill:\s*`([a-z][a-z0-9-]*)`")
SKILL_PHASE_RE = re.compile(r"`([a-z][a-z0-9-]*)`\s*/\s*`([a-z][a-z0-9-]*)`")
SKILLS_BULLET_RE = re.compile(r"^\s*[-*]\s*`([a-z][a-z0-9-]*)`")
PLACEHOLDER_IDS = {"skill-id", "id"}


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


def qa_dir(root: Path) -> Path:
    return root / ".qualityai"


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return out
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            out[key.strip()] = value.strip().strip("'\"")
    return None


def prose_lines(text: str):
    """Yield (line_number, line) outside fenced code blocks."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            yield number, line


def skill_ids(root: Path) -> list[str]:
    skills = qa_dir(root) / "skills"
    if not skills.is_dir():
        return []
    return sorted(p.name for p in skills.iterdir() if p.is_dir())


def skill_phases(root: Path, skill: str) -> set[str]:
    playbook = qa_dir(root) / "skills" / skill / "playbook"
    if not playbook.is_dir():
        return set()
    return {p.name for p in playbook.iterdir() if (p / "PLAYBOOK.md").is_file()}


def check_skills(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    skills = qa_dir(root) / "skills"
    if not skills.is_dir():
        return [Issue("SKILL_DIR", ".qualityai/skills", "directory missing")]
    for skill in skill_ids(root):
        base = skills / skill
        where = rel(root, base)
        for name in SKILL_FILES:
            if not (base / name).is_file():
                issues.append(Issue("SKILL_FILE", where, f"missing {name}"))
        if not skill_phases(root, skill):
            issues.append(Issue("SKILL_PHASE", where, "no playbook/<phase>/PLAYBOOK.md"))
        examples = base / "examples"
        names = sorted(p.stem for p in examples.iterdir() if p.is_file()) if examples.is_dir() else []
        tokens = [set(n.lower().split("-")) for n in names]
        if not any(t & GOOD_TOKENS for t in tokens):
            issues.append(Issue("SKILL_EXAMPLES", where, "examples/ needs a good pattern (e.g. good-pattern.md)"))
        if not any(t & BAD_TOKENS for t in tokens):
            issues.append(Issue("SKILL_EXAMPLES", where, "examples/ needs a bad pattern (e.g. bad-pattern.md)"))
        refs = base / "references"
        if not refs.is_dir() or not any(p.is_file() for p in refs.iterdir()):
            issues.append(Issue("SKILL_REFERENCES", where, "references/ needs at least one file"))
        skill_md = base / "SKILL.md"
        if skill_md.is_file():
            meta = frontmatter(read(skill_md))
            if meta is None:
                issues.append(Issue("SKILL_FRONTMATTER", rel(root, skill_md), "missing frontmatter"))
            else:
                found = [k for k in ("name", "id") if k in meta]
                if not found:
                    issues.append(Issue("SKILL_FRONTMATTER", rel(root, skill_md), "needs `name` (or `id`)"))
                for key in found:
                    if meta[key] != skill:
                        issues.append(
                            Issue("SKILL_FRONTMATTER", rel(root, skill_md), f"{key}={meta[key]!r} != folder {skill!r}")
                        )
    return issues


def markdown_files(root: Path) -> list[Path]:
    files = sorted(root.glob("*.md"))
    qa = qa_dir(root)
    if qa.is_dir():
        files += sorted(qa.rglob("*.md"))
    return files


def link_targets(text: str):
    for number, line in prose_lines(text):
        stripped = INLINE_CODE_RE.sub("", line)
        for match in INLINE_LINK_RE.finditer(stripped):
            yield number, match.group(1)
        match = REF_LINK_RE.match(stripped)
        if match:
            yield number, match.group(1)


def clean_target(raw: str) -> str | None:
    target = raw.strip()
    end = target.find(">")
    if target.startswith("<") and end > 0 and (end == len(target) - 1 or target[end + 1].isspace()):
        target = target[1:end]
    else:
        target = target.split()[0] if target.split() else ""
    if not target or target.startswith("#") or SCHEME_RE.match(target) or PLACEHOLDER_RE.search(target):
        return None
    return re.split(r"[#?]", target, maxsplit=1)[0] or None


def check_links(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in markdown_files(root):
        for number, raw in link_targets(read(path)):
            target = clean_target(raw)
            if target is None:
                continue
            base = root if target.startswith("/") else path.parent
            resolved = (base / target.lstrip("/")).resolve()
            if not resolved.exists():
                issues.append(Issue("LINK", f"{rel(root, path)}:{number}", f"broken link {raw.strip()!r}"))
    return issues


def reference_files(root: Path) -> list[Path]:
    qa = qa_dir(root)
    files = sorted((qa / "agents").glob("*.agent.md"))
    files += sorted((qa / "agents" / "gates").glob("*.md"))
    files += [qa / "instructions" / "WORKFLOWS.md", qa / "instructions" / "FINDING-SCHEMA.md"]
    return [f for f in files if f.is_file()]


def check_skill_refs(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    known = set(skill_ids(root))
    for path in reference_files(root):
        where = rel(root, path)
        in_skills_section = False
        for number, line in prose_lines(read(path)):
            if line.startswith("#"):
                in_skills_section = line.lstrip("#").strip().lower() == "skills"
            found: list[tuple[str, str | None]] = []
            for m in SKILL_PATH_RE.finditer(line):
                found.append((m.group(1), m.group(2)))
            for regex in (SKILL_APPLIED_RE, SKILL_LABEL_RE):
                m = regex.search(line)
                if m:
                    found.append((m.group(1), None))
            if in_skills_section and (m := SKILLS_BULLET_RE.match(line)):
                found.append((m.group(1), None))
            for m in SKILL_PHASE_RE.finditer(line):
                if m.group(1) in known and m.group(2) not in known:
                    found.append((m.group(1), m.group(2)))
            for skill, phases in found:
                if skill in PLACEHOLDER_IDS or skill.startswith("<"):
                    continue
                if skill not in known:
                    issues.append(Issue("SKILL_REF", f"{where}:{number}", f"unknown skill {skill!r}"))
                elif phases:
                    for phase in phases.split("|"):
                        if phase and phase not in skill_phases(root, skill):
                            issues.append(
                                Issue("SKILL_REF", f"{where}:{number}", f"unknown phase {skill}/{phase}")
                            )
    return sorted(set(issues), key=lambda i: (i.path, i.message))


def check_checklists(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in sorted((qa_dir(root) / "agents").glob("*.agent.md")):
        for number, line in prose_lines(read(path)):
            if CHECKLIST_RE.match(line):
                issues.append(
                    Issue("CHECKLIST", f"{rel(root, path)}:{number}", "inline checklist; delegate to a skill")
                )
    return issues


def check_stubs(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    context = qa_dir(root) / "context"
    for path in sorted(context.rglob("*.md")) if context.is_dir() else []:
        text = read(path)
        has_status = bool(STATUS_STUB_RE.search(text))
        has_banner = bool(STUB_BANNER_RE.search(text))
        if has_status and not has_banner:
            issues.append(Issue("STUB", rel(root, path), "status: stub but STUB banner is missing"))
        if has_banner and not has_status:
            issues.append(Issue("STUB", rel(root, path), "STUB banner but `status: stub` is missing"))
    return issues


def quarantine_tool(root: Path):
    path = qa_dir(root) / "skills" / "flaky-quarantine" / "tooling" / "validate_quarantine.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("validate_quarantine", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check_quarantine(root: Path) -> list[Issue]:
    tool = quarantine_tool(root)
    if tool is None:
        return []
    found = tool.validate_root(root, None, date.today())
    return [Issue(i.code, i.path, i.message) for i in found]


def validate(root: Path) -> list[Issue]:
    checks = (check_skills, check_links, check_skill_refs, check_checklists, check_stubs, check_quarantine)
    return [issue for check in checks for issue in check(root)]


def run_unit_tests() -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    suite = unittest.defaultTestLoader.loadTestsFromName("test_validate_pack")
    return unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()


def run_command(label: str, command: list[str]) -> bool:
    print(f"== {label}", flush=True)
    ok = subprocess.run(command, cwd=REPO).returncode == 0
    if not ok:
        print(f"FAILED: {label}")
    return ok


def self_check() -> int:
    skills = REPO / ".qualityai" / "skills"
    spec = skills / "spec-based-testing"
    evals = skills / "eval-harness"
    quarantine = skills / "flaky-quarantine"
    py = sys.executable
    results = [
        run_unit_tests(),
        run_command("validate_spec_cases --self-check", [py, str(spec / "tooling/validate_spec_cases.py"), "--self-check"]),
        run_command(
            "validate_spec_cases examples",
            [py, str(spec / "tooling/validate_spec_cases.py"), *map(str, sorted(spec.glob("examples/*.json")))],
        ),
        run_command("validate_eval_case --self-check", [py, str(evals / "tooling/validate_eval_case.py"), "--self-check"]),
        run_command(
            "validate_eval_case --root .qualityai/evals",
            [py, str(evals / "tooling/validate_eval_case.py"), "--root", str(qa_dir(REPO) / "evals")],
        ),
        run_command(
            "validate_quarantine --self-check",
            [py, str(quarantine / "tooling/validate_quarantine.py"), "--self-check"],
        ),
    ]
    print("== validate_pack (this repo)")
    issues = validate(REPO)
    for issue in issues:
        print(issue)
    results.append(not issues)
    print("OK" if all(results) else "FAILED")
    return 0 if all(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=REPO)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    issues = validate(args.root.resolve())
    for issue in issues:
        print(issue)
    print(f"{len(issues)} issue(s)" if issues else "OK")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
