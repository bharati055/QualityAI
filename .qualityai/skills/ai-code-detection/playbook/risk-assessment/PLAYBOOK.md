# Ai Code Detection: Risk Assessment Playbook

<!--
skill_id: ai-code-detection
phase: risk-assessment
version: "1.0.0"
-->

## Purpose

Translate review-depth into risk focus areas for other specialists.

## When to Use

- After detect

## When NOT to Use

- Do not replace security-patterns or testing-patterns

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

### Step 1: Map depth to checks

- Which gates/skills must be thorough

### Step 2: Call out blind spots

- Likely missing validation, tests, error paths

### Step 3: Set expectations

- What 'done' means for elevated review

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
- Findings with `skill_applied`: `ai-code-detection#risk-assessment`
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
