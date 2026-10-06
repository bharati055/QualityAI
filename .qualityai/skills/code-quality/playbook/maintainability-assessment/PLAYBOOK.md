# Code Quality: Maintainability Assessment Playbook

<!--
skill_id: code-quality
phase: maintainability-assessment
version: "1.0.0"
-->

## Purpose

Judge whether the change is maintainable enough for the criticality of the path.

## When to Use

- Critical modules or large diffs

## When NOT to Use

- Do not block solely on style

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

### Step 1: Criticality

- Payment/auth/data integrity?

### Step 2: Debt introduced

- What future cost?

### Step 3: Recommendation

- pass/warn/fail with rationale

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
- Findings with `skill_applied`: `code-quality#maintainability-assessment`
- Short summary for the orchestrator

## Examples

- `../../examples/readable-function.md` — Clear structure
- `../../examples/unreadable-function.md` — Dense logic without seams

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
