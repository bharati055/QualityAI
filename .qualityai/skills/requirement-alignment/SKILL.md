---
name: requirement-alignment
description: Parse requirements, map them to changes, validate alignment, and find gaps.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['requirements', 'traceability', 'acceptance-criteria']
domain: quality
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Parse requirements, map them to changes, validate alignment, and find gaps.**

## What This Skill Covers

- Extracting intent and AC from text
- Mapping code/diff to requirements
- Detecting drift and missing AC
- Flagging untestable or vague requirements

## What This Skill Does NOT Cover

- Jira API sync (later addon)
- Writing product requirements for the business
- Project management / sprint planning

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: requirement-alignment#...`.

## Playbooks

- `playbook/parse/PLAYBOOK.md` — Extract clear intent, acceptance criteria, and constraints from requirement text.
- `playbook/map/PLAYBOOK.md` — Map each acceptance criterion to evidence in the change (or mark unmapped).
- `playbook/validate/PLAYBOOK.md` — Decide whether the change satisfies stated intent with evidence.
- `playbook/gap-analysis/PLAYBOOK.md` — List missing requirements, missing implementation, and missing validation.

## Examples

- `examples/clear-requirement.md` — Well-formed AC and how to parse them
- `examples/vague-requirement.md` — Untestable language and how to flag it
- `examples/well-aligned-code.md` — Change that maps cleanly to AC
- `examples/drifted-code.md` — Implementation that diverges from intent

## Tooling

Optional. Not required for v1.

## References

- `references/acceptance-criteria-format.md` — What good AC look like
- `references/traceability-model.md` — AC ↔ change ↔ tests conceptual model
- `references/jira-integration.md` — Later addon note; v1 uses pasted/in-repo text

## How Agents Use This Skill

Primary agent: `qa.researcher`.

Delegate here; do not copy this methodology into the agent file.
