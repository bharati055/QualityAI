---
name: ai-code-detection
description: Review-depth rubric for likely AI-assisted or high-volume generated changes — not authorship detection.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['ai-assisted', 'review-depth', 'risk']
domain: quality
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Review-depth rubric for likely AI-assisted or high-volume generated changes — not authorship detection.**

## What This Skill Covers

- Signals that warrant deeper review (size, generic structure, missing edge cases)
- Risk/review-depth assessment
- Strategy for stricter review without authorship claims

## What This Skill Does NOT Cover

- Claiming Copilot vs Claude vs human authorship as fact
- Blocking merges solely on 'looks AI-generated'
- Plagiarism detection products

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: ai-code-detection#...`.

## Playbooks

- `playbook/detect/PLAYBOOK.md` — Decide whether elevated review depth is warranted. Never assert which model wrote the code.
- `playbook/risk-assessment/PLAYBOOK.md` — Translate review-depth into risk focus areas for other specialists.
- `playbook/review-strategy/PLAYBOOK.md` — Provide a concrete stricter review plan for the orchestrator.

## Examples

- `examples/high-volume-generic-diff.md` — Signals for elevated depth
- `examples/missing-edge-cases.md` — Generated-looking happy-path-only change
- `examples/mixed-generated-human.md` — Mixed change; still no authorship claim
- `examples/well-reviewed-assisted-change.md` — Elevated depth completed well

## Tooling

Optional. Not required for v1.

## References

- `references/review-depth-rubric.md` — normal / elevated / high criteria
- `references/high-volume-change-signals.md` — Signal catalog
- `references/false-positive-mitigation.md` — Avoid authorship claims

## How Agents Use This Skill

Primary agent: `qa.ai-detector`.

Delegate here; do not copy this methodology into the agent file.
