# Spec-Based Testing: Report Playbook

<!--
skill_id: spec-based-testing
phase: report
version: "1.0.0"
-->

## Purpose

Publish the spec-based case set: a table a human can read, findings for cases the change never mentioned, and JSON that the pack script can check.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §5, step 3
- After `compare` has set `compared_to_diff` true
- When the orchestrator needs the test-suggestion or test-quality section of the report

## When NOT to Use

- Derive or compare is unfinished
- The user asked to write the test class now — hand the `unmentioned` rows to the matching test-type skill and follow that skill
- Recording an escaped defect — `eval-harness`

## Inputs

| Input | Required | Description |
|---|---|---|
| Finished case set | yes | Output of `compare` |
| Findings from derive and compare | yes | Missing sources and `unmentioned` cases |
| Test-type context | no | `test-types.md` and the framework doc, to name a suggested type only |

## Prerequisites

- `playbook/compare` is done
- Read `../../references/case-set.md`
- Findings follow `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

### Step 1: Render the case table

- One row per case: `id`, `source`, `source_ref`, `title`, `expected`, `mentioned_in_diff`, `flags`, `diff_evidence`
- Then list `source_gaps`, `skipped`, and `diff_only`
- Use the words `ac`, `journey`, and `failure_mode` in the source column so the report names the source

### Step 2: Attach findings

- Carry forward derive findings for **context missing**
- Carry forward compare findings for `unmentioned`
- Evidence for an `unmentioned` case is the `source_ref` plus a note that the diff has no matching behavior. `file` may be null when the gap is the absence of a test.
- `skill_applied` is `spec-based-testing#derive` or `spec-based-testing#report` for this summary, and `spec-based-testing#compare` on each `unmentioned` finding
- `agent` is the role that owned that source

### Step 3: Point at the next skill

- For each `unmentioned` case, name one test-type skill to design the test (`unit-testing`, `api-testing`, `integration-testing`, `contract-testing`, `test-automation`, `soak-testing`, or `performance-validation`)
- Optional `suggested_test_type` on the case. Do not paste that skill's checklist here.
- `diff_only` rows go to `testing-patterns` for assertion quality

### Step 4: Write JSON and check it

- Write the finished object from `references/case-set.md`
- Run:

```bash
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py path/to/case-set.json
```

- If the script reports invalid, fix the set. Do not drop `unmentioned` flags to make it pass.

### Step 5: Hand off

- Put the table, findings, and JSON path in the orchestrator summary
- Recommended status follows the compare decision (pass / warn / fail)
- Humans merge. This phase does not edit product tests unless the user asked for a separate implementation PR.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Compare passed and the JSON validates |
| warn | Compare warned and the JSON validates |
| fail | Compare failed, or the case set omits source names or `unmentioned` flags |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Markdown case table with source and flags
- Findings list
- JSON case set that `validate_spec_cases.py` accepts
- Short summary: counts of cases, `unmentioned`, `diff_only`, and context gaps
- `skill_applied`: `spec-based-testing#report` on the summary

## Examples

- `../../examples/good-pattern.md` — table, Java sketch for `FM-14`, pointer at the JSON
- `../../examples/refund-case-set.json`
- `../../examples/bad-pattern.md` — report that cannot name a source

## Related Skills

- Test-type skills — write the missing test
- `testing-patterns` — quality of tests the diff already has
- `requirement-alignment` — gaps in intent versus code, not this table
- `eval-harness` — turn a missed `unmentioned` case into a regression case after an incident or revert

## Anti-Patterns

- A report that lists tests without `source`
- Hiding `unmentioned` rows in prose
- Shipping the template skeleton (`templates/spec-based-testing/CASE-SET-TEMPLATE.md`) as if it were this change
- Claiming the phase passed because existing tests are green

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
- Form to copy: `.qualityai/templates/spec-based-testing/CASE-SET-TEMPLATE.md`
