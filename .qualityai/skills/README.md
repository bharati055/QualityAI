# Skills

## Cross-cutting

| ID | Purpose |
|---|---|
| `requirement-alignment` | Intent vs change |
| `architecture-patterns` | Design fit and drift |
| `ai-code-detection` | Review-depth rubric (not authorship claims) |
| `testing-patterns` | Umbrella test quality (still valid) |
| `security-patterns` | Security and unsafe defaults |
| `code-quality` | Maintainability and reviewability |
| `performance-validation` | Perf/reliability risk |

## Test-type (split)

| ID | Purpose |
|---|---|
| `unit-testing` | Unit design/review |
| `api-testing` | API design/review |
| `integration-testing` | Integration design/review |
| `contract-testing` | Consumer/provider contracts |
| `test-automation` | UI/E2E (Selenium/Playwright patterns) |
| `soak-testing` | Endurance / soak |

## Suite trust

| ID | Purpose |
|---|---|
| `failure-triage` | product_defect vs test_script_issue vs environment |
| `flaky-quarantine` | Flake detect + quarantine (owner, end date, ticket) |

## Independence and eval

| ID | Purpose |
|---|---|
| `spec-based-testing` | Cases from AC, journeys, and FMEA first; then the feature diff. Flag `unmentioned`. |
| `eval-harness` | Incident, revert, or false positive → regression case for the agent or skill that missed it |

Eval files live under `../evals/` (records and cases).

Each skill: `SKILL.md`, `playbook/`, `coverage/`, `examples/`, `references/`.

Playbooks follow `../templates/PLAYBOOK-TEMPLATE.md`.
