# Finding Schema

Every finding and the consolidated report MUST use these fields. Addons (GitHub, Jira, GCO) will consume the same contract later.

## Finding object

```json
{
  "finding": "Short statement of the issue",
  "evidence": {
    "file": "path/or/null-if-process-gap",
    "lines": "optional-range",
    "code_snippet": "optional short excerpt",
    "note": "If no file, explain the gap (e.g. missing AC)"
  },
  "severity": "high|medium|low",
  "confidence": 0.0,
  "rationale": "Why this matters for risk or requirement intent",
  "recommendation": "Concrete next action for a human",
  "skill_applied": "skill-id#section-or-phase",
  "agent": "qa.role-name"
}
```

### Confidence bands

| Range | Meaning |
|---|---|
| 0.95–1.00 | Definitive (e.g. hardcoded secret string) |
| 0.85–0.94 | High |
| 0.70–0.84 | Moderate |
| 0.50–0.69 | Low — prefer warn, invite human judgment |
| &lt; 0.50 | Uncertain — escalate; do not treat as blocking fact |

### Severity

- **high** — plausible production harm, security, data loss, or critical path without validation/tests
- **medium** — meaningful quality gap, limited blast radius
- **low** — maintainability or polish; do not flood the report

### `skill_applied`

Use canonical IDs only:

`requirement-alignment`, `architecture-patterns`, `ai-code-detection`, `testing-patterns`, `security-patterns`, `code-quality`, `performance-validation`

Example: `testing-patterns#review` or `security-patterns#input-validation`

## Report envelope

```json
{
  "status": "pass|warn|fail",
  "summary": "One or two sentences",
  "riskScore": 0,
  "confidence": 0.0,
  "gates": {
    "requirement": "pass|warn|fail",
    "design": "pass|warn|fail",
    "aiRisk": "pass|warn|fail",
    "testQuality": "pass|warn|fail",
    "security": "pass|warn|fail",
    "prReview": "pass|warn|fail",
    "deploymentReadiness": "pass|warn|fail"
  },
  "findings": [],
  "recommendedActions": []
}
```

`status` and gate values are **recommendations**. Never imply the agent merged or blocked the change.

## Markdown rendering (for humans)

```markdown
## QualityAI report

**Recommended status:** fail
**Summary:** ...

### Gates
| Gate | Recommendation |
|---|---|
| requirement | pass |
| ... | ... |

### Findings
1. **[high]** ... (`skill_applied`, confidence)
   - Evidence: ...
   - Recommendation: ...

### Recommended actions
- ...
```
