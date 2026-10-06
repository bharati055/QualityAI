# Architecture Patterns: Design Playbook

<!--
skill_id: architecture-patterns
phase: design
version: "1.0.0"
-->

## Purpose

Guide design choices for a change before or during implementation.

## When to Use

- New feature or structural change

## When NOT to Use

- Do not replace domain product decisions

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

### Step 1: Identify boundaries

- Modules, APIs, data ownership

### Step 2: Choose patterns

- Fit existing architecture; avoid inventing new layers without need

### Step 3: Document risks

- Where design could drift

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
- Findings with `skill_applied`: `architecture-patterns#design`
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
