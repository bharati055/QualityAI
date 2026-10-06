---
name: security-patterns
description: Review for secrets, injection, auth/session issues, and unsafe defaults.
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: ['security', 'validation', 'secrets']
domain: security
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **Review for secrets, injection, auth/session issues, and unsafe defaults.**

## What This Skill Covers

- Secret leakage patterns
- Input validation / injection risks
- AuthZ/AuthN footguns at code level
- Unsafe defaults and error handling that leaks data

## What This Skill Does NOT Cover

- Full penetration testing
- Cloud IAM redesign
- Compliance certification

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: security-patterns#...`.

## Playbooks

- `playbook/create/PLAYBOOK.md` — Design secure approach for a feature touching trust boundaries.
- `playbook/review/PLAYBOOK.md` — Review the change for security issues with evidence.
- `playbook/validate/PLAYBOOK.md` — Validate that claimed security controls exist and are wired.
- `playbook/refactor/PLAYBOOK.md` — Propose secure refactors that preserve behavior.
- `playbook/failure-analysis/PLAYBOOK.md` — Analyze a security incident or near-miss for systemic gaps.

## Examples

- `examples/secure-auth-flow.md` — Sane authz checks
- `examples/insecure-auth-flow.md` — Missing authz
- `examples/secret-detection-example.md` — Hardcoded secret pattern
- `examples/input-validation-example.md` — Validated vs raw input (Java sample ok)

## Tooling

Optional. Not required for v1.

## References

- `references/owasp-top-10.md` — Map findings to OWASP themes
- `references/secret-patterns.md` — Secret shapes to watch
- `references/input-validation-rules.md` — Validation expectations
- `references/output-encoding.md` — Encoding notes
- `references/threat-model.md` — Lightweight threat sketch

## How Agents Use This Skill

Primary agent: `qa.security-reviewer`.

Delegate here; do not copy this methodology into the agent file.
