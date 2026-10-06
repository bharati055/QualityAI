# Testing Patterns: Plan Playbook

<!--
skill_id: testing-patterns
phase: plan
version: "1.0.0"
-->

## Purpose

Plan execution order, fixtures, and data for tests.

## When to Use

- Strategy exists

## When NOT to Use

- Do not skip risk-based prioritization

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

### Step 1: Prioritize

- Critical path first

### Step 2: Fixtures

- Factories over hardcoded opaque IDs

### Step 3: Definition of done

- Which scenarios must pass before merge recommendation

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
- Findings with `skill_applied`: `testing-patterns#plan`
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
