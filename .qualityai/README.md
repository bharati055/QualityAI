# QualityAI Pack

Drop-in markdown pack to **scale QA with AI**: role-agents, shared skills, context docs, workflows.

Vendor as `.qualityai/`. Point your coding agent at it. No GitHub/Jira/CLI required for v1.

## Layout

```text
.qualityai/
├── instructions/   # workflows, AI/human boundary, review flow, schema
├── templates/      # playbook + context doc forms
├── context/        # host knowledge (strategy, gates, squad, journeys, architecture)
├── agents/         # role / specialist agents + gates/
└── skills/         # shared methodology
```

## Quick start

Follow **`instructions/ONBOARDING.md`** end-to-end. Short version:

1. Copy this folder to `your-repo/.qualityai/`.
2. Fill `context/` from templates (strategy, test types, frameworks, stage gates).
3. Point the agent (Cursor: `instructions/CONSUME.md`).
4. Ask for: feature test suggestion | PR review | coverage & gaps.

## Rules

- Shared skills; roles differ by **context scope**.
- Findings use `instructions/FINDING-SCHEMA.md`.
- AI may open a PR; must not push to `main` (`instructions/AI-HUMAN-BOUNDARY.md`).
- Language-agnostic; Java for code samples; Python for scripts.
