# Requirement Alignment: Map Playbook

<!--
skill_id: requirement-alignment
phase: map
version: "1.0.0"
-->

## Purpose

Map each acceptance criterion to evidence in the change (or mark unmapped).

## When to Use

- Parse playbook completed or AC list available

## When NOT to Use

- Do not judge test quality here — hand off to testing-patterns

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

### Step 1: Build matrix

- For each AC, note supporting files/behaviors or UNMAPPED

### Step 2: Check partial maps

- Flag AC only partially addressed

### Step 3: Surface orphans

- Large change areas with no AC mapping — possible scope creep

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
- Findings with `skill_applied`: `requirement-alignment#map`
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
