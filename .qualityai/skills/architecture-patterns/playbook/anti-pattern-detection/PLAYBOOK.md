# Architecture Patterns: Anti Pattern Detection Playbook

<!--
skill_id: architecture-patterns
phase: anti-pattern-detection
version: "1.0.0"
-->

## Purpose

Identify architectural smells in the change.

## When to Use

- Suspected god objects, circular deps, leaky abstractions

## When NOT to Use

- Do not flag every large class without risk rationale

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

### Step 1: Scan for smells

- Tight coupling, circular deps, shared mutable globals

### Step 2: Assess blast radius

- Who depends on this?

### Step 3: Recommend

- Minimal structural fix direction

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
- Findings with `skill_applied`: `architecture-patterns#anti-pattern-detection`
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
