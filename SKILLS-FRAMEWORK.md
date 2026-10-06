# QualityAI Skills Framework

## Overview

QualityAI skills are reusable, expertly-designed methodologies for solving specific quality problems. A skill is not just a document; it is a complete system including:

- **Playbooks**: Step-by-step workflows for different phases (create, update, review, refactor, plan, analyze, failure-analysis)
- **Examples**: Real-world QA scenarios with proven solutions
- **Tooling**: Shared utilities and scripts that multiple skills use
- **Coverage**: Explicit documentation of what the skill covers and its limitations
- **SKILL.md**: The entry point that agents use to invoke the skill

This design ensures:
- ✅ **Reusability**: Agents delegate to skills; skills don't duplicate each other
- ✅ **Expertise**: Each skill encodes 10+ years of domain knowledge, not generic checklists
- ✅ **Auditability**: Every finding traces back to a skill's published methodology
- ✅ **Maintainability**: Updates to methodology happen once, in the skill; agents inherit the improvements
- ✅ **Scalability**: New agents can use existing skills without re-implementing logic

---

## Skills Directory Structure

```text
skills/
├── README.md                                    # Skill ecosystem overview
│
├── testing-patterns/
│   ├── SKILL.md                                # Entry point: What is testing-patterns?
│   ├── PLAYBOOK.md                             # Quick start
│   ├── coverage/
│   │   ├── COVERAGE.md                         # What testing-patterns DOES cover
│   │   └── GAPS.md                             # What it DOESN'T (and won't)
│   │
│   ├── playbook/
│   │   ├── create/
│   │   │   └── PLAYBOOK.md                     # How to design test strategy
│   │   ├── plan/
│   │   │   └── PLAYBOOK.md                     # How to plan test execution
│   │   ├── review/
│   │   │   └── PLAYBOOK.md                     # How to review test quality
│   │   ├── refactor/
│   │   │   └── PLAYBOOK.md                     # How to improve weak tests
│   │   ├── update/
│   │   │   └── PLAYBOOK.md                     # How to maintain tests as code changes
│   │   └── failure-analysis/
│   │       └── PLAYBOOK.md                     # How to analyze test failures
│   │
│   ├── examples/
│   │   ├── good-test-example.md                # Exemplary test design
│   │   ├── bad-test-example.md                 # Anti-pattern: brittle test
│   │   ├── edge-case-example.md                # How to handle edge cases
│   │   └── async-handling-example.md           # Async/await testing patterns
│   │
│   ├── tooling/
│   │   ├── test-quality-checker.ts             # Shared tool for analyzing test quality
│   │   ├── coverage-calculator.ts              # Computes real vs reported coverage
│   │   ├── brittleness-detector.ts             # Identifies flaky/brittle test patterns
│   │   └── README.md                           # How to use tooling utilities
│   │
│   └── references/
│       ├── edge-case-taxonomy.md               # Exhaustive list of edge cases by domain
│       ├── assertion-patterns.md               # When to assert, what to assert
│       ├── mock-vs-stub.md                     # Decision tree for mocking
│       └── performance-considerations.md       # Testing performance-sensitive code
│
├── security-patterns/
│   ├── SKILL.md
│   ├── PLAYBOOK.md
│   ├── coverage/
│   │   ├── COVERAGE.md                         # What security checks are included
│   │   └── GAPS.md                             # What requires manual review
│   │
│   ├── playbook/
│   │   ├── create/
│   │   │   └── PLAYBOOK.md                     # Design secure architecture
│   │   ├── review/
│   │   │   └── PLAYBOOK.md                     # Review code for security issues
│   │   ├── validate/
│   │   │   └── PLAYBOOK.md                     # Run security validations
│   │   ├── refactor/
│   │   │   └── PLAYBOOK.md                     # Fix security vulnerabilities
│   │   └── failure-analysis/
│   │       └── PLAYBOOK.md                     # Analyze security breaches
│   │
│   ├── examples/
│   │   ├── secure-auth-flow.md
│   │   ├── insecure-auth-flow.md               # ❌ What NOT to do
│   │   ├── secret-detection-example.md
│   │   └── input-validation-example.md
│   │
│   ├── tooling/
│   │   ├── secret-detector.ts
│   │   ├── injection-detector.ts
│   │   ├── vulnerability-scanner.ts
│   │   └── owasp-mapper.ts                     # Maps findings to OWASP Top 10
│   │
│   └── references/
│       ├── owasp-top-10.md
│       ├── secret-patterns.md                  # Hardcoded password, API key patterns
│       ├── input-validation-rules.md
│       ├── output-encoding.md
│       └── threat-model.md
│
├── architecture-patterns/
│   ├── SKILL.md
│   ├── PLAYBOOK.md
│   ├── coverage/
│   │   ├── COVERAGE.md
│   │   └── GAPS.md
│   │
│   ├── playbook/
│   │   ├── design/
│   │   │   └── PLAYBOOK.md                     # Design for maintainability
│   │   ├── review/
│   │   │   └── PLAYBOOK.md                     # Review design against principles
│   │   ├── anti-pattern-detection/
│   │   │   └── PLAYBOOK.md                     # Identify architectural smells
│   │   └── refactor/
│   │       └── PLAYBOOK.md                     # Restructure for better design
│   │
│   ├── examples/
│   │   ├── monolithic-good.md
│   │   ├── monolithic-bad.md
│   │   ├── microservice-good.md
│   │   └── coupling-anti-pattern.md
│   │
│   ├── tooling/
│   │   ├── dependency-analyzer.ts
│   │   ├── coupling-detector.ts
│   │   ├── layering-validator.ts
│   │   └── pattern-matcher.ts
│   │
│   └── references/
│       ├── SOLID-principles.md
│       ├── clean-architecture.md
│       ├── coupling-cohesion.md
│       └── domain-driven-design.md
│
├── code-quality/
│   ├── SKILL.md
│   ├── PLAYBOOK.md
│   ├── coverage/
│   │   ├── COVERAGE.md
│   │   └── GAPS.md
│   │
│   ├── playbook/
│   │   ├── review/
│   │   │   └── PLAYBOOK.md                     # Deep code review
│   │   ├── refactor/
│   │   │   └── PLAYBOOK.md                     # Improve code quality
│   │   └── maintainability-assessment/
│   │       └── PLAYBOOK.md                     # Is this code maintainable?
│   │
│   ├── examples/
│   │   ├── readable-function.md
│   │   ├── unreadable-function.md
│   │   ├── complex-logic.md
│   │   └── well-commented-function.md
│   │
│   ├── tooling/
│   │   ├── complexity-analyzer.ts              # Cyclomatic complexity, cognitive complexity
│   │   ├── naming-checker.ts                   # Check if names are descriptive
│   │   ├── duplication-detector.ts             # Find copy-pasted code
│   │   └── comment-quality-checker.ts
│   │
│   └── references/
│       ├── naming-conventions.md
│       ├── cyclomatic-complexity.md
│       ├── function-sizing.md
│       └── comment-best-practices.md
│
├── requirement-alignment/
│   ├── SKILL.md
│   ├── PLAYBOOK.md
│   ├── coverage/
│   │   ├── COVERAGE.md
│   │   └── GAPS.md
│   │
│   ├── playbook/
│   │   ├── parse/
│   │   │   └── PLAYBOOK.md                     # Extract intent from requirements
│   │   ├── map/
│   │   │   └── PLAYBOOK.md                     # Map code to requirements
│   │   ├── validate/
│   │   │   └── PLAYBOOK.md                     # Does code satisfy requirements?
│   │   └── gap-analysis/
│   │       └── PLAYBOOK.md                     # What's missing?
│   │
│   ├── examples/
│   │   ├── clear-requirement.md
│   │   ├── vague-requirement.md
│   │   ├── well-aligned-code.md
│   │   └── drifted-code.md
│   │
│   ├── tooling/
│   │   ├── requirement-parser.ts
│   │   ├── acceptance-criteria-extractor.ts
│   │   ├── gap-detector.ts
│   │   └── traceability-mapper.ts
│   │
│   └── references/
│       ├── jira-integration.md
│       ├── acceptance-criteria-format.md
│       └── traceability-model.md
│
├── ai-code-detection/
│   ├── SKILL.md
│   ├── PLAYBOOK.md
│   ├── coverage/
│   │   ├── COVERAGE.md
│   │   └── GAPS.md
│   │
│   ├── playbook/
│   │   ├── detect/
│   │   │   └── PLAYBOOK.md                     # Identify AI-generated code
│   │   ├── risk-assessment/
│   │   │   └── PLAYBOOK.md                     # Assess risk level
│   │   └── review-strategy/
│   │       └── PLAYBOOK.md                     # How to review AI code
│   │
│   ├── examples/
│   │   ├── copilot-signature.md
│   │   ├── claude-signature.md
│   │   ├── human-written-code.md
│   │   └── mixed-generated-human.md
│   │
│   ├── tooling/
│   │   ├── pattern-detector.ts                 # Detects Copilot/Claude patterns
│   │   ├── entropy-calculator.ts               # Code diversity and entropy
│   │   ├── confidence-scorer.ts                # Confidence in AI detection
│   │   └── risk-classifier.ts                  # Risk level for generated code
│   │
│   └── references/
│       ├── copilot-patterns.md                 # Known Copilot code signatures
│       ├── claude-patterns.md                  # Known Claude code signatures
│       ├── chatgpt-patterns.md                 # Known ChatGPT patterns
│       └── false-positive-mitigation.md        # Avoid false positives
│
└── performance-validation/
    ├── SKILL.md
    ├── PLAYBOOK.md
    ├── coverage/
    │   ├── COVERAGE.md
    │   └── GAPS.md
    │
    ├── playbook/
    │   ├── plan/
    │   │   └── PLAYBOOK.md                     # Plan performance testing
    │   ├── baseline/
    │   │   └── PLAYBOOK.md                     # Establish baseline
    │   ├── execute/
    │   │   └── PLAYBOOK.md                     # Run performance tests
    │   ├── analyze/
    │   │   └── PLAYBOOK.md                     # Analyze results
    │   ├── regression-detection/
    │   │   └── PLAYBOOK.md                     # Detect performance regressions
    │   └── refactor/
    │       └── PLAYBOOK.md                     # Fix performance issues
    │
    ├── examples/
    │   ├── good-performance.md
    │   ├── performance-regression.md
    │   ├── optimization-opportunity.md
    │   └── load-test-analysis.md
    │
    ├── tooling/
    │   ├── performance-metrics-collector.ts
    │   ├── regression-detector.ts
    │   ├── threshold-checker.ts
    │   ├── bottleneck-analyzer.ts
    │   └── benchmark-comparator.ts
    │
    └── references/
        ├── performance-metrics.md              # What to measure
        ├── baseline-strategy.md                # How to establish baseline
        ├── load-testing-patterns.md
        └── common-bottlenecks.md
```

