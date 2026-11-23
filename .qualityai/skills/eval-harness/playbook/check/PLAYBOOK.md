# Eval Harness: Check Playbook

<!--
skill_id: eval-harness
phase: check
version: "1.0.0"
-->

## Purpose

Confirm a record and its case are a usable regression pair: the right kind, the agent or skill that missed it, and the three case sections. Then run the pack script.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §6, step 3
- Before opening or updating the PR that adds the pair
- When `qa.lead` reviews the eval set

## When NOT to Use

- The case has not been written
- The task is to score a live model run. This phase checks the files only.
- Editing the product defect. Link the product PR in Evidence as text if one exists.

## Inputs

| Input | Required | Description |
|---|---|---|
| Record | yes | `.qualityai/evals/records/rec-<slug>.md` |
| Case | yes | `.qualityai/evals/cases/eval-<slug>.md` |
| Validator | yes | `tooling/validate_eval_case.py` |

## Prerequisites

- `playbook/record` and `playbook/case` are done
- Read `../../references/case-format.md`
- Humans approve the PR. Do not push to `main`.

## Steps

### Step 1: Match the pair

- Case `record_id` equals the record `id`.
- `kind` matches.
- Case `target_type` and `target_id` match the record's `missed_by_type` and `missed_by_id`.
- Filename stems match the ids.

### Step 2: Read the three sections

- Input is enough to face the decision without the expected finding.
- Bad outcome describes what that target did.
- Expected finding matches the kind: a real finding for `incident` and `revert`, `no_finding` for `false_positive`.
- No secrets in either file.

### Step 3: Run the script

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
```

- Fix every line it prints. Do not delete a shipped example to quiet an unrelated error.
- `example: true` files are pack patterns. A new host case uses `example: false` or omits the key.

### Step 4: Keep retired cases

- When a case no longer applies, set `status` to `retired` and say why in `## Bad outcome` or a short `## Notes` section.
- Leave the record in place.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | The script exits 0 and a human can see the miss from the case alone |
| warn | The script passes and the input is broader than it needs to be |
| fail | The script exits non-zero, the target differs from the record, or a section is empty |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- A pair the validator accepts
- `skill_applied`: `eval-harness#check` if a finding is needed
- PR note: record id, case id, target, kind

## Examples

- `.qualityai/evals/README.md` — index of the shipped pairs
- `../../examples/good-pattern.md`
- `../../examples/bad-pattern.md` — fails this phase

## Related Skills

- `eval-harness#record` and `#case`
- `qa.lead` owns the set; the role that missed drafts the pair
- Target skill playbooks stay the methodology under test

## Anti-Patterns

- Merging a case that names no skill and no agent
- Treating `example: true` samples as this product's incident history
- Removing a failed case from the tree so the script goes green
- Adding a CI workflow in this phase

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
- Forms: `.qualityai/templates/eval/`
