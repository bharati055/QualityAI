# QualityAI Architecture

## 1. Overview

QualityAI v1 is a **portable markdown pack**: agents, skills, and instructions that a host repository vendors under `.qualityai/`. An AI coding agent in that repo reads the pack and runs a specialist quality review.

The platform split remains:

1. **v1 core pack** — tool-agnostic, copyable, no CI or tracker required.
2. **Later addons** — GitHub Actions/workflows, Jira intake, GCO telemetry, optional CLI/rules engine. Addons consume the pack’s report contract; they do not own methodology.

## 2. Design goals

- Start from requirements (whatever text the host provides), not only from tests.
- Treat likely AI-assisted changes with a stricter **review-depth rubric**, not a fake authorship detector.
- Keep standards in skills; keep agents thin.
- Stay independent of GitHub, Jira, and GCO in v1.
- Preserve a stable layout and IDs so addons can attach later.

## 3. High-level architecture (v1)

```text
Host repository
  AGENTS.md (or equivalent) --> .qualityai/instructions/
                                    |
                                    v
                             .qualityai/agents/     (orchestrate, decide)
                                    |
                                    v
                             .qualityai/skills/     (methodology)
                                    |
                                    v
                             Quality report (markdown + finding fields)
```

Later addons wrap the same report:

```text
GitHub Action / Jira adapter / GCO exporter  -->  same finding schema
```

## 4. Architectural principles

### 4.1 Pack is CI-agnostic

v1 runs locally in any repo whose agent can read `.qualityai/`. No GitHub Action is required.

### 4.2 Integrations are addons

GitHub, Jira, GCO, Jenkins, GitLab, Slack call or display pack output. They do not embed checklists.

### 4.3 Requirements are the source of truth

Missing, vague, or untested intent is a gate finding. Jira is one future source, not the v1 dependency.

### 4.4 Quality is multi-layered

Requirement alignment, architecture, AI-assisted scrutiny, tests, security, code quality, performance, deployment readiness.

### 4.5 Specialized agents with feedback

Specialists analyze; feedback counterparts challenge; orchestrator and critic consolidate.

## 5. v1 repository structure (this project and consumer repos)

Canonical layout for the pack (what v1 implements and what hosts vendor):

```text
.qualityai/
├── README.md
├── instructions/
│   ├── CONSUME.md                 # tool-agnostic contract + Cursor AGENTS.md example
│   ├── REVIEW-FLOW.md             # parallel specialists then sequential gates
│   ├── FINDING-SCHEMA.md          # evidence / severity / confidence contract
│   └── operating-principles.md    # pointer to DESIGN-PRINCIPLES.md
│
├── templates/
│   └── PLAYBOOK-TEMPLATE.md       # shared structure for every skill playbook
│
├── agents/
│   ├── qa.orchestrator.agent.md
│   ├── qa.orchestrator.agent.feedback.md
│   ├── qa.researcher.agent.md
│   ├── qa.researcher.agent.feedback.md
│   ├── qa.architect.agent.md
│   ├── qa.architect.agent.feedback.md
│   ├── qa.tester.agent.md
│   ├── qa.tester.agent.feedback.md
│   ├── qa.security-reviewer.agent.md
│   ├── qa.security-reviewer.agent.feedback.md
│   ├── qa.code-reviewer.agent.md
│   ├── qa.code-reviewer.agent.feedback.md
│   ├── qa.ai-detector.agent.md
│   ├── qa.ai-detector.agent.feedback.md
│   ├── qa.critic.agent.md
│   ├── qa.critic.agent.feedback.md
│   └── gates/
│       ├── requirement-gate.md
│       ├── design-gate.md
│       ├── ai-risk-gate.md
│       ├── test-quality-gate.md
│       ├── security-gate.md
│       ├── pr-review-gate.md
│       └── deployment-readiness-gate.md
│
└── skills/
    ├── requirement-alignment/
    ├── architecture-patterns/
    ├── ai-code-detection/
    ├── testing-patterns/
    ├── security-patterns/
    ├── code-quality/
    └── performance-validation/
```

Each skill directory follows [SKILLS-FRAMEWORK.md](SKILLS-FRAMEWORK.md): `SKILL.md`, `playbook/`, `coverage/`, `examples/`, `references/`. Optional `tooling/` is not required for v1.

This QualityAI repo currently holds product docs at the root. The `.qualityai/` tree is the v1 implementation target.

### 5.1 Explicitly not v1

Do not treat these as required to consume the pack:

- `cli.ts`, `config.yml` rules engine, language YAML packs
- `.github/workflows`, Jira sync, GCO exporters
- `integrations/` adapters

Those belong in a future `addons/` (or similar) tree.

## 6. Core components (v1)

### 6.1 Instructions

Teach the host agent how to load the pack, which specialists to run, how gates sequence, and how to emit findings.

### 6.2 Agents

Orchestrator routes. Specialists each own one concern and **only** invoke their skills. Feedback agents validate evidence and confidence. Critic looks for conflicts and missed risk.

### 6.3 Skills

Folder-per-skill methodology. Canonical IDs (stable):

| ID | Used by |
|---|---|
| `requirement-alignment` | `qa.researcher`, requirement gate |
| `architecture-patterns` | `qa.architect`, design gate |
| `ai-code-detection` | `qa.ai-detector`, AI-risk gate |
| `testing-patterns` | `qa.tester`, test-quality gate |
| `security-patterns` | `qa.security-reviewer`, security gate |
| `code-quality` | `qa.code-reviewer` |
| `performance-validation` | `qa.architect` / `qa.tester` as relevant, deployment gate |

### 6.4 Report

Markdown summary plus structured finding fields (see §10). Addons later convert this to PR comments, Jira notes, or GCO events.

