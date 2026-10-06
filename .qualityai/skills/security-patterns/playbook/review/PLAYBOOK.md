# Security Patterns: Review Playbook

<!--
skill_id: security-patterns
phase: review
version: "1.0.0"
-->

## Purpose

Review the change for security issues with evidence.

## When to Use

- Any change on trust boundary or user input

## When NOT to Use

- Do not spam low-value style findings

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

### Step 1: Trust boundaries

- Inputs, outputs, auth, data stores

### Step 2: Check patterns

- Secrets, injection, authz gaps, unsafe defaults

### Step 3: Emit findings

- High severity for exploitable paths

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
- Findings with `skill_applied`: `security-patterns#review`
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
