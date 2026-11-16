# Context Doc Template

Every file under `.qualityai/context/` SHOULD follow this shape so humans and AI parse it consistently.

```markdown
# [Title]

<!--
context_id: [stable-id]
owner_role: [qa.engineer|qa.lead|qa.architect|shared]
version: "1.0.0"
last_reviewed: YYYY-MM-DD
-->

## Purpose

One paragraph: what this doc is for.

## Scope

- In scope: ...
- Out of scope: ...

## Content

### [Section]

Structured bullets or tables. Prefer tables for gates and matrices.

## Links

- Related context docs
- Related skills (skill-id)

## Change control

- Updates via PR only; human approval required.
```
