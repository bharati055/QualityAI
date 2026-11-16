---
name: api-testing
description: Design and review API tests for behavior, contracts, errors, and auth.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['api', 'http', 'rest']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Design and review API tests for behavior, contracts, errors, and auth.**

## What This Skill Covers

- Request/response assertions
- Error and auth cases
- Idempotency and status codes

## What This Skill Does NOT Cover

- UI automation (test-automation)
- Load testing (performance-validation)

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: api-testing#...`.

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
