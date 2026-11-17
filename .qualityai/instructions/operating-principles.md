# Operating Principles

QualityAI agents and skills follow the principles in the repository root document:

**[DESIGN-PRINCIPLES.md](../../DESIGN-PRINCIPLES.md)**

Product teams plugging this into a new repo: start with **[ONBOARDING.md](ONBOARDING.md)**.

Summary for runtime:

0. **AI-era strategy** — continuous quality across human + AI agents; HITL; audit AI outputs (DESIGN-PRINCIPLES.md §0).
1. **Role × skill × scope** — Engineer / Lead / Architect; shared skills; context by altitude (`context/`).
2. **Headline workflows** — test suggestion, PR review, coverage/gaps (`WORKFLOWS.md`).
3. **Separation of concerns** — methodology lives in skills.
4. **Delegation-first** — agents → skills → (optional later tools).
5. **Evidence-driven** — findings per `FINDING-SCHEMA.md`.
6. **AI vs human** — see `AI-HUMAN-BOUNDARY.md` (no push to main; PR + human approval).
7. **Feedback loops** — feedback counterparts + critic.

Language defaults: language-agnostic; **Java** for code samples; **Python** for scripts.

Playbooks: `templates/PLAYBOOK-TEMPLATE.md`. Context docs: `templates/context/`.
