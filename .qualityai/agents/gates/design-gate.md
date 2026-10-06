# Gate: Design Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `architecture-patterns`
- Prior specialist findings for this concern

## Questions

- Does implementation fit expected architecture/boundaries?
- Are anti-patterns or risky drift present?

## Recommendation

| Result | When |
|---|---|
| fail | High-severity architecture drift on a critical path |
| warn | Moderate layering/coupling concerns |
| pass | Design fit acceptable for the change size |

## Output

- Gate id: `design`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
