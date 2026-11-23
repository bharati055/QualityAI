# Eval Harness: Record Playbook

<!--
skill_id: eval-harness
phase: record
version: "1.0.0"
-->

## Purpose

Write down an incident, a revert, or a false-positive finding, and name the agent or skill that missed it. The record is the input to the regression case. It is not the case itself.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §6, step 1
- A defect escaped that a QualityAI run should have raised
- A change was reverted after review had passed it
- A finding was rejected because it was wrong

## When NOT to Use

- The suite failure is not yet classified — `failure-triage` first. Come back if the miss was the agent's
- The need is a quarantine — `flaky-quarantine`
- The need is to re-review the PR — the original skill, then this record if that review was the miss
- Filing a tracker ticket. Paste an id a human already has. Do not call Jira.

## Inputs

| Input | Required | Description |
|---|---|---|
| What happened | yes | Incident narrative, revert reason, or the rejected finding |
| Evidence | yes | Pasted log, diff excerpt, or finding text. No secrets. |
| Who missed it | yes | One agent id or one skill id |
| Date | yes | The day the human records it |

## Prerequisites

- Read `../../SKILL.md` and `../../references/case-format.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`
- Copy `.qualityai/templates/eval/RECORD-TEMPLATE.md`

## Steps

### Step 1: Choose the kind

- `incident` — a product defect escaped. Review or test suggestion did not raise it.
- `revert` — the change was backed out. Name what review failed to hold.
- `false_positive` — QualityAI emitted a finding a human rejected as wrong.
- One record, one kind. A second problem is a second record.

### Step 2: Name who missed it

- `missed_by_type: skill` when the methodology was skipped or misapplied (`spec-based-testing`, `testing-patterns`, …).
- `missed_by_type: agent` when the role ignored a skill it should have run (`qa.engineer`, `qa.lead`, `qa.architect`, or another `qa.*` agent).
- Pick one primary target. The case repeats it. Mention the other in the narrative if both played a part.

### Step 3: Write the two sections

- `## What happened` states the outcome in a few sentences: customer impact, revert, or the finding a human threw out.
- `## Evidence` holds the pasted proof. Include the spec excerpt and the diff or finding the agent saw, when that is what made the miss visible.
- Strip secrets. A ticket id or URL as text is enough.

### Step 4: Save the record

- Frontmatter matches `references/case-format.md`.
- Path: `.qualityai/evals/records/rec-<slug>.md`
- `example: false` unless you are editing a pack sample
- Do not write the regression case in this file. That is `playbook/case`.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Kind, target, date, narrative, and evidence are all present |
| warn | Evidence is thin but a human can still see the miss |
| fail | No agent or skill is named, or the kind is unclear |

Severity for findings: high / medium / low per FINDING-SCHEMA.md. A record is process output. Use a finding only when the team tried to close the miss with no record.

## Output

- `.qualityai/evals/records/rec-<slug>.md`
- `skill_applied`: `eval-harness#record` if a finding is needed
- The record id, ready for `playbook/case`

## Examples

- `../../examples/good-pattern.md` — incident record for the refund double-charge
- `.qualityai/evals/records/` — shipped samples for incident, revert, and false positive
- `../../examples/bad-pattern.md` — no kind and no target

## Related Skills

- `eval-harness#case` — next step
- `failure-triage` — classify a red build before calling it an agent miss
- `spec-based-testing` — common skill target when specs were skipped
- `flaky-quarantine` — flake debt, not this record

## Anti-Patterns

- "The agent missed a bug" with no evidence and no target
- A record that already embeds a half-written expected finding and never gets a case file
- Pasting credentials into Evidence
- Calling GitHub or Jira from the harness
- Deleting an old record instead of retiring its case

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
