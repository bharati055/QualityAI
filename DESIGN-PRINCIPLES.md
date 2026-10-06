# QualityAI Design Principles & Agent Operating Model

## Overview

This document codifies the operating principles for QualityAI's multi-agent system. These principles ensure the pack is maintainable, scalable, and auditable.

v1 is markdown-only under `.qualityai/` (agents, skills, instructions). Tools, GitHub/Jira APIs, and telemetry are later addons. Agents still delegate to skills; they never inline skill logic.

## 0. AI-Era Quality Strategy

These principles define *why* QualityAI exists in the age of AI-assisted delivery and AI-facing products. Operating principles in later sections define *how* agents and skills behave.

### 0.1 Define the AI-Era Quality Strategy

**Principle:** Establish an end-to-end quality framework that spans **human agents and AI agents**, evolving QA from traditional sample-based auditing toward **continuous, AI-enabled quality management**.

**What this means:**

- Quality is not a periodic audit sample of a few PRs or chats; it is an ongoing system of gates, skills, and feedback loops.
- Both human reviewers and AI coding/review agents operate under the same standards, evidence rules, and gate model.
- Continuous management covers requirements → design → implementation → tests → security → review → deployment readiness (and later production signals such as GCO).

**Implications for the pack:**

- Skills and gates encode continuous review methodology, not one-off checklists.
- Feedback agents and critic exist to keep AI review honest over time.
- Humans remain decision-makers; AI increases coverage and consistency, not authority to merge alone.

### 0.2 Establish AI Quality & Testing Frameworks

**Principle:** Design and maintain comprehensive **evaluation benchmarks**, **testing protocols**, and **human-in-the-loop (HITL)** workflows to verify AI agents, support bots, and recommendation engines operate as intended.

**What this means:**

- AI systems under test (coding agents, support bots, recommenders, etc.) need explicit evaluation criteria—not only unit tests of the surrounding app code.
- HITL workflows define when a human must confirm, override, or escalate AI output before it affects users or production.
- Benchmarks and protocols should be versioned in skills/playbooks so they are auditable and reusable across repos.

**Implications for the pack:**

- `testing-patterns`, `requirement-alignment`, and related skills must cover AI-system behavior where the host product includes AI features.
- Gate recommendations and finding schema support HITL: agents recommend; humans decide.
- Later addons (CI, GCO) can feed benchmarks with automated signals; v1 documents the frameworks in markdown.

### 0.3 Audit AI Outputs & User Interactions

**Principle:** Continuously evaluate AI-generated outputs for **intent fulfillment**, **safety**, **tone**, and **hallucination prevention**.

**Examples of outputs to audit** (domain-specific hosts will vary):

- Automated support chats
- Tour / product recommendation accuracy
- Booking or transactional updates generated or mediated by AI
- AI-assisted code and PR summaries (via this pack’s review agents)

**What this means:**

- Every material AI output should be checkable against stated intent (requirements, user ask, policy).
- Safety includes security, privacy, harmful content, and incorrect irreversible actions.
- Tone and brand/voice matter for user-facing agents; hallucinations must be detected or constrained with evidence and escalation.

**Implications for the pack:**

- `ai-code-detection` raises review depth for AI-assisted *code*; product hosts should add or extend skills for AI *user-facing* outputs using the same evidence and HITL rules.
- Findings must cite evidence and confidence; unverifiable claims are over-claiming.
- Continuous audit is the goal; sample-only review of AI chats/recommendations is insufficient as volume grows.

---

## 1. Strict Separation of Concerns (SoC)

### 1.1 Principle

Each component should have one and only one responsibility. No duplication of logic across agents, skills, or prompts. This is non-negotiable for maintainability and auditability.

### 1.2 Implementation

**Agent Level (High-Level Decision Making)**
- Agents own orchestration, routing, and decision logic
- Agents call skills; they never re-implement skill logic inline
- Agents interpret skill outputs and make go/no-go decisions
- Example: `qa.tester.agent.md` decides whether to run edge-case analysis, but delegates to `testing-patterns` (`.qualityai/skills/testing-patterns/`) for actual detection

**Skill Level (Reusable Expertise)**
- Skills encapsulate proven techniques and methodologies
- Each skill solves ONE specific problem
- Skills are language-agnostic where possible; they document the "how" once
- Example: skill `security-patterns` defines password handling, secrets detection, input validation—once. Used by `qa.security-reviewer.agent.md` and `qa.code-reviewer.agent.md`

