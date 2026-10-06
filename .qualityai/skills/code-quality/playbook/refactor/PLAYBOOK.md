# Code Quality: Refactor Playbook

<!--
skill_id: code-quality
phase: refactor
version: "1.0.0"
-->

## Purpose

Propose maintainability refactors.

## When to Use

- After review

## When NOT to Use

- Do not rewrite for taste alone

## Inputs

| Input | Required | Description |
|---|---|---|
| Change / diff | yes | Files or PR under review |
| Requirement text | no | AC or ticket text when relevant |
| Prior findings | no | From other agents |

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

### Step 1: Smallest safe step

- Extract, rename, dedupe

### Step 2: Preserve behavior

- Require tests via testing-patterns

### Step 3: Avoid drive-by

- Stay in changed area unless risk demands

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No material issues for this phase |
| warn | Gaps exist but not critical-path blockers |
| fail | Critical-path gaps with evidence |

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

- Phase recommendation: pass | warn | fail
- Findings list (may be empty)
- Findings with `skill_applied`: `code-quality#refactor`
- Short summary for the orchestrator

## Examples

- `../../examples/readable-function.md` — Clear structure
- `../../examples/unreadable-function.md` — Dense logic without seams

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
