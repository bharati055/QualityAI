---
name: testing-patterns
description: Design and review tests for meaningful coverage of behavior, failures, and edge cases.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['testing', 'edge-cases', 'assertions']
domain: testing
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Design and review tests for meaningful coverage of behavior, failures, and edge cases.**

## What This Skill Covers

- Unit/integration test design
- Happy, failure, and edge paths
- Assertion quality and brittleness
- Failure analysis of tests

## What This Skill Does NOT Cover

- Performance/load testing (performance-validation)
- Security testing methodology (security-patterns)
- Choosing a specific framework as dogma

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: testing-patterns#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md` — Design a test strategy for a feature or change.
- `playbook/plan/PLAYBOOK.md` — Plan execution order, fixtures, and data for tests.
- `playbook/review/PLAYBOOK.md` — Review existing tests for quality beyond coverage percentage.
- `playbook/refactor/PLAYBOOK.md` — Improve weak tests while preserving intent.
- `playbook/update/PLAYBOOK.md` — Update tests when production behavior changes.
- `playbook/failure-analysis/PLAYBOOK.md` — Analyze why tests failed and whether the test or code is wrong.

## Examples

- `examples/good-test-example.md` — Strong happy + failure coverage
- `examples/bad-test-example.md` — Brittle / hollow assertions
- `examples/edge-case-example.md` — Boundary and null handling
- `examples/async-handling-example.md` — Timeouts and concurrency notes

## Tooling

Optional. Not required for v1.

## References

- `references/edge-case-taxonomy.md` — Common edge cases
- `references/assertion-patterns.md` — What to assert
- `references/mock-vs-stub.md` — Mocking decision tree
- `references/performance-considerations.md` — When tests intersect perf

## How Agents Use This Skill

Primary agent: `qa.tester`.

Delegate here; do not copy this methodology into the agent file.
