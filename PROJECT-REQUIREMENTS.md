# QualityAI Project Requirements

## 1. Overview

QualityAI is an open-source library of **QA role-agents, shared testing skills, host context docs, and operating instructions**. Teams vendor it into any repository so AI coding agents can **scale testing** as product code and features grow—without hiring QA headcount 1:1.

v1 is a **markdown drop-in pack** (typically `.qualityai/`). The **headline job is test scaling**: suggest the tests a feature needs when code is generated (including toward more autonomous coding), depict coverage and gaps, and run PR quality review as a first-class workflow. It is not a hosted platform or a merge-blocking CI product (CI adapters come later).

The problem it addresses: AI-assisted delivery increases feature velocity faster than human QA can keep up. Traditional sample-based auditing and tribal Confluence knowledge do not scale. QualityAI turns a QA org model (Engineer / Lead / Architect) plus shared craft skills into in-repo, AI-readable artifacts any squad can consume—with a hard **AI vs human** boundary (e.g. AI may open a PR; only humans approve merge to main).

Later addons (not v1) attach the pack to GitHub workflows/Actions, Jira requirement intake, GCO (GCP Monitoring), and an optional CLI/rules engine.

## 2. Problem Statement

Teams generate code quickly, open changes immediately, and rely on shallow review. Risks include:

- Feature code ships without a proportional test strategy (unit, API, integration, contract, security, performance, SOAK).
- Changes pass basic tests but violate architecture or standards.
- Implementation drifts from requirement intent.
- Security, reliability, observability, and edge cases are skipped.
- Reviewers are overloaded and check the surface, not the risk.
- Coverage percentage is treated as quality; gaps in critical journeys stay invisible.
- Tribal standards live in Confluence or people’s heads, not in machine-readable repo docs.
- Hiring more human QA per squad does not scale with autonomous / AI-generated feature volume.

QualityAI does not replace human merge judgment or human ownership of release risk. It gives every host repo the same role-agents, shared skills, and context docs so AI can take volume work (suggest tests, gap analysis, PR review) while humans approve what lands on main.

## 3. Product Vision

Become the portable **AI-enabled QA operating model** for software delivery: scale test design, coverage visibility, and review depth with product growth.

Engineering teams should be able to:

- vendor one pack and get consistent QA behavior across squads,
- map AI agents to central QA roles (Engineer, Lead/Manager, Architect) with different scope,
- share testing skills (API, automation, performance, SOAK, unit, security, integration, contract) across those roles,
- keep product/framework/strategy knowledge in templated, AI-readable `.md` context docs,
- suggest tests when feature code is generated; review when a PR is raised; report coverage and gaps,
- later plug the same pack into CI stage gates, Jira, and GCO without rewriting the brain.

## 4. Goals

### 4.1 Primary goals (v1)

- Ship a coherent set of **role-agents**, **shared test-type skills**, **context doc templates**, and instructions.
- Make the pack consumable by copying `.qualityai/` into any repo.
- Headline workflows: **suggest tests for a feature**, **PR review**, **coverage & gap depiction**.
- Keep skills as the single source of methodology; agents apply skills within their role scope.
- Require evidence, severity, confidence, and skill citation on every finding.
- Encode AI vs human authority explicitly (HITL): what AI may propose vs what only humans may approve.
- Encode lifecycle / env quality gates as documented combinations of test types and criticality (PR → DEV → SIT → UAT → PreProd → Prod), as context—not as required live CI in v1.

### 4.2 Secondary goals (later addons)

- GitHub workflows/Actions that invoke or comment using the same pack.
- Jira (and similar) requirement intake feeding the requirement-alignment skill.
- GCO (Google Cloud Monitoring / GCP Console) for three use cases: (1) create effective SLOs and alerts, (2) use service performance metrics to determine performance and load requirements, (3) use those metrics for test-failure RCA and reporting.
- Optional CLI/rules engine that evaluates the same skills deterministically where possible.

## 5. Scope

### 5.1 In scope for v1

