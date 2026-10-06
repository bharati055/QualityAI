# Requirement Alignment: Parse Playbook

<!--
skill_id: requirement-alignment
phase: parse
version: "1.0.0"
-->

## Purpose

Extract clear intent, acceptance criteria, and constraints from requirement text.

## When to Use

- Requirement text exists or is claimed missing

## When NOT to Use

- Do not invent product requirements when none were provided — record the gap

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

### Step 1: Inventory sources

- Collect PR description, ticket paste, in-repo docs, user-stated AC
- If none: emit a finding that requirements are missing

### Step 2: Normalize AC

- List discrete acceptance criteria
- Mark vague items (untestable language)
- Note constraints (security, perf, compliance) called out in text

### Step 3: Publish intent summary

- Write a short intent paragraph and AC checklist for downstream playbooks

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
- Findings with `skill_applied`: `requirement-alignment#parse`
- Short summary for the orchestrator

## Examples

- `../../examples/clear-requirement.md` — Well-formed AC and how to parse them
- `../../examples/vague-requirement.md` — Untestable language and how to flag it

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
