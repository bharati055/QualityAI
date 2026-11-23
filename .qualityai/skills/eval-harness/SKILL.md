---
name: eval-harness
description: Record an incident, revert, or false-positive finding and turn it into a regression case for the agent or skill that missed it.
version: "1.0.0"
created: 2026-11-23
authors: [qa-lead]
tags: ['eval', 'incident', 'false-positive']
domain: quality
languages: [language-agnostic, java, python]
---

## When to Use

Use when a QualityAI run missed something real, or raised a finding that was wrong: **record the incident, revert, or false positive, then store a regression case** (input, bad outcome, expected finding) for the agent or skill that missed it.

The place to store both files is `.qualityai/evals/`. Entry workflow: `.qualityai/instructions/WORKFLOWS.md` §6.

## What This Skill Covers

- A record whose kind is `incident`, `revert`, or `false_positive`
- Naming the agent (`qa.engineer`, `qa.lead`, `qa.architect`, or another `qa.*` role) or the skill that missed it
- A regression case with **input**, **bad outcome**, and **expected finding**
- Checking that the case points at that same agent or skill and at the record

## What This Skill Does NOT Cover

- Running the case against a model, or CI eval gates
- LLM-as-judge scoring
- Risk-tiered autonomy
- Opening a Jira issue or a GitHub comment (paste an id as text if a human already has one)
- Quarantine metadata enforcement (`flaky-quarantine` records the quarantine; this skill records the miss)
- Re-doing the original review (`spec-based-testing`, `testing-patterns`, and the rest stay the methodology)

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file and `.qualityai/evals/README.md`.
2. Run `playbook/record`, then `playbook/case`, then `playbook/check`.
3. Write files under `.qualityai/evals/records/` and `.qualityai/evals/cases/` via a PR. Do not push to `main`.
4. Check the tree:

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
```

## Playbooks

- `playbook/record/PLAYBOOK.md` — Write the incident, revert, or false-positive record.
- `playbook/case/PLAYBOOK.md` — Turn that record into the regression case.
- `playbook/check/PLAYBOOK.md` — Confirm the pair is complete and aimed at the miss.

## Examples

- `examples/good-pattern.md` — How the shipped refund incident becomes a case
- `examples/bad-pattern.md` — "The agent missed a bug" with no input and no target
- Shipped pairs under `.qualityai/evals/` (marked `example: true`)

## Tooling

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --self-check
```

Standard library only. The script checks records and cases. It does not execute them.

## References

- `references/case-format.md` — Record and case fields
- `.qualityai/templates/eval/RECORD-TEMPLATE.md`
- `.qualityai/templates/eval/CASE-TEMPLATE.md`

## How Agents Use This Skill

The role that owned the miss drafts the record and the case. `qa.lead` keeps `.qualityai/evals/` reviewable. The orchestrator routes the workflow and does not close a miss that has no case. Do not copy this methodology into the agent file.
