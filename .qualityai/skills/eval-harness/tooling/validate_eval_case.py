#!/usr/bin/env python3
"""Validate eval-harness records and regression cases.

Checks markdown files under .qualityai/evals/ against references/case-format.md.
Does not execute a case, call a model, or open a tracker.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

KINDS = {"incident", "revert", "false_positive"}
TARGET_TYPES = {"agent", "skill"}
SEVERITIES = {"high", "medium", "low"}
STATUSES = {"open", "retired"}

RECORD_FIELDS = {"id", "kind", "missed_by_type", "missed_by_id", "date", "example"}
RECORD_REQUIRED = {"id", "kind", "missed_by_type", "missed_by_id", "date"}
CASE_FIELDS = {"id", "kind", "target_type", "target_id", "record_id", "status", "example"}
CASE_REQUIRED = {"id", "kind", "target_type", "target_id", "record_id", "status"}

RECORD_SECTIONS = {"what happened", "evidence"}
CASE_SECTIONS = {"input", "bad outcome", "expected finding"}
OPTIONAL_SECTIONS = {"notes"}

MISS_FINDING_KEYS = {"finding", "severity", "skill_applied", "agent", "confidence", "rationale"}
FALSE_POSITIVE_KEYS = MISS_FINDING_KEYS | {"expected", "rejected_finding"}

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AGENT_ID = re.compile(r"^qa\.[a-z0-9]+(?:[.-][a-z0-9]+)*$")
SKILL_APPLIED = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*#[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|AKIA[0-9A-Z]{16}"
    r"|(?i:(?:api[_-]?key|password)\s*[:=]\s*\S+)"
)

FRONTMATTER = re.compile(r"<!--(.*?)-->", re.DOTALL)
JSON_FENCE = re.compile(r"```json\s*(.*?)```", re.DOTALL)


def _frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    match = FRONTMATTER.search(text)
    if not match:
        return {}, ["missing frontmatter comment"]
    fields: dict[str, str] = {}
    errors: list[str] = []
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if not line:
            continue
        if ":" not in line:
            errors.append(f"frontmatter line is not key: value ({line})")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in fields:
            errors.append(f"duplicate frontmatter key {key}")
        fields[key] = value
    return fields, errors


def _sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    found: dict[str, str] = {}
    for part in parts[1:]:
        lines = part.splitlines()
        title = lines[0].strip().lower()
        found[title] = "\n".join(lines[1:]).strip()
    return found


def _target_id_ok(target_type: str, target_id: str) -> bool:
    if target_type == "agent":
        return AGENT_ID.match(target_id) is not None
    if target_type == "skill":
        return SLUG.match(target_id) is not None
    return False


def _check_common(fields: dict[str, str], allowed: set[str], required: set[str]) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(fields) - allowed)
    if unknown:
        errors.append(f"unknown frontmatter fields: {', '.join(unknown)}")
    missing = sorted(required - set(fields))
    if missing:
        errors.append(f"missing frontmatter fields: {', '.join(missing)}")
    kind = fields.get("kind")
    if kind is not None and kind not in KINDS:
        errors.append("kind must be incident, revert, or false_positive")
    if "example" in fields and fields["example"] not in {"true", "false"}:
        errors.append("example must be true or false")
    return errors


def _check_sections(sections: dict[str, str], required: set[str]) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(sections) - required - OPTIONAL_SECTIONS)
    if unknown:
        errors.append(f"unknown sections: {', '.join(unknown)}")
    for title in sorted(required):
        body = sections.get(title, "")
        if len(body) < 40:
            errors.append(f"section '{title}' is missing or too short")
    return errors


def _secrets(text: str) -> list[str]:
    if SECRET.search(text):
        return ["file looks like it contains a secret; remove it"]
    return []


def validate_record(text: str, stem: str) -> tuple[dict[str, str], list[str]]:
    fields, errors = _frontmatter(text)
    errors.extend(_check_common(fields, RECORD_FIELDS, RECORD_REQUIRED))
    errors.extend(_secrets(text))
    record_id = fields.get("id", "")
    if record_id and (not record_id.startswith("rec-") or SLUG.match(record_id[4:]) is None):
        errors.append("id must look like rec-<slug>")
    if record_id and stem and record_id != stem:
        errors.append(f"id {record_id} does not match filename {stem}")
    missed_type = fields.get("missed_by_type")
    if missed_type is not None and missed_type not in TARGET_TYPES:
        errors.append("missed_by_type must be agent or skill")
    missed_id = fields.get("missed_by_id", "")
    if missed_type in TARGET_TYPES and missed_id and not _target_id_ok(missed_type, missed_id):
        errors.append("missed_by_id does not match missed_by_type")
    date = fields.get("date")
    if date is not None:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            errors.append("date must be YYYY-MM-DD")
    errors.extend(_check_sections(_sections(text), RECORD_SECTIONS))
    return fields, errors


def _finding_errors(kind: str, body: str) -> list[str]:
    fences = JSON_FENCE.findall(body)
    if len(fences) != 1:
        return ["expected finding must contain one ```json object"]
    try:
        data = json.loads(fences[0])
    except json.JSONDecodeError as exc:
        return [f"expected finding JSON is invalid ({exc})"]
    if not isinstance(data, dict):
        return ["expected finding JSON must be an object"]

    allowed = FALSE_POSITIVE_KEYS if kind == "false_positive" else MISS_FINDING_KEYS
    errors: list[str] = []
    unknown = sorted(set(data) - allowed)
    if unknown:
        errors.append(f"expected finding has unknown fields: {', '.join(unknown)}")

    severity = data.get("severity")
    if severity not in SEVERITIES:
        errors.append("expected finding severity must be high, medium, or low")

    has_skill = "skill_applied" in data
    has_agent = "agent" in data
    if not has_skill and not has_agent:
        errors.append("expected finding needs skill_applied or agent")
    if has_skill and (not isinstance(data["skill_applied"], str) or SKILL_APPLIED.match(data["skill_applied"]) is None):
        errors.append("skill_applied must look like skill-id#section")
    if has_agent and (not isinstance(data["agent"], str) or AGENT_ID.match(data["agent"]) is None):
        errors.append("agent must look like qa.<role>")

    if "confidence" in data:
        confidence = data["confidence"]
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append("confidence must be a number from 0 to 1")
    if "rationale" in data and (not isinstance(data["rationale"], str) or not data["rationale"].strip()):
        errors.append("rationale must be a non-empty string")

    if kind == "false_positive":
        if data.get("finding") is not None:
            errors.append("false_positive finding must be null")
        if data.get("expected") != "no_finding":
            errors.append('false_positive expected must be "no_finding"')
        rejected = data.get("rejected_finding")
        if not isinstance(rejected, str) or not rejected.strip():
            errors.append("false_positive needs a non-empty rejected_finding")
    else:
        finding = data.get("finding")
        if not isinstance(finding, str) or not finding.strip():
            errors.append("incident and revert findings must be a non-empty string")
        if "expected" in data or "rejected_finding" in data:
            errors.append("incident and revert findings do not use expected or rejected_finding")
    return errors


def validate_case(text: str, stem: str) -> tuple[dict[str, str], list[str]]:
    fields, errors = _frontmatter(text)
    errors.extend(_check_common(fields, CASE_FIELDS, CASE_REQUIRED))
    errors.extend(_secrets(text))
    case_id = fields.get("id", "")
    if case_id and (not case_id.startswith("eval-") or SLUG.match(case_id[5:]) is None):
        errors.append("id must look like eval-<slug>")
    if case_id and stem and case_id != stem:
        errors.append(f"id {case_id} does not match filename {stem}")
    target_type = fields.get("target_type")
    if target_type is not None and target_type not in TARGET_TYPES:
        errors.append("target_type must be agent or skill")
    target_id = fields.get("target_id", "")
    if target_type in TARGET_TYPES and target_id and not _target_id_ok(target_type, target_id):
        errors.append("target_id does not match target_type")
    record_id = fields.get("record_id", "")
    if record_id and (not record_id.startswith("rec-") or SLUG.match(record_id[4:]) is None):
        errors.append("record_id must look like rec-<slug>")
    status = fields.get("status")
    if status is not None and status not in STATUSES:
        errors.append("status must be open or retired")
    sections = _sections(text)
    errors.extend(_check_sections(sections, CASE_SECTIONS))
    kind = fields.get("kind")
    if kind in KINDS and "expected finding" in sections and len(sections["expected finding"]) >= 40:
        errors.extend(_finding_errors(kind, sections["expected finding"]))
    return fields, errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    records_dir = root / "records"
    cases_dir = root / "cases"
    if not records_dir.is_dir() or not cases_dir.is_dir():
        return [f"{root} must contain records/ and cases/"]

    records: dict[str, dict[str, str]] = {}
    for path in sorted(records_dir.glob("*.md")):
        fields, file_errors = validate_record(path.read_text(encoding="utf-8"), path.stem)
        for item in file_errors:
            errors.append(f"{path}: {item}")
        record_id = fields.get("id")
        if record_id:
            if record_id in records:
                errors.append(f"{path}: duplicate record id {record_id}")
            records[record_id] = fields

    case_targets: dict[str, int] = {record_id: 0 for record_id in records}
    for path in sorted(cases_dir.glob("*.md")):
        fields, file_errors = validate_case(path.read_text(encoding="utf-8"), path.stem)
        for item in file_errors:
            errors.append(f"{path}: {item}")
        record_id = fields.get("record_id")
        if not record_id:
            continue
        if record_id not in records:
            errors.append(f"{path}: record_id {record_id} does not match a record")
            continue
        case_targets[record_id] = case_targets.get(record_id, 0) + 1
        record = records[record_id]
        if fields.get("kind") and fields.get("kind") != record.get("kind"):
            errors.append(f"{path}: kind {fields.get('kind')} does not match record {record.get('kind')}")
        if fields.get("target_type") and fields.get("target_type") != record.get("missed_by_type"):
            errors.append(f"{path}: target_type does not match the record")
        if fields.get("target_id") and fields.get("target_id") != record.get("missed_by_id"):
            errors.append(f"{path}: target_id does not match the record")

    for record_id, count in sorted(case_targets.items()):
        if count < 1:
            errors.append(f"record {record_id} has no regression case")
    return errors


def _self_check() -> int:
    root = Path(__file__).resolve().parents[3] / "evals"
    errors = validate_root(root)
    if errors:
        print("self-check: shipped eval tree is invalid:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    sample = (root / "cases" / "eval-refund-double-charge.md").read_text(encoding="utf-8")
    broken_target = sample.replace("target_id: spec-based-testing", "target_id: qa.engineer")
    _, broken_errors = validate_case(broken_target, "eval-refund-double-charge")
    if not any("target_id does not match target_type" in item for item in broken_errors):
        print("self-check: agent id on a skill target should fail", file=sys.stderr)
        return 1

    hollow = (root / "cases" / "eval-hollow-assert-false-positive.md").read_text(encoding="utf-8")
    stripped = hollow.replace('"rejected_finding": "Assertion assertEquals(0, cart.items().size()) is hollow",\n', "")
    _, hollow_errors = validate_case(stripped, "eval-hollow-assert-false-positive")
    if not any("rejected_finding" in item for item in hollow_errors):
        print("self-check: false positive without rejected_finding should fail", file=sys.stderr)
        return 1

    print(f"self-check ok ({root})")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-check"]:
        return _self_check()
    if argv == ["--root"] or len(argv) != 2 or argv[0] != "--root":
        print("usage: validate_eval_case.py --root <evals-dir> | --self-check", file=sys.stderr)
        return 2
    root = Path(argv[1])
    errors = validate_root(root)
    if errors:
        print(f"invalid: {root}", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    record_count = len(list((root / "records").glob("*.md")))
    case_count = len(list((root / "cases").glob("*.md")))
    print(f"ok: {root} ({record_count} records, {case_count} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
