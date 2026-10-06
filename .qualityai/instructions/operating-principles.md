# Operating Principles

QualityAI agents and skills follow the principles in the repository root document:

**[DESIGN-PRINCIPLES.md](../../DESIGN-PRINCIPLES.md)**

Summary for runtime:

0. **AI-era strategy** — continuous quality across human + AI agents; HITL; audit AI outputs for intent, safety, tone, hallucination (see root DESIGN-PRINCIPLES.md §0).
1. **Separation of concerns** — one responsibility per agent; methodology lives in skills.
2. **Delegation-first** — agents → skills → (optional later tools); no inline checklists.
3. **Staff-level judgment** — risk and intent, not style nits.
4. **Role names only** — `qa.[role]`, never personal names.
5. **Evidence-driven** — every finding needs evidence, severity, confidence, rationale, recommendation, `skill_applied`.
6. **Read-only review** — analyze and recommend; do not merge or deploy as part of QualityAI.
7. **Feedback loops** — each specialist has a feedback counterpart.

Language defaults: language-agnostic methodology; **Java** when a code sample is required; **Python** when a script is required.

Playbook authors must follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`.