---

## Skill Anatomy: SKILL.md

Every skill starts with a SKILL.md that serves as the agent's entry point. It should include:

```markdown
---
name: [skill-name]
description: One-line description of what this skill does
version: "1.0.0"
created: YYYY-MM-DD
authors: [roles]
tags: [tag1, tag2, ...]
domain: [quality|security|architecture|testing]
languages: [typescript, python, java]
---

## When to Use

[Clear trigger conditions]

## What This Skill Covers

- Item 1
- Item 2
- Item 3

## What This Skill Does NOT Cover

- Out-of-scope item 1
- Out-of-scope item 2
(See references/GAPS.md for full scope boundary)

## How to Use This Skill

[Quick reference]

## Playbooks

- playbook/create/PLAYBOOK.md — [Purpose]
- playbook/review/PLAYBOOK.md — [Purpose]
- playbook/refactor/PLAYBOOK.md — [Purpose]
- ...

## Examples

- examples/good-pattern.md — [What it shows]
- examples/bad-pattern.md — [What it shows]

## Tooling

[Describe shared utilities available in tooling/]

## References

- references/deep-dive-1.md
- references/deep-dive-2.md

## How Agents Use This Skill

[How qa.tester.agent.md or qa.security-reviewer.agent.md invokes this]
```

---

