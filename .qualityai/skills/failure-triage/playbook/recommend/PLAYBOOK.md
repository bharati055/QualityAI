# Failure Triage: Recommend Playbook

<!--
skill_id: failure-triage
phase: recommend
version: "1.0.0"
-->

## Purpose

Turn a classified failure into one concrete next action with a named owner. The recommendation keeps the suite trustworthy: failures that mean product risk stay loud, test and environment debt gets an owner and a date, and nothing is silently muted or deleted.

## When to Use

- A failure has a class and evidence from `classify` / `evidence`
- A team asks "what do we do with this red test?"
- A flake candidate needs a decision on quarantine
- When the orchestrator or role-agent routes `failure-triage` / `recommend` work

## When NOT to Use

- The failure has no class yet — run `classify` first
- A quarantine record needs to be built — `flaky-quarantine` / `quarantine`
- The question is code design or test design in general — `code-quality`, `testing-patterns`

## Inputs

| Input | Required | Description |
|---|---|---|
| Classified finding | yes | Class, evidence, confidence from `classify` and `evidence` |
| Squad and journey context | no | `.qualityai/context/squad/`, `journeys/` for owner and criticality |
| Policy | yes | `.qualityai/context/suite-trust.md` |
| Existing tickets or registry | no | `.qualityai/quarantine/*.json`, tracker ids the human pasted |

## Prerequisites

- Read `../../SKILL.md`
- Read `.qualityai/context/suite-trust.md`; if it says "context missing", say so instead of inventing thresholds
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: Pick the action from the class

| Class | Recommendation | Owner |
|---|---|---|
| `product_defect` | Keep the test active; a human files the defect with the failing assertion and repro; block the gate if the journey is critical | Squad that owns the code under test |
| `test_script_issue` | Fix the test (explicit wait, isolated data, order independence); if it is a flake by `suite-trust.md` thresholds, add `flaky-quarantine` / `quarantine` | Squad that owns the test |
| `environment` | Re-run after the dependency is healthy; ask the environment owner for a fix; quarantine only if the test cannot be isolated | Environment or platform owner |
| `unknown` | Name the missing evidence and who can supply it; keep the test active | `qa.lead` |

### Step 2: Check the guard rails

- Never recommend deleting or commenting out a failing test to reach green.
- Never recommend a mute without `owner`, `end_date`, `ticket_id`, `reason`, and `exit_criteria`; hand that to `flaky-quarantine`.
- Never recommend quarantine for `product_defect` or `unknown`.
- Do not create tickets. In v1 a human files them; the recommendation says what the ticket must contain.

### Step 3: Write the human action

- One imperative sentence with the owner, the change, and the check that proves it is done.
- For a quarantine hand-off, name the `flaky-quarantine#quarantine` step and list the fields still missing.

### Step 4: Set severity

- `product_defect` on a critical journey, payment, or auth path: high
- Flake on a critical journey: medium (high if already quarantined past `end_date`)
- Other `test_script_issue` or `environment`: low to medium by how often the suite goes red

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Every classified failure has an action, an owner, and a done-check |
| warn | A failure has an action but no owner yet, or waits on a human-supplied ticket |
| fail | A recommendation would mute, delete, or ignore a failure with no record, or a critical-journey `product_defect` has no action |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- One recommendation per class group, each with owner and done-check
- `skill_applied`: `failure-triage#recommend`
- Hand-offs to `flaky-quarantine` listed by `test_id`

Example finding:

```json
{
  "finding": "Fix CheckoutIT#shouldConfirmBooking wait; quarantine only if it fails again",
  "evidence": {
    "file": null,
    "note": "Classified test_script_issue (0.86): runs 8812 and 8813 disagree on SHA 3fa9c1d; fixed 500 ms sleep before click"
  },
  "severity": "medium",
  "confidence": 0.86,
  "rationale": "Script-side flake on the booking journey; first failure in the 7-day window, below the 3-failure threshold in suite-trust.md",
  "recommendation": "@squad-payments replaces the sleep with an explicit wait and shows 10 green CI runs; if it fails 3 times in 7 days, run flaky-quarantine#quarantine with a QA ticket",
  "skill_applied": "failure-triage#recommend",
  "agent": "qa.engineer"
}
```

## Examples

- `../../examples/good-pattern.md` — action and owner per class
- `../../examples/bad-pattern.md` — mute with no record; flake re-labelled a product defect

## Related Skills

- `failure-triage#classify`, `failure-triage#evidence` — produce the input
- `flaky-quarantine` — owns quarantine metadata and expiry
- `test-automation` — how to fix a script-side problem
- `eval-harness` — store a triage miss or false positive (`WORKFLOWS.md` §6)

## Anti-Patterns

- "Re-run until green" as the recommendation
- Recommendations with no owner
- Muting a `product_defect` so the release can go out
- Filing or syncing tickets from the pack in v1

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
