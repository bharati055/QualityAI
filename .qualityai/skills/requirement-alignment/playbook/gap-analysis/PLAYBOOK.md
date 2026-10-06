# Requirement Alignment: Gap Analysis Playbook

<!--
skill_id: requirement-alignment
phase: gap-analysis
version: "1.0.0"
-->

## Purpose

List missing requirements, missing implementation, and missing validation.

## When to Use

- After validate, or when user asks what is missing

## When NOT to Use

- Do not fill gaps by writing code unless user asks outside review

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

### Step 1: Gap catalog

- Missing AC
- AC without code
- Code without AC
- Untestable AC

### Step 2: Prioritize

- Order by business risk

### Step 3: Recommend

- Concrete human actions to close gaps

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
- Findings with `skill_applied`: `requirement-alignment#gap-analysis`
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
