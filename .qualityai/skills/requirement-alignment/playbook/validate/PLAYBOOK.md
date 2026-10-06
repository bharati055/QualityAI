# Requirement Alignment: Validate Playbook

<!--
skill_id: requirement-alignment
phase: validate
version: "1.0.0"
-->

## Purpose

Decide whether the change satisfies stated intent with evidence.

## When to Use

- Map playbook completed

## When NOT to Use

- Do not deep-dive security/perf — related skills

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

### Step 1: Verify mapped AC

- Confirm evidence actually implements the AC

### Step 2: Score alignment

- pass / warn / fail recommendation for requirement fit

### Step 3: Emit findings

- Use schema; skill_applied requirement-alignment#validate

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
- Findings with `skill_applied`: `requirement-alignment#validate`
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
