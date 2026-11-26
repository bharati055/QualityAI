# Flaky Quarantine: Expiry Review Playbook

<!--
skill_id: flaky-quarantine
phase: expiry-review
version: "1.0.0"
-->

## Purpose

Find quarantines past their `end_date` and make each one a visible decision. An expired quarantine that nobody mentions is a permanent mute; this phase turns it into an escalation finding so the owner fixes, extends, or deletes the test.

## When to Use

- A scheduled suite-health pass (weekly is a good default)
- A PR touches `.qualityai/quarantine/` or a muted test
- The pack checker reports `QUAR_EXPIRED`
- When the orchestrator or role-agent routes `flaky-quarantine` / `expiry-review` work (usually `qa.lead`)

## When NOT to Use

- The quarantine is still inside its window — nothing to review
- The test was never classified a flake — `failure-triage`
- A new quarantine is being added — `quarantine`

## Inputs

| Input | Required | Description |
|---|---|---|
| Registry | yes | `.qualityai/quarantine/*.json` |
| Review date | yes | Today, or the date the human names |
| Run history since quarantine | no | Whether the test, run unmuted, would now pass |
| Ticket status | no | Pasted by a human; the AI does not query the tracker |
| Policy | yes | `.qualityai/context/suite-trust.md` (expiry rule, extension limit) |

## Prerequisites

- Read `../../SKILL.md` and `../../references/quarantine-metadata.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: List expired records

- Run `python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --root . --today <review date>`.
- Each `QUAR_EXPIRED` line is one record that needs a finding. A record whose `end_date` equals the review date is not expired.

### Step 2: Gather the state of each

- Is the mute still in the code (annotation, tag, skip list)?
- Did the owner's exit criteria get met? Cite the runs.
- Is the ticket open, closed, or unknown (as the human reported)?
- How many extensions has this test had? A second extension goes to the Architect (`suite-trust.md`).

### Step 3: Choose the recommendation

| State | Recommend |
|---|---|
| Exit criteria met | Remove the mute and the record in a PR |
| Fix in progress, one extension left | Lead-approved extension by PR with a new `end_date` and a reason; checker still caps at 90 days |
| No progress | Owner fixes this week, or the test is deleted with human approval and a note on where the risk is covered |
| Second extension requested | Escalate to `qa.architect`; do not extend |

### Step 4: Emit the escalation finding

- `skill_applied: flaky-quarantine#expiry-review`, `agent: qa.lead`.
- Severity high on a critical journey, otherwise medium. The checker accepts only these two.
- Put the record's `ticket_id` in `finding` or `evidence.note`. The checker matches on it.
- Put the finding in the same document as the record (the registry file or the report) so the checker can pair them.

### Step 5: Re-run the checker

- Run `validate_quarantine.py` again; `QUAR_EXPIRED` clears only when the finding or the removal is in the PR.
- Hand the decision to a human. The AI may open the PR; it never merges.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No expired records, or each expired record is removed or has an approved extension |
| warn | Expired records exist with an escalation finding and an owner decision pending within one working day |
| fail | An expired record has no escalation finding, or a mute outlived its record |

Severity for findings: high on a critical journey, medium otherwise; low is not accepted for an expired quarantine.

## Output

- One escalation finding per expired record
- `skill_applied`: `flaky-quarantine#expiry-review`
- Summary for the orchestrator: expired, extended, removed, escalated to the Architect

Example finding:

```json
{
  "finding": "Quarantine QA-1301 expired on 2026-11-20 without a fix or extension",
  "evidence": {
    "file": null,
    "note": "SearchApiTest#returnsFacets still muted; ticket QA-1301 open per human; 6 days past end_date; no extension on record"
  },
  "severity": "medium",
  "confidence": 0.9,
  "rationale": "An expired quarantine hides a regression signal with no owner decision",
  "recommendation": "Owner @squad-search fixes the test, or the Lead approves one extension through a PR, or the test is deleted with approval",
  "skill_applied": "flaky-quarantine#expiry-review",
  "agent": "qa.lead"
}
```

## Examples

- `../../examples/good-quarantine-record.json` — expired record `QA-1301` paired with its escalation finding
- `../../examples/bad-quarantine-record.json` — expired record with no escalation (`QUAR_EXPIRED`)

## Related Skills

- `flaky-quarantine#quarantine` — the record being reviewed
- `failure-triage` — re-classify if the failure mode changed
- `qa.lead` / `qa.architect` agents — escalation owners

## Anti-Patterns

- Bumping `end_date` in the same PR with no reason or approval
- Extending more than once without the Architect
- Escalation with severity low
- Removing the record but leaving the `@Disabled` in code
- Querying or editing the tracker from the pack in v1

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
