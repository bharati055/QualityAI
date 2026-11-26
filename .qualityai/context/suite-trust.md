# Suite Trust (Flaky / Quarantine Policy)

<!--
context_id: suite-trust
owner_role: qa.lead
version: "1.0.0"
last_reviewed: 2026-11-26
-->

## Purpose

Rules so a red regression run means real product risk. Feeds `failure-triage` and `flaky-quarantine`. The numbers below are defaults; the host Lead edits them by PR when the suite's history says otherwise.

## Scope

- In scope: when a test counts as a flake candidate, when it may be quarantined, how it may be muted, what happens when the quarantine ends
- Out of scope: Jira or GitHub issue creation (a human files the ticket in v1), fixing the test (the owner does that)

## Content

### Flake detection thresholds

Counted per `test_id`, on CI runs of the default branch or of a PR, over a rolling window.

| Signal | Default | Action |
|---|---|---|
| Failed, then passed on rerun of the same commit | 1 time | Suspect: note it, no action |
| Intermittent failure with no product change touching the test or code under test | 3 or more in 7 days | Candidate flaky: run `failure-triage` |
| Pass-on-rerun rate over the last 20 runs | above 30% | Investigate script and environment first (`test_script_issue` or `environment`) |
| Same test red on 3 consecutive runs | 3 runs | Not a flake: treat as `product_defect` until triage says otherwise |

Auto-retry is allowed once per test. A pass that needed a retry still counts as a failure for the first two rows.

### When quarantine is allowed

| Triage class | Quarantine? |
|---|---|
| `test_script_issue` with flake evidence | Yes |
| `environment` with flake evidence | Yes, when the test cannot be isolated from the environment |
| `product_defect` | No. File the defect; the test stays active |
| `unknown` | No. Collect more evidence first |

A test on a critical journey (`journeys/`) needs Lead approval in the PR and a named compensating check in `reason`. Escalate when quarantined tests exceed 5% of a suite, or when the same test is quarantined a third time.

### Quarantine requirements (mandatory fields)

Every quarantine recommendation and record MUST include:

- **owner** (team or person)
- **end_date** (ISO date)
- **ticket_id** (Jira or tracker)
- **reason**
- **exit_criteria**

Plus `test_id`. Format, examples, and the checker: `skills/flaky-quarantine/references/quarantine-metadata.md`. Records live in `.qualityai/quarantine/*.json` of the host repo.

| Setting | Default |
|---|---|
| Default window | 30 days from the PR that applies the quarantine |
| Longest `end_date` the checker accepts | 90 days ahead |
| Extensions | One, approved by the Lead in a PR that states why; a second one goes to the Architect |

If no ticket exists yet, the AI emits a `flaky-quarantine#detect` finding that names the missing ticket. A human files the ticket, then the quarantine is applied by PR with the real `ticket_id`.

### Expiry

When `end_date` passes and the test is still muted, the Lead (`qa.lead`) records a `flaky-quarantine#expiry-review` finding naming the `ticket_id`: severity high on a critical journey, otherwise medium. Within one working day the owner does one of:

1. Fixes the test and removes the mute and the record
2. Gets a Lead-approved extension through a PR
3. Deletes the test, with human approval and a note on where the risk is now covered

The pack checker fails a PR that carries an expired record without that finding.

### Allowed mute mechanisms

| Mechanism | Rule |
|---|---|
| `@Disabled("QA-1234 reason")` or the framework's skip marker | Ticket id in the reason string, or in the comment line directly above |
| Quarantine tag (`@Tag("quarantine")`) with a CI profile that excludes the tag | Ticket id as above, plus a registry record |
| CI skip list | The registry file `.qualityai/quarantine/*.json` is the list; no other list |

Not allowed: commenting out or deleting a test to get green, blanket `continue-on-error`, raising retries until it passes, conditional skips used as a mute, any mute without a ticket id. The checker flags unticketed mute annotations in test sources.

## Links

- Skills `failure-triage`, `flaky-quarantine`; `quality-gates/`
- `../instructions/WORKFLOWS.md` §4, `../instructions/FINDING-SCHEMA.md`

## Change control

- Updates via PR only; human approval required.
