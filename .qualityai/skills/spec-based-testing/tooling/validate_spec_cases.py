#!/usr/bin/env python3
"""Validate a finished spec-based-testing case set.

The case set is JSON from spec-based-testing#report. This script checks
the contract in references/case-set.md. It does not read a git diff and
it does not call a tracker or forge API.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SOURCES = ("ac", "journey", "failure_mode")
SOURCE_STATES = ("present", "missing", "out_of_scope")
TEST_TYPES = {
    "unit-testing",
    "api-testing",
    "integration-testing",
    "contract-testing",
    "test-automation",
    "soak-testing",
    "performance-validation",
}
TOP_LEVEL = {
    "specs_read_before_diff",
    "compared_to_diff",
    "sources_consulted",
    "source_gaps",
    "skipped",
    "cases",
    "diff_only",
}
CASE_KEYS = {
    "id",
    "source",
    "source_ref",
    "title",
    "expected",
    "mentioned_in_diff",
    "diff_evidence",
    "flags",
    "also_from",
    "suggested_test_type",
}
ID_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def _is_id(value: object) -> bool:
    if not isinstance(value, str) or not value or value[0] == "-" or value[-1] == "-":
        return False
    if "--" in value:
        return False
    return set(value) <= ID_CHARS and any(ch.isalnum() for ch in value)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_case_set(data: object) -> list[str]:
    """Return a list of human-readable errors. Empty means valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["case set must be a JSON object"]

    extra = sorted(set(data) - TOP_LEVEL)
    if extra:
        errors.append(f"unknown top-level fields: {', '.join(extra)}")

    if data.get("specs_read_before_diff") is not True:
        errors.append("specs_read_before_diff must be true (derive finishes before the diff is used)")
    if data.get("compared_to_diff") is not True:
        errors.append("compared_to_diff must be true (this script checks the post-compare set)")

    consulted = data.get("sources_consulted")
    if not isinstance(consulted, dict) or set(consulted) != set(SOURCES):
        errors.append("sources_consulted must be an object with keys ac, journey, failure_mode")
        consulted = {}
    else:
        for key in SOURCES:
            if consulted[key] not in SOURCE_STATES:
                errors.append(f"sources_consulted.{key} must be present, missing, or out_of_scope")
        if not any(consulted.get(key) == "present" for key in SOURCES):
            errors.append("at least one source must be present")

    gaps = data.get("source_gaps")
    gap_sources: set[str] = set()
    if not isinstance(gaps, list):
        errors.append("source_gaps must be an array")
        gaps = []
    else:
        for index, gap in enumerate(gaps):
            label = f"source_gaps[{index}]"
            if not isinstance(gap, dict) or set(gap) != {"source", "note"}:
                errors.append(f"{label} must have only source and note")
                continue
            if gap["source"] not in SOURCES:
                errors.append(f"{label}.source must be ac, journey, or failure_mode")
            elif gap["source"] in gap_sources:
                errors.append(f"{label}.source is duplicated")
            else:
                gap_sources.add(gap["source"])
            if not _nonempty(gap.get("note")):
                errors.append(f"{label}.note must be a non-empty string")

    if isinstance(consulted, dict) and set(consulted) == set(SOURCES):
        for key in SOURCES:
            state = consulted.get(key)
            if state == "missing" and key not in gap_sources:
                errors.append(f"sources_consulted.{key} is missing but source_gaps has no note")
            if state != "missing" and key in gap_sources:
                errors.append(f"source_gaps lists {key}, which is {state}, not missing")

    skipped = data.get("skipped")
    if not isinstance(skipped, list):
        errors.append("skipped must be an array")
    else:
        for index, item in enumerate(skipped):
            label = f"skipped[{index}]"
            if not isinstance(item, dict) or set(item) != {"source", "source_ref", "note"}:
                errors.append(f"{label} must have only source, source_ref, and note")
                continue
            if item["source"] not in SOURCES:
                errors.append(f"{label}.source must be ac, journey, or failure_mode")
            elif isinstance(consulted, dict) and consulted.get(item["source"]) != "present":
                errors.append(f"{label}.source must be a present source")
            if not _nonempty(item.get("source_ref")) or not _nonempty(item.get("note")):
                errors.append(f"{label} needs a non-empty source_ref and note")

    cases = data.get("cases")
    seen_ids: set[str] = set()
    if not isinstance(cases, list):
        errors.append("cases must be an array")
        cases = []
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue
        unknown = sorted(set(case) - CASE_KEYS)
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        if not _is_id(case.get("id")):
            errors.append(f"{label}.id must be a lowercase slug")
        elif case["id"] in seen_ids:
            errors.append(f"{label}.id {case['id']} is duplicated")
        else:
            seen_ids.add(case["id"])
        source = case.get("source")
        if source not in SOURCES:
            errors.append(f"{label}.source must be ac, journey, or failure_mode")
        elif isinstance(consulted, dict) and consulted.get(source) != "present":
            errors.append(f"{label}.source {source} is not a present source")
        if not _nonempty(case.get("source_ref")):
            errors.append(f"{label}.source_ref must be a non-empty string")
        if not _nonempty(case.get("title")) or not _nonempty(case.get("expected")):
            errors.append(f"{label} needs a non-empty title and expected")
        mentioned = case.get("mentioned_in_diff")
        if not isinstance(mentioned, bool):
            errors.append(f"{label}.mentioned_in_diff must be a boolean")
        evidence = case.get("diff_evidence")
        flags = case.get("flags")
        if not isinstance(evidence, str):
            errors.append(f"{label}.diff_evidence must be a string")
        if not isinstance(flags, list) or not all(isinstance(flag, str) for flag in flags or []):
            errors.append(f"{label}.flags must be an array of strings")
        elif mentioned is True:
            if flags != []:
                errors.append(f"{label}.flags must be [] when the diff mentions the case")
            if not evidence or not evidence.strip():
                errors.append(f"{label}.diff_evidence must name the mention")
        elif mentioned is False:
            if flags != ["unmentioned"]:
                errors.append(f"{label}.flags must be [\"unmentioned\"] when the diff never mentions the case")
            if evidence != "":
                errors.append(f"{label}.diff_evidence must be empty when the case is unmentioned")
        also = case.get("also_from")
        if not isinstance(also, list):
            errors.append(f"{label}.also_from must be an array")
        else:
            for extra_index, item in enumerate(also):
                extra_label = f"{label}.also_from[{extra_index}]"
                if not isinstance(item, dict) or set(item) != {"source", "source_ref"}:
                    errors.append(f"{extra_label} must have only source and source_ref")
                    continue
                if item["source"] not in SOURCES:
                    errors.append(f"{extra_label}.source must be ac, journey, or failure_mode")
                elif isinstance(consulted, dict) and consulted.get(item["source"]) != "present":
                    errors.append(f"{extra_label}.source must be present")
                if not _nonempty(item.get("source_ref")):
                    errors.append(f"{extra_label}.source_ref must be non-empty")
                if item.get("source") == source and item.get("source_ref") == case.get("source_ref"):
                    errors.append(f"{extra_label} duplicates the case source")
        if "suggested_test_type" in case and case["suggested_test_type"] not in TEST_TYPES:
            errors.append(f"{label}.suggested_test_type is not a test-type skill id")

    diff_only = data.get("diff_only")
    if not isinstance(diff_only, list):
        errors.append("diff_only must be an array")
    else:
        for index, item in enumerate(diff_only):
            label = f"diff_only[{index}]"
            if not isinstance(item, dict) or set(item) != {"evidence", "note"}:
                errors.append(f"{label} must have only evidence and note")
                continue
            if not _nonempty(item.get("evidence")) or not _nonempty(item.get("note")):
                errors.append(f"{label} needs non-empty evidence and note")

    if isinstance(consulted, dict) and set(consulted) == set(SOURCES) and isinstance(cases, list):
        covered = {key: False for key in SOURCES}
        for case in cases:
            if not isinstance(case, dict):
                continue
            if case.get("source") in covered:
                covered[case["source"]] = True
            for item in case.get("also_from") or []:
                if isinstance(item, dict) and item.get("source") in covered:
                    covered[item["source"]] = True
        if isinstance(skipped, list):
            for item in skipped:
                if isinstance(item, dict) and item.get("source") in covered:
                    covered[item["source"]] = True
        for key in SOURCES:
            if consulted.get(key) == "present" and not covered[key]:
                errors.append(
                    f"sources_consulted.{key} is present but no case, also_from, or skipped row uses it"
                )

    return errors


