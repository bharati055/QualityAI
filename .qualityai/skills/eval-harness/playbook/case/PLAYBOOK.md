# Eval Harness: Case Playbook

<!--
skill_id: eval-harness
phase: case
version: "1.0.0"
-->

## Purpose

Turn one record into a regression case the same agent or skill should meet next time. The case has three parts: input, bad outcome, and expected finding.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §6, step 2
- A record exists under `.qualityai/evals/records/` and has no case yet
- The team wants the miss to survive as a fixture, not only as a story

## When NOT to Use

- There is no record. Write `playbook/record` first.
- The task is to execute the case in CI. This pack stores the case. It does not run a model judge.
- The task is to fix the product defect. That is a product PR. The case only locks the review miss.

## Inputs

| Input | Required | Description |
|---|---|---|
| Record file | yes | Output of `playbook/record` |
| Input the agent saw | yes | Spec, diff, or prompt, trimmed to what the decision needed |
| Bad outcome | yes | What the agent or skill did |
| Expected finding | yes | JSON in `references/case-format.md` |

## Prerequisites

- The record validates as far as its own fields (kind, target, sections)
- Read `../../references/case-format.md`
- Copy `.qualityai/templates/eval/CASE-TEMPLATE.md`

## Steps

### Step 1: Point at the record

- Set `record_id` to the record's `id`.
- Copy `kind` from the record.
- Set `target_type` and `target_id` to the record's `missed_by_type` and `missed_by_id`.
- Set `status` to `open`.
- Case id is `eval-<slug>`. Save as `.qualityai/evals/cases/eval-<slug>.md`.

### Step 2: Write the input

- Include only what a later run needs to face the same decision: the spec lines, the diff or test, and the question that was asked.
- A Java excerpt belongs here when the miss was about that code. Keep it short.
- Drop secrets, unrelated files, and the correct answer. The expected finding is the next section, not a hint buried in the input.

### Step 3: Write the bad outcome

- State what the agent or skill actually produced: no finding, a green test plan, a revert that review had allowed, or the false-positive text.
- Name that agent or skill again in the prose so the section stands alone.

### Step 4: Write the expected finding

- For `incident` and `revert`: `finding` is the statement that should have been emitted, with `severity`, and `skill_applied` or `agent` (include both when you know them).
- For `false_positive`: `finding` is null, `expected` is `no_finding`, `rejected_finding` quotes the bad finding, and `skill_applied` or `agent` names who emitted it.
- Use FINDING-SCHEMA severity values. Do not invent a second schema.

### Step 5: Leave execution out

- Do not add a score, a model name, or a CI job. Those are later.
- Every case for a record uses that record's agent or skill. Several cases may share one record when one review missed more than one finding. A different target is a different record.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Input, bad outcome, and expected finding are present and match the record's kind and target |
| warn | The input is broader than the decision, but a human can still rerun it |
| fail | Any of the three sections is missing, or the target does not match the record |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- `.qualityai/evals/cases/eval-<slug>.md`
- `skill_applied`: `eval-harness#case` if a finding is needed
- Hand the pair to `playbook/check`

## Examples

- `../../examples/good-pattern.md`
- `.qualityai/evals/cases/eval-refund-double-charge.md` — incident case (FM-14)
- `.qualityai/evals/cases/eval-refund-partial.md` — second case on the same record (AC-2)
- `.qualityai/evals/cases/eval-checkout-promo-revert.md` — revert case
- `.qualityai/evals/cases/eval-hollow-assert-false-positive.md` — false-positive case
- `../../examples/bad-pattern.md`

## Related Skills

- `eval-harness#record` — previous step
- `eval-harness#check` — next step
- The target skill — do not restate its playbook inside the case

## Anti-Patterns

- Expected finding with no input
- A false positive stored as a normal finding the agent should raise again
- Targeting a different skill than the record names
- Putting the right answer only in the input so the bad outcome is unexplained
- Product fix described as if it were the expected finding

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
