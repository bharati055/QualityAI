# Ai Code Detection: Review Strategy Playbook

<!--
skill_id: ai-code-detection
phase: review-strategy
version: "1.0.0"
-->

## Purpose

Provide a concrete stricter review plan for the orchestrator.

## When to Use

- Elevated or high depth

## When NOT to Use

- Do not run unrelated skills yourself — recommend them

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

### Step 1: Sequence checks

- security, tests, requirements, architecture as needed

### Step 2: Human attention

- What a human must still verify

### Step 3: Exit criteria

- When elevated review can recommend pass/warn/fail

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
- Findings with `skill_applied`: `ai-code-detection#review-strategy`
- Short summary for the orchestrator

## Examples

- `../../examples/high-volume-generic-diff.md` — Signals for elevated depth
- `../../examples/missing-edge-cases.md` — Generated-looking happy-path-only change

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
