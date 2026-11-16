---
name: failure-triage
description: Classify test failures as product defect, test script issue, environment, or unknown — with evidence.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['triage', 'rca', 'stability']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Classify test failures as product defect, test script issue, environment, or unknown — with evidence.**

## What This Skill Covers

- Failure categorization
- Evidence requirements
- Routing to fix owners

## What This Skill Does NOT Cover

- Automatic Jira filing in v1 (Phase 2 adapter)
- Silent deletion of failing tests

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: failure-triage#...`.

## Playbooks

- `playbook/classify/PLAYBOOK.md`
- `playbook/evidence/PLAYBOOK.md`
- `playbook/recommend/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`

## Tooling

Optional; not required for v1.

## References

- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
