# AI vs Human Authority

Hard rules for every QualityAI workflow. See also root [DESIGN-PRINCIPLES.md](../../DESIGN-PRINCIPLES.md) §6.

## AI MAY

- Read code, tests, requirements, and `.qualityai/context/` (if a context file is still a **STUB**, treat facts as missing — do not invent from TODO placeholders)
- Suggest tests for a feature (types + cases) using shared skills + role scope
- Run PR review and emit evidence-backed findings
- Depict coverage and gaps (not coverage % alone)
- Draft test code or context updates when asked
- Open a **PR** (branch + pull request) when the host tool allows
- Recommend gate pass / warn / fail

## AI MUST NOT

- Push directly to `main` or other protected branches
- Merge PRs (including its own)
- Deploy to Prod / PreProd / UAT autonomously
- Silently edit strategy, stage gates, or other context without a PR
- Treat recommendations as already-enforced CI policy
- Claim model authorship as a blocking fact
- Force-push, delete protected history, or change permissions

## Human MUST

- Approve PRs that change product code, tests, or QualityAI context
- Own merge-to-main and release decisions
- Maintain or approve critical journeys, FMEA, and stage-gate criticality
- Override or escalate when confidence is low or risk is high

## Nuances

| Situation | Expected behavior |
|---|---|
| Feature code generated | AI suggests required tests; may draft tests on a branch |
| PR raised | AI reviews; does not merge |
| Context doc outdated | AI opens PR to update template-filled `.md`; human approves |
| Stage gate fail recommendation | Human decides ship / fix / waive |
| Secrets in diff | Report finding; never ask user to paste secrets into chat |
