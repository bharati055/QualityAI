# Eval harness

Place to record an incident, a revert, or a false-positive finding, and the regression case that comes from it.

Skill: `.qualityai/skills/eval-harness/`. Workflow: `.qualityai/instructions/WORKFLOWS.md` §6.

## Layout

```text
evals/
├── README.md
├── records/     # what happened, and who missed it
└── cases/       # input, bad outcome, expected finding
```

| Kind | Record means | Case expected finding |
|---|---|---|
| `incident` | A defect escaped | The finding the agent or skill should have emitted |
| `revert` | A change was backed out | The finding that should have held the change |
| `false_positive` | A QualityAI finding was wrong | `no_finding`, plus the rejected text |

Each case names one target: an agent (`qa.engineer`, `qa.lead`, `qa.architect`, …) or a skill (`spec-based-testing`, `testing-patterns`, …).

## Add a pair

1. Copy `.qualityai/templates/eval/RECORD-TEMPLATE.md` to `records/rec-<slug>.md`.
2. Copy `.qualityai/templates/eval/CASE-TEMPLATE.md` to `cases/eval-<slug>.md`.
3. Follow `skills/eval-harness/playbook/record`, `case`, then `check`.
4. Open a PR. Humans merge. Do not push to `main`.

Field rules: `skills/eval-harness/references/case-format.md`.

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
```

## Shipped examples

These files are patterns (`example: true`), not this product's production history. Replace them with real misses or leave them as the shape to copy.

| Kind | Target | Record | Case |
|---|---|---|---|
| incident | skill `spec-based-testing` | `records/rec-refund-double-charge.md` | `cases/eval-refund-double-charge.md` |
| revert | agent `qa.lead` | `records/rec-checkout-promo-revert.md` | `cases/eval-checkout-promo-revert.md` |
| false_positive | skill `testing-patterns` | `records/rec-hollow-assert-false-positive.md` | `cases/eval-hollow-assert-false-positive.md` |

## What this place does not do

- It does not run the case in CI or score a model.
- It does not file a Jira issue or post a GitHub comment.
- It does not set risk tiers or enforce quarantine metadata.

Those stay later addons. The files are the harness.