**Prompt Level (LLM Instruction)**
- Prompts instruct LLMs on how to apply skills
- Prompts do not re-document skills; they reference them
- Prompts focus on tone, context, and output format
- Example: instructions say "Use skill `security-patterns`" rather than re-listing all security patterns

### 1.3 Violation Detection

Red flags that SoC is being violated:

❌ Same logic appears in two agent files
❌ Skill duplicates logic that exists in another skill
❌ Prompt contains detailed methodology instead of referencing a skill
❌ Agent implements feature-specific logic that should be in a reusable skill

### 1.4 Structure Example

```
Good:
├── .qualityai/agents/qa.security-reviewer.agent.md
│   └── Delegates to: skills/security-patterns/
│
├── .qualityai/skills/
│   └── security-patterns/             # Single source of truth (folder + SKILL.md)
│
└── .qualityai/instructions/
    └── References: security-patterns
    └── Instructs: Use this skill to analyze code

Bad:
├── agents/qa.security-reviewer.agent.md
│   └── "Check for hardcoded passwords, validate inputs, ..."  # ❌ Logic in agent
│
├── agents/qa.code-reviewer.agent.md
│   └── "Look for hardcoded passwords, ..."  # ❌ Duplicate logic
│
└── No skills/ folder                        # ❌ No reusability
```

---

## 2. Delegation-First Model

### 2.1 Principle

Agents delegate to skills. Skills delegate to tools or lower-level skills. This creates a clear hierarchy and prevents agents from becoming monolithic.

### 2.2 Delegation Hierarchy

```
Agent (Decision Maker)
  └─ delegates to ─> Skill (Expertise)
                       └─ delegates to ─> Tool (Execution)
                                           └─ delegates to ─> Data/API
```

**Agent Responsibilities:**
- Parse task context and inputs
- Decide which skills to invoke
- Interpret skill outputs
- Make go/no-go decisions
- Delegate, never execute

**Skill Responsibilities:**
- Document proven methodology
- Guide agents on when to apply the skill
- Explain expected inputs/outputs
- Delegate to tools if needed
- Never duplicate logic from other skills

**Tool Responsibilities:**
- Execute isolated, deterministic operations
- Parse code, analyze patterns, check configs
- Return raw data; don't interpret
- Example: `tools/code-analyzer.ts` returns AST, patterns found; doesn't judge

### 2.3 Example Flow

```
User: "Review this PR for security issues"
        |
        v
qa.security-reviewer.agent.md
  ├─ Parse PR metadata
  ├─ Delegate: "Apply security-patterns skill"
  │     |
  │     v
  │   skills/security-patterns/
  │     ├─ Check: secret detection (playbook + references in v1)
  │     ├─ Check: input validation
  │     └─ Return: {secrets_found: [...], validation_gaps: [...]}
  │     Optional later: tools/secret-detector.ts
  │
  ├─ Do not invent a second skill for the same concern
  │
  ├─ Aggregate findings
  ├─ Make decision: PASS / FAIL / WARN
  └─ Return: Structured report
```

### 2.4 Anti-Pattern: Agent Implementing Logic

❌ **Wrong:**
```markdown
# qa.tester.agent.md
You are a test quality reviewer.
1. Check if tests cover the happy path
2. Check if tests cover error paths
3. Look for assertions that are too weak
4. Look for brittle mocking patterns
(... 50 more checks ...)
```

✅ **Right:**
```markdown
# qa.tester.agent.md
You are a test quality reviewer. Your job is to:
1. Delegate to `.qualityai/skills/testing-patterns/`
2. Interpret the findings
3. Make a go/no-go **recommendation** (humans merge)
4. Explain your reasoning

Use this skill:
- `testing-patterns` (`.qualityai/skills/testing-patterns/SKILL.md`)
```

---

## 3. Principal/Staff-Level Seniority Throughout

### 3.1 Principle

Every agent should operate at a principal or staff engineer level of judgment. Agents should not ask obvious questions or miss nuance. This requires careful prompt design and domain expertise.

### 3.2 Implementation

**High-Level Thinking:**
- Agents should think in terms of business risk, not just code rules
- Agents should ask "why" before jumping to "fix it"
- Agents should identify patterns that repeat across the codebase
- Agents should know when to escalate vs. resolve

**Expert Judgment:**
- Agents should use skills developed by experts in their domain
- Agents should reason about trade-offs, not just checklist compliance
- Agents should detect architectural or strategic issues, not just style issues

**Mentorship Model:**
- Each agent should be mentored by a feedback agent (peer review)
- Feedback agent challenges assumptions: Is this finding justified? Is evidence present?
- Final output should reflect expert consensus, not a single pass

### 3.3 Example: Staff-Level Thinking

