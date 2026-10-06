# QualityAI Architecture

## 1. Overview

QualityAI is a platform for enforcing software quality from requirement intent to deployment readiness. Its goal is to protect engineering teams from low-quality AI-generated code, weak review quality, and shallow validation that passes basic automation while still introducing risk.

The architecture is intentionally split into two layers:

1. Core QualityAI engine: platform-agnostic, portable, and reusable across any repository, pipeline, or organization.
2. Integration addons: thin adapters for GitHub Actions, Jira, Jenkins, GitLab, Gatling, Slack, and similar tools.

The design follows a quality gate model with a specialist multi-agent review framework, combined with feedback loops to reduce false positives and increase review depth.

## 2. Design Goals

- Start quality validation from requirements, not just code changes.
- Treat AI-generated code as a higher-risk category that deserves stricter scrutiny.
- Make quality standards explicit, codified, and reusable.
- Preserve deep human review by providing prioritized and actionable insights.
- Work across CI/CD systems without vendor lock-in.
- Keep the core product portable, installable, and easy to adapt.

## 3. High-Level Architecture

```text
+----------------------------------------------------------------------------------+
|                               QualityAI Platform                                 |
|                                                                                  |
|  +---------------------------+   +--------------------------------------------+    |
|  |   Requirements Layer       |   |   Core Review Engine                       |    |
|  | - Jira integration         |   | - Rule engine                              |    |
|  | - Acceptance criteria     |   | - Test quality evaluator                   |    |
|  | - Requirement mapping      |   | - Security and reliability checks          |    |
|  | - Traceability store       |   | - Architecture validation                  |    |
|  +---------------------------+   | - AI-code detection                        |    |
|                                      | - PR risk summarizer                       |    |
|  +---------------------------+   | - Reporting and quality score             |    |
|  |   Multi-Agent Orchestration|   +--------------------------------------------+    |
|  | - Orchestrator             |                         |                         |
|  | - Specialist agents        |                         |                         |
|  | - Feedback agents         |                         |                         |
|  | - Gates and consensus     |                         |                         |
|  +---------------------------+                         |                         |
|                                                          |                         |
|        +---------------------------+   +---------------------------+                 |
|        | GitHub Actions Addon      |   | Jenkins Addon            |                 |
|        | Jira Addon                |   | GitLab CI Addon          |                 |
|        | Gatling Addon             |   | Slack Addon              |                 |
|        +---------------------------+   +---------------------------+                 |
+----------------------------------------------------------------------------------+
```

## 4. Architectural Principles

### 4.1 Core is CI/CD Agnostic

The core engine is designed to operate independently of any single toolchain. Users should be able to run it locally, from Jenkins, GitHub Actions, GitLab CI, or any custom pipeline.

### 4.2 Integrations are Addons

GitHub Actions, Jira, and other ecosystems are treated as adapters. They call the core engine and normalize output into their native experience.

### 4.3 Requirements are the Source of Truth

The platform validates code against requirements, not just tests. If a requirement is missing, unclear, or not testable, that becomes part of the quality gate feedback.

### 4.4 Quality is Multi-Layered

Quality is not a single metric. It is a combination of:

- requirement alignment
- code quality
- security and reliability
- testing quality
- architecture consistency
- AI risk analysis
- deployment readiness

### 4.5 Specialized Agents with Feedback Loops

A single general-purpose agent is not enough for deep review. Agents are specialized by role and cross-validated by feedback agents to reduce hallucination and false positives.

## 5. Core Repository Structure

The QualityAI platform should be structured with a dedicated root for all AI-related project files. The core is under `.qualityai/`, while GitHub-specific workflow files remain in `.github/` as optional integrations.

