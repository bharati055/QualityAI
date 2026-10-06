---
name: performance-validation
description: Plan and assess performance/reliability risk; later pairs with GCO metrics for SLOs, load, and RCA.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['performance', 'reliability', 'load']
domain: quality
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Plan and assess performance/reliability risk; later pairs with GCO metrics for SLOs, load, and RCA.**

## What This Skill Covers

- Perf test planning and baselines
- Regression detection mindset
- Bottleneck hypotheses from code/diff
- Linking to future GCO metrics (SLOs, load reqs, RCA)

## What This Skill Does NOT Cover

- Running GCO itself in v1
- Full capacity planning projects
- Micro-benchmark fetishism without risk

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: performance-validation#...`.

## Playbooks

- `playbook/plan/PLAYBOOK.md` — Plan performance validation for a change.
- `playbook/baseline/PLAYBOOK.md` — Establish or reference a performance baseline.
- `playbook/execute/PLAYBOOK.md` — Execute or specify how to execute perf checks.
- `playbook/analyze/PLAYBOOK.md` — Interpret results against requirements and risk.
- `playbook/regression-detection/PLAYBOOK.md` — Detect performance regressions in a change.
- `playbook/refactor/PLAYBOOK.md` — Propose performance-oriented refactors.

## Examples

- `examples/good-performance.md` — Bounded work on hot path
- `examples/performance-regression.md` — N+1 / unbounded pattern
- `examples/optimization-opportunity.md` — Safe optimization candidate
- `examples/load-test-analysis.md` — Reading load results

## Tooling

Optional. Not required for v1.

## References

- `references/performance-metrics.md` — What to measure
- `references/baseline-strategy.md` — Baselines
- `references/load-testing-patterns.md` — Load patterns
- `references/common-bottlenecks.md` — Common smells
- `references/gco-use-cases.md` — SLOs/alerts, load reqs, RCA via GCP Monitoring

## How Agents Use This Skill

Primary agent: `qa.architect / qa.tester (as routed)`.

Delegate here; do not copy this methodology into the agent file.
