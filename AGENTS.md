# Agent instructions

## QualityAI

This repository **is** the QualityAI pack. Headline job: **scale testing** with AI role-agents; PR review is a workflow.

1. Read `.qualityai/instructions/WORKFLOWS.md`, `AI-HUMAN-BOUNDARY.md`, `FINDING-SCHEMA.md`.
2. For PR review also follow `REVIEW-FLOW.md`.
3. Follow `.qualityai/agents/qa.orchestrator.agent.md` unless a single role is requested (`qa.engineer` / `qa.lead` / `qa.architect`).
4. Load role scope from `.qualityai/context/` (squad / journeys / architecture + strategy & gates).
5. Agents delegate to `.qualityai/skills/<skill-id>/` (including test-type + `failure-triage` / `flaky-quarantine`); no inline checklists.
6. Playbooks follow `templates/PLAYBOOK-TEMPLATE.md`; context docs follow `templates/context/`.
7. AI may open a PR; **must not** push to `main`, merge, or deploy. Humans approve.
8. Language-agnostic; **Java** for code samples; **Python** for scripts.

Root docs describe product scope. Runtime pack is `.qualityai/`. Consumers: copy `.qualityai/` and see `instructions/CONSUME.md`.