```text
project-root/
├── .qualityai/                              # Core QualityAI configuration and engine
│   ├── README.md                            # Product overview and entry point
│   ├── config.yml                          # Core configuration
│   ├── setup.sh                            # Setup script for repo onboarding
│   ├── cli.ts                              # CLI entry point
│   ├── package.json                        # Core runtime dependencies
│   ├── tsconfig.json                       # TypeScript config (if TypeScript is used)
│   │
│   ├── core/                               # Core engine
│   │   ├── engine.ts                       # Main orchestration engine
│   │   ├── rules-engine.ts                 # Rule evaluation engine
│   │   ├── standards-validator.ts          # Standards/rule validation
│   │   ├── code-analyzer.ts                # Static code analysis logic
│   │   ├── requirement-mapper.ts           # Maps requirements to checks
│   │   ├── test-quality-evaluator.ts       # Test quality analysis
│   │   ├── ai-code-detector.ts             # AI-generation detection logic
│   │   ├── risk-scoring.ts                 # Risk profile scoring
│   │   ├── report-generator.ts             # Final markdown/JSON report
│   │   ├── output-normalizer.ts           # Normalizes output for all integrations
│   │   ├── decision-engine.ts             # Gate decisions and summary logic
│   │   └── logger.ts                      # Structured logs
│   │
│   ├── agents/                             # Multi-agent quality review design
│   │   ├── README.md                      # Agent framework and conventions
│   │   ├── orchestrator/
│   │   │   ├── quality-orchestrator.agent.md
│   │   │   ├── quality-orchestrator.feedback.md
│   │   │   └── orchestrator-config.yml
│   │   │
│   │   ├── specialists/
│   │   │   ├── researcher/
│   │   │   │   ├── researcher.agent.md
│   │   │   │   ├── researcher.agent.feedback.md
│   │   │   │   └── config.yml
│   │   │   ├── architect/
│   │   │   │   ├── architect.agent.md
│   │   │   │   ├── architect.agent.feedback.md
│   │   │   │   └── config.yml
│   │   │   ├── tester/
│   │   │   │   ├── tester.agent.md
│   │   │   │   ├── tester.agent.feedback.md
│   │   │   │   └── config.yml
│   │   │   ├── security-reviewer/
│   │   │   │   ├── security-reviewer.agent.md
│   │   │   │   ├── security-reviewer.agent.feedback.md
│   │   │   │   └── config.yml
│   │   │   ├── code-reviewer/
│   │   │   │   ├── code-reviewer.agent.md
│   │   │   │   ├── code-reviewer.agent.feedback.md
│   │   │   │   └── config.yml
│   │   │   ├── ai-detector/
│   │   │   │   ├── ai-code-detector.agent.md
│   │   │   │   ├── ai-code-detector.feedback.md
│   │   │   │   └── config.yml
│   │   │   └── critic/
│   │   │       ├── critic.agent.md
│   │   │       ├── critic.agent.feedback.md
│   │   │       └── config.yml
│   │   │
│   │   ├── gates/
│   │   │   ├── requirement-gate.agent.md
│   │   │   ├── design-gate.agent.md
│   │   │   ├── ai-risk-gate.agent.md
│   │   │   ├── security-gate.agent.md
│   │   │   ├── test-quality-gate.agent.md
│   │   │   └── deployment-readiness-gate.agent.md
│   │   │
│   │   ├── orchestration/
│   │   │   ├── parallel-evaluators.ts
│   │   │   ├── sequential-gates.ts
│   │   │   ├── feedback-loop.ts
│   │   │   ├── consensus-builder.ts
│   │   │   └── prompt-router.ts
│   │   │
│   │   ├── prompts/
│   │   │   ├── system-prompts/
│   │   │   │   ├── researcher.md
│   │   │   │   ├── architect.md
│   │   │   │   ├── tester.md
│   │   │   │   ├── security-reviewer.md
│   │   │   │   ├── ai-detector.md
│   │   │   │   └── critic.md
│   │   │   └── feedback-prompts/
│   │   │       ├── give-constructive-feedback.md
│   │   │       ├── validate-findings.md
│   │   │       └── consensus-building.md
│   │   │
│   │   └── tools/
│   │       ├── code-analyzer.ts
│   │       ├── requirement-parser.ts
│   │       ├── pattern-matcher.ts
│   │       ├── test-analyzer.ts
│   │       └── security-checker.ts
│   │
│   ├── rules/                             # Rule library
│   │   ├── base-rules.yml
│   │   ├── index.ts
│   │   ├── by-language/
│   │   │   ├── typescript.yml
│   │   │   ├── python.yml
│   │   │   ├── java.yml
│   │   │   └── js.yml
│   │   ├── by-domain/
│   │   │   ├── payment-systems.yml
│   │   │   ├── auth-systems.yml
│   │   │   ├── api-services.yml
│   │   │   └── data-pipelines.yml
│   │   └── custom.yml
│   │
│   ├── skills/
│   │   ├── testing-patterns.md
│   │   ├── security-patterns.md
│   │   ├── architecture-patterns.md
│   │   ├── edge-case-detection.md
│   │   ├── error-handling.md
│   │   └── quality-standards.md
│   │
│   ├── standards/
│   │   ├── coding-standards.md
│   │   ├── security-checklist.md
│   │   ├── performance-expectations.md
│   │   ├── accessibility-standards.md
│   │   ├── observability-requirements.md
│   │   └── review-principles.md
│   │
│   ├── templates/
│   │   ├── pr-report-template.md
│   │   ├── rule-template.yml
│   │   └── quality-gate-template.md
│   │
│   ├── docs/
│   │   ├── ARCHITECTURE.md
│   │   ├── INTEGRATIONS.md
│   │   ├── RULES-ENGINE.md
│   │   ├── JIRA-INTEGRATION.md
│   │   └── EXTENDING-QUALITYAI.md
│   │
│   ├── examples/
│   │   ├── github-actions-example/
│   │   ├── jenkins-example/
│   │   ├── local-cli-example/
│   │   └── jira-integrated-example/
│   │
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── e2e/
│       ├── performance/
│       ├── security/
│       ├── chaos/
│       ├── fixtures/
│       └── utils/
│
├── integrations/                            # Optional add-ons
│   ├── README.md
│   ├── github-actions/
│   │   ├── action.yml
│   │   ├── setup-github.sh
│   │   └── workflows/
│   │       └── quality-gate.yml
│   │
│   ├── jira/
│   │   ├── jira-config.yml
│   │   ├── jira-sync.ts
│   │   ├── requirements-mapper.ts
│   │   └── setup-jira.sh
│   │
│   ├── jenkins/
│   │   ├── Jenkinsfile-template
│   │   ├── setup-jenkins.sh
│   │   └── pipeline-config.groovy
│   │
│   ├── gitlab-ci/
│   │   ├── .gitlab-ci.yml-template
│   │   └── setup-gitlab.sh
│   │
│   ├── gatling/
│   │   ├── performance-rules.yml
│   │   ├── gatling-config.scala
│   │   └── setup-gatling.sh
│   │
│   ├── slack/
│   │   ├── slack-reporter.ts
│   │   └── setup-slack.sh
│   │
│   └── circleci/
│       ├── config.yml-template
│       └── setup-circleci.sh
│
├── .github/                                # GitHub-native files only
│   └── workflows/
│       └── quality-gate.yml               # Example GitHub workflow using the core engine
│
├── docs/
│   ├── INTRODUCTION.md
│   ├── GETTING-STARTED.md
│   ├── CONTRIBUTING.md
│   └── ROADMAP.md
│
├── examples/
│   ├── github-pr-example/
│   ├── jenkins-pipeline-example/
│   ├── local-cli-example/
│   └── jira-connected-example/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── performance/
│   ├── security/
│   ├── chaos/
│   └── README.md
│
├── README.md
├── PROJECT-REQUIREMENTS.md
├── ARCHITECTURE.md
├── LICENSE
└── .gitignore
```

