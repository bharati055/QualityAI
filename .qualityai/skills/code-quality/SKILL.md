---
name: code-quality
description: Review maintainability, clarity, duplication, and change reviewability.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['maintainability', 'readability', 'complexity']
domain: quality
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Review maintainability, clarity, duplication, and change reviewability.**

## What This Skill Covers

- Naming and structure for reviewability
- Complexity and duplication signals
- Comment quality (signal vs noise)
- Maintainability assessment

## What This Skill Does NOT Cover

- Formatter/linter config wars
- Security issues (security-patterns)
- Requirement fit (requirement-alignment)

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: code-quality#...`.

## Playbooks

- `playbook/review/PLAYBOOK.md` — Deep but prioritized code review for maintainability.
- `playbook/refactor/PLAYBOOK.md` — Propose maintainability refactors.
- `playbook/maintainability-assessment/PLAYBOOK.md` — Judge whether the change is maintainable enough for the criticality of the path.

## Examples

- `examples/readable-function.md` — Clear structure
- `examples/unreadable-function.md` — Dense logic without seams
- `examples/complex-logic.md` — Complexity hotspot
- `examples/well-commented-function.md` — Comments that add signal

## Tooling

Optional. Not required for v1.

## References

- `references/naming-conventions.md` — Naming guidance
- `references/cyclomatic-complexity.md` — Complexity as a signal
- `references/function-sizing.md` — Size heuristics
- `references/comment-best-practices.md` — When to comment

## How Agents Use This Skill

Primary agent: `qa.code-reviewer`.

Delegate here; do not copy this methodology into the agent file.
