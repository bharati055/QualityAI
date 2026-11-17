# QualityAI

Open-source **AI QA operating model**: role-agents, shared testing skills, and machine-readable context docs any repository can vendor.

**Headline:** scale testing as product code and features grow—without hiring QA 1:1. Suggest tests when feature code is generated; review when a PR is raised; depict coverage and gaps. GitHub Actions, Jira, and GCO are later addons.

## What v1 is

- **Role-agents** — QA Engineer (squad), QA Lead, QA Architect (+ orchestrator/critic). Same craft skills; different scope.
- **Skills** — shared methodology (API, automation, unit, integration, contract, security, performance/SOAK, … as the library evolves).
- **Context** — templated `.md` (test strategy, frameworks, stage gates PR→Prod, journeys, architecture/FMEA)—AI-readable Confluence-as-code.
- **Workflows** — feature test suggestion, PR review, coverage & gaps.
- **HITL** — AI may open a PR; humans approve merge to `main`.

Copy `.qualityai/` into another repo. Follow [`.qualityai/instructions/ONBOARDING.md`](.qualityai/instructions/ONBOARDING.md). Point the agent at it (Cursor: `AGENTS.md` / `CONSUME.md`). Fill `context/`. Run a workflow.

The pack lives under [`.qualityai/`](.qualityai/).

## What v1 is not

- GitHub workflows or Actions (context *documents* stage gates; CI enforcement is later)
- Jira (or other tracker) integration
- Live GCO wiring (docs prepare for it)
- A local CLI or YAML rules engine
- Autonomous merge/deploy (AI must not push to main)

See [PROJECT-REQUIREMENTS.md](PROJECT-REQUIREMENTS.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Consume in any repo

The pack is **tool-agnostic**. Any markdown-capable coding agent can read `.qualityai/`.

v1 documents a concrete **Cursor** wiring via host `AGENTS.md`. Other tools (Claude Code, Copilot, etc.) use the same pack — point their instruction file at `.qualityai/`.

```text
your-project/
├── .qualityai/          # vendored from this repo
│   ├── agents/
│   ├── skills/
│   └── instructions/
├── AGENTS.md            # Cursor example: point agents at .qualityai/
└── ...
```

Until the pack files exist in this repository, treat the layout in ARCHITECTURE.md as the v1 contract.

## Language and example defaults

- Skills and playbooks are **language-agnostic** by default.
- When a code sample is needed: **Java**.
- When a script is needed: **Python**.
- Every skill playbook follows one **shared playbook template**.

## Later addons

1. GitHub workflows / Actions
2. Jira requirement intake
3. GCO (GCP Monitoring / Console): SLOs/alerts, performance/load requirements from metrics, test-failure RCA/reporting
4. Optional CLI / rules engine that consumes the same skills

## Packaging

This repository **is** the publishable open-source pack (root docs + `.qualityai/` to vendor). Licensed under [MIT](LICENSE).

## Design docs

- [PROJECT-REQUIREMENTS.md](PROJECT-REQUIREMENTS.md) — product scope, v1 vs addons
- [ARCHITECTURE.md](ARCHITECTURE.md) — pack layout and review flow
- [SKILLS-FRAMEWORK.md](SKILLS-FRAMEWORK.md) — how a skill is structured
- [DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md) — agent operating model