- Drop-in directory layout: `agents/`, `skills/`, `instructions/`, `context/` (templated host knowledge), `templates/`.
- Role-agents aligned to a QA org model (Engineer / Lead / Architect) plus orchestrator/critic/feedback as needed; specialist concern agents may remain as skills-facing helpers during transition.
- Shared test-type and quality skills (folder-per-skill with `SKILL.md`, playbooks, coverage/gaps, examples, references), evolving toward: API, test automation, performance, SOAK, unit, security, integration, contract — alongside existing requirement/architecture/code-quality skills.
- One shared playbook template that every skill playbook must follow.
- Machine-readable **context doc templates** for test strategy, test types, automation frameworks (e.g. Selenium/Playwright), performance frameworks (e.g. Gatling/JMeter), and env/stage quality gates (PR, DEV, SIT, UAT, PreProd, Prod).
- Three headline workflows: feature test suggestion, PR review, coverage/gap report.
- Host-repo consumption contract (how to vendor and point the host agent at the pack).
- Finding/output schema (markdown + JSON-shaped fields) that later addons can consume unchanged.
- Explicit **AI can / cannot** and **human must** boundary document.
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

v1 output is advisory. Enforcement is a later CI concern. AI must not push to `main` or bypass human approval.

### 7.11 Scale testing with AI role-agents, not headcount

Map QA Manager/Lead, QA Architect, and squad QA Engineers to AI agents. Shared skills provide craft; role scope and context docs provide altitude (squad vs cross-app vs system).

### 7.12 Context docs are first-class knowledge

Product area, frameworks, test strategy, and stage gates live as templated `.md` under `.qualityai/context/` (or host equivalent). Humans author; AI may propose updates only via PR for human approval.

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

Skills are **shared craft** used by multiple role-agents. The system SHALL ship skills as directories (not flat single files).

**Current canonical skills (shipped):**

| Skill ID | Primary concern |
|---|---|
| `requirement-alignment` | Requirements / intent vs change |
| `architecture-patterns` | Design and architectural fit |
| `ai-code-detection` | AI-assisted review-depth rubric |
| `testing-patterns` | Test quality beyond coverage (umbrella; split over time) |
| `security-patterns` | Security and unsafe defaults |
| `code-quality` | Maintainability and review depth |
| `performance-validation` | Performance and reliability risk |

**Test-type and suite-trust skills (split from umbrella / new):**

| Skill ID | Concern |
|---|---|
| `api-testing` | API test design and review |
| `test-automation` | UI/E2E automation (e.g. Selenium/Playwright) patterns |
| `unit-testing` | Unit-level design and quality |
| `integration-testing` | Service/component integration |
| `contract-testing` | Consumer/provider contracts |
| `soak-testing` | Endurance / soak scenarios |
| `failure-triage` | Classify failures: product vs test script vs environment |
| `flaky-quarantine` | Identify flakes; quarantine with owner, end date, ticket ID |
| (existing) `security-patterns`, `performance-validation`, `testing-patterns` | Security; load/perf; umbrella patterns still valid |

Each skill SHALL include: `SKILL.md`, phase playbooks, `coverage/COVERAGE.md`, `coverage/GAPS.md`, annotated examples, and references. Executable `tooling/` is optional and not required for v1.

### 8.3 Role-agent model

Agents map to a scalable QA org. Shared skills + different **scope/context** per role.

| Role-agent | Scope / knowledge | Typical use of skills |
|---|---|---|
| `qa.engineer` (squad) | Product area + framework details from squad context docs | Design/suggest local tests; apply API/unit/automation skills in-area |
| `qa.lead` (manager) | Cross-app features, integrations, external dependencies, critical user journeys | Journey coverage, cross-system gaps, stage-gate fitness |
| `qa.architect` | SUT technical architecture, FMEA/failure modes, performance metrics, observability | System risk, perf/SOAK strategy, architectural testability |
| `qa.orchestrator` | Routes workflows; consolidates reports | Invokes role-agents + skills per workflow |
| `qa.critic` (+ feedback pairs) | Cross-checks | Reduce false positives / blind spots |

Transitional note: existing concern agents (`qa.tester`, `qa.security-reviewer`, etc.) MAY remain until role-agents fully absorb their routing; skill IDs stay stable.

Gate instruction files SHALL exist for: requirement, design, AI-risk, test quality, security, PR review, deployment readiness. Stage/env gate **definitions** (which test types run at PR/DEV/SIT/UAT/PreProd/Prod and at what criticality) SHALL live in context docs; live CI enforcement is an addon.

### 8.3a Headline workflows

The pack SHALL support these entry workflows (orchestrator-routed):

