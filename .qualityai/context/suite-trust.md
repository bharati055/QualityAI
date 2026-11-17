> **STUB — implement as needed by this project.**
> This file is a placeholder template. Do not treat empty or TODO sections as product truth.
> Fill before relying on related skills/workflows; until then agents should say "context missing" rather than invent facts.
> Updates via PR only; human approval required.

# Suite Trust (Flaky / Quarantine Policy)

<!--
context_id: suite-trust
owner_role: qa.lead
status: stub
version: "0.1.0-stub"
last_reviewed: YYYY-MM-DD
-->

## Purpose

Project rules so regression failures mean real product risk. Feeds `failure-triage` and `flaky-quarantine`.

## Content (TODO — project fills)

### Flake detection thresholds

| Signal | Default to customize | Action |
|---|---|---|
| Intermittent fail without product change | e.g. ≥3 in 7 days | Candidate flaky |
| Pass-on-rerun rate | e.g. >30% | Investigate script/env |

### Quarantine requirements (mandatory fields)

Every quarantine MUST include:

- **owner** (team or person)
- **end_date** (ISO date)
- **ticket_id** (Jira or tracker)
- **reason**
- **exit_criteria**

### Expiry

- TODO: what Lead does when `end_date` passes without fix (recommend: blocking process finding)

### Allowed mute mechanisms

- TODO: `@Disabled` / tag / CI skip list — always with ticket link in code comment

## Links

- Skills `failure-triage`, `flaky-quarantine`; `quality-gates/`

## Change control

- Updates via PR only; human approval required.
