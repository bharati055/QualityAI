---
name: spec-based-testing
description: Derive test cases from acceptance criteria, journeys, and FMEA before comparing them to the feature diff.
version: "1.0.0"
created: 2026-11-23
authors: [qa-lead]
tags: ['independence', 'acceptance-criteria', 'journeys', 'fmea']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use when QA should suggest or judge tests for a feature: **derive cases from acceptance criteria, journeys, and FMEA first, then compare that set to the feature diff.**

Entry workflow: `.qualityai/instructions/WORKFLOWS.md` §5.

## What This Skill Covers

- Building the case set with the feature diff closed
- Naming every case with source `ac`, `journey`, or `failure_mode` and a `source_ref`
- Comparing the finished set to the feature diff
- Flagging `unmentioned` when the change has no evidence of the case
- Listing `diff_only` tests that match no spec case

## What This Skill Does NOT Cover

- Whether an acceptance criterion is well-formed (`requirement-alignment#parse`)
- Whether the product code satisfies the requirement (`requirement-alignment#map` / `#validate`)
- How to design or score the test body (test-type skills, `testing-patterns`)
- Risk-tiered autonomy, Jira import, or CI execution of the case set

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Run the phases **in order**: `playbook/derive` → `playbook/compare` → `playbook/report`.
3. Keep the feature diff closed until `compare`.
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: spec-based-testing#...`.
5. Check the finished JSON with `tooling/validate_spec_cases.py`.

## Playbooks

- `playbook/derive/PLAYBOOK.md` — Cases from AC, journeys, and failure modes. Diff stays closed.
- `playbook/compare/PLAYBOOK.md` — Mark mention in the diff. Flag `unmentioned`.
- `playbook/report/PLAYBOOK.md` — Table, findings, and the JSON case set.

## Examples

- `examples/good-pattern.md` — Refund cases with source names and two `unmentioned` flags
- `examples/bad-pattern.md` — Cases copied from the diff, sources blank
- `examples/refund-case-set.json` — Finished case set the validator accepts

## Tooling

```bash
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py path/to/case-set.json
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py --self-check
```

Standard library only. The script checks the contract. It does not read a git diff and it does not call a tracker.

## References

- `references/case-set.md` — JSON fields
- `references/mentioned-in-diff.md` — When a diff mentions a case

## How Agents Use This Skill

| Role | Sources it derives |
|---|---|
| `qa.engineer` | `ac` (squad slice) |
| `qa.lead` | `journey` |
| `qa.architect` | `failure_mode` |

The orchestrator merges those sets, then runs `compare` once. A single-role request marks the other sources `out_of_scope`. Do not copy this methodology into the agent file.
