# Security Patterns: Create Playbook

<!--
skill_id: security-patterns
phase: create
version: "1.0.0"
-->

## Purpose

Design secure approach for a feature touching trust boundaries.

## When to Use

- New API, auth, payment, or PII path

## When NOT to Use

- Do not invent crypto algorithms

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

### Step 1: Threat sketch

- Assets, attackers, entry points

### Step 2: Controls

- Validation, authz, secrets handling

### Step 3: Test plan link

- Point to testing-patterns for security-relevant tests

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
- Findings with `skill_applied`: `security-patterns#create`
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
