# Eval case: replace with a short title

<!--
id: eval-replace-me
kind: incident
target_type: skill
target_id: spec-based-testing
record_id: rec-replace-me
status: open
example: false
-->

`kind`, `target_type`, and `target_id` match the record. `status` is `open` or `retired`.

Save as `.qualityai/evals/cases/eval-replace-me.md`. Field rules: `.qualityai/skills/eval-harness/references/case-format.md`.

## Input

The smallest spec, diff, or prompt that should have produced the right result. No secrets.

## Bad outcome

What the agent or skill actually did: no finding, the wrong finding, or a false positive.

## Expected finding

For an incident or revert, `finding` is the statement that should have been emitted. For a false positive, use `"finding": null`, `"expected": "no_finding"`, and `rejected_finding`.

```json
{
  "finding": "Replace with the missed issue",
  "severity": "high",
  "skill_applied": "spec-based-testing#compare",
  "agent": "qa.engineer"
}
```
