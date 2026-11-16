# Headline Workflows

Test scaling is the product headline. PR review is a first-class workflow. All workflows obey `AI-HUMAN-BOUNDARY.md` and `FINDING-SCHEMA.md`.

## 1. Feature test suggestion

**When:** Feature code is being generated or proposed (including toward more autonomous coding).

**Goal:** Recommend which test types and cases the feature needs before/while it lands.

**Inputs:** Requirement/AC text, change or design notes, `.qualityai/context/` (test-strategy, test-types, frameworks, quality-gates, squad/journeys/architecture as relevant).

**Routing:**

1. `qa.orchestrator` loads context by scope.
2. `qa.engineer` — area-level tests via `unit-testing` / `api-testing` / `integration-testing` / `test-automation`.
3. `qa.lead` — journey / cross-app / external-deps / `contract-testing` / stage gates.
4. `qa.architect` — FMEA, `performance-validation`, `soak-testing`, deep security when risk warrants.
5. Prefer **independent** suggestions from AC/journeys/FMEA, not only from coding-agent tests.

**Output:** Prioritized test plan (types + scenarios + suggested stage: PR/DEV/SIT/…), gaps if context is missing, findings schema for blockers.

## 2. PR review

**When:** A PR is raised or a review is requested.

**Goal:** Evidence-backed quality review of the change and its tests.

**Flow:** Follow `REVIEW-FLOW.md` (specialists/role-agents → feedback → critic → sequential gates).

**Output:** Consolidated report; recommendations only; human merges.

## 3. Coverage and gaps

**When:** Asked to show what is covered vs missing for a feature, epic, or release slice.

**Goal:** Depict coverage against AC, critical journeys, and stage-gate expectations—not line-coverage alone.

**Routing:** Lead owns journey matrix; Engineer owns squad/framework mapping; Architect flags system-level untested failure modes.

**Output:** Coverage matrix + gap list + recommended next tests, with `skill_applied` citations.

## 4. Failure triage & quarantine (suite trust)

**When:** CI/regression failures, intermittent reds, or “is this a real bug?” questions.

**Goal:** Keep the suite trustworthy — failures should mean genuine product risk (or clearly owned test/env debt).

**Routing:**

1. `failure-triage` — classify `product_defect` | `test_script_issue` | `environment` | `unknown`.
2. If flake: `flaky-quarantine` — require **owner**, **end date**, **ticket ID**, reason, exit criteria.
3. `qa.lead` escalates expired quarantines; humans attach/create Jira (Phase 2 can automate link).

**Output:** Triage findings + optional quarantine recommendation (apply via PR; no push to main).

## Context loading by role

| Role | Primary context |
|---|---|
| `qa.engineer` | `context/squad/`, frameworks, `test-types.md` |
| `qa.lead` | `context/journeys/`, integrations, `quality-gates/` |
| `qa.architect` | `context/architecture/` (incl. FMEA), `performance-testing.md` |