## 7. Multi-agent review model

Unchanged in spirit: orchestrator + specialists + feedback pairs + sequential gates + critic.

### 7.1 Roles

- Researcher: requirement alignment and intent
- Architect: design and architectural consistency
- Tester: test quality and edge cases
- Security-reviewer: security and reliability
- Code-reviewer: maintainability
- AI-detector: stricter review rubric for likely AI-assisted or high-volume generated change (no vendor fingerprint claims)
- Critic: conflicts, blind spots, business risk
- Orchestrator: routing, merge, final recommendation

### 7.2 Feedback pairs

Primary agent analyzes; `qa.[role].agent.feedback.md` asks whether each finding is justified, evidenced, and correctly severitized.

### 7.3 Sequential gates

After parallel specialists:

1. requirement-gate
2. design-gate
3. ai-risk-gate
4. test-quality-gate
5. security-gate
6. pr-review-gate
7. deployment-readiness-gate

Gates are markdown instructions, not pipeline jobs.

## 8. Quality review flow (v1)

```text
Change + requirement text in the host repo
          |
          v
Instructions (CONSUME + REVIEW-FLOW)
          |
          v
Orchestrator selects specialists
          |
          v
Parallel specialist analysis (each -> skills)
          |
          v
Feedback validation
          |
          v
Sequential gates
          |
          v
Critic + orchestrator consolidated report
          |
          v
Human decides (v1 never merges)
```

Jira sync is not in this flow until the Jira addon exists. Requirement text may be a PR description, ticket paste, or in-repo docs.

## 9. Agent responsibilities (summary)

- **Orchestrator:** parse context, invoke agents, merge findings, run gates, write the report.
- **Specialists:** one concern; delegate to named skills; never inline a second skill’s checklist.
- **Feedback:** evidence, over-claim, under-claim, missing consideration.
- **Critic:** cross-agent consistency and residual business risk.

## 10. Finding and report contract

v1 has no CLI. The contract is the document schema later engines and Actions MUST reuse.

Finding:

```json
{
  "finding": "Missing input validation on user-supplied data",
  "evidence": {
    "file": "src/api/payment.ts",
    "lines": "45-50",
    "code_snippet": "const amount = req.body.amount;"
  },
  "severity": "high",
  "confidence": 0.95,
  "rationale": "Unvalidated amount on a payment path.",
  "recommendation": "Validate amount as a positive number before processing.",
  "skill_applied": "security-patterns#input-validation",
  "agent": "qa.security-reviewer"
}
```

Report envelope:

```json
{
  "status": "fail",
  "summary": "High risk: payment path lacks validation; tests miss failure cases.",
  "riskScore": 82,
  "confidence": 0.91,
  "gates": {
    "requirement": "pass",
    "design": "warn",
    "aiRisk": "warn",
    "security": "fail",
    "testQuality": "fail",
    "prReview": "fail",
    "deploymentReadiness": "fail"
  },
  "findings": [],
  "recommendedActions": []
}
```

`status` and gate values are **recommendations**.

## 11. Later addon architecture

Addons stay thin.

### 11.1 GitHub workflows / Actions

Trigger on PR, gather diff metadata, run or attach an agent review, post the report, optionally fail the job if the host chooses enforcement.

### 11.2 Jira

Import issues and acceptance criteria into the same `requirement-alignment` skill. Do not invent a second requirements methodology.

### 11.3 GCO (Google Cloud Monitoring / GCP Console)

Not part of v1 runtime. Later addon use cases:

1. **SLOs and alerts** — define and operate SLOs/alerts in GCO from quality and reliability signals.
2. **Performance and load requirements** — use service performance metrics to derive performance and load expectations that skills/gates can check against.
3. **Test-failure RCA** — correlate metrics with failing tests to support root-cause analysis and reports.

Optional secondary telemetry (pack version, gate outcomes, finding counts) may share the same pipeline but is not the primary GCO story.

### 11.4 Optional CLI / rules engine

A future `qualityai analyze` command may emit the same schema. It must load the same skill IDs. It is not the v1 install path.

### 11.5 Other CI (Jenkins, GitLab, Slack)

Same adapter pattern as GitHub: call or render the report.

## 12. Consumer setup (v1)

```text
project-root/
├── .qualityai/          # vendored pack
├── AGENTS.md            # Cursor example: "Use .qualityai/instructions and agents"
├── src/
└── README.md
```

Example:

```bash
cp -r QualityAI/.qualityai ./my-service/.qualityai
```

Then add a short pointer in the host `AGENTS.md`. GitHub/Jira/GCO setup scripts are phase 2.

## 13. Data flow

**v1 inputs:** host code/diff, requirement text in-repo or in the prompt, pack files.

**v1 processing:** specialists → skills → feedback → gates → report.

**v1 outputs:** markdown report for humans and agents.

**Later inputs/outputs:** Jira issues, PR metadata, GCO metrics, CI status.

## 14. Security and safety

- v1 agents analyze and recommend only; they do not modify host code, merge, or deploy.
- No arbitrary code execution required to use the pack.
- Do not log secrets. Do not ask users to paste credentials.
- Findings trace to skill IDs.

## 15. Evolution

| Phase | Ships |
|---|---|
| 1 (v1) | `.qualityai/` agents, skills, instructions, schema |
| 2 | GitHub Actions/workflows, Jira intake, GCO telemetry |
| 3 | Optional CLI/engine, more CI adapters, org packs |

## 16. Conclusion

v1 architecture is a drop-in quality brain. Keep the engine and adapters off the critical path until the pack is complete and stable. Addons must remain consumers of skills and of the finding schema, never a second source of QA truth.
