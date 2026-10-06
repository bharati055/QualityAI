# Agent instructions

## QualityAI

This repository **is** the QualityAI pack. For quality review work in this repo or when validating the pack:

1. Read `.qualityai/instructions/REVIEW-FLOW.md` and `.qualityai/instructions/FINDING-SCHEMA.md`.
2. Follow `.qualityai/agents/qa.orchestrator.agent.md` unless a single specialist is requested.
3. Agents must delegate to `.qualityai/skills/<skill-id>/` and must not invent checklists inline.
4. All skill playbooks must follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`.
5. Gates recommend; do not merge, push, or deploy as part of QualityAI review.
6. Prefer language-agnostic guidance; use **Java** when a code sample is required; use **Python** for scripts.

Product design docs at the repo root (`PROJECT-REQUIREMENTS.md`, `ARCHITECTURE.md`, `SKILLS-FRAMEWORK.md`, `DESIGN-PRINCIPLES.md`) describe scope. Runtime methodology lives under `.qualityai/`.

To consume this pack in another repo, copy `.qualityai/` and see `.qualityai/instructions/CONSUME.md`.
