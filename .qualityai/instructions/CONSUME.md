# Consume QualityAI

How a host repository loads this pack.

## Contract (tool-agnostic)

1. Vendor this tree as `.qualityai/` at the host repo root (copy, subtree, or submodule).
2. Tell your coding agent to:
   - read `.qualityai/instructions/` first,
   - run agents under `.qualityai/agents/`,
   - delegate methodology to `.qualityai/skills/` only,
   - emit findings per `FINDING-SCHEMA.md`.
3. No network service, GitHub App, Jira, or CLI is required for v1.

Other tools (Claude Code, Copilot, etc.): add the same pointer in that tool’s instruction file. The pack itself does not change per tool.

## Cursor example (`AGENTS.md`)

Add or extend the host repo `AGENTS.md`:

```markdown
# Agent instructions

## QualityAI

For quality review, requirement alignment, test quality, security review, architecture fit,
AI-assisted review depth, or deployment-readiness recommendations:

1. Read `.qualityai/instructions/REVIEW-FLOW.md` and `.qualityai/instructions/FINDING-SCHEMA.md`.
2. Follow `.qualityai/agents/qa.orchestrator.agent.md` unless the user asks for a single specialist.
3. Agents must delegate to `.qualityai/skills/<skill-id>/` and must not invent checklists inline.
4. Gates recommend; do not merge, push, or deploy as part of QualityAI review.
5. Prefer language-agnostic guidance; use Java only when a code sample is required; use Python for scripts.
```

A complete example also lives at the QualityAI repository root `AGENTS.md`.

## What to copy

Minimum:

- `.qualityai/instructions/`
- `.qualityai/agents/`
- `.qualityai/skills/`
- `.qualityai/templates/` (for authors extending skills)
- `.qualityai/README.md`

Root product docs (`PROJECT-REQUIREMENTS.md`, etc.) are optional for consumers.

## Versioning

Treat skill IDs and agent role names as stable APIs. Prefer additive playbooks over renaming IDs.
