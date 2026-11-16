---
name: contract-testing
description: Design and review consumer/provider contract tests.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['contract', 'pact', 'compatibility']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Design and review consumer/provider contract tests.**

## What This Skill Covers

- Consumer expectations
- Provider verification
- Breaking change detection

## What This Skill Does NOT Cover

- Full E2E UX
- Performance SLOs

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: contract-testing#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md`
- `playbook/review/PLAYBOOK.md`
- `playbook/validate/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
