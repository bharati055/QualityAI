# Spec-Based Testing: Derive Playbook

<!--
skill_id: spec-based-testing
phase: derive
version: "1.0.0"
-->

## Purpose

Build the test-case set from acceptance criteria, journeys, and failure modes while the feature diff stays closed. Cases come from those specs so a later comparison can see what the change never mentioned.

## When to Use

- Workflow `.qualityai/instructions/WORKFLOWS.md` §5, step 1
- Feature test suggestion, before any test list is taken from the coding agent
- The start of every `spec-based-testing` run

## When NOT to Use

- The acceptance criterion is vague or untestable — hand that criterion to `requirement-alignment#parse`. Do not invent an outcome.
- The task is to judge an assertion or a brittle test — `testing-patterns`
- The task is to classify a CI failure — `failure-triage`
- `compare` has already started. Do not add spec cases from the diff during compare.

## Inputs

| Input | Required | Description |
|---|---|---|
| Acceptance criteria | yes for `qa.engineer` | Pasted AC or in-repo text. Not a Jira fetch. |
| Journeys | yes for `qa.lead` | `.qualityai/context/journeys/` |
| Failure modes | yes for `qa.architect` | `.qualityai/context/architecture/` FMEA, plus journey "Known failure modes" when they state a mode |
| Other role's sources | no | Mark `out_of_scope` on a single-role run |
| Feature diff | no | Must stay closed in this phase |
| Prior findings | no | Parsed AC from `requirement-alignment` when that already ran |

## Prerequisites

- Read `../../SKILL.md` and `../../references/case-set.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`
- Stub context (`status: stub`, or the STUB banner) is **context missing**, not product truth

## Steps

### Step 1: Close the diff

- Do not open the feature diff, its tests, or a coding-agent test plan in this phase.
- If the diff is already in the prompt, do not copy cases out of it. Derive only from the specs.
- Set `specs_read_before_diff` to true. Leave `compared_to_diff` false until `compare`. Leave `mentioned_in_diff` unset until `compare`.

### Step 2: Record which sources exist

- For `ac`, `journey`, and `failure_mode`, set `present`, `missing`, or `out_of_scope`.
- `missing`: the source is in this role's scope and the text is absent or still a stub. Add `source_gaps` with note **context missing**. Do not invent rows.
- `out_of_scope`: a single-role request did not include that source.
- At least one source is `present`, or stop with a gap finding and no invented cases.

### Step 3: Cases from acceptance criteria

- When `ac` is `present`, add one case per testable criterion.
- `source` is `ac`. `source_ref` is the id the criterion already has.
- `title` and `expected` use the criterion's outcome, not class or method names from code.
- If a criterion has no observable outcome, do not mint a case. Append `skipped` and point at `requirement-alignment#parse`.

### Step 4: Cases from journeys

- When `journey` is `present`, add a case for each in-scope step: the success signal, and the dependency failure impact when the journey states one.
- `source` is `journey`. `source_ref` is `journey-<id>#step-<n>` (or the journey file anchor the team already uses).
- Add an SLI case only when that journey file states a target. A blank or TODO target is **context missing** for that metric — `skipped`, not an invented number.
- When `failure_mode` is `present`, a journey "Known failure modes" row that is not already in the FMEA uses `source` `failure_mode` and a `source_ref` that points at the journey section. When `failure_mode` is `out_of_scope`, leave those rows for the architect.

### Step 5: Cases from failure modes

- When `failure_mode` is `present`, add one case per in-scope FMEA row: the failure, the detection the test must show, and the expected containment from the row.
- `source` is `failure_mode`. `source_ref` is the FMEA id (`FM-14` or the row id already in the file).
- Do not add a mode the FMEA does not contain.

### Step 6: Keep every source when specs overlap

- Derive in order: AC, then journeys, then failure modes.
- If a later spec states a behavior already in the set, keep the earlier `source` and append `{source, source_ref}` to `also_from`.
- Do not drop the failure mode because an AC already mentioned a happy path.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Every in-scope source is `present` or `out_of_scope`, and each present source was read |
| warn | An in-scope source is `missing` (context missing) but at least one source produced an honest set |
| fail | No spec source was present, or cases were taken from the diff |

Severity for findings: high / medium / low per FINDING-SCHEMA.md. A missing FMEA on a payment, auth, or critical-journey change is high as a process gap. A missing source on a low-risk change is medium.

## Output

- Draft case set (JSON fields in `references/case-set.md`) with `compared_to_diff` false
- `source_gaps` and `skipped` filled
- Findings for missing in-scope sources, `skill_applied`: `spec-based-testing#derive`
- Short summary for the orchestrator: counts per source, and that the diff is still closed

## Examples

- `../../examples/good-pattern.md` — AC, journey, and FM-14 derived before the refund diff is opened
- `../../examples/bad-pattern.md` — test names copied from `RefundService` with no source

## Related Skills

- `requirement-alignment` — parse vague AC; do not derive cases there
- `testing-patterns` and test-type skills — design the test after `report`
- `eval-harness` — when a later incident shows this derive step was skipped

## Anti-Patterns

- Opening the diff to "see what to test"
- Copying coding-agent test names onto AC ids
- Inventing an FMEA row, journey step, or criterion when the file is missing or a stub
- Leaving `source` or `source_ref` blank
- One case that silently merges a happy path and a failure mode

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if a code sample is needed; Python if a script is needed
- The validator runs on the finished set after `compare`, not on this draft
