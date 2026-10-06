# Security Patterns: Refactor Playbook

<!--
skill_id: security-patterns
phase: refactor
version: "1.0.0"
-->

## Purpose

Propose secure refactors that preserve behavior.

## When to Use

- After high/medium findings

## When NOT to Use

- Do not apply patches in read-only review unless asked

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

### Step 1: Prefer standard libs

- Known validators/auth frameworks

### Step 2: Least privilege

- Narrow trust

### Step 3: Verify with tests

- Hand off scenarios to testing-patterns

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
- Findings with `skill_applied`: `security-patterns#refactor`
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
