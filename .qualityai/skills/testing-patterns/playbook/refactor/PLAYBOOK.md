# Testing Patterns: Refactor Playbook

<!--
skill_id: testing-patterns
phase: refactor
version: "1.0.0"
-->

## Purpose

Improve weak tests while preserving intent.

## When to Use

- After review findings

## When NOT to Use

- Do not delete coverage without replacement

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

### Step 1: Target brittle tests

- Time, order, hardcoded env

### Step 2: Strengthen asserts

- Behavior outcomes, not implementation trivia

### Step 3: Keep signal

- Prefer fewer strong tests over many weak ones

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
- Findings with `skill_applied`: `testing-patterns#refactor`
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
