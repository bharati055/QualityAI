#!/usr/bin/env python3
"""Validate quarantine metadata (stdlib only).

Usage:
    validate_quarantine.py [--root DIR] [--source DIR ...] [--today YYYY-MM-DD]
    validate_quarantine.py FILE [FILE ...]
    validate_quarantine.py --self-check

With --root, checks:
    - every *.json / *.md under <root>/.qualityai/quarantine/ (the host's registry)
    - the shipped examples: examples/good-*.json must pass, examples/bad-*.json must fail
    - test sources under --source dirs (default: the root) for muted tests without a ticket

Issues print as `CODE path: message`; exit status is 1 when any are found.
The format is documented in references/quarantine-metadata.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

REQUIRED_FIELDS = ("test_id", "owner", "end_date", "ticket_id", "reason", "exit_criteria")
OPTIONAL_FIELDS = ("mechanism", "start_date", "notes")
MECHANISMS = {"disabled-annotation", "tag", "ci-skip-list"}

QUARANTINE_SKILL = "flaky-quarantine#quarantine"
EXPIRY_SKILL = "flaky-quarantine#expiry-review"
ESCALATION_SEVERITIES = {"high", "medium"}

MAX_DAYS_AHEAD = 90
MIN_TEXT_LENGTH = 10

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TICKET_RE = re.compile(r"^([A-Z][A-Z0-9]{1,9}-\d+|#\d+|[\w.-]+/[\w.-]+#\d+|https?://\S+)$")
TICKET_IN_TEXT_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b|(?<![\w/])#\d+\b|https?://\S+")
PLACEHOLDER_RE = re.compile(r"(?i)^(todo|tbd|tba|unknown|none|null|n/?a|\?+|-+|xxx+|fixme|later|pending)$")

SOURCE_SUFFIXES = {".java", ".kt", ".groovy", ".scala", ".py", ".js", ".jsx", ".ts", ".tsx", ".cs"}
SKIP_DIRS = {".git", ".qualityai", "node_modules", "target", "build", "dist", ".venv", "venv", "__pycache__"}
MUTE_RE = re.compile(
    r"@Disabled\b|@Ignore\b|@Test\s*\(\s*[^)]*enabled\s*=\s*false"
    r"|@pytest\.mark\.skip\b(?!if)|@unittest\.skip\b(?!If|Unless)|\bpytest\.skip\("
    r"|\b(?:it|test|describe)\.skip\(|\bx(?:it|describe)\("
    r"|\[Ignore\b|@Tag\s*\(\s*\"quarantine\"|@pytest\.mark\.quarantine\b"
)
COMMENT_RE = re.compile(r"^\s*(?://|#|\*|/\*)")

FENCE_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


def parse_date(value: object) -> date | None:
    if isinstance(value, str) and DATE_RE.match(value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def blank_or_placeholder(value: object) -> bool:
    return not isinstance(value, str) or not value.strip() or bool(PLACEHOLDER_RE.match(value.strip()))


def check_record(record: object, where: str, as_of: date) -> tuple[list[Issue], date | None]:
    """Return issues for one quarantine record and its parsed end_date."""
    if not isinstance(record, dict):
        return [Issue("QUAR_SHAPE", where, "quarantine record must be an object")], None
    issues: list[Issue] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            issues.append(Issue("QUAR_MISSING", where, f"missing required field `{field}`"))
        elif blank_or_placeholder(record[field]):
            issues.append(Issue("QUAR_EMPTY", where, f"`{field}` is empty or a placeholder"))
    for field in sorted(set(record) - set(REQUIRED_FIELDS) - set(OPTIONAL_FIELDS)):
        issues.append(Issue("QUAR_UNKNOWN", where, f"unknown field `{field}`"))

    ticket = record.get("ticket_id")
    if isinstance(ticket, str) and not blank_or_placeholder(ticket) and not TICKET_RE.match(ticket.strip()):
        issues.append(Issue("QUAR_TICKET", where, f"ticket_id {ticket!r} is not a tracker id (e.g. QA-1234, #42, URL)"))

    for field in ("reason", "exit_criteria"):
        text = record.get(field)
        if isinstance(text, str) and not blank_or_placeholder(text) and len(text.strip()) < MIN_TEXT_LENGTH:
            issues.append(Issue("QUAR_SHORT", where, f"`{field}` needs at least {MIN_TEXT_LENGTH} characters"))

    end: date | None = None
    if "end_date" in record and not blank_or_placeholder(record["end_date"]):
        end = parse_date(record["end_date"])
        if end is None:
            issues.append(Issue("QUAR_DATE", where, f"end_date {record['end_date']!r} is not an ISO date (YYYY-MM-DD)"))
        elif end > as_of + timedelta(days=MAX_DAYS_AHEAD):
            issues.append(
                Issue("QUAR_DATE_FAR", where, f"end_date {end} is more than {MAX_DAYS_AHEAD} days ahead; quarantine is temporary")
            )
    if "start_date" in record:
        start = parse_date(record["start_date"])
        if start is None:
            issues.append(Issue("QUAR_DATE", where, f"start_date {record['start_date']!r} is not an ISO date (YYYY-MM-DD)"))
        elif end is not None and start > end:
            issues.append(Issue("QUAR_DATE", where, "start_date is after end_date"))

    if "mechanism" in record and record["mechanism"] not in MECHANISMS:
        issues.append(Issue("QUAR_MECHANISM", where, f"mechanism must be one of {sorted(MECHANISMS)}"))
    return issues, end


def finding_text(finding: dict) -> str:
    evidence = finding.get("evidence")
    parts = [finding.get(k) for k in ("finding", "rationale", "recommendation")]
    if isinstance(evidence, dict):
        parts += [evidence.get("note"), evidence.get("file")]
    return " ".join(p for p in parts if isinstance(p, str))


def is_escalation(finding: object, record: dict) -> bool:
    if not isinstance(finding, dict) or finding.get("skill_applied") != EXPIRY_SKILL:
        return False
    if finding.get("severity") not in ESCALATION_SEVERITIES:
        return False
    text = finding_text(finding)
    ticket = record.get("ticket_id")
    return isinstance(ticket, str) and bool(re.search(rf"(?<![\w-]){re.escape(ticket)}(?![\w-])", text))


def check_document(doc: object, path: str, today: date, honour_as_of: bool = False) -> list[Issue]:
    """Validate one parsed quarantine document (registry file, report, or recommendation set)."""
    if not isinstance(doc, dict):
        return [Issue("QUAR_SHAPE", path, "document must be a JSON object with `quarantines` and/or `findings`")]
    issues: list[Issue] = []
    as_of = today
    if honour_as_of and "as_of" in doc:
        parsed = parse_date(doc["as_of"])
        if parsed is None:
            issues.append(Issue("QUAR_DATE", path, "as_of is not an ISO date (YYYY-MM-DD)"))
        else:
            as_of = parsed

    records = doc.get("quarantines", [])
    findings = doc.get("findings", [])
    if not isinstance(records, list):
        return issues + [Issue("QUAR_SHAPE", path, "`quarantines` must be a list")]
    if not isinstance(findings, list):
        return issues + [Issue("QUAR_SHAPE", path, "`findings` must be a list")]

    entries: list[tuple[str, object]] = [(f"{path}:quarantines[{i}]", r) for i, r in enumerate(records)]
    for i, finding in enumerate(findings):
        if isinstance(finding, dict) and finding.get("skill_applied") == QUARANTINE_SKILL:
            where = f"{path}:findings[{i}]"
            if "quarantine" not in finding:
                issues.append(Issue("QUAR_MISSING", where, "quarantine recommendation needs a `quarantine` object"))
            else:
                entries.append((f"{where}.quarantine", finding["quarantine"]))

    seen: dict[str, str] = {}
    for where, record in entries:
        found, end = check_record(record, where, as_of)
        issues += found
        if not isinstance(record, dict):
            continue
        test_id = record.get("test_id")
        if isinstance(test_id, str) and test_id.strip():
            if test_id in seen:
                issues.append(Issue("QUAR_DUPLICATE", where, f"test_id {test_id!r} already quarantined at {seen[test_id]}"))
            seen[test_id] = where
        if end is not None and end < as_of and not any(is_escalation(f, record) for f in findings):
            issues.append(
                Issue(
                    "QUAR_EXPIRED",
                    where,
                    f"end_date {end} has passed with no `{EXPIRY_SKILL}` finding (severity high|medium) "
                    f"naming ticket {record.get('ticket_id')!r}",
                )
            )
    return issues


def load_documents(path: Path) -> tuple[list[object], list[Issue]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        try:
            return [json.loads(text)], []
        except json.JSONDecodeError as exc:
            return [], [Issue("QUAR_JSON", path.as_posix(), f"invalid JSON: {exc}")]
    docs: list[object] = []
    issues: list[Issue] = []
    for index, match in enumerate(FENCE_RE.finditer(text), 1):
        try:
            docs.append(json.loads(match.group(1)))
        except json.JSONDecodeError as exc:
            issues.append(Issue("QUAR_JSON", f"{path.as_posix()}#json-block-{index}", f"invalid JSON: {exc}"))
    return docs, issues


def check_file(path: Path, today: date, honour_as_of: bool = False, label: str | None = None) -> list[Issue]:
    docs, issues = load_documents(path)
    name = label or path.as_posix()
    for doc in docs:
        issues += check_document(doc, name, today, honour_as_of)
    return issues


def check_registry(root: Path, today: date) -> list[Issue]:
    registry = root / ".qualityai" / "quarantine"
    issues: list[Issue] = []
    if not registry.is_dir():
        return issues
    for path in sorted(p for p in registry.rglob("*") if p.suffix in {".json", ".md"} and p.is_file()):
        issues += check_file(path, today, label=path.relative_to(root).as_posix())
    return issues


def check_examples(root: Path, today: date) -> list[Issue]:
    examples = root / ".qualityai" / "skills" / "flaky-quarantine" / "examples"
    issues: list[Issue] = []
    if not examples.is_dir():
        return issues
    for path in sorted(examples.glob("good-*.json")):
        label = path.relative_to(root).as_posix()
        issues += check_file(path, today, honour_as_of=True, label=label)
    for path in sorted(examples.glob("bad-*.json")):
        label = path.relative_to(root).as_posix()
        if not check_file(path, today, honour_as_of=True, label=label):
            issues.append(Issue("QUAR_EXAMPLE", label, "bad example passes validation; it must be rejected"))
    return issues


def source_files(directory: Path):
    for path in sorted(directory.rglob("*")):
        if path.suffix in SOURCE_SUFFIXES and path.is_file():
            if not SKIP_DIRS & set(path.relative_to(directory).parts[:-1]):
                yield path


def in_string(line: str, index: int) -> bool:
    """True when `index` sits inside an open string literal (odd quote count before it)."""
    before = line[:index]
    return before.count('"') % 2 == 1 or before.count("'") % 2 == 1


def check_source_text(text: str, name: str) -> list[Issue]:
    """Flag mute annotations whose line or preceding comment lacks a ticket id."""
    issues: list[Issue] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        if COMMENT_RE.match(line) or not any(not in_string(line, m.start()) for m in MUTE_RE.finditer(line)):
            continue
        previous = ""
        for back in range(number - 2, -1, -1):
            if lines[back].strip():
                previous = lines[back] if COMMENT_RE.match(lines[back]) else ""
                break
        if not TICKET_IN_TEXT_RE.search(line) and not TICKET_IN_TEXT_RE.search(previous):
            issues.append(
                Issue("QUAR_MUTE", f"{name}:{number}", f"muted test without ticket id: {line.strip()[:80]!r}")
            )
    return issues


def check_sources(directories: list[Path], root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for directory in directories:
        for path in source_files(directory):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            try:
                name = path.relative_to(root).as_posix()
            except ValueError:
                name = path.as_posix()
            issues += check_source_text(text, name)
    return issues


def validate_root(root: Path, sources: list[Path] | None, today: date) -> list[Issue]:
    issues = check_registry(root, today) + check_examples(root, today)
    issues += check_sources(sources if sources else [root], root)
    return issues


def _good_record(**overrides: object) -> dict:
    record = {
        "test_id": "CheckoutIT#shouldConfirmBooking",
        "owner": "@squad-payments",
        "end_date": "2026-12-15",
        "ticket_id": "QA-1234",
        "reason": "Fails 4 of 20 CI runs without product change; waits on animation",
        "exit_criteria": "10 consecutive green CI runs after explicit wait",
    }
    record.update(overrides)
    return record


def _escalation(ticket: str = "QA-1234", **overrides: object) -> dict:
    finding = {
        "finding": f"Quarantine {ticket} expired without fix",
        "evidence": {"file": None, "note": f"end_date passed for {ticket}"},
        "severity": "high",
        "confidence": 0.9,
        "rationale": "Expired quarantine hides a test from CI indefinitely",
        "recommendation": "Fix, extend with a new PR, or delete the test",
        "skill_applied": EXPIRY_SKILL,
        "agent": "qa.lead",
    }
    finding.update(overrides)
    return finding


def _self_check() -> int:
    failures: list[str] = []
    today = date(2026, 11, 26)

    def codes(doc: object, **kwargs: object) -> set[str]:
        return {i.code for i in check_document(doc, "t", today, **kwargs)}

    def expect(label: str, got: set[str], want: set[str]) -> None:
        if got != want:
            failures.append(f"{label}: expected {sorted(want)}, got {sorted(got)}")

    expect("good record", codes({"quarantines": [_good_record()]}), set())
    for field in REQUIRED_FIELDS:
        record = _good_record()
        del record[field]
        expect(f"missing {field}", codes({"quarantines": [record]}), {"QUAR_MISSING"})
    for field in ("owner", "ticket_id", "reason", "exit_criteria", "end_date"):
        expect(f"empty {field}", codes({"quarantines": [_good_record(**{field: " "})]}), {"QUAR_EMPTY"})
        expect(f"TBD {field}", codes({"quarantines": [_good_record(**{field: "TBD"})]}), {"QUAR_EMPTY"})
    expect("bad date", codes({"quarantines": [_good_record(end_date="15/12/2026")]}), {"QUAR_DATE"})
    expect("impossible date", codes({"quarantines": [_good_record(end_date="2026-02-30")]}), {"QUAR_DATE"})
    expect("far date", codes({"quarantines": [_good_record(end_date="2027-06-01")]}), {"QUAR_DATE_FAR"})
    expect("bad ticket", codes({"quarantines": [_good_record(ticket_id="soon")]}), {"QUAR_TICKET"})
    for ticket in ("#42", "acme/shop#42", "https://tracker.example/QA-1"):
        expect(f"ticket {ticket}", codes({"quarantines": [_good_record(ticket_id=ticket)]}), set())
    expect("short reason", codes({"quarantines": [_good_record(reason="flaky")]}), {"QUAR_SHORT"})
    expect("unknown field", codes({"quarantines": [_good_record(severity="high")]}), {"QUAR_UNKNOWN"})
    expect("bad mechanism", codes({"quarantines": [_good_record(mechanism="delete")]}), {"QUAR_MECHANISM"})
    expect("good mechanism", codes({"quarantines": [_good_record(mechanism="tag")]}), set())
    expect("start after end", codes({"quarantines": [_good_record(start_date="2026-12-20")]}), {"QUAR_DATE"})
    expect("not an object", codes({"quarantines": ["CheckoutIT"]}), {"QUAR_SHAPE"})
    expect("document shape", codes([1]), {"QUAR_SHAPE"})
    expect("duplicate test", codes({"quarantines": [_good_record(), _good_record()]}), {"QUAR_DUPLICATE"})

    expired = _good_record(end_date="2026-11-01")
    expect("expired, no escalation", codes({"quarantines": [expired]}), {"QUAR_EXPIRED"})
    expect("expired, escalated", codes({"quarantines": [expired], "findings": [_escalation()]}), set())
    expect("ends today is not expired", codes({"quarantines": [_good_record(end_date="2026-11-26")]}), set())
    expect(
        "escalation for other ticket",
        codes({"quarantines": [expired], "findings": [_escalation("QA-9")]}),
        {"QUAR_EXPIRED"},
    )
    expect(
        "escalation too weak",
        codes({"quarantines": [expired], "findings": [_escalation(severity="low")]}),
        {"QUAR_EXPIRED"},
    )
    expect(
        "escalation wrong skill",
        codes({"quarantines": [expired], "findings": [_escalation(skill_applied="failure-triage#recommend")]}),
        {"QUAR_EXPIRED"},
    )

    recommendation = {
        "finding": "Quarantine CheckoutIT#shouldConfirmBooking",
        "skill_applied": QUARANTINE_SKILL,
        "quarantine": _good_record(),
    }
    expect("good recommendation", codes({"findings": [recommendation]}), set())
    expect("recommendation without metadata", codes({"findings": [{**recommendation, "quarantine": {}}]}), {"QUAR_MISSING"})
    bare = {k: v for k, v in recommendation.items() if k != "quarantine"}
    expect("recommendation without object", codes({"findings": [bare]}), {"QUAR_MISSING"})
    detect = {"finding": "Candidate flaky", "skill_applied": "flaky-quarantine#detect"}
    expect("detect finding needs no metadata", codes({"findings": [detect]}), set())
    expect("quarantines not a list", codes({"quarantines": {}}), {"QUAR_SHAPE"})

    as_of_doc = {"as_of": "2026-12-20", "quarantines": [_good_record()]}
    expect("as_of ignored by default", codes(as_of_doc), set())
    expect("as_of honoured for examples", codes(as_of_doc, honour_as_of=True), {"QUAR_EXPIRED"})

    ticketed = '@Disabled("QA-1234 flaky, see ticket")\n@Test void a() {}\n'
    expect("ticketed @Disabled", {i.code for i in check_source_text(ticketed, "A.java")}, set())
    commented = "// QA-1234: flaky until 2026-12-15\n@Disabled\n@Test void a() {}\n"
    expect("commented @Disabled", {i.code for i in check_source_text(commented, "A.java")}, set())
    for label, snippet in {
        "bare @Disabled": "@Disabled\n@Test void a() {}\n",
        "reason without ticket": '@Disabled("flaky")\n',
        "stale comment gap": "// QA-1234\nint x = 1;\n@Disabled\n",
        "@Ignore": "@Ignore\n",
        "testng": "@Test(enabled = false)\n",
        "pytest skip": "@pytest.mark.skip\ndef test_a(): ...\n",
        "unittest skip": '@unittest.skip("flaky")\n',
        "jest skip": "it.skip('works', () => {})\n",
        "quarantine tag": '@Tag("quarantine")\n',
    }.items():
        expect(label, {i.code for i in check_source_text(snippet, "A")}, {"QUAR_MUTE"})
    expect("conditional skipif is allowed", {i.code for i in check_source_text("@pytest.mark.skipif(win)\n", "A")}, set())
    expect("mute inside string literal", {i.code for i in check_source_text('x = "@Disabled and it.skip(a)"\n', "A")}, set())
    expect("comment mention ignored", {i.code for i in check_source_text("// do not use @Disabled\n", "A")}, set())

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        reg = root / ".qualityai" / "quarantine"
        reg.mkdir(parents=True)
        (reg / "ok.json").write_text(json.dumps({"quarantines": [_good_record()]}), encoding="utf-8")
        (reg / "broken.json").write_text("{", encoding="utf-8")
        (reg / "notes.md").write_text(
            "```json\n" + json.dumps({"quarantines": [{"test_id": "X#y"}]}) + "\n```\n", encoding="utf-8"
        )
        (root / "src").mkdir()
        (root / "src" / "A.java").write_text("@Disabled\n", encoding="utf-8")
        (root / "node_modules").mkdir()
        (root / "node_modules" / "B.js").write_text("it.skip('x')\n", encoding="utf-8")
        found = {i.code for i in validate_root(root, None, today)}
        expect("root walk", found, {"QUAR_JSON", "QUAR_MISSING", "QUAR_MUTE"})
        skills = root / ".qualityai" / "skills" / "flaky-quarantine" / "examples"
        skills.mkdir(parents=True)
        (skills / "bad-pass.json").write_text(json.dumps({"quarantines": [_good_record()]}), encoding="utf-8")
        found = {i.code for i in check_examples(root, today)}
        expect("bad example that passes", found, {"QUAR_EXAMPLE"})

    schema_path = Path(__file__).resolve().parents[1] / "references" / "quarantine.schema.json"
    if schema_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        expect("schema required", set(schema["required"]), set(REQUIRED_FIELDS))
        expect("schema properties", set(schema["properties"]), set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS))
        expect("schema mechanisms", set(schema["properties"]["mechanism"]["enum"]), MECHANISMS)
        expect("schema ticket pattern", {schema["properties"]["ticket_id"]["pattern"]}, {TICKET_RE.pattern})

    if failures:
        print("self-check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("self-check ok")
    return 0


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".qualityai").is_dir():
            return candidate
    return start


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", type=Path, help="validate these JSON/Markdown files only")
    parser.add_argument("--root", type=Path, help="host repo root (default: nearest parent holding .qualityai)")
    parser.add_argument("--source", action="append", type=Path, default=[], help="test source dir to scan (repeatable)")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD) for expiry checks")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        return _self_check()
    today = date.today()
    if args.today:
        parsed = parse_date(args.today)
        if parsed is None:
            parser.error("--today must be YYYY-MM-DD")
        today = parsed
    if args.files:
        issues = [i for path in args.files for i in check_file(path, today)]
    else:
        root = (args.root or find_repo_root(Path.cwd())).resolve()
        issues = validate_root(root, [s.resolve() for s in args.source], today)
    for issue in issues:
        print(issue)
    print(f"{len(issues)} issue(s)" if issues else "OK")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
