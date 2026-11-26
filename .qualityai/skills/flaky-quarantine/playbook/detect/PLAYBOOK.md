# Flaky Quarantine: Detect Playbook

<!--
skill_id: flaky-quarantine
phase: detect
version: "1.0.0"
-->

## Purpose

Decide from run history whether a test is a flake candidate, using the thresholds in `.qualityai/context/suite-trust.md`. Detect only says "candidate" or "not a flake"; it never mutes anything.

## When to Use

- A test went red and green with no product change
- A team reports a "flaky" or "random red" test
- A weekly suite-health pass over CI history
- When the orchestrator or role-agent routes `flaky-quarantine` / `detect` work

## When NOT to Use

- The test fails on every run of a commit — that is not a flake; `failure-triage` / `classify`
- The failure class is already known and a quarantine is approved — `quarantine`
- The test is already quarantined and the question is its end date — `expiry-review`

## Inputs

| Input | Required | Description |
|---|---|---|
| Run history | yes | Per `test_id`: result, run id, commit SHA, date, whether a retry happened. At least 20 runs or 7 days; say if less |
| Change list | no | Product and test changes in the window, to rule out real regressions |
| Policy | yes | `.qualityai/context/suite-trust.md` (thresholds, allowed classes) |
| Registry | no | `.qualityai/quarantine/*.json`, to skip tests already quarantined |
| Prior findings | no | `failure-triage` classification |

## Prerequisites

- Read `../../SKILL.md` and `../../references/quarantine-metadata.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: Build the history table

- One row per run: date, run id, SHA, result, retried (yes/no).
- Drop runs where the test or the code under test changed; they test a different thing.
- Count a pass that needed a retry as a failure for the thresholds.

### Step 2: Apply the thresholds

Use the values in `suite-trust.md`; the defaults are:

| Signal | Default | Result |
|---|---|---|
| Fail then pass on one SHA | 1 | Suspect: note only |
| Intermittent failures, no relevant change | 3 or more in 7 days | Candidate flaky |
| Pass-on-rerun rate over last 20 runs | above 30% | Candidate; investigate script and environment |
| Red 3 runs in a row | 3 | Not a flake; hand to `failure-triage` as a likely defect |

If `suite-trust.md` is a stub, say "context missing" and use the defaults above as a proposal only.

### Step 3: Check it is not already handled

- Search the registry for the `test_id`. Already quarantined: skip, or hand to `expiry-review` if past `end_date`.
- Look for an open ticket the human pasted; name it so `quarantine` can reuse it.

### Step 4: Emit the candidate

- Severity: medium on a critical journey, otherwise low.
- Confidence by the number of qualifying runs: 5 or more failures 0.85+, 3 to 4 about 0.75, fewer than 3 not a candidate.
- Recommendation: run `failure-triage` to classify, then `quarantine` only for `test_script_issue` or `environment`.
- If no ticket exists, say so here. The AI does not create it; a human does.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No test meets a candidate threshold |
| warn | One or more candidates with a clear next step and owner |
| fail | A candidate on a critical journey keeps running unmuted and unowned for 7 days, or the suite exceeds the quarantine share in `suite-trust.md` |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Phase recommendation: pass | warn | fail
- One finding per candidate test with the history table in `evidence.note`
- `skill_applied`: `flaky-quarantine#detect`
- Short summary for the orchestrator: candidates, suspects, and tests that are not flakes

Example finding:

```json
{
  "finding": "Candidate flaky: CheckoutPromoIT#shouldApplyCode",
  "evidence": {
    "file": null,
    "note": "7 days, 20 runs: 6 first-attempt failures, all passed on rerun; no change to CheckoutPromoIT or promo-service in window; runs 8801, 8806, 8812, 8820, 8833, 8840"
  },
  "severity": "medium",
  "confidence": 0.85,
  "rationale": "6 failures in 7 days against the 3-in-7 threshold; 30% pass-on-rerun rate; booking journey",
  "recommendation": "qa.lead runs failure-triage on this test; if classed environment or test_script_issue, a human files a ticket and flaky-quarantine#quarantine records it",
  "skill_applied": "flaky-quarantine#detect",
  "agent": "qa.lead"
}
```

## Examples

- `../../examples/good-pattern.md` — candidate to record to expiry
- `../../examples/bad-pattern.md` — mutes with no history or ticket

## Related Skills

- `failure-triage` — classify the candidate before quarantine
- `flaky-quarantine#quarantine` — build the record
- `test-automation` — fix the script

## Anti-Patterns

- Calling a test flaky from one failure
- Counting runs that straddle a product change
- Treating three red runs in a row as noise
- Muting during detect
- Creating or syncing tickets from the pack

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