1. **Feature test suggestion** — When feature code is generated or proposed, recommend required test types and cases from requirements + context (strategy, test_types, frameworks, stage gates), aimed at autonomous-ready delivery.
2. **PR review** — When a PR is raised, run role-appropriate review (code, tests, security, alignment) and produce a finding report.
3. **Coverage & gaps** — Depict what is covered vs missing against AC, critical journeys, and stage-gate expectations (not coverage % alone).

### 8.3b Context knowledge pack

Host (or org) knowledge SHALL be stored as templated, AI-readable markdown under `.qualityai/context/` (humans maintain; AI may propose updates only via PR).

Minimum template set:

- `test-strategy.md` — overall QA approach
- `test-types.md` — definitions and when to use each type
- `test-automation-framework.md` — e.g. Selenium / Playwright details
- `performance-testing.md` — approach + Gatling/JMeter (or equivalent) details
- `quality-gates/` — stage docs: `GitWorkflow_PR.md`, `GitWorkflow_DEV_Env.md`, `GitWorkflow_SIT.md`, `GitWorkflow_UAT.md`, `GitWorkflow_PreProd.md`, `GitWorkflow_Prod.md` (each: test-type combination + criticality)
- `squad/` — product-area and framework notes for `qa.engineer`
- `journeys/` — critical user journeys and cross-app deps for `qa.lead`
- `architecture/` — SUT architecture, FMEA, observability/perf signals for `qa.architect`

### 8.3c AI vs human authority

The pack SHALL document and enforce in instructions:

| AI MAY | Human MUST |
|---|---|
| Read code, tests, context, requirements | Own release/merge risk |
| Suggest tests, gaps, and review findings | Approve merges to `main` / protected branches |
| Draft test code or context doc updates | Approve PRs that change product code, tests, or context |
| Open a PR (when the host tool allows) | Review and approve that PR |
| Recommend gate pass/warn/fail | Decide to merge, ship, or override |

AI MUST NOT: push directly to `main`, merge its own PRs, deploy to Prod, silently edit protected context without a PR, or present recommendations as completed enforcement.

### 8.4 Instructions

The pack SHALL include operating instructions that cover:

- when to invoke which role-agent and skill,
- the three headline workflows,
- how to load `.qualityai/context/` by role scope,
- parallel analysis vs sequential gates,
- finding schema and confidence bands,
- AI vs human boundary,
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

- As a tech lead, I want to copy `.qualityai/` into a service repo so QA quality does not depend on who is on the PR.
- As a developer using an AI coding agent, I want that agent to follow published skills instead of improvising a checklist.

### 10.2 Scale testing without linear hiring

- As an engineering manager, I want AI role-agents (Engineer/Lead/Architect) to absorb test-design and gap volume as features grow.
- As a developer generating a feature, I want suggested tests (types + cases) before/while code is written so autonomous delivery stays testable.

### 10.3 PR review and coverage gaps

- As a reviewer, I want a QualityAI PR review with evidence-backed findings.
- As a QA lead, I want coverage and gaps depicted against AC, journeys, and stage gates—not only coverage %.

### 10.4 Context as code

- As a QA architect, I want test strategy, frameworks, and env gates as templated `.md` in-repo so AI and humans share one source of truth.
- As a human approver, I want AI context updates only via PR.

### 10.5 AI vs human

- As a platform owner, I want AI never to push to main; it may open a PR that I approve.

### 10.6 Later addons

- As a platform engineer, I want GitHub Actions to enforce stage-gate combinations documented in context.
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

- Role-agents: `qa.engineer`, `qa.lead`, `qa.architect` (+ orchestrator/critic; specialists remain as helpers).
- Shared skills including split test-type skills and suite-trust skills (`failure-triage`, `flaky-quarantine`).
- Context templates (strategy, test types, frameworks, stage gates, squad/journeys/architecture).
- Workflows: feature test suggestion, PR review, coverage/gaps, failure triage / quarantine recommendations.
- AI vs human boundary; finding schema; consumption contract.
- Industry alignment documented (this file §17).

### Phase 2 — autonomy, independence, suite trust, first addons

