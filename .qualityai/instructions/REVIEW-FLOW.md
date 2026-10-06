# Review Flow

How QualityAI runs a review in a host repo.

## Entry

1. Load this file and `FINDING-SCHEMA.md`.
2. Default entry agent: `qa.orchestrator` (`.qualityai/agents/qa.orchestrator.agent.md`).
3. If the user names one concern (e.g. security only), run that specialist + its feedback agent, then still apply the matching gate.

## Inputs to gather

- Change set (diff, PR description, or listed files)
- Requirement text (ticket paste, AC, in-repo docs, or “none provided”)
- Host stack hints (optional): language, frameworks — do not require Java/Python unless relevant

## Phase A — Parallel specialists

Orchestrator invokes specialists that are relevant to the change. Prefer parallel reasoning when concerns are independent.

| Agent | Skill |
|---|---|
| `qa.researcher` | `requirement-alignment` |
| `qa.architect` | `architecture-patterns` (+ `performance-validation` when perf risk is clear) |
| `qa.tester` | `testing-patterns` |
| `qa.security-reviewer` | `security-patterns` |
| `qa.code-reviewer` | `code-quality` |
| `qa.ai-detector` | `ai-code-detection` |

Each specialist:

1. Reads its agent file
2. Follows the matching skill `SKILL.md` and the phase playbook (usually `review`)
3. Emits findings per schema
4. Hands output to its feedback agent (`qa.<role>.agent.feedback.md`)

## Phase B — Feedback validation

For each specialist report, the feedback agent:

- Confirms evidence exists
- Adjusts severity/confidence if over- or under-claimed
- Flags missing considerations (does not re-run the whole skill unless gaps are material)

## Phase C — Critic

`qa.critic` reconciles conflicts across specialists, calls out blind spots, and prioritizes business risk.

## Phase D — Sequential gates

Run gate files under `agents/gates/` in order. Each gate is a **recommendation**, not a merge block.

1. `requirement-gate.md`
2. `design-gate.md`
3. `ai-risk-gate.md`
4. `test-quality-gate.md`
5. `security-gate.md`
6. `pr-review-gate.md`
7. `deployment-readiness-gate.md`

## Phase E — Consolidated report

Orchestrator produces one report:

- Summary (short)
- Gate table: pass / warn / fail (recommended)
- Prioritized findings (schema)
- Recommended human actions
- Explicit statement: humans decide merge

## Read-only rule

Do not modify host code, merge, push, or deploy as part of this flow unless the user separately asks for implementation work outside QualityAI review.