## 6. Core Components

### 6.1 Requirements Layer

This layer captures and normalizes requirement data from tools like Jira.

Responsibilities:
- read issue metadata and acceptance criteria
- map dependencies and constraints to quality rules
- trace PRs to the requirement they are meant to satisfy
- highlight drift between requirement intent and implementation

### 6.2 Rules Engine

The rules engine defines quality expectations using reusable rule packs and custom overrides.

Responsibilities:
- parse requirement-derived rules
- load project or org-specific standards
- evaluate code quality against standards
- classify rules as warning, fail, or blocking

### 6.3 Code Analysis Layer

This layer inspects the code and project metadata to identify likely issues.

Responsibilities:
- detect missing validations and error handling
- inspect anti-patterns and architecture drift
- find weak or brittle tests
- identify likely AI-generated code patterns

### 6.4 Multi-Agent Orchestration Layer

This is the review intelligence layer. It orchestrates specialist agents and feedback agents to produce a deeper, more balanced review than a single LLM or static rule engine.

Responsibilities:
- route work to specialists
- run specific tasks in parallel when independent
- apply sequential gate reasoning after exploratory analysis
- reconcile findings and identify the largest risks
- ensure review output is balanced, justified, and explained

### 6.5 Reporting Layer

This layer converts raw analysis into a summary that can be consumed by humans and automation.

