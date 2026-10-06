# Architecture Patterns: Refactor Playbook

<!--
skill_id: architecture-patterns
phase: refactor
version: "1.0.0"
-->

## Purpose

Propose structural improvements without rewriting the product.

## When to Use

- After review findings

## When NOT to Use

- Do not apply refactors during read-only review unless user asks

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

- High-risk smells first

### Step 2: Plan steps

- Incremental, testable moves

### Step 3: Guardrails

- Keep behavior; point to testing-patterns for coverage

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
- Findings with `skill_applied`: `architecture-patterns#refactor`
- Short summary for the orchestrator

## Examples

- `../../examples/monolithic-good.md` — Clear modular monolith boundaries
- `../../examples/monolithic-bad.md` — Boundary leakage

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
