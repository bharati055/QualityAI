---
name: unit-testing
description: Design and review unit tests for fast, meaningful logic coverage.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['unit', 'isolation']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Design and review unit tests for fast, meaningful logic coverage.**

## What This Skill Covers

- Branch/logic coverage with strong asserts
- Mock boundaries
- Failure paths at unit level

## What This Skill Does NOT Cover

- Full service integration
- E2E journeys

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: unit-testing#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md`
- `playbook/review/PLAYBOOK.md`
- `playbook/refactor/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
