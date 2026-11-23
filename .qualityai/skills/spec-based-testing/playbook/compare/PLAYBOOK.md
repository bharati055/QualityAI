# Spec-Based Testing: Compare Playbook

<!--
skill_id: spec-based-testing
phase: compare
version: "1.0.0"
-->

## Purpose

Open the feature diff only after `derive`. Mark which spec cases the change mentions, and flag `unmentioned` on the rest. The flag means the code change never mentioned that case.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §5, step 2
- Immediately after a derive case set exists
- PR review, when test-quality needs to see spec cases the diff missed

## When NOT to Use

- `derive` has not been done. Do not compare an empty or diff-sourced list.
- The task is to decide if the implementation meets the AC — `requirement-alignment`
- The task is to score assertion quality — `testing-patterns` (it can run after this phase, using `diff_only` and the case set)

## Inputs

| Input | Required | Description |
|---|---|---|
| Draft case set from `derive` | yes | `specs_read_before_diff` true. Sources already named. |
| Feature diff | yes | Production, tests, and any change description already pasted. Do not call a forge API. |
| Context docs | no | Only to confirm a critical journey or FMEA severity already in the case |

## Prerequisites

- `playbook/derive` is done for every in-scope source
- Read `../../references/mentioned-in-diff.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

### Step 1: Open the diff

- Read the feature diff now: production changes, tests, and the pasted change description.
- Do not add a new spec case because the diff contains a branch. New spec cases are a derive mistake — return to `derive` with the diff closed again.

### Step 2: Decide mention for each case

- For each derived case, set `mentioned_in_diff` using `references/mentioned-in-diff.md`.
- True only when the diff states the same behavior. A nearby happy path is not a mention of a failure-mode case.
- When true, set `diff_evidence` to a file and symbol or a short quote. Set `flags` to `[]`.
- When false, set `diff_evidence` to `""` and `flags` to `["unmentioned"]`.

### Step 3: List diff-only tests

- Scan tests and described behaviors in the diff that match no case.
- Append `{evidence, note}` to `diff_only`.
- The note says which spec sources were checked. It does not assign `source` `ac`, `journey`, or `failure_mode`.
- Leave quality of those tests to `testing-patterns`.

### Step 4: Set severity

- `unmentioned` on a critical journey step, a payment or auth path, or a high-severity failure mode → finding severity high.
- `unmentioned` on a non-critical criterion → medium.
- `diff_only` with no unmentioned spec case → low, unless the only tests in the diff are `diff_only` and a critical case was derived — then the unmentioned case carries the severity.

### Step 5: Mark the set finished

- Set `compared_to_diff` to true.
- Do not flip `specs_read_before_diff` to false.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Every derived case is mentioned, and every in-scope source is `present` or `out_of_scope` |
| warn | An `unmentioned` case is non-critical, an in-scope source is `missing`, or the diff has `diff_only` tests beside a covered spec |
| fail | An `unmentioned` case sits on a critical journey step, a payment or auth path, or a high-severity failure mode |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Finished case set with mention fields and flags
- One finding per high `unmentioned` case. Medium and low cases may share one finding when every `source_ref` is listed in the evidence.
- `skill_applied`: `spec-based-testing#compare`
- `diff_only` notes for the orchestrator (these are not spec cases)

## Examples

- `../../examples/good-pattern.md` — `AC-2` and `FM-14` flagged `unmentioned`; full refund mentioned
- `../../examples/refund-case-set.json` — the same set as JSON
- `../../examples/bad-pattern.md` — happy-path test treated as proof of the failure mode

## Related Skills

- `spec-based-testing#derive` — the only place new spec cases are added
- `testing-patterns` — assertion quality of mentioned and `diff_only` tests
- `requirement-alignment` — intent versus implementation, separate from this flag
- `eval-harness` — store the miss when an `unmentioned` case later escapes or the change is reverted

## Anti-Patterns

- Marking `mentioned_in_diff` true because the same class changed
- Treating a green coding-agent test as the spec case
- Dropping `unmentioned` cases so the phase can pass
- Giving a `diff_only` test an AC id it does not have
- Calling GitHub or Jira to fetch the diff. Use the diff already in hand.

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