## Playbook Anatomy: playbook/[phase]/PLAYBOOK.md

Each playbook is a step-by-step workflow for a specific phase. Example structure:

```markdown
# Testing Patterns: Create Playbook

## Purpose

This playbook guides you through designing a test strategy for a feature.

## When to Use

When starting to plan test coverage for a new feature or major refactor.

## Steps

### Step 1: Understand Requirements
- Read acceptance criteria
- Identify edge cases
- Define failure modes

### Step 2: Design Test Strategy
- Decide: unit vs integration vs e2e
- Identify test scenarios
- Plan mock/stub strategy

### Step 3: Structure Tests
- Set up test file naming
- Plan fixtures/factories
- Design test helper functions

## Output

A test strategy document that includes:
- Test scenarios (happy path, error paths, edge cases)
- Mock/stub strategy
- Test file structure

## Tools

Use tooling/coverage-calculator.ts to verify coverage plan.

## Examples

See examples/good-test-example.md for well-designed tests.
```

---

## Coverage: coverage/COVERAGE.md

Every skill must have explicit coverage documentation:

```markdown
# Testing Patterns: Coverage

## What This Skill Covers

✅ Unit test design
✅ Integration test design
✅ Test naming conventions
✅ Mock and stub patterns
✅ Edge case identification
✅ Error path testing
✅ Assertion patterns

## What This Skill DOES NOT Cover

❌ Performance testing (see performance-validation skill)
❌ Security testing (see security-patterns skill)
❌ Load testing
❌ CI/CD pipeline configuration
❌ Test framework selection (Mocha, Jest, etc.)

## Known Limitations

- This skill assumes single-threaded code; async/concurrency testing has specialized guides in references/
- This skill does NOT handle browser automation (Selenium, Cypress) — those have domain-specific skills
- This skill focuses on backend/service testing, not UI testing

## Gaps & Future Work

- ML model testing (roadmap: Q2 2027)
- Snapshot testing best practices (roadmap: Q3 2027)
```

