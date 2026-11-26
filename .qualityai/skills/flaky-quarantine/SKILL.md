---
name: flaky-quarantine
description: Identify flaky tests and recommend quarantine with owner, end date, ticket ID, and exit criteria.
version: "1.0.0"
created: 2026-11-16
authors: [qa-lead]
tags: ['flaky', 'quarantine', 'suite-trust']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when the concern matches: **Identify flaky tests and recommend quarantine with owner, end date, ticket ID, and exit criteria.**

## What This Skill Covers

- Flake signals (thresholds in `.qualityai/context/suite-trust.md`)
- Quarantine metadata: owner, end date, ticket ID, reason, exit criteria
- Expiry escalation

## What This Skill Does NOT Cover

- Permanent mute without ticket
- Pushing quarantine to main without PR
- Creating or syncing tickets (Phase 2 adapter; a human files the ticket in v1)

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose a phase playbook under `playbook/`.
3. Emit findings with `skill_applied: flaky-quarantine#...`.

## Playbooks

- `playbook/detect/PLAYBOOK.md`
- `playbook/quarantine/PLAYBOOK.md`
- `playbook/expiry-review/PLAYBOOK.md`

## Examples

- `examples/good-pattern.md`
- `examples/bad-pattern.md`
- `examples/good-quarantine-record.json`
- `examples/bad-quarantine-record.json`

## Tooling

```bash
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --root .
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --self-check
```

Rejects incomplete quarantine records, mutes without a ticket id, and expired records with no `flaky-quarantine#expiry-review` finding. `scripts/validate_pack.py` runs it, so pack-integrity CI fails on those. It does not call a tracker.

## References

- `references/quarantine-metadata.md` (format, rules, issue codes)
- `references/quarantine.schema.json`
- `references/notes.md`

## How Agents Use This Skill

Used by `qa.engineer`, `qa.lead`, and/or `qa.architect` per role scope. Do not copy methodology into agent files.
