---
name: architecture-patterns
description: Review design fitness, layering, coupling, and architectural drift.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['architecture', 'design', 'coupling']
domain: architecture
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Review design fitness, layering, coupling, and architectural drift.**

## What This Skill Covers

- Boundary and layering checks
- Coupling/cohesion smells
- Anti-pattern detection at design level
- Refactor guidance for structure

## What This Skill Does NOT Cover

- Full system redesign
- Infrastructure-as-code deep review (unless change includes it)
- Micro-optimizations (see performance-validation)

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: architecture-patterns#...`.

## Playbooks

- `playbook/design/PLAYBOOK.md` — Guide design choices for a change before or during implementation.
- `playbook/review/PLAYBOOK.md` — Review the change against expected architecture.
- `playbook/anti-pattern-detection/PLAYBOOK.md` — Identify architectural smells in the change.
- `playbook/refactor/PLAYBOOK.md` — Propose structural improvements without rewriting the product.

## Examples

- `examples/monolithic-good.md` — Clear modular monolith boundaries
- `examples/monolithic-bad.md` — Boundary leakage
- `examples/microservice-good.md` — Sensible service boundaries
- `examples/coupling-anti-pattern.md` — Tight coupling example

## Tooling

Optional. Not required for v1.

## References

- `references/SOLID-principles.md` — SOLID as review lenses
- `references/clean-architecture.md` — Dependency rule
- `references/coupling-cohesion.md` — Coupling/cohesion checks
- `references/domain-driven-design.md` — Bounded context hints

## How Agents Use This Skill

Primary agent: `qa.architect`.

Delegate here; do not copy this methodology into the agent file.
