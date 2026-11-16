---
name: soak-testing
description: Endurance/soak scenario design and review for leaks, degradation, and long-run stability.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['soak', 'endurance', 'reliability']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Endurance/soak scenario design and review for leaks, degradation, and long-run stability.**

## What This Skill Covers

- Duration/success criteria
- Resource leak signals
- When soak is required

## What This Skill Does NOT Cover

- Short spike-only load (see performance-validation)
- Functional AC alone

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: soak-testing#...`.

## Playbooks

- `playbook/plan/PLAYBOOK.md`
- `playbook/execute/PLAYBOOK.md`
- `playbook/analyze/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
