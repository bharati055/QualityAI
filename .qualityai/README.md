# QualityAI Pack

Drop-in markdown pack: **agents**, **skills**, and **instructions** for requirement-aware QA review.

Vendor this folder into any repo as `.qualityai/`. Point your coding agent at it. No GitHub, Jira, or CLI required for v1.

## Layout

```text
.qualityai/
├── README.md
├── instructions/     # how to load and run the pack
├── templates/        # shared playbook template (all skills follow this)
├── agents/           # thin role files + gates/
└── skills/           # methodology (single source of truth)
```

## Quick start

1. Copy this folder to `your-repo/.qualityai/`.
2. Add a host pointer (Cursor: see `instructions/CONSUME.md` for `AGENTS.md` example).
3. Ask the agent to run a QualityAI review on a change.

## Rules

- Agents **delegate** to skills; they do not re-implement checklists.
- Findings use `instructions/FINDING-SCHEMA.md`.
- Gates **recommend**; humans decide merge.
- Language-agnostic by default; Java for code samples; Python for scripts.
