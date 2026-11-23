# Case set contract

Finished output of `spec-based-testing#report`. UTF-8 JSON. `tooling/validate_spec_cases.py` checks this shape.

## Top level

| Field | Required | Values |
|---|---|---|
| `specs_read_before_diff` | yes | `true`. Derive finished before the diff was used. |
| `compared_to_diff` | yes | `true` on a finished set. |
| `sources_consulted` | yes | Object with keys `ac`, `journey`, `failure_mode`. Each value is `present`, `missing`, or `out_of_scope`. At least one is `present`. |
| `source_gaps` | yes | One `{source, note}` for each source that is `missing`. Empty array when none are missing. |
| `skipped` | yes | Criteria seen and not turned into cases (usually untestable AC). `{source, source_ref, note}`. Empty array is valid. |
| `cases` | yes | Derived cases. May be empty only when every present source had nothing in scope (explain in `skipped` or leave a gap note). |
| `diff_only` | yes | Tests or behaviors found in the diff that match no case. `{evidence, note}`. Empty array is valid. |

`missing` means the spec was in scope and absent or still a stub. Say **context missing** in the note. Do not invent the spec.

`out_of_scope` means this role was not asked for that source. A single-role run uses it for the other two sources.

## Case

| Field | Required | Values |
|---|---|---|
| `id` | yes | `^[a-z0-9]+(-[a-z0-9]+)*$`. Unique in the set. |
| `source` | yes | `ac`, `journey`, or `failure_mode` |
| `source_ref` | yes | Id the spec already uses (`AC-2`, `journey-checkout#step-4`, `FM-14`). Non-empty. |
| `title` | yes | Behavior the case proves |
| `expected` | yes | Observable outcome from the spec |
| `mentioned_in_diff` | yes | Boolean. See `mentioned-in-diff.md`. |
| `diff_evidence` | yes | File and symbol, or a short quote, when mentioned. Empty string when not mentioned. |
| `flags` | yes | `["unmentioned"]` when `mentioned_in_diff` is false. `[]` when true. |
| `also_from` | yes | Extra `{source, source_ref}` pairs when another spec states the same behavior. `[]` if none. |
| `suggested_test_type` | no | One of `unit-testing`, `api-testing`, `integration-testing`, `contract-testing`, `test-automation`, `soak-testing`, `performance-validation` |

A case `source` must be a source marked `present`.

## Source order

Derive in this order so the primary `source` is stable when two specs overlap: acceptance criteria, then journeys, then failure modes. Put the later spec in `also_from`.

## Worked file

`../examples/refund-case-set.json`
