# Headline Workflows

Test scaling is the product headline. PR review is a first-class workflow. All workflows obey `AI-HUMAN-BOUNDARY.md` and `FINDING-SCHEMA.md`.

## 1. Feature test suggestion

**When:** Feature code is being generated or proposed (including toward more autonomous coding).

**Goal:** Recommend which test types and cases the feature needs before/while it lands.

**Inputs:** Acceptance criteria, journeys, FMEA, and `.qualityai/context/` (test-strategy, test-types, frameworks, quality-gates, squad/journeys/architecture as relevant). The feature diff is an input to §5 step 2, after the case set exists.

**Routing:**

1. `qa.orchestrator` loads context by scope.
2. Run §5 (spec-based test generation) so the case list comes from AC, journeys, and FMEA before anyone treats coding-agent tests as that list.
3. `qa.engineer` — design the squad cases via `unit-testing` / `api-testing` / `integration-testing` / `test-automation`.
4. `qa.lead` — journey / cross-app / external-deps / `contract-testing` / stage gates.
5. `qa.architect` — `performance-validation`, `soak-testing`, deep security when risk warrants. Failure-mode cases are already in §5.

**Output:** Prioritized test plan (types + scenarios + suggested stage: PR/DEV/SIT/…), gaps if context is missing, findings schema for blockers.

## 2. PR review

**When:** A PR is raised or a review is requested.

**Goal:** Evidence-backed quality review of the change and its tests.

**Flow:** Follow `REVIEW-FLOW.md` (specialists/role-agents → feedback → critic → sequential gates).

When the change has acceptance criteria, journeys, or FMEA, include §5 so the test-quality gate can see cases the diff never mentioned.

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

## 5. Spec-based test generation

**When:** Feature test suggestion, or a review where tests may share the coding agent's assumptions.

**Goal:** Derive cases from acceptance criteria, journeys, and FMEA first. Compare that set to the feature diff afterward. Name the source of every case. Flag cases the change never mentioned.

**Order:**

1. `spec-based-testing` / `derive` — build the case set with the feature diff closed. Sources are `ac` (engineer), `journey` (lead), and `failure_mode` (architect). If a source is missing, say **context missing**. Do not invent AC, journeys, or failure modes.
2. `spec-based-testing` / `compare` — open the feature diff. Mark each case `mentioned_in_diff`. Add flag `unmentioned` when the diff never mentions the case. List diff tests that match no spec case as `diff_only`.
3. `spec-based-testing` / `report` — emit the case table, findings, and the JSON case set. Check it with `.qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py`.

**Routing:** The orchestrator merges role case sets using `.qualityai/skills/spec-based-testing/references/case-set.md` (a source is `present` if any role read it), then runs compare once. A single-role request derives only that role's sources and marks the others `out_of_scope`.

**Output:** Case set (source and source ref on every case) and findings for `unmentioned` cases (`skill_applied: spec-based-testing#compare`). Hand test design to the test-type skill. Humans merge.

## 6. Eval / incident harness

**When:** An incident escaped, a change was reverted, or a QualityAI finding was a false positive.

**Goal:** Store a record, then a regression case the same agent or skill should meet next time: input, bad outcome, expected finding.

**Order:**

1. `eval-harness` / `record` — write `.qualityai/evals/records/rec-<slug>.md` (`incident`, `revert`, or `false_positive`) naming the agent or skill that missed it.
2. `eval-harness` / `case` — write `.qualityai/evals/cases/eval-<slug>.md` with input, bad outcome, and expected finding.
3. `eval-harness` / `check` — confirm the pair. Run `.qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals`.

**Routing:** The role that owned the miss drafts the pair. `qa.lead` keeps the set reviewable. The orchestrator does not drop a miss that has no case.

**Output:** The two files, via PR. The harness does not run the case in CI and does not file a ticket.

## Context loading by role

| Role | Primary context |
|---|---|
| `qa.engineer` | `context/squad/`, frameworks, `test-types.md` |
| `qa.lead` | `context/journeys/`, integrations, `quality-gates/` |
| `qa.architect` | `context/architecture/` (incl. FMEA), `performance-testing.md` |
