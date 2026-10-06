# Security Patterns: Validate Playbook

<!--
skill_id: security-patterns
phase: validate
version: "1.0.0"
-->

## Purpose

Validate that claimed security controls exist and are wired.

## When to Use

- After fixes or when PR claims 'secured'

## When NOT to Use

- Do not assume a library = correct usage

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

### Step 1: Trace control

- From entry to enforcement

### Step 2: Negative cases

- Unauthorized / invalid input paths

### Step 3: Residual risk

- Document what remains

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
- Findings with `skill_applied`: `security-patterns#validate`
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