- **Risk-tiered autonomy** — low/medium/high change tiers map to HITL depth (align with Anthropic-style approval tiers).
- **Independent test generation from specs** — QA agents derive tests from AC/journeys/FMEA, not only from coding-agent output (avoid shared-assumption green tests).
- **Eval / incident harness** — turn incidents, reverts, and false positives into regression eval cases for agents/skills.
- **Flaky quarantine enforcement hooks** — owner, end date, Jira ID required in CI metadata (Jira sync as adapter).
- GitHub Actions that **comment** QualityAI reports; begin wiring context `quality-gates/` as advisory checks.
- Jira requirement intake + quarantine ticket linkage.
- GCO: SLOs/alerts; perf/load from metrics; test-failure RCA.

### Phase 3 — CI enforcement & platform

- **CI enforcement** of GitWorkflow matrices (PR/DEV/SIT/UAT/PreProd/Prod) as merge/promote gates.
- Additional CI adapters (Jenkins, GitLab, Slack).
- Org rule packs, dashboards, audit log storage.
- Deterministic scanners behind skills; optional CLI emitting the same schema.

## 13. Success metrics (v1)

v1 succeeds when:

- A host repo can run **test suggestion**, **PR review**, and **coverage/gap** workflows from the vendored pack + filled context templates.
- Role-agents use shared skills but different context altitude (squad vs journeys vs architecture/FMEA).
- Findings cite skill ID + evidence; agents do not duplicate skill logic.
- AI never merges to main; human approval is required for PRs that change code, tests, or context.
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

## 16. Suite trust: flaky tests, quarantine, failure triage

A regression suite is only useful if failures indicate **genuine product risk**. QualityAI SHALL include skills and playbooks for:

### 16.1 Failure triage

Classify failures into at least:

| Category | Meaning |
|---|---|
| `product_defect` | Real product bug; fix product (or accept risk) |
| `test_script_issue` | Bad/brittle/outdated test; fix or rewrite test |
| `environment` | Infra, data, timing, dependency outage |
| `unknown` | Needs human escalation |

Every triage finding SHALL include evidence (logs, flake history, recent deploys) and `skill_applied: failure-triage#...`.

### 16.2 Flaky identification & quarantine

Rules (host may tighten thresholds in context):

- Repeated intermittent failures without product change → candidate flaky.
- Quarantine recommendations MUST include: **owner**, **end date**, **Jira (or ticket) ID**, reason, and exit criteria.
- Quarantined tests MUST NOT silently disappear; they remain visible as debt with an expiry.
- Expired quarantine without fix → escalate as blocking process finding for Lead.

Skill IDs: `failure-triage`, `flaky-quarantine`. Jira create/link is Phase 2 adapter; v1 records ticket ID fields for humans to attach.

## 17. Industry alignment & risks

### 17.1 Alignment

QualityAI’s strategy matches how leading orgs adapt to AI-written code:

- **Google** — bottleneck moved from writing to review/integration; guardrails, AI review aids, human judgment on architecture/risk; human golden sets + LLM judges + CI eval gates.
- **Anthropic (Claude Code)** — continuous AI review; risk-tiered human approvals; protect tests from agent weakening; evidence of passing checks; humans own direction, risky paths, and outcomes.
- **Industry / Microsoft-style agent governance** — own the outcome, delegate volume; least privilege; draft PRs; auditability; independent validation from requirements.

Role × skill × context × HITL is therefore a **sound, scalable** response to autonomous feature generation.

### 17.2 Material risks (must stay designed-in)

| Risk | Mitigation in QualityAI |
|---|---|
| Coding agent and its tests share wrong assumptions (“green but wrong”) | Independent test suggestion from AC/journeys/FMEA (`qa.*` roles + requirement-alignment); Phase 2 independence workflow |
| Review fatigue / noise | Severity ordering; role scope; risk tiers (Phase 2) |
| Flaky suite destroys trust | `failure-triage` + `flaky-quarantine` with owner/end date/ticket |
| Agents bypass policy | `AI-HUMAN-BOUNDARY.md`; no push to main; context via PR |
| Non-deterministic markdown agents | Strict playbooks/examples; later eval harness + CI |
| Stage gates only on paper | Context matrices now; CI enforcement in Phase 3 |

## 18. Conclusion

QualityAI scales QA with AI the way strong orgs always scaled: clear roles, shared craft, written strategy, and stage gates—now as an in-repo pack. Test scaling is the headline; PR review is a workflow; suite trust (triage/quarantine) keeps regressions meaningful; humans keep authority over main and production. Risk-tiered autonomy, independent spec-based tests, eval harnesses, and CI-enforced GitWorkflow matrices are the deliberate Phase 2/3 path.
