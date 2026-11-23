# Test Strategy

<!--
context_id: test-strategy
owner_role: qa.lead
version: "1.0.0"
last_reviewed: 2026-11-16
-->

## Purpose

Overall QA approach for this product/repo. Role-agents use this when suggesting tests and judging gaps.

## Scope

- In scope: risk-based testing philosophy, environments, ownership
- Out of scope: step-by-step tool setup (see framework docs)

## Content

### Principles

- [Host: e.g. risk-based; shift-left; critical journeys first]

### Risk classes

| Risk class | Examples | Minimum test types |
|---|---|---|
| Critical | Payments, auth, booking confirmations | unit + API + integration + contract + targeted E2E |
| High | Search, recommendations | API + integration + journey smoke |
| Medium | Admin/content | API + unit |
| Low | Copy/config | unit or review-only |

### Ownership

| Concern | Human role | AI role-agent |
|---|---|---|
| Squad feature tests | Squad QA / dev | `qa.engineer` |
| Cross-app journeys | QA Lead | `qa.lead` |
| FMEA / perf / observability | QA Architect | `qa.architect` |

## Links

- `test-types.md`, `quality-gates/`, `journeys/`, `architecture/`
- Skills: `testing-patterns`, `performance-validation`, `requirement-alignment`, `spec-based-testing`, `eval-harness`

## Change control

- Updates via PR only; human approval required.
