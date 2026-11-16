# Quality Gate: PR

<!--
context_id: quality-gate-pr
owner_role: qa.lead
version: "1.0.0"
stage: PR
last_reviewed: 2026-11-16
-->

## Purpose

Pull request / pre-merge. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| Unit | yes | blocking | All touched modules |
| API | yes | blocking | Changed endpoints |
| Integration | selective | warn | If cross-module change |
| Contract | selective | blocking | If provider/consumer changed |
| UI/E2E smoke | selective | warn | If UI critical path touched |
| Security checks | yes | blocking | Secrets/auth/input on trust boundary |
| Performance | no | info | Flag hot-path risk only |
| SOAK | no | info | Not at PR |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.
