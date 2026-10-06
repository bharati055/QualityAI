# Gate: Test Quality Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `testing-patterns`
- Prior specialist findings for this concern

## Questions

- Are happy and failure paths covered where risk demands?
- Are assertions meaningful (not brittle/vacuous)?
- Are skipped/xfailed tests justified?

## Recommendation

| Result | When |
|---|---|
| fail | Critical path lacks failure-path tests or has hollow assertions |
| warn | Coverage gaps on non-critical but important paths |
| pass | Test quality adequate for change risk |

## Output

- Gate id: `test-quality`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
