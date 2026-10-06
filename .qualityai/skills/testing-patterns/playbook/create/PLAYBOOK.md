# Testing Patterns: Create Playbook

<!--
skill_id: testing-patterns
phase: create
version: "1.0.0"
-->

## Purpose

Design a test strategy for a feature or change.

## When to Use

- New feature or major behavior change

## When NOT to Use

- Do not implement production code here

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

### Step 1: Understand behavior

- AC, failure modes, edge cases

### Step 2: Choose layers

- unit vs integration vs e2e — justify

### Step 3: List scenarios

- Happy, error, boundary, null/empty

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
- Findings with `skill_applied`: `testing-patterns#create`
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
