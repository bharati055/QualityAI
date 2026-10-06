# Gate: Deployment Readiness Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `performance-validation`
- Prior specialist findings for this concern

## Questions

- Cumulative gate recommendations considered?
- Any unresolved high risk on critical path?
- Perf/reliability risks called out when relevant?

## Recommendation

| Result | When |
|---|---|
| fail | Any blocking high-risk recommendation remains |
| warn | Residual medium risks; deploy with caution / follow-ups |
| pass | No unresolved high risks; residual risk accepted or none |

## Output

- Gate id: `deployment-readiness`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
