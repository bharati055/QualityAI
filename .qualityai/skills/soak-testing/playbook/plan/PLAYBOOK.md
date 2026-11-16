# Soak Testing: Plan Playbook

<!--
skill_id: soak-testing
phase: plan
version: "1.0.0"
-->

## Purpose

Execute the `plan` phase for soak-testing.

## When to Use

- When the orchestrator or role-agent routes `soak-testing` / `plan` work

## When NOT to Use

- When another skill owns the concern (see SKILL.md gaps)

## Inputs

| Input | Required | Description |
|---|---|---|
| Change / diff / failure logs | yes | Subject under analysis |
| Requirement / journey / FMEA text | no | For independent validation |
| Context docs | yes | Relevant `.qualityai/context/` files |
| Prior findings | no | From other agents |

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: Load context

- Read role-appropriate context and this skill's references

### Step 2: Analyze

- Apply `plan` methodology for `soak-testing`
- Prefer evidence over opinion

### Step 3: Emit findings

- Use schema; set `skill_applied: soak-testing#plan`
- For quarantine: require owner, end date, ticket id fields even if ticket created later by human

## Decision Criteria

| Outcome | When |
|---|---|
| pass | No material issues |
| warn | Gaps or debt with clear owner path |
| fail | Critical-path / suite-trust / security gaps with evidence |

## Output

- Phase recommendation: pass | warn | fail
- Findings list
- Short summary for orchestrator

## Examples

- See `../../examples/`

## Related Skills

- `testing-patterns` (umbrella), `failure-triage`, `flaky-quarantine` as applicable

## Anti-Patterns

- Findings without evidence
- Quarantine without owner/end date/ticket
- Treating coding-agent tests as sole proof of intent

## Notes (optional)

- Language-agnostic; Java for code samples; Python for scripts
