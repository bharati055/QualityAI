# Gate: Requirements Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `requirement-alignment`
- Prior specialist findings for this concern

## Questions

- Is requirement intent clear and testable?
- Does the change map to acceptance criteria?
- Are gaps or drifts called out with evidence?

## Recommendation

| Result | When |
|---|---|
| fail | Critical AC unmet or large intent drift with high-severity findings |
| warn | AC incomplete or partial mapping |
| pass | Intent clear and change aligned (or N/A with documented reason) |

## Output

- Gate id: `requirement`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
