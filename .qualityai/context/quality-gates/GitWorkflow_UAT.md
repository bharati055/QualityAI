# Quality Gate: UAT

<!--
context_id: quality-gate-uat
owner_role: qa.lead
version: "1.0.0"
stage: UAT
last_reviewed: 2026-11-16
-->

## Purpose

User acceptance. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| UI/E2E smoke | yes | blocking | Business journeys |
| API | selective | warn |  |
| Integration | selective | warn |  |
| Performance | selective | warn |  |
| SOAK | no | info |  |
| Security checks | selective | blocking | Regulated paths |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.
