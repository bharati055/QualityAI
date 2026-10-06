# Gate: AI-Assisted Risk Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `ai-code-detection`
- Prior specialist findings for this concern

## Questions

- Does the change warrant elevated review depth?
- Were stricter checks applied if yes?

## Recommendation

| Result | When |
|---|---|
| fail | High review-depth warranted but specialist/security/test gaps remain unaddressed |
| warn | Elevated depth recommended; residual medium findings |
| pass | Normal depth sufficient or elevated depth completed cleanly |

## Output

- Gate id: `ai-risk`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
