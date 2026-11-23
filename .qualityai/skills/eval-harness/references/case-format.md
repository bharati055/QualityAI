# Eval record and case format

Normative shape for `.qualityai/evals/`. `tooling/validate_eval_case.py` checks it. Markdown with an HTML-comment frontmatter block, same style as playbooks.

Do not put secrets, tokens, or credentials in either file.

## Record — `.qualityai/evals/records/rec-<slug>.md`

```markdown
<!--
id: rec-<slug>
kind: incident
missed_by_type: skill
missed_by_id: spec-based-testing
date: YYYY-MM-DD
example: false
-->
```

| Field | Required | Values |
|---|---|---|
| `id` | yes | `rec-` plus a lowercase slug. Matches the filename stem. |
| `kind` | yes | `incident` (escaped defect), `revert` (change backed out), `false_positive` (a QualityAI finding that was wrong) |
| `missed_by_type` | yes | `agent` or `skill` |
| `missed_by_id` | yes | Agent id `qa.<role>` (letters, digits, hyphens, dots) or a skill id (lowercase slug) |
| `date` | yes | `YYYY-MM-DD` the human recorded |
| `example` | no | `true` on pack samples. Omit, or `false`, on a host case. |

Required sections:

- `## What happened` — what escaped, what was reverted, or which finding was wrong
- `## Evidence` — pasted log, diff excerpt, revert reason, or the finding text. A ticket id or URL may be pasted as text. Do not call Jira or GitHub from this skill.

## Case — `.qualityai/evals/cases/eval-<slug>.md`

```markdown
<!--
id: eval-<slug>
kind: incident
target_type: skill
target_id: spec-based-testing
record_id: rec-<slug>
status: open
example: false
-->
```

| Field | Required | Values |
|---|---|---|
| `id` | yes | `eval-` plus a lowercase slug. Matches the filename stem. |
| `kind` | yes | Same kind as the record |
| `target_type` | yes | Same as the record's `missed_by_type` |
| `target_id` | yes | Same as the record's `missed_by_id` |
| `record_id` | yes | The record `id` |
| `status` | yes | `open` or `retired` |
| `example` | no | Same meaning as on the record |

Required sections:

- `## Input` — the smallest spec, diff, or prompt that should have produced the right result
- `## Bad outcome` — what that agent or skill actually did
- `## Expected finding` — one JSON object

### Expected finding JSON

A miss (`incident` or `revert`) states the finding that should have been emitted:

```json
{
  "finding": "Short statement of the missed issue",
  "severity": "high",
  "skill_applied": "spec-based-testing#compare",
  "agent": "qa.architect"
}
```

`finding` is a non-empty string. `severity` is `high`, `medium`, or `low`. At least one of `skill_applied` or `agent` is present. `skill_applied` uses a canonical id and a `#` section. `agent` matches `qa.<role>`.

A `false_positive` states that the bad finding should not recur:

```json
{
  "finding": null,
  "expected": "no_finding",
  "rejected_finding": "The finding text that was wrong",
  "severity": "medium",
  "skill_applied": "testing-patterns#review",
  "agent": "qa.tester"
}
```

`finding` is null, `expected` is `no_finding`, and `rejected_finding` quotes the false positive. `severity` is the severity that was claimed. `skill_applied` or `agent` still names who emitted it.

Optional keys on either object: `confidence` (number from 0 to 1), `rationale`. Unknown keys are rejected so a typo cannot pass.

## Pairing rules

- Every record has at least one case.
- `kind`, and the agent or skill id, match across the pair.
- `status: retired` stays in the tree so the miss is not deleted quietly.

## Forms

Copy `.qualityai/templates/eval/RECORD-TEMPLATE.md` and `CASE-TEMPLATE.md`. Shipped files with `example: true` are patterns, not this host's production history.