Responsibilities:
- produce a markdown summary for PR comments
- produce structured JSON for API/CI integrations
- emit risk score, gate status, and required next action
- maintain consistent output across integrations

## 7. Multi-Agent Review Model

QualityAI is built around a specialist review model with feedback validation.

### 7.1 Core Review Pattern

The system uses a primary orchestrator and specialist agents for major quality categories:

- Researcher: requirement alignment and intent validation
- Architect: design patterns and architectural consistency
- Tester: test quality and edge-case coverage
- Security-reviewer: security and reliability risk
- Code-reviewer: code quality and maintainability
- AI-detector: identify AI-generated or AI-assisted code
- Critic: identify conflicts, blind spots, and business risk

### 7.2 Feedback Pairs

Each specialist agent is paired with a feedback agent. This is important for quality and reduction of hallucination.

Patterns:
- primary agent performs analysis
- feedback agent validates the diagnosis
- orchestrator compares the two outputs
- final report includes confidence level and rationale

Example:

```text
researcher.agent.md  -> analyzes requirement drift
researcher.agent.feedback.md -> validates if requirement findings are justified
```

This helps the system reduce false positives and encourages deeper reasoning.

### 7.3 Sequential Gates

After agents run in parallel, the system applies policy gates in sequence:

1. requirement-gate
2. design-gate
3. ai-risk-gate
4. security-gate
5. test-quality-gate
6. deployment-readiness-gate

This gives the model a review flow similar to a human QA pipeline, while still allowing parallel work between specialist reviews.

### 7.4 Consensus and Risk Prioritization

The critic agent and orchestrator are responsible for reconciling findings across agents. The final decision should be a risk- and confidence-weighted quality report rather than a simple pass/fail string.

## 8. Quality Gate Execution Flow

```text
PR / Change Request / Issue
          |
          v
+---------------------------+
| Requirement Intake        |
| - Jira sync               |
| - Acceptance criteria    |
| - Requirement graph       |
+---------------------------+
          |
          v
+---------------------------+
| Specialist Analysis       |
| - Researcher             |
| - Architect              |
| - Tester                |
| - Security reviewer     |
| - Code reviewer         |
| - AI detector           |
+---------------------------+
          |
          v
+---------------------------+
| Feedback Validation       |
| - Validate findings       |
| - Reduce hallucinations   |
| - Score confidence        |
+---------------------------+
          |
          v
+---------------------------+
| Sequential Gate Review    |
| - requirement gate       |
| - design gate            |
| - ai-risk gate           |
| - security gate          |
| - test-quality gate      |
| - deployment gate        |
+---------------------------+
          |
          v
+---------------------------+
| Output: Quality Report   |
| - Summary                |
| - Risk score             |
| - Required actions       |
| - Merge recommendation   |
+---------------------------+
```

