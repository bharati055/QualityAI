---
name: test-automation
description: UI/E2E automation patterns aligned to host Selenium/Playwright (or equivalent) framework docs.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['e2e', 'ui', 'playwright', 'selenium']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **UI/E2E automation patterns aligned to host Selenium/Playwright (or equivalent) framework docs.**

## What This Skill Covers

- Critical path automation
- Page/screen patterns
- Smoke vs full tagging

## What This Skill Does NOT Cover

- Unit-only logic
- Raw load generation

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: test-automation#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md`
- `playbook/review/PLAYBOOK.md`
- `playbook/refactor/PLAYBOOK.md`
- `playbook/failure-analysis/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
