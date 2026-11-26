# QualityAI Pack

Drop-in markdown pack to **scale QA with AI**: role-agents, shared skills, context docs, workflows.

Vendor as `.qualityai/`. Point your coding agent at it. No GitHub/Jira/CLI required for v1.

## Layout

```text
.qualityai/
├── instructions/   # workflows, AI/human boundary, review flow, schema
├── templates/      # playbook + context doc forms
├── context/        # host knowledge (strategy, gates, squad, journeys, architecture)
├── evals/          # incident, revert, and false-positive cases
├── agents/         # role / specialist agents + gates/
└── skills/         # shared methodology
```

## Quick start

Follow **`instructions/ONBOARDING.md`** end-to-end. Short version:

1. Copy this folder to `your-repo/.qualityai/`.
2. Fill `context/` from templates (strategy, test types, frameworks, stage gates).
3. Point the agent (Cursor: `instructions/CONSUME.md`).
4. Ask for: feature test suggestion | spec-based tests | PR review | coverage & gaps | an eval case.

## Pack integrity

From the QualityAI repo root (the checker is not part of the vendored pack):

```bash
python3 scripts/validate_pack.py --self-check   # unit tests + all pack checkers
python3 scripts/validate_pack.py --root <dir>   # contract check only
```

It verifies skill folder contents and frontmatter, relative links, skill ids referenced by agents, gates, `WORKFLOWS.md` and `FINDING-SCHEMA.md`, no `- [ ]` checklists in `*.agent.md`, and stub status/banner sync in `context/`. Add new skills with the full folder set (`SKILL.md`, `PLAYBOOK.md`, `coverage/`, `playbook/<phase>/`, good and bad `examples/`, `references/`).

## Rules

- Shared skills; roles differ by **context scope**.
- Findings use `instructions/FINDING-SCHEMA.md`.
- AI may open a PR; must not push to `main` (`instructions/AI-HUMAN-BOUNDARY.md`).
- Language-agnostic; Java for code samples; Python for scripts.