## 9. Agent Orchestration Model

### 9.1 Orchestrator Responsibilities

- Parse the task or PR context.
- Gather requirement metadata and change metadata.
- Select and invoke relevant agents.
- Merge findings and confidence scores.
- Trigger sequential gates after initial analysis.
- Generate final review recommendations.

### 9.2 Specialist Agent Responsibilities

Each specialist agent focuses on one aspect of quality, with narrow responsibilities and clear outputs.

Examples:
- researcher: requirement alignment and intent compliance
- architect: architecture drift and design fitness
- tester: test sufficiency and risk pathways
- security-reviewer: vulnerability and reliability risk
- code-reviewer: maintainability and code quality
- ai-detector: probability of AI-generated changes
- critic: risk prioritization and missed issues

### 9.3 Feedback Agent Responsibilities

Each specialist has a validation peer that asks:
- Is the finding justified?
- Is it evidence-backed?
- Is it over- or under-claiming risk?
- Is it missing a critical consideration?

This creates a deliberate feedback loop rather than a blind pass from a single LLM call.

## 10. Core Engine Interfaces

The core engine shall expose a small set of interfaces that can be embedded in any environment.

### 10.1 CLI Interface

```bash
qualityai analyze \
  --repo-path . \
  --config .qualityai/config.yml \
  --format markdown
```

### 10.2 API Interface

```json
{
  "repoPath": ".",
  "changeSet": {
    "type": "pull_request",
    "branch": "feature/payment-update",
    "base": "main"
  },
  "requirements": ["REQ-101", "REQ-102"],
  "output": "markdown"
}
```

### 10.3 Output Interface

Core output should be normalized to a common schema:

```json
{
  "status": "fail",
  "summary": "High risk: AI-generated code missing security validation.",
  "riskScore": 82,
  "confidence": 0.91,
  "gates": {
    "requirement": "pass",
    "design": "fail",
    "aiRisk": "fail",
    "security": "fail",
    "testQuality": "warn",
    "deploymentReadiness": "fail"
  },
  "findings": [
    {
      "category": "security",
      "severity": "high",
      "message": "Input validation missing in API boundary."
    }
  ],
  "recommendedActions": [
    "Add input validation before request processing.",
    "Require security review before merge."
  ]
}
```

This normalized output is then converted by each integration into the appropriate format: PR comment, Jenkins status, Slack message, Jira update, and so on.

## 11. Optional Addon Architecture

Addons are deliberately thin and should call the shared core engine. They are meant to adapt the output for different developer ecosystems.

### 11.1 GitHub Actions Addon

Responsibilities:
- trigger workflow on PR or push
- gather metadata (changed files, commit SHA, PR title, issue references)
- call the QualityAI CLI
- post a summary comment to the PR
- fail the job if blocking checks are not passed

### 11.2 Jira Addon

Responsibilities:
- sync tickets and acceptance criteria
- map requirement IDs to quality checks
- update issue status or add comments when quality gates fail or pass

### 11.3 Jenkins Addon

Responsibilities:
- call the same QualityAI CLI in a Jenkins stage
- render build status based on gate results
- archive reports for audit purposes

### 11.4 GitLab CI Addon

Responsibilities:
- trigger as a pipeline job
- parse output and expose status to merge requests

### 11.5 Gatling Addon

Responsibilities:
- add performance-check scenarios to quality gate evaluation
- compare results against thresholds for the repo or service
- fail quality gate if performance regression is detected

### 11.6 Slack Addon

Responsibilities:
- send summarized outcomes to engineering channels
- provide risk-level notifications
- surface drag tasks or manual review requests

## 12. Integration Principle

The core system should never require GitHub or Jira to function. GitHub Actions, Jira, and Jenkins are adapters that consume the core engine's output, not the source of truth.

This leads to better portability and easier adoption across multiple teams and environments.

## 13. Repository and Project Setup Model

