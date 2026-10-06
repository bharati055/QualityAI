# Security Patterns: Failure Analysis Playbook

<!--
skill_id: security-patterns
phase: failure-analysis
version: "1.0.0"
-->

## Purpose

Analyze a security incident or near-miss for systemic gaps.

## When to Use

- Incident, bug bounty, or failed security test

## When NOT to Use

- Do not blame individuals

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

### Step 1: Timeline

- What failed when

### Step 2: Root cause classes

- Missing control vs broken control vs misuse

### Step 3: Prevent recurrence

- Skill/playbook updates + tests

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
- Findings with `skill_applied`: `security-patterns#failure-analysis`
- Short summary for the orchestrator

## Examples

- `../../examples/secure-auth-flow.md` — Sane authz checks
- `../../examples/insecure-auth-flow.md` — Missing authz

## Related Skills

- See SKILL.md Related concerns via orchestrator routing

## Anti-Patterns

- Duplicating another skill's checklist
- Findings without evidence
- Authorship claims (especially for ai-code-detection)

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