❌ **Junior-Level:**
```
Test found: Missing unit test for function X
Recommendation: Write a unit test
```

✅ **Staff-Level:**
```
Finding: Function X is in the critical path for payment processing.
Evidence: Test coverage for X is 40%; error paths are not covered.
Risk: Unhandled exception in production could lose customer transactions.
Recommendation: Add error path tests + integration test for failure scenario.
Rationale: This is high-risk infrastructure; test coverage must be >90% for all error paths.
Confidence: 92% (verified against codebase and domain knowledge)
```

### 3.4 Achieving Staff-Level Reasoning

1. **Skill Design**: Skills should encode expertise from 10+ years in the domain, not generic checklists
2. **Feedback Loops**: Feedback agents should challenge reasoning, not just rubber-stamp
3. **Context**: Agents should have access to architecture, requirements, risk profile, not just code diffs
4. **Escalation**: Agents should know when to say "this requires human judgment" vs. making a call

---

## 4. No Real Names, Just Roles and Principles

### 4.1 Principle

Agents and skills should be named by their role and function, not by person, team, or personality. This ensures the system remains professional, maintainable, and scalable.

### 4.2 Naming Conventions

**Agents:** `qa.[role].agent.md`
- `qa.researcher.agent.md` (not `qa.alice-requirement-checker.agent.md`)
- `qa.architect.agent.md` (not `qa.bob-design-reviewer.agent.md`)
- `qa.security-reviewer.agent.md` (not `qa.security-team-agent.agent.md`)

**Skills:** folder `skills/<skill-id>/` with `SKILL.md`
- `skills/security-patterns/` (not `skills/alice-security-expertise.md`)
- `skills/testing-patterns/` (not `skills/bob-testing-framework.md`)
- `skills/architecture-patterns/` (not `skills/john-architecture-principles.md`)

**Feedback Agents:** `qa.[role].agent.feedback.md`
- `qa.researcher.agent.feedback.md` (reviewer of researcher findings)
- `qa.tester.agent.feedback.md` (reviewer of tester findings)

**Tools:** `[action]-[target].ts`
- `tools/code-analyzer.ts` (not `tools/alice-parser.ts`)
- `tools/secret-detector.ts`
- `tools/pattern-matcher.ts`

### 4.3 Why This Matters

✅ **Durability**: If Alice leaves, the system doesn't break; the role is eternal
✅ **Transferability**: Knowledge is tied to function, not person
✅ **Scalability**: New team members learn the role, not the person
✅ **Auditability**: "qa.security-reviewer found X" is clear and professional
✅ **Maintainability**: Refactoring doesn't require renaming everything when a person changes

### 4.4 Anti-Pattern: Personalized Names

❌ **Wrong:**
```
├── agents/vikas-qa-orchestrator.agent.md
├── agents/alice-requirement-checker.agent.md
├── skills/bob-testing-expertise.md
└── tools/jane-parser.ts
```

✅ **Right:**
```
├── .qualityai/agents/qa.orchestrator.agent.md
├── .qualityai/agents/qa.researcher.agent.md
├── .qualityai/skills/testing-patterns/
└── tools/code-analyzer.ts              # later; not required for v1
```

---

## 5. Evidence-Driven Decision Making

### 5.1 Principle

Every finding, recommendation, and decision must be backed by evidence. Agents should never claim something is true without citing specific evidence. This ensures trust, auditability, and reduces false positives.

### 5.2 Implementation

**All Findings Must Include:**

1. **Evidence**: Specific code lines, rule IDs, or test names
2. **Severity**: How critical is this finding? (high/medium/low)
3. **Confidence**: How sure is the agent? (0-100%)
4. **Rationale**: Why does this matter?
5. **Recommendation**: What should the team do?

### 5.3 Evidence Template

Every agent output should follow this structure:

```json
{
  "finding": "Missing input validation on user-supplied data",
  "evidence": {
    "file": "src/api/payment.ts",
    "lines": "45-50",
    "code_snippet": "const amount = req.body.amount;",
    "rule_id": "SECURITY-002"
  },
  "severity": "high",
  "confidence": 0.95,
  "rationale": "User input is used directly in a payment calculation without validation. This could allow negative amounts, strings, or injection attacks.",
  "recommendation": "Add input validation before processing: validate(amount, 'positive-number')",
  "skill_applied": "security-patterns#input-validation"
}
```

### 5.4 Confidence Scoring

Agents must report how confident they are in each finding:

