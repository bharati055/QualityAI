# Gate: PR Review Gate

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `code-quality`
- Prior specialist findings for this concern

## Questions

- Is there a high-signal human summary?
- Are findings prioritized and actionable?

## Recommendation

| Result | When |
|---|---|
| fail | Report too noisy or missing critical context for a human reviewer |
| warn | Summary weak but findings usable |
| pass | Clear summary and prioritized actions |

## Output

- Gate id: `pr-review`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
