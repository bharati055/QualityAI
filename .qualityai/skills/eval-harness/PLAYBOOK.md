# Eval Harness — Quick Start

1. Open `SKILL.md` and `.qualityai/evals/README.md`.
2. `playbook/record` → `.qualityai/evals/records/rec-<slug>.md`
3. `playbook/case` → `.qualityai/evals/cases/eval-<slug>.md` with input, bad outcome, and expected finding
4. `playbook/check`, then:

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
```

The case names the agent or skill that missed it. Humans merge the PR. This harness does not run CI and does not file a ticket.
