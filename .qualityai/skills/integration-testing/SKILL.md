---
name: integration-testing
description: Design and review integration tests across components/services.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['integration', 'services']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Design and review integration tests across components/services.**

## What This Skill Covers

- Multi-component flows
- Real or test-double boundaries
- Data/setup teardown

## What This Skill Does NOT Cover

- Pure unit isolation
- Full prod SOAK

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: integration-testing#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md`
- `playbook/review/PLAYBOOK.md`
- `playbook/gap-analysis/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
