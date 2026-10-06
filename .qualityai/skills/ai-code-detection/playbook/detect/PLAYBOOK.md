# Ai Code Detection: Detect Playbook

<!--
skill_id: ai-code-detection
phase: detect
version: "1.0.0"
-->

## Purpose

Decide whether elevated review depth is warranted. Never assert which model wrote the code.

## When to Use

- Large or generic-looking diffs; user suspects AI-assisted generation

## When NOT to Use

- Do not output 'written by X model' as a finding

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

### Step 1: Collect signals

- Diff size/complexity
- Generic names, missing edge cases, boilerplate patterns
- User/PR statements about AI assistance

### Step 2: Classify depth

- normal | elevated | high — based on signals, not authorship

### Step 3: Document rationale

- Evidence = signals; confidence reflects signal strength

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
- Findings with `skill_applied`: `ai-code-detection#detect`
- Short summary for the orchestrator

## Examples

- `../../examples/high-volume-generic-diff.md` — Signals for elevated depth
- `../../examples/missing-edge-cases.md` — Generated-looking happy-path-only change

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
