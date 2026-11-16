# Test Automation Framework

<!--
context_id: test-automation-framework
owner_role: qa.engineer
version: "1.0.0"
last_reviewed: 2026-11-16
-->

## Purpose

How UI/E2E (and related) automation is structured in this repo so `qa.engineer` suggests tests that fit the real framework.

## Content

### Stack

| Item | Value (host fills) |
|---|---|
| Primary tool | Playwright / Selenium / other |
| Language | e.g. Java / TypeScript |
| Runner | e.g. JUnit / TestNG / Playwright test |
| Repo path | e.g. `tests/e2e/` |
| Environments | URLs per DEV/SIT/UAT |

### Conventions

- Page object / screen pattern: [host]
- Test data strategy: [host]
- Tagging for smoke vs full: [host]

### Do / Don't for AI

- DO: propose tests matching existing patterns and tags
- DO NOT: invent a second framework or push to main

## Links

- Skills: `testing-patterns` (→ `test-automation`)
- Gates: `quality-gates/`

## Change control

- Updates via PR only; human approval required.
