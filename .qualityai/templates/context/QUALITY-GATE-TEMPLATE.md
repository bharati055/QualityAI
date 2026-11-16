# GitWorkflow_[STAGE] Template

```markdown
# Quality Gate: [STAGE]

<!--
context_id: quality-gate-[stage]
owner_role: qa.lead
version: "1.0.0"
stage: [PR|DEV|SIT|UAT|PreProd|Prod]
last_reviewed: YYYY-MM-DD
-->

## Purpose

Which test types run (or must have passed) at this stage, and at what criticality.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| Unit | yes/no | blocking/warn/info | |
| API | | | |
| Integration | | | |
| Contract | | | |
| UI/E2E smoke | | | |
| Security checks | | | |
| Performance | | | |
| SOAK | | | |

## Entry / exit criteria

- Entry: ...
- Exit: ...

## AI vs human

- AI may recommend fail/warn based on this matrix.
- Human decides merge/promote. AI never promotes to this env autonomously.

## Change control

- Updates via PR only; human approval required.
```
