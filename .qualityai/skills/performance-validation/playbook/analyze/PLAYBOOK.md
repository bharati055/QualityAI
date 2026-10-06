# Performance Validation: Analyze Playbook

<!--
skill_id: performance-validation
phase: analyze
version: "1.0.0"
-->

## Purpose

Interpret results against requirements and risk.

## When to Use

- Results available

## When NOT to Use

- Do not overfit noise

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

### Step 1: Compare to baseline/reqs

- Regression?

### Step 2: Hypothesize bottlenecks

- Code evidence

### Step 3: Recommend

- Fix, accept, or gather more data

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
- Findings with `skill_applied`: `performance-validation#analyze`
- Short summary for the orchestrator

## Examples

- `../../examples/good-performance.md` — Bounded work on hot path
- `../../examples/performance-regression.md` — N+1 / unbounded pattern

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