- **95-100%**: Definitive (e.g., hardcoded password string)
- **85-94%**: High confidence (e.g., missing error handling in known risky pattern)
- **70-84%**: Moderate confidence (e.g., possible performance issue based on code structure)
- **50-69%**: Low confidence (e.g., might be dead code, but not certain)
- **<50%**: Uncertain (escalate to human review)

### 5.5 Anti-Pattern: Unsupported Claims

❌ **Wrong:**
```
Finding: "This code is poorly written"
Recommendation: "Rewrite it"
```

✅ **Right:**
```
Finding: "Test covers happy path but not error paths"
Evidence:
  - File: tests/payment.test.ts
  - Lines: 12-40
  - Test: "should process valid payment"
  - Missing: No test for "should reject invalid amount"
  - Missing: No test for "should handle API timeout"
Severity: high
Confidence: 98%
Rationale: Payment processing is critical path. Untested error paths could crash in production.
Recommendation: Add error path tests for amount validation and API timeout scenarios
Skill applied: testing-patterns#error-path-coverage
```

---

## 6. Read-Only for Security and Ops

### 6.1 Principle

QualityAI agents are analysis and recommendation engines. They must never modify code, merge PRs, or execute deployments. The system is strictly read-only with respect to the codebase and production systems.

### 6.2 Implementation

**What Agents CAN Do (v1):**
- Read code, tests, requirements in the host repo
- Analyze patterns and risks
- Generate reports and recommendations in chat or files the human requested

**What Agents CANNOT Do:**
- Modify host code, merge, or deploy as part of a QualityAI review
- Delete branches, commits, logs, or audit trails
- Change permissions
- Post to GitHub or Jira as a required v1 step (that is a later addon)
- Claim which AI product authored a diff as a blocking fact

### 6.3 Security Constraints

**Integrations (later addons, not v1):**
- GitHub/Jira/Jenkins access is defined by those addons. v1 needs no API tokens.
- When addons exist, they should be read-only unless the host explicitly enables posting a report.

**Data Access:**
- Agents can read source code, configs, logs
- Agents cannot access secrets, API keys, or credentials
- All credential access is through secure vaults only (read for reference, never log)

**Audit Trail:**
- Every agent decision is logged with:
  - Agent name (role)
  - Timestamp
  - Input data (sanitized)
  - Decision rationale
  - Output recommendation
- Logs cannot be modified or deleted by agents

### 5.4 Gate Model: Gate Suggests, Human Decides

The quality gates provide recommendations, not enforcement:

```
QualityAI Gate
    |
    ├─ Suggests: "This PR should be blocked due to missing error handling"
    ├─ Evidence: [security finding details]
    ├─ Confidence: 92%
    │
    └─ Human Reviewer
        ├─ Reads recommendation
        ├─ Reviews evidence
        ├─ Decides: "I agree, request changes" OR "I disagree, approved anyway"
        └─ Action: Update PR status or merge
```

---

## 7. Continuous Improvement via Feedback Loops (CI via Feedback Loop)

### 7.1 Principle

The system continuously improves through structured feedback loops. Each agent has a feedback counterpart that validates reasoning. Over time, findings that were wrong or missed teach the system to improve.

### 7.2 Feedback Loop Architecture

```
Primary Agent Runs
  ├─ Produces: [finding_1, finding_2, ..., finding_N]
  │
  └─> Feedback Agent Validates
      ├─ Checks: Is each finding evidence-backed?
      ├─ Checks: Is the severity justified?
      ├─ Checks: Is confidence realistic?
      ├─ Checks: What did we miss?
      │
      └─> Produces: [validated_findings + adjustments]
          ├─ Confidence score adjustments
          ├─ Missing findings flagged
          ├─ False positive detections
          └─ Consensus recommendation
```

### 7.3 Learning from Feedback

**Positive Feedback Loop:**
1. Agent makes finding → Feedback agent validates → Human confirms
2. Mark as "valid finding" in the rule/skill
3. Next time similar pattern is seen, confidence increases

**Negative Feedback Loop:**
1. Agent makes finding → Feedback agent questions it → Human disagrees
2. Mark as "false positive" in logs
3. Skill/prompt is refined to avoid recurrence

### 7.4 Feedback Loop Metrics

Track over time:
- **Precision**: % of agent findings that humans confirm
- **Recall**: % of real issues agent findings catch
- **Confidence Calibration**: Do 90% confident findings have 90% human agreement?
- **Feedback Loop Health**: How often does feedback agent catch false positives?

### 7.5 Continuous Improvement Process

