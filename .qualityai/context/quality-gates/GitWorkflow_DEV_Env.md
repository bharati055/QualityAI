# Quality Gate: DEV Env

<!--
context_id: quality-gate-dev-env
owner_role: qa.lead
version: "1.0.0"
stage: DEV_Env
last_reviewed: 2026-11-16
-->

## Purpose

DEV environment verification. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| Unit | yes | blocking | CI green |
| API | yes | blocking |  |
| Integration | yes | blocking |  |
| Contract | selective | blocking |  |
| UI/E2E smoke | yes | warn | Smoke pack |
| Security checks | selective | warn |  |
| Performance | no | info |  |
| SOAK | no | info |  |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.
