# Performance Validation: Execute Playbook

<!--
skill_id: performance-validation
phase: execute
version: "1.0.0"
-->

## Purpose

Execute or specify how to execute perf checks.

## When to Use

- Plan ready

## When NOT to Use

- v1 may specify Python scripts/scenarios without running infra

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

### Step 1: Run or describe

- Commands/scripts (Python preferred)

### Step 2: Capture results

- Raw metrics + context

### Step 3: Stop conditions

- When to abort

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
- Findings with `skill_applied`: `performance-validation#execute`
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
