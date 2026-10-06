# QualityAI Project Requirements

## 1. Overview

QualityAI is an open-source library of **QA skills, specialist agents, and operating instructions**. Teams vendor it into any repository so AI-assisted coding agents can run requirement-aware, evidence-based quality review.

v1 is a **markdown drop-in pack** (typically `.qualityai/`). It encodes review methodology: what to check, how to check it, what is in or out of scope, and how to report findings. It is not a hosted platform, not a CI runner, and not an issue tracker.

The problem it addresses: AI-assisted delivery produces a high volume of syntactically valid code that often misses design intent, security, edge cases, requirement traceability, and meaningful tests. Existing linters and coverage numbers do not close that gap. QualityAI turns senior QA judgment into reusable artifacts any repo can consume.

Later addons (not v1) attach the pack to GitHub workflows/Actions, Jira requirement intake, GCO (GCP Monitoring), and an optional CLI/rules engine.

## 2. Problem Statement

Teams generate code quickly, open changes immediately, and rely on shallow review. Risks include:

- Changes pass basic tests but violate architecture or standards.
- Implementation drifts from requirement intent.
- Security, reliability, observability, and edge cases are skipped.
- Reviewers are overloaded and check the surface, not the risk.
- Coverage percentage is treated as quality.
- Tribal standards live in people’s heads, not in the repo.

QualityAI v1 does not replace human merge judgment. It gives every host repo the same specialist review playbooks and a shared finding contract so an AI agent (and a human) can review with depth.

## 3. Product Vision

Become the portable quality-and-trust **knowledge layer** for AI-assisted software delivery.

Engineering teams should be able to:

- vendor one pack and get consistent review behavior,
- validate changes against requirements and standards, not only tests,
- apply stricter review when changes look AI-assisted,
- keep methodology in skills (auditable, versioned) rather than in one-off prompts,
- later plug the same pack into CI, Jira, and telemetry without rewriting the brain.

## 4. Goals

### 4.1 Primary goals (v1)

- Ship a complete, coherent set of skills, agents, and instructions.
- Make the pack consumable by copying `.qualityai/` into any repo.
- Keep skills as the single source of methodology; agents only orchestrate and decide.
- Require evidence, severity, confidence, and skill citation on every finding.
- Encode lifecycle quality gates as agent/skill responsibilities, not CI jobs.

### 4.2 Secondary goals (later addons)

- GitHub workflows/Actions that invoke or comment using the same pack.
- Jira (and similar) requirement intake feeding the requirement-alignment skill.
- GCO (Google Cloud Monitoring / GCP Console) for three use cases: (1) create effective SLOs and alerts, (2) use service performance metrics to determine performance and load requirements, (3) use those metrics for test-failure RCA and reporting.
- Optional CLI/rules engine that evaluates the same skills deterministically where possible.

## 5. Scope

### 5.1 In scope for v1

- Drop-in directory layout: `agents/`, `skills/`, `instructions/`.
- All specialist agents, feedback pairs, orchestrator, critic, and gate instruction files.
- All canonical skills (folder-per-skill with `SKILL.md`, playbooks, coverage/gaps, examples, references).
- One shared playbook template that every skill playbook must follow (keeps structure consistent across all skills).
- Host-repo consumption contract (how to vendor and point the host agent at the pack).
- Finding/output schema (markdown + JSON-shaped fields) that later addons can consume unchanged.
- Honest coverage boundaries, especially for AI-assisted-code review (rubric, not a detector product).
- Language defaults: methodology is language-agnostic; when a code sample is required use Java; when a script is required use Python.
- This repository is the publishable open-source pack (docs at root + `.qualityai/` as the consumable tree).

### 5.2 Out of scope for v1

- GitHub Actions, workflows, PR bots, merge checks.
- Jira or other issue-tracker integrations.
- GCO or any production telemetry pipeline.
- CLI, YAML rules engine, language-specific scanners as required runtime.
- Merge blocking or org-wide policy enforcement.
- Full enterprise workflow orchestration, sandboxed code execution, replacing Jira/GitHub.
- Claiming reliable identification of Copilot vs Claude vs human authorship.

### 5.3 In scope later (addons)

- GitHub workflows/Actions adapter.
- Jira skill/adapter for issue and acceptance-criteria intake.
- GCO (GCP Monitoring / Console): SLOs/alerts; performance/load requirements from metrics; test-failure RCA/reporting.
- Optional CLI/API and GitLab/Jenkins/Slack adapters that call the same core later.

## 6. Target users

### 6.1 Primary (v1)

- Teams using Cursor or similar AI coding agents who want reusable QA review.
- Senior engineers, architects, and QA leads who want standards in-repo.
- Anyone vendoring quality methodology into many repositories.

### 6.2 Later

