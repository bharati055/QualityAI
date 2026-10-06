# Gate: Security Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `security-patterns`
- Prior specialist findings for this concern

## Questions

- Secrets, injection, auth, and validation risks reviewed?
- High-severity security findings unresolved?

## Recommendation

| Result | When |
|---|---|
| fail | Unresolved high-severity security finding |
| warn | Medium security concerns needing follow-up |
| pass | No material unresolved security findings |

## Output

- Gate id: `security`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
