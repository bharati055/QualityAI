# Shared Playbook Template

**Every** skill playbook under `.qualityai/skills/*/playbook/*/PLAYBOOK.md` MUST follow this structure. Do not invent alternate section orders.

Copy this file when creating a new playbook. Replace bracketed placeholders. Delete optional sections only if marked optional and unused.

---

```markdown
# [Skill Display Name]: [Phase] Playbook

<!--
skill_id: [canonical-id]
phase: [create|plan|review|refactor|update|validate|parse|map|...]
version: "1.0.0"
-->

## Purpose

One paragraph: what this playbook achieves and why it exists.

## When to Use

- Trigger condition 1
- Trigger condition 2

## When NOT to Use

- Out-of-scope situation (point to another skill or playbook if relevant)

## Inputs

| Input | Required | Description |
|---|---|---|
| Change / diff | yes | Files or PR under review |
| Requirement text | [yes/no] | AC, ticket paste, or in-repo docs |
| Prior findings | no | Output from another agent/skill |

## Prerequisites

- List what must already be true (e.g. SKILL.md read, another playbook done)

## Steps

### Step 1: [Name]

- Concrete actions (imperative bullets)
- What to look for / produce

### Step 2: [Name]

- ...

### Step N: [Name]

- ...

## Decision Criteria

| Outcome | When |
|---|---|
| pass | ... |
| warn | ... |
| fail | ... |

Severity for findings: use high / medium / low per FINDING-SCHEMA.md.

## Output

What the agent must emit:

- Findings conforming to `.qualityai/instructions/FINDING-SCHEMA.md`
- `skill_applied`: `[skill-id]#[section-or-phase]`
- Short summary for the orchestrator

## Examples

- Link to `../../examples/...`
- Brief note on what each example teaches

## Related Skills

- `other-skill-id` — when to hand off (do not duplicate their logic)

## Anti-Patterns

- What NOT to do in this phase

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
```

---

## Checklist for authors

Before merging a new or changed playbook:

- [ ] Filename is `PLAYBOOK.md` under `playbook/<phase>/`
- [ ] Frontmatter comment includes `skill_id` and `phase`
- [ ] Purpose / When / When NOT / Inputs / Steps / Decision Criteria / Output present
- [ ] Steps are actionable (not vague slogans)
- [ ] Findings cite this skill via `skill_applied`
- [ ] No duplicated methodology from another skill
- [ ] Coverage boundaries match `coverage/COVERAGE.md` and `coverage/GAPS.md`
