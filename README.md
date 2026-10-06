# QualityAI

Open-source **QA skills, agents, and instructions** that any repository can vendor and run through an AI coding agent.

v1 is a drop-in markdown pack under `.qualityai/`. It is not a CI product, not a Jira product, and not a rules engine. GitHub Actions, Jira intake, and GCO telemetry are later addons.

## What v1 is

- **Skills** — reusable QA methodology (playbooks, coverage/gaps, examples). Skills are the single source of expertise.
- **Agents** — thin role files that delegate to skills, interpret findings, and recommend go/no-go. They do not re-implement checklists.
- **Instructions** — how a host repo loads the pack, how review flow runs, and the evidence/output contract.

Copy `.qualityai/` into another repo. Point that repo’s agent instructions at it (Cursor: see `AGENTS.md` / `.qualityai/instructions/CONSUME.md`). Run a review. No GitHub, Jira, or CLI required.

The pack already lives in this repository under [`.qualityai/`](.qualityai/).

## What v1 is not

- GitHub workflows or Actions
- Jira (or other tracker) integration
- GCO / observability telemetry
- A local CLI or YAML rules engine
- Merge-blocking enforcement (gates recommend; humans decide)

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