```
Week 1: Deploy qa.tester.agent
  └─ Precision: 85%, Recall: 78%

Week 2: Analyze false positives + misses
  └─ Adjust: skills/testing-patterns/
  └─ Adjust: prompts/qa.tester.md

Week 3: Re-measure
  └─ Precision: 91%, Recall: 85%

Week 4: Feedback loop catches 2 more issues
  └─ Skills improved further

Month 2: Precision: 94%, Recall: 89%
```

### 7.6 Feedback Loop Documentation

Each agent should have a `feedback-log.md`:

```markdown
# qa.tester.agent Feedback Log

## Valid Findings (Human Agreed)
- Finding 001: Missing error path test → CONFIRMED
- Finding 002: Brittle mock setup → CONFIRMED

## False Positives (Human Disagreed)
- Finding 003: "Too many assertions" → FALSE POSITIVE (no rule violation)
  └─ Action: Refined prompt to not flag assertion count

## Missed Findings (Human Found What We Missed)
- Issue: Agent missed 3 async timeout scenarios
  └─ Action: Updated testing-patterns#async-handling

## Confidence Calibration
- 95% confident findings: 92% accuracy (well-calibrated)
- 70% confident findings: 61% accuracy (overconfident, reduce)
```

---

## 8. Governance and Auditability

### 8.1 Every Decision is Traceable

All agent outputs must include:

```json
{
  "decision_id": "QA-2026-10-06-PR-142-SEC-001",
  "timestamp": "2026-10-06T14:32:15Z",
  "agent": "qa.security-reviewer",
  "input": {
    "pr": "142",
    "files_analyzed": 12,
    "lines_of_code": 450
  },
  "findings": [...],
  "final_decision": "FAIL",
  "feedback_agent_review": "qa.security-reviewer.feedback",
  "confidence": 0.94,
  "audit_trail": [
    "qa.security-reviewer: Applied security-patterns → 3 findings",
    "qa.security-reviewer.feedback: Validated all 3 findings → Confidence raised from 0.88 to 0.94",
    "qa.critic: Reviewed for missing context → No escalation needed"
  ]
}
```

### 8.2 Retention and Audit

- All agent logs retained for minimum 1 year
- Logs are immutable (no modification, only append)
- Audit logs can be queried by: date, PR, agent, finding type, etc.
- Compliance teams can regenerate reports for any past PR

---

## 9. Summary: QualityAI Operating Principles

| Principle | What It Means | Why It Matters |
|---|---|---|
| **AI-Era Quality Strategy** | End-to-end quality across human + AI agents; continuous management over sample audits | Scales quality with AI-assisted delivery |
| **AI Quality & Testing Frameworks** | Benchmarks, protocols, and HITL for AI agents/bots/recommenders | Verifies AI systems operate as intended |
| **Audit AI Outputs** | Continuous check of intent, safety, tone, hallucination | Protects users and trust in AI-generated interactions |
| **Separation of Concern** | One responsibility per component | Maintainability, no duplication, clear ownership |
| **Delegation-First** | Agents → Skills → Tools | Reusability, scalability, clear hierarchy |
| **Staff-Level Seniority** | Every agent thinks like a principal engineer | Deep insights, not surface-level checks |
| **No Real Names** | Roles, not people | Durability, transferability, professionalism |
| **Evidence-Driven** | Every claim is backed by evidence + confidence | Trust, auditability, fewer false positives |
| **Read-Only** | No code changes, no deployments | Security, safety, humans remain in control |
| **Feedback Loops** | Every agent has a validating peer | Continuous improvement, precision and recall |

---

## 10. Implementation Checklist

Before deploying a new agent:

- [ ] Agent has ONE clear responsibility (SoC)
- [ ] Agent delegates to skills, doesn't re-implement logic
- [ ] Agent prompts reference skills, don't duplicate them
- [ ] Agent operates at staff-engineer level of reasoning
- [ ] Agent uses role-based naming (no person names)
- [ ] Agent outputs include evidence, confidence, rationale
- [ ] Agent never modifies code or triggers deployments (read-only)
- [ ] Agent has a feedback counterpart for validation
- [ ] All outputs logged with audit trail
- [ ] Feedback loop metrics tracked
- [ ] Documentation updated with new agent role and responsibilities
- [ ] AI-era strategy considered: continuous quality (not sample-only), HITL where AI outputs affect users, hallucination/safety/intent checks when auditing AI outputs

---

## 11. Conclusion

These principles ensure QualityAI is not just powerful, but also maintainable, trustworthy, and auditable. They reflect 18+ years of QA leadership and modern agentic AI best practices.

By adhering to these principles, QualityAI becomes a system that engineering teams can rely on for deep, consistent, evidence-based quality review—with human judgment always in control.
