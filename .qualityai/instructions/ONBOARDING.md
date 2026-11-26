# Onboarding QualityAI into a product repo

How a product team plugs this pack into their Git repository and makes agents useful for **their** domain, architecture, and frameworks.

Agents are **not** fine-tuned per product. They become domain-aware by reading **templated context docs** plus your code. Skills stay shared; **context is product-specific**.

Also read: `CONSUME.md`, `WORKFLOWS.md`, `AI-HUMAN-BOUNDARY.md`.

---

## Mental model

| Layer | Owner | Changes per product? |
|---|---|---|
| Skills, role-agents, workflows, finding schema | QualityAI (this pack) | No — vendor as-is |
| `.qualityai/context/` | Product team | **Yes** — domain, architecture, frameworks, gates, journeys |
| Host `AGENTS.md` (or equivalent) | Product team | Thin pointer only |

```text
Your product repo
├── AGENTS.md              ← points at .qualityai/
├── .qualityai/
│   ├── instructions/      ← how to run (from QualityAI)
│   ├── agents/            ← Engineer / Lead / Architect (from QualityAI)
│   ├── skills/            ← shared craft (from QualityAI)
│   └── context/           ← YOU fill this (product knowledge)
├── src/
└── tests/
```

---

## Step 1 — Vendor the pack

Choose one:

```bash
# Copy (simplest)
cp -r /path/to/QualityAI/.qualityai ./your-service/.qualityai

# Or git submodule / subtree (better for updates)
# git submodule add <QualityAI-url> vendor/QualityAI
# then symlink or copy .qualityai from the submodule
```

Minimum to keep:

- `instructions/`
- `agents/`
- `skills/`
- `templates/`
- `context/` (start from the shipped stubs)
- `evals/` (records and regression cases)
- `README.md`

---

## Step 2 — Point your coding agent at the pack

### Cursor

Add or extend repo-root `AGENTS.md`:

```markdown
# Agent instructions

## QualityAI

1. Read `.qualityai/instructions/ONBOARDING.md` only when setting up; for day-to-day work read `WORKFLOWS.md`, `AI-HUMAN-BOUNDARY.md`, and `FINDING-SCHEMA.md`.
2. Follow `.qualityai/agents/qa.orchestrator.agent.md` unless a single role is requested (`qa.engineer` / `qa.lead` / `qa.architect`).
3. Load product knowledge from `.qualityai/context/` before suggesting tests or reviewing.
4. Delegate methodology to `.qualityai/skills/<skill-id>/`; do not invent checklists.
5. AI may open a PR; must not push to `main`, merge, or deploy. Humans approve.
6. Language-agnostic; Java for code samples; Python for scripts.
```

### Other tools (Claude Code, Copilot, etc.)

Same contract: point that tool’s instruction file at `.qualityai/`. The pack does not change per tool. See `CONSUME.md`.

---

## Step 3 — Capture product knowledge (the real work)

Fill `.qualityai/context/` **before** expecting strong results. Use forms under `templates/context/`.

**Stub rule:** Files marked `> **STUB — implement as needed by this project.**` (and `status: stub`) are **optional placeholders**. Do not treat TODO/empty stub content as product truth. Agents must say **"context missing"** rather than invent facts until the stub is implemented. See `context/README.md` and `templates/context/STUB-BANNER.md`.

### Priority order (minimum viable → deep)

| Priority | Path | Owner role | Purpose |
|---|---|---|---|
| P0 | `test-strategy.md` | Lead | Risk classes, ownership |
| P0 | `test-types.md` | Shared | When to use each test type |
| P0 | `test-automation-framework.md` | Engineer | Playwright/Selenium (or equiv.) paths, tags |
| P0 | `quality-gates/GitWorkflow_PR.md` | Lead | What must pass at PR |
| P1 | `quality-gates/GitWorkflow_*.md` | Lead | DEV → Prod matrices |
| P1 | `squad/*.md` | Engineer | Product area + local rules |
| P1 | `journeys/*.md` (start with **one** critical journey; use `templates/context/JOURNEY-TEMPLATE.md`) | Lead | Path + deps + **journey SLIs** (latency p95/p99, pass rate, concurrency, availability, data quality/completeness) |
| P1–P2 | `performance-testing.md` | Architect | Gatling/JMeter, SLIs |
| P1–P2 | `architecture/*.md` | Architect | SUT, FMEA |
| P1–P2 | `suite-trust.md` | Lead | Flake thresholds, quarantine fields, expiry (defaults shipped; tune) |

### P2 stubs (implement as needed — not required for day-1 pilot)

