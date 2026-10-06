# Testing Patterns: Failure Analysis Playbook

<!--
skill_id: testing-patterns
phase: failure-analysis
version: "1.0.0"
-->

## Purpose

Analyze why tests failed and whether the test or code is wrong.

## When to Use

- Failing tests / flakes

## When NOT to Use

- Do not silence failures

## Inputs

| Input | Required | Description |
|---|---|---|
| Change / diff | yes | Files or PR under review |
| Requirement text | no | AC or ticket text when relevant |
| Prior findings | no | From other agents |

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

### Step 1: Reproduce

- Isolate failing case

### Step 2: Classify

- Product bug vs bad test vs env flake

### Step 3: Recommend fix path

- Code, test, or infra

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No material issues for this phase |
| warn | Gaps exist but not critical-path blockers |
| fail | Critical-path gaps with evidence |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Phase recommendation: pass | warn | fail
- Findings list (may be empty)
- Findings with `skill_applied`: `testing-patterns#failure-analysis`
- Short summary for the orchestrator

## Examples

- `../../examples/good-test-example.md` — Strong happy + failure coverage
- `../../examples/bad-test-example.md` — Brittle / hollow assertions

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