---

## Examples: examples/

Examples should be real, concrete, and annotated:

```markdown
# Good Test Example

## What Makes This Good

✅ Clear test names
✅ Covers happy path AND error path
✅ Uses descriptive assertions
✅ Minimal mocking
✅ No hardcoded test data (uses factories)

## Code

[Actual code example]

## Key Takeaways

- [Learning 1]
- [Learning 2]
- [Learning 3]
```

---

## Tooling: tooling/

Shared utilities that agents and skills use:

```typescript
// tooling/test-quality-checker.ts

export class TestQualityChecker {
  /**
   * Analyze test quality beyond coverage percentage
   * @param testFile - Path to test file
   * @returns Quality report with evidence
   */
  async analyzeTestQuality(testFile: string): Promise<TestQualityReport> {
    return {
      coverage: 0.89,
      edgeCasesCovered: ['empty input', 'null', 'timeout'],
      edgeCasesMissing: ['negative amount', 'unicode'],
      brittlePatterns: ['hardcoded IDs', 'time-dependent assertions'],
      confidence: 0.92
    };
  }
}
```

---

## How to Write a Skill

### 1. Start with SKILL.md

Define:
- **When**: When should agents use this skill?
- **What**: What does it cover? What doesn't it?
- **How**: How do agents invoke it?

### 2. Create Playbooks for Major Workflows

For each phase (create, review, refactor, analyze):
- Document the exact steps
- Provide templates and checklists
- Link to examples

### 3. Add Examples

Real, annotated examples that show:
- Good patterns (✅)
- Bad patterns (❌)
- Edge cases (⚠️)

### 4. Build Tooling

Shared utilities that:
- Analyze code systematically
- Produce structured output
- Are reusable by multiple agents and skills

### 5. Document Coverage

Be explicit about:
- What this skill DOES handle
- What it DOESN'T handle
- Known limitations

---

## How Agents Use Skills

**Example: qa.tester.agent.md**

```markdown
# qa.tester.agent.md

You are a test quality reviewer.

Your job:
1. Delegate to skills/testing-patterns skill
2. Interpret the findings
3. Make a go/no-go decision

When analyzing test quality:
- Use skills/testing-patterns/playbook/review/PLAYBOOK.md
- Run tooling/test-quality-checker.ts
- Consult examples/good-test-example.md and examples/bad-test-example.md
- Reference skills/testing-patterns/references/edge-case-taxonomy.md for completeness

Report your findings with evidence, confidence, and rationale.
```

---

## Skill Versioning & Evolution

Skills evolve as we learn:

```yaml
# SKILL.md frontmatter
version: "1.0.0"
changelog:
  1.0.0: "Initial release"
  1.1.0: "Added async/await patterns guide"
  2.0.0: "Reorganized playbooks; added AI-generated code detection"
```

When a skill changes:
- Update playbook/*/PLAYBOOK.md
- Add examples/new-pattern.md
- Update references/
- Bump version
- Log changes in changelog

---

## Skill Governance

### Quality Standards for Skills

- [ ] SKILL.md complete with metadata
- [ ] All playbooks documented
- [ ] Coverage/COVERAGE.md and coverage/GAPS.md written
- [ ] At least 3 examples provided
- [ ] Tooling/shared utilities implemented
- [ ] References reviewed and current
- [ ] Peer review by 2+ senior engineers
- [ ] Tested with 3+ real-world scenarios
- [ ] Documentation reviewed for clarity

### Maintenance

- Skills reviewed quarterly
- Feedback loops tracked (false positives, missed findings)
- Updates published with changelog
- Agents automatically inherit improvements

---

## Conclusion

QualityAI skills are the **reusable expertise layer** of the platform. They encode:
- 18+ years of QA leadership
- Industry best practices
- Lessons learned from thousands of PRs and code reviews
- Proven playbooks for quality validation

By building comprehensive skills and keeping agents lightweight, we ensure:
- **Durability**: Methodology stays; people change
- **Scalability**: New agents use existing skills
- **Auditability**: Every finding traces to a published skill
- **Improvement**: Feedback loops improve skills over time