- Platform/DevOps teams wiring quality gates into CI.
- Engineering managers who want reports and telemetry.
- Security and compliance stakeholders who need audit trails from addons.

## 7. Core principles

### 7.1 Quality starts at requirements

A change is good only if it satisfies intended requirements and project standards.

### 7.2 Tests are necessary, not sufficient

Passing tests is a minimum. Skills must judge whether tests are meaningful and risk-aligned.

### 7.3 AI-assisted code needs higher scrutiny

v1 does not ship an authorship detector. The ai-code-detection skill is a **review-depth rubric**: when a change is large, generic, or likely AI-assisted, apply stricter checks. Do not claim a vendor-specific “signature” as fact.

### 7.4 Review quality must scale with volume

Agents specialize; feedback agents challenge findings; humans keep merge authority.

### 7.5 Standards must be codified in skills

Agents and prompts reference skills. They do not duplicate methodology.

### 7.6 Core is tool-agnostic

v1 runs wherever an agent can read markdown in the repo. GitHub, Jira, and GCO are addons.

### 7.7 Gates recommend; humans decide

v1 output is advisory. Enforcement is a later CI concern.

### 7.8 AI-era quality is continuous, not sample-based

Quality spans human and AI agents. Evolve from traditional sample-based auditing toward continuous, AI-enabled quality management across the delivery lifecycle.

### 7.9 AI systems need evaluation frameworks and HITL

AI agents, support bots, and recommendation engines require evaluation benchmarks, testing protocols, and human-in-the-loop workflows so they operate as intended and humans can override or escalate.

### 7.10 Audit AI outputs for intent, safety, tone, and hallucination

Continuously evaluate AI-generated outputs (e.g. support chats, recommendations, booking/transactional updates, AI-assisted code) for intent fulfillment, safety, tone, and hallucination prevention.

## 8. Functional requirements

### 8.1 Consumption contract

The system shall be consumable without GitHub or Jira.

Requirements:

- Host repos vendor `.qualityai/` (copy, subtree, or submodule).
- The pack SHALL be tool-agnostic: any markdown-capable coding agent can load it.
- v1 SHALL document a concrete Cursor wiring via host `AGENTS.md`. Other agents (Claude Code, Copilot, etc.) SHALL be supported by pointing their instruction file at `.qualityai/` (short note only; no separate pack per tool).
- Host instruction files SHALL tell agents to load `.qualityai/instructions/` and delegate to `.qualityai/agents/` and `.qualityai/skills/`.
- No network service SHALL be required for v1 review.
- Skill IDs and agent role names SHALL be stable so addons can attach later without renaming.
- This repository SHALL be the publishable open-source distribution, licensed under MIT.

### 8.2 Skills library

The system SHALL ship these canonical skills as directories (not flat single files):

| Skill ID | Primary gate / concern |
|---|---|
| `requirement-alignment` | Requirements / intent vs change |
| `architecture-patterns` | Design and architectural fit |
| `ai-code-detection` | AI-assisted review-depth rubric |
| `testing-patterns` | Test quality beyond coverage |
| `security-patterns` | Security and unsafe defaults |
| `code-quality` | Maintainability and review depth |
| `performance-validation` | Performance and reliability risk |

Each skill SHALL include: `SKILL.md`, phase playbooks, `coverage/COVERAGE.md`, `coverage/GAPS.md`, annotated examples, and references. Executable `tooling/` is optional and not required for v1.

### 8.3 Agent set

The system SHALL ship these roles (each with a feedback counterpart except where noted):

- `qa.orchestrator` — route work, merge findings, produce the consolidated recommendation
- `qa.researcher` — requirement alignment
- `qa.architect` — design and architecture
- `qa.tester` — test quality
- `qa.security-reviewer` — security and reliability
- `qa.code-reviewer` — code quality
- `qa.ai-detector` — apply the AI-assisted review-depth rubric (not vendor fingerprinting)
- `qa.critic` — conflicts, blind spots, over/under-claiming

Gate instruction files SHALL exist for: requirement, design, AI-risk, test quality, security, PR review, deployment readiness. They are sequential policy checks after specialist analysis, not CI jobs.

### 8.4 Instructions

The pack SHALL include operating instructions that cover:

- when to invoke which agent and skill,
- parallel specialist analysis vs sequential gates,
- finding schema and confidence bands,
- read-only behavior (analyze and recommend; do not modify host code),
- how host repos should reference the pack.

### 8.5 Finding and report contract

Every finding SHALL include: evidence (file/lines or explicit gap), severity, confidence, rationale, recommendation, and `skill_applied` using the canonical skill ID (for example `requirement-alignment#acceptance-criteria`).

The orchestrator SHALL produce one consolidated report with gate statuses (pass / warn / fail as **recommendations**), risk summary, and required human actions.