### 13.1 Root Structure for a Consumer Repo

```text
project-root/
├── .qualityai/                           # Copied from QualityAI core setup
│   ├── config.yml
│   ├── rules/
│   ├── skills/
│   ├── agents/
│   ├── setup.sh
│   └── cli.ts
│
├── .github/                              # Optional GitHub integration
│   └── workflows/
│       └── quality-gate.yml
│
├── src/
├── tests/
├── docs/
└── README.md
```

### 13.2 Setup Workflow

Users can install QualityAI by copying the `.qualityai/` directory and enabling one or more optional integrations.

Example:

```bash
cp -r QualityAI/.qualityai ./project/.qualityai
cd project
./.qualityai/setup.sh
```

Then choose integrations:

```bash
./.qualityai/integrations/github-actions/setup-github.sh
./.qualityai/integrations/jira/setup-jira.sh
./.qualityai/integrations/gatling/setup-gatling.sh
```

This makes the project usable not only in GitHub-hosted environments but in any repo or pipeline environment.

## 14. Data Flow Model

### 14.1 Inputs

- repository code and diffs
- requirement definitions from Jira or issue tracker
- project configuration and standards
- quality policies and custom rules
- CI metadata (PR info, branch, commit SHA)

### 14.2 Processing

- map requirements to quality checks
- analyze changed code
- run specialist agents in parallel
- validate with feedback agents
- run sequential quality gates
- compute risk scores and summary report

### 14.3 Outputs

- PR comment or review summary
- merge-blocking or warning status
- JSON report for other tools
- audit logs for traceability
- recommendation for manual review

## 15. Security and Safety Considerations

QualityAI is designed to review code without introducing unsafe execution or security risk.

Important design constraints:
- no arbitrary code execution in the core engine
- source inspection only unless explicitly required by a user-defined integration
- all external integrations must be permission-bound
- secrets must be handled through secure config, not in repo content
- all findings should be auditable and traceable to rule IDs or agent outputs

## 16. Test Strategy and Quality Validation

The project should include a strong multi-layered test strategy to validate the platform itself.

The test structure is:

```text
tests/
├── unit/
├── integration/
├── e2e/
├── performance/
├── security/
├── chaos/
├── fixtures/
├── utils/
└── README.md
```

This ensures that QualityAI itself is not a fragile system. The platform must validate its own logic, including:
- rule engine correctness
- gate logic correctness
- feedback loop reliability
- security of agent and integration execution
- performance under large repos and high concurrency
- resilience to API failures and degraded environments

## 17. Evolution Strategy

### Phase 1: Core Engine

- Rule engine
- requirement mapper
- basic PR review summaries
- simple AI detection heuristics
- basic multi-agent orchestration skeleton

### Phase 2: Standards and Gates

- domain-specific rule packs
- stronger testing quality checks
- requirement-to-code traceability
- gate-based review flow

### Phase 3: Integrations

- GitHub Actions
- Jira
- Jenkins
- GitLab
- Slack
- Gatling

### Phase 4: Enterprise Scale

- dashboards
- policy approvals and audit trails
- team-specific rule sets
- advanced orchestration and consensus logic

## 18. Expected Benefits

- deeper and more standardized code review
- reduced risk from AI-generated code
- better coverage of requirement drift and edge-case gaps
- accelerated adoption across organizations with different CI/CD tools
- easier transfer of QA tribal knowledge into reusable policies
- improved quality across the full delivery lifecycle

## 19. Conclusion

QualityAI is designed as a portable and extensible quality intelligence platform. Its foundation is a requirement-driven, multi-agent review system that enforces standards across the full software lifecycle while remaining independent from any specific delivery tool.

By keeping the core engine portable and the integrations optional, the system becomes adaptable to GitHub, Jenkins, GitLab, GitHub Enterprise, self-hosted pipelines, and other enterprise environments without sacrificing quality or consistency.

This architecture balances automation, governance, and human review in a way that is practical for modern AI-assisted development.
