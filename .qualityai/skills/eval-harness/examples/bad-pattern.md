# Bad pattern — a note that cannot regress

## What was written

```markdown
# Miss

The agent missed a bug last week. We should do better.
```

No kind. No agent or skill. No date. No evidence. No input, bad outcome, or expected finding. There is nothing for the next run to face, and nothing for `validate_eval_case.py` to accept.

## Why it fails

- An incident, revert, or false positive is a specific miss with a target.
- The case is the regression: the same input, the bad outcome that happened, and the finding that should happen instead.
- "Do better" does not name `spec-based-testing`, `qa.lead`, or any other id.

## What to do instead

1. `playbook/record` — kind, who missed it, what happened, evidence.
2. `playbook/case` — input, bad outcome, expected finding JSON.
3. `playbook/check` — run the validator.

Use `.qualityai/evals/records/rec-refund-double-charge.md` and its case as the pattern.