def _load(path: Path) -> tuple[object | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"file not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"{path}: invalid JSON ({exc})"


def _summary(data: dict) -> str:
    cases = data.get("cases") or []
    unmentioned = 0
    if isinstance(cases, list):
        unmentioned = sum(
            1
            for case in cases
            if isinstance(case, dict) and case.get("flags") == ["unmentioned"]
        )
    diff_only = data.get("diff_only") or []
    diff_count = len(diff_only) if isinstance(diff_only, list) else 0
    return f"ok: {len(cases) if isinstance(cases, list) else 0} cases, {unmentioned} unmentioned, {diff_count} diff_only"


def _self_check() -> int:
    example = Path(__file__).resolve().parents[1] / "examples" / "refund-case-set.json"
    data, error = _load(example)
    if error:
        print(error, file=sys.stderr)
        return 1
    errors = validate_case_set(data)
    if errors:
        print("self-check: shipped example is invalid:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    assert isinstance(data, dict)
    mutants: list[tuple[str, dict]] = []

    closed = json.loads(json.dumps(data))
    closed["specs_read_before_diff"] = False
    mutants.append(("specs_read_before_diff false", closed))

    blank_ref = json.loads(json.dumps(data))
    blank_ref["cases"][0]["source_ref"] = ""
    mutants.append(("empty source_ref", blank_ref))

    bad_flag = json.loads(json.dumps(data))
    bad_flag["cases"][1]["flags"] = []
    mutants.append(("unmentioned case without flag", bad_flag))

    mentioned_flag = json.loads(json.dumps(data))
    mentioned_flag["cases"][0]["flags"] = ["unmentioned"]
    mutants.append(("mentioned case flagged unmentioned", mentioned_flag))

    no_evidence = json.loads(json.dumps(data))
    no_evidence["cases"][0]["diff_evidence"] = ""
    mutants.append(("mentioned case without diff_evidence", no_evidence))

    bad_source = json.loads(json.dumps(data))
    bad_source["cases"][0]["source"] = "code"
    mutants.append(("source code", bad_source))

    all_out = json.loads(json.dumps(data))
    all_out["sources_consulted"] = {key: "out_of_scope" for key in SOURCES}
    all_out["cases"] = []
    mutants.append(("no present source", all_out))

    missing_gap = json.loads(json.dumps(data))
    missing_gap["sources_consulted"]["failure_mode"] = "missing"
    missing_gap["cases"] = [case for case in missing_gap["cases"] if case["source"] != "failure_mode"]
    mutants.append(("missing source without gap note", missing_gap))

    unread = json.loads(json.dumps(data))
    unread["cases"] = [case for case in unread["cases"] if case["source"] == "ac"]
    for case in unread["cases"]:
        case["also_from"] = []
    mutants.append(("present journey with no case or skip", unread))

    failed: list[str] = []
    for name, mutant in mutants:
        if not validate_case_set(mutant):
            failed.append(name)
    if failed:
        print("self-check: expected these mutants to fail:", file=sys.stderr)
        for name in failed:
            print(f"- {name}", file=sys.stderr)
        return 1

    print(f"self-check ok ({example})")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--self-check"]:
        return _self_check()
    if not argv or argv[0].startswith("-"):
        print(
            "usage: validate_spec_cases.py <case-set.json> [more.json ...] | --self-check",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for raw in argv:
        path = Path(raw)
        data, error = _load(path)
        if error:
            print(error, file=sys.stderr)
            exit_code = 1
            continue
        errors = validate_case_set(data)
        if errors:
            print(f"invalid: {path}", file=sys.stderr)
            for item in errors:
                print(f"- {item}", file=sys.stderr)
            exit_code = 1
            continue
        assert isinstance(data, dict)
        print(f"{path}: {_summary(data)}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
