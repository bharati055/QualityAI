# Testing Patterns: Review Playbook

<!--
skill_id: testing-patterns
phase: review
version: "1.0.0"
-->

## Purpose

Review existing tests for quality beyond coverage percentage.

## When to Use

- PR adds/changes tests or claims coverage

## When NOT to Use

- Do not equate line coverage with quality

## Inputs

| Input | Required | Description |
|---|---|---|
| Change / diff | yes | Files or PR under review |
| Requirement text | no | AC or ticket text when relevant |
| Prior findings | no | From other agents |

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

### Step 1: Map tests to AC/risk

- Missing failure paths?

### Step 2: Inspect assertions

- Vacuous or brittle asserts

### Step 3: Flag skips

- skipped/xfailed without justification

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No material issues for this phase |
| warn | Gaps exist but not critical-path blockers |
| fail | Critical-path gaps with evidence |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Phase recommendation: pass | warn | fail
- Findings list (may be empty)
- Findings with `skill_applied`: `testing-patterns#review`
- Short summary for the orchestrator

## Examples

- `../../examples/good-test-example.md` — Strong happy + failure coverage
- `../../examples/bad-test-example.md` — Brittle / hollow assertions

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