### 8.6 Requirement alignment (no Jira required)

v1 SHALL work from whatever requirement text the host provides (ticket paste, PR description, `docs/`, acceptance criteria in-repo). Jira sync is an addon. The skill SHALL still flag missing, untestable, or drifted intent.

### 8.7 Platform-agnostic core

Core skills and agents SHALL NOT depend on GitHub Actions, Jenkins, or Jira APIs. Optional integrations MUST be layered later as adapters that consume the same report contract.

## 9. Non-functional requirements

### 9.1 Explainability

Findings MUST be reproducible in the sense that the same skill and evidence trail can be followed by a human. Failing recommendations MUST name the skill (and section) violated.

### 9.2 Portability

The pack MUST be usable in small and large repos with only a markdown-capable agent. No required compile step for v1.

### 9.3 Usability

Reports MUST be concise and severity-ordered. Noise is a defect.

### 9.4 Security

v1 agents are read-only relative to the host codebase. They MUST NOT instruct silent code mutation, merge, or deploy. They MUST NOT request that secrets be pasted into chat.

### 9.5 Extensibility

New skills and agents MAY be added without renaming existing IDs. Addons MUST NOT fork methodology into workflow YAML.

## 10. Key user stories

### 10.1 Portable pack

- As a tech lead, I want to copy `.qualityai/` into a service repo so review quality does not depend on who is on the PR.
- As a developer using an AI coding agent, I want that agent to follow published skills instead of improvising a checklist.

### 10.2 Requirement-driven quality

- As a product owner, I want acceptance criteria used in review even when Jira is not connected.
- As a team lead, I want drift from intent called out with evidence.

### 10.3 AI-assisted scrutiny

- As a reviewer, I want large or generic AI-assisted diffs to trigger a stricter rubric, without fake certainty about which model wrote the code.

### 10.4 Test integrity

- As a QA engineer, I want weak assertions, missing failure paths, and skipped tests called out beyond coverage percentage.

### 10.5 Later addons

- As a platform engineer, I want a GitHub Action that posts the same report the agent already produces.
- As a delivery lead, I want Jira AC imported into the same requirement-alignment skill.
- As an SRE or QA lead, I want GCO metrics used for SLOs/alerts, load expectations, and test-failure RCA later.

## 11. Quality gates (logical, not CI)

These gates are instruction-level in v1:

1. **Requirements** — is the intent clear, testable, and reflected in the change?
2. **Design** — does implementation match expected architecture?
3. **AI-assisted risk** — does the change warrant deeper review?
4. **Test quality** — do tests validate behavior and risk, not just pass?
5. **Security and reliability** — are unsafe patterns and missing validation called out?
6. **PR review** — is there a high-signal summary for a human?
7. **Deployment readiness** — cumulative go/no-go **recommendation**.

## 12. Functional priorities

### Phase 1 — v1 pack (current)

- Complete agent set (including feedback pairs and critic).
- Complete canonical skill directories.
- Instructions and consumption contract.
- Finding/report schema.
- Host-repo onboarding documented in README.

### Phase 2 — addons

- GitHub workflows / Actions.
- Jira requirement intake skill/adapter.
- GCO (GCP Monitoring / Console): SLOs and alerts; performance/load requirement derivation from service metrics; test-failure RCA and reporting from those metrics.
- Optional CLI that emits the same report schema.

### Phase 3 — platform extras

- Additional CI adapters (Jenkins, GitLab, Slack).
- Org rule packs, dashboards, audit log storage.
- Deterministic scanners behind skills where they add signal.

## 13. Success metrics (v1)

v1 succeeds when:

- A host repo can run a specialist review using only the vendored pack.
- Findings cite skill ID + evidence; agents do not duplicate skill logic.
- A human can follow a finding back to a playbook section.
- The AI-assisted rubric increases review depth without claiming authorship as fact.
- Adding GitHub/Jira/GCO later does not require renaming skills or agents.

## 14. Risks and constraints

- Over-broad skills create review fatigue — coverage/GAPS.md is mandatory.
- AI-authorship claims will be wrong — v1 forbids them as blocking facts.
- Inconsistent names across docs would break consumption — canonical IDs in this file win.
- Markdown-only review is non-deterministic across models — instructions and examples must be strict; a later engine can add determinism.
- The pack must stay practical; it augments human judgment.

## 15. Future considerations

- More issue trackers than Jira.
- Domain skill packs (fintech, healthcare, SaaS).
- Review analytics via GCO.
- Expanded agent library only when a new concern does not fit an existing skill.

## 16. Conclusion

QualityAI v1 is the reusable QA brain: skills, agents, and instructions in a folder any repo can vendor. The platform around it — GitHub, Jira, GCO, CLI — is intentionally later, so the methodology stays portable and the addons stay thin.
