# Failure Triage: Classify Playbook

<!--
skill_id: failure-triage
phase: classify
version: "1.0.0"
-->

## Purpose

Put one failing test into exactly one class: `product_defect`, `test_script_issue`, `environment`, or `unknown`. The class decides who fixes it and whether the failure may ever be quarantined, so it must rest on evidence from `evidence`, not on how the log looks.

## When to Use

- A CI or regression run is red and someone asks "real bug or noise?"
- A test failed, passed on rerun, and the team wants to know why
- `flaky-quarantine#detect` produced a candidate and the class is still open
- When the orchestrator or role-agent routes `failure-triage` / `classify` work

## When NOT to Use

- The test is green and only needs review — `testing-patterns`
- The failure is already classified and only needs a next step — `recommend`
- The question is whether the test is a flake by statistics — `flaky-quarantine` / `detect`
- A load or soak result is out of range — `performance-validation`, `soak-testing`

## Inputs

| Input | Required | Description |
|---|---|---|
| Failure log | yes | Assertion message, stack trace, run id or URL, commit SHA |
| Run history | yes | Last 20 results of the same `test_id` (or "unavailable" — then say so) |
| Diff or change list | no | Product and test changes since the last green run |
| Environment facts | no | `.qualityai/context/environments.md`, dependency status for the failure window |
| Policy | yes | `.qualityai/context/suite-trust.md` |
| Prior findings | no | From `evidence` or other agents |

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: Pin the failure

- Record `test_id`, run id, commit SHA, and the first failing assertion or exception (not the last cascade error).
- Note whether it failed on this commit only, or on earlier commits too.

### Step 2: Ask the four questions in order

| # | Question | Yes points to |
|---|---|---|
| 1 | Does the assertion check behavior the diff or a recent product change altered, and is the new behavior wrong against the requirement? | `product_defect` |
| 2 | Does the failure come from the test itself: wrong wait, shared state, order dependence, stale fixture, hollow or over-strict assertion? | `test_script_issue` |
| 3 | Does the failure come from outside the code under test: dependency 5xx or timeout, runner out of memory, expired credential, data refresh, clock or network? | `environment` |
| 4 | None of the above can be shown | `unknown` |

Stop at the first yes that has evidence. A yes without evidence does not count; go to the next question.

### Step 3: Check the tie-breakers

- Failed on 3 or more consecutive runs of the same commit: lean `product_defect` or `test_script_issue`; intermittent failures lean `environment` or `test_script_issue`.
- Passes locally but fails only in CI: `environment` or `test_script_issue`; do not call it a product defect on that alone.
- The assertion text matches a requirement the product no longer meets: `product_defect`, even if the test also looks fragile.
- Two classes fit equally: pick `unknown`, list both candidates in `rationale`.

### Step 4: Set confidence

- Two independent signals from `evidence`: 0.85 or higher
- One signal: 0.50 to 0.69, and prefer `warn`
- Pattern match only: `unknown`, below 0.50

### Step 5: Emit the finding

- Set `skill_applied: failure-triage#classify`; put the class in `finding`, the log lines and run ids in `evidence`.
- Name the fix owner in `recommendation`, per `recommend`.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Every failure in scope has a class backed by 2 independent signals |
| warn | A class rests on one signal, or a failure stays `unknown` with a named next step |
| fail | A failure on a critical journey is `unknown` or unclassified, or a `product_defect` was re-labelled to get green |

Severity for findings: `product_defect` on a critical journey or payment/auth path is high; other classes are medium or low per blast radius.

## Output

- One finding per failing `test_id` (group identical root causes)
- `skill_applied`: `failure-triage#classify`
- Short summary for the orchestrator: counts per class and which findings need a human

Example finding:

```json
{
  "finding": "CheckoutIT#shouldConfirmBooking: test_script_issue",
  "evidence": {
    "file": "src/test/java/shop/CheckoutIT.java",
    "lines": "88-94",
    "code_snippet": "Thread.sleep(500); page.click(\"#confirm\");",
    "note": "Run 8812 failed on the click (ElementNotInteractable); run 8813, same SHA 3fa9c1d, passed. Fixed 500 ms sleep races the confirmation animation."
  },
  "severity": "medium",
  "confidence": 0.86,
  "rationale": "No product change since the last green run; two runs on one SHA disagree; the sleep is the only timing control",
  "recommendation": "Owner @squad-payments replaces the sleep with an explicit wait; see flaky-quarantine if it fails 3 times in 7 days",
  "skill_applied": "failure-triage#classify",
  "agent": "qa.engineer"
}
```

## Examples

- `../../examples/good-pattern.md` — environment, test_script_issue, and product_defect each with their evidence
- `../../examples/bad-pattern.md` — class chosen from the log text; flake called a product defect

## Related Skills

- `failure-triage#evidence` — what each class must prove
- `failure-triage#recommend` — owner and next action once the class is set
- `flaky-quarantine` — only for flakes classed `test_script_issue` or `environment`
- `test-automation` — fixing the script once the class is `test_script_issue`

## Anti-Patterns

- Choosing a class from the exception name alone
- Calling an intermittent failure `product_defect` without a product change or a repeatable repro
- Calling a red test `environment` without a dependency or runner signal
- Closing a failure as `unknown` with no next step
- Re-labelling a failure so the gate passes

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
