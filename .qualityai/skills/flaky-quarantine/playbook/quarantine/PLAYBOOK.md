# Flaky Quarantine: Quarantine Playbook

<!--
skill_id: flaky-quarantine
phase: quarantine
version: "1.0.0"
-->

## Purpose

Recommend a time-boxed quarantine for a classified flake, with every field a reviewer and the pack checker need: owner, end date, ticket, reason, exit criteria. The quarantine goes in by pull request and a human approves it. A quarantine without this metadata is a permanent mute, and the checker rejects it.

## When to Use

- `failure-triage` classed the test `test_script_issue` or `environment` with flake evidence
- `detect` produced a candidate and a human wants the test out of the blocking path
- When the orchestrator or role-agent routes `flaky-quarantine` / `quarantine` work

## When NOT to Use

- The class is `product_defect` or `unknown` — the test stays active
- The test can be fixed in the same PR — fix it instead
- The quarantine already exists and has passed `end_date` — `expiry-review`
- No ticket id has been supplied — emit a `detect` finding that names the blocker (Step 2)

## Inputs

| Input | Required | Description |
|---|---|---|
| Classified flake | yes | Class, evidence, run ids from `failure-triage` and `detect` |
| Ticket id | yes | Supplied by a human; v1 never creates tickets |
| Owner | yes | Team or person from `.qualityai/context/squad/` or the ticket |
| Policy | yes | `.qualityai/context/suite-trust.md` (window, mechanisms) |
| Registry | no | `.qualityai/quarantine/*.json` |

## Prerequisites

- Read `../../SKILL.md` and `../../references/quarantine-metadata.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`: AI may open a PR, must not push to `main`

## Steps

### Step 1: Confirm the test qualifies

- Class is `test_script_issue` or `environment`, with evidence (`failure-triage#evidence`).
- Not already in the registry.
- On a critical journey: name the compensating check in `reason` and mark the PR for Lead approval.

### Step 2: Check the ticket

- A human-supplied `ticket_id` is required (`QA-1234`, `#42`, `org/repo#42`, or a URL).
- Missing: stop. Emit a `flaky-quarantine#detect` finding that says "quarantine blocked: ticket_id missing" and what the ticket must hold (test id, evidence, owner, exit criteria). Do not invent an id or write `TBD`.

### Step 3: Write the record

| Field | How to fill it |
|---|---|
| `test_id` | The stable id the runner prints |
| `owner` | One accountable team or person, not "QA" |
| `end_date` | ISO date, default 30 days out, at most 90 |
| `ticket_id` | The human-supplied id |
| `reason` | The evidence: failure count, window, what does not change, suspected cause |
| `exit_criteria` | Something observable: "10 consecutive green CI runs after explicit wait" |
| `mechanism` | One of `disabled-annotation`, `tag`, `ci-skip-list` |

### Step 4: Pick the mechanism

- Follow the allowed mechanisms in `suite-trust.md`.
- Annotation: ticket id in the reason string.
- Always add the record to `.qualityai/quarantine/<area>.json` so expiry can be checked.

### Step 5: Validate and hand off

- Run `python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --root .`; fix every issue.
- Emit the recommendation. A human applies it through a PR; the AI may open the PR, never merge it.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Record complete, class qualifies, checker is clean |
| warn | Complete record but the test is on a critical journey and waits on Lead approval, or the window is longer than 30 days |
| fail | A mute exists with a missing field, no ticket, or a `product_defect` / `unknown` test is being muted |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- One recommendation per test, with the record in a `quarantine` object (this is what the checker reads)
- `skill_applied`: `flaky-quarantine#quarantine`
- Short summary: how many records, which need Lead approval, which are blocked on a ticket

Example recommendation:

```json
{
  "finding": "Quarantine CheckoutPromoIT#shouldApplyCode until 2026-12-10",
  "evidence": {
    "file": "src/test/java/shop/CheckoutPromoIT.java",
    "note": "6 of 20 runs failed on first attempt, all passed on rerun; promo-service cold start"
  },
  "severity": "low",
  "confidence": 0.85,
  "rationale": "Environment-side flake; the suite stays trustworthy while the owner adds a warm-up",
  "recommendation": "Apply by PR: annotate the test and add the registry record; human approves",
  "skill_applied": "flaky-quarantine#quarantine",
  "agent": "qa.lead",
  "quarantine": {
    "test_id": "CheckoutPromoIT#shouldApplyCode",
    "owner": "@squad-payments",
    "end_date": "2026-12-10",
    "ticket_id": "QA-1240",
    "reason": "Passes on rerun in 3 of 3 retries; fails on first run when the promo service is cold",
    "exit_criteria": "Warm-up step added and 10 consecutive green CI runs",
    "mechanism": "disabled-annotation"
  }
}
```

Matching test change:

```java
// QA-1240: quarantined until 2026-12-10, owner @squad-payments
@Disabled("QA-1240 promo-service cold start; exit: warm-up + 10 green runs")
@Test
void shouldApplyCode() { /* unchanged */ }
```

## Examples

- `../../examples/good-quarantine-record.json` — active record, expired record with escalation, and a recommendation
- `../../examples/bad-quarantine-record.json` — every rejection the checker makes
- `../../examples/good-pattern.md`, `../../examples/bad-pattern.md` — annotation forms

## Related Skills

- `failure-triage` — class and evidence before quarantine
- `flaky-quarantine#detect` — candidate and blocked-ticket findings
- `flaky-quarantine#expiry-review` — what happens at `end_date`
- `test-automation` — the fix that ends the quarantine

## Anti-Patterns

- `@Disabled` with no ticket, or a ticket only in a PR comment
- `end_date` far out so nobody looks at it
- Reason such as "flaky" with no counts
- Exit criteria such as "when fixed"
- Quarantining a `product_defect`
- Pushing the quarantine to `main`

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