| Stub path | Fill when… |
|---|---|
| `environments.md` | CI failures are mis-triaged as product bugs |
| `test-data.md` | Data/PII/fixture issues cause flakes or risk |
| `security-testing.md` | Security reviews need product trust-boundary facts |
| `api-and-contracts.md` | API/contract skills lack spec locations |
| `observability.md` | RCA needs dashboards/metrics (prep for GCO) |
| `nfr.md` | Need system defaults / cross-cutting NFRs (journey SLIs still go on the journey file) |
| `glossary.md` | Domain language is ambiguous |

Leaving P2 stubs unfilled is OK. Implement only when a workflow needs them.

### Migration tip

If knowledge lives in Confluence today:

1. Pick pages for strategy, test types, frameworks, CI gates, top journeys.
2. Paste/adapt into the matching `.md` templates (keep tables; avoid vague prose).
3. Open a PR; human QA Lead/Architect approves.
4. Delete or link the Confluence page as “source moved to repo.”

Humans author; AI may **propose** context updates **only via PR** (`AI-HUMAN-BOUNDARY.md`).

---

## Step 4 — Pilot (do not boil the ocean)

1. **One squad**, **one service**, **one critical journey**.
2. Run workflows in order:
   - Feature **test suggestion** on a real feature (`WORKFLOWS.md` §1)
   - **PR review** on a real PR (`REVIEW-FLOW.md`)
   - **Coverage & gaps** for that journey (`WORKFLOWS.md` §3)
   - **Spec-based test generation** on that feature (`WORKFLOWS.md` §5)
   - Optional: **failure triage / flaky quarantine** on real CI noise (`WORKFLOWS.md` §4)
   - When a suggestion was wrong, record one **eval case** (`WORKFLOWS.md` §6)
3. When suggestions are wrong, **fix context or add an example** — do not fork skills casually.

### Independence rule

QA role-agents derive tests from **acceptance criteria, journeys, and FMEA** before they compare those cases to the feature diff. Follow `WORKFLOWS.md` §5 and skill `spec-based-testing`.

Every case names its source (`ac`, `journey`, or `failure_mode`). Cases the code change never mentioned are flagged `unmentioned`. Coding-agent tests are a comparison input, not the spec.

---

## Step 5 — Suggested timeline

| When | Outcome |
|---|---|
| Week 1 | Pack vendored; `AGENTS.md` wired; P0 context filled (skeletons OK) |
| Week 2 | One journey + squad notes; first test-suggestion + PR review runs |
| Week 3 | Fix context gaps from real misses; start triage/quarantine on flakes |
| Week 4+ | Architecture/FMEA/perf; more journeys; later CI addon for gates |

---

## Step 6 — Later (Phase 2/3 addons)

Not required for first value:

- Risk-tiered autonomy (low / medium / high HITL)
- GitHub Actions posting QualityAI reports / enforcing `quality-gates/` matrices
- Jira AC intake and quarantine ticket create/sync (the quarantine metadata checker already ships: `flaky-quarantine/tooling/validate_quarantine.py`)
- GCO metrics for SLOs, load requirements, failure RCA

Spec-based test generation and the eval harness are already in the pack (`WORKFLOWS.md` §5 and §6). They are markdown workflows plus a Python checker. They do not run CI and they do not file tickets.

Keep using the same skills and context; addons only adapt delivery.

---

## Roles & RACI (product side)

| Activity | Engineer | Lead | Architect | Human approver |
|---|---|---|---|---|
| Fill `squad/` | R | C | I | A (PR) |
| Fill `journeys/` + gates | C | R | C | A (PR) |
| Fill `architecture/` + perf | I | C | R | A (PR) |
| Run day-to-day workflows | R | R | R | — |
| Merge to `main` | — | — | — | **A** |

R = does work, A = accountable approval, C = consulted, I = informed.

---

## Done when

- [ ] `.qualityai/` present and agent pointer configured
- [ ] P0 context files filled for this product
- [ ] At least one critical journey documented
- [ ] Team has run test suggestion + PR review once on real work
- [ ] Everyone knows: AI opens PRs; humans merge to `main`

---

## Troubleshooting

| Symptom | Likely fix |
|---|---|
| Generic / useless test suggestions | Fill `squad/`, `test-types.md`, framework doc |
| Misses cross-service risk | Fill `journeys/` + integrations |
| Ignores your Playwright/Selenium layout | Complete `test-automation-framework.md` paths/tags |
| Suggests wrong stage checks | Edit `quality-gates/GitWorkflow_*.md` |
| Mis-labels env failures as product bugs | Implement stub `environments.md` |
| Flakes / quarantine chaos | Tune `suite-trust.md` thresholds; keep `.qualityai/quarantine/` records passing `validate_quarantine.py` |
| API/contract suggestions miss specs | Implement stub `api-and-contracts.md` |
| Agents invent domain terms | Implement stub `glossary.md` |
| Agents treat stub TODOs as facts | Remind: stubs ≠ truth; report context missing |
| Agents edit `main` directly | Re-assert `AI-HUMAN-BOUNDARY.md` in host `AGENTS.md` |
