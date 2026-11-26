# Quarantine Metadata

Machine-checkable format for quarantine records and recommendations. Policy defaults live in `.qualityai/context/suite-trust.md`; the checker is `tooling/validate_quarantine.py`; the JSON Schema is `quarantine.schema.json` (same fields, kept in sync by `--self-check`).

## Record

| Field | Required | Rule |
|---|---|---|
| `test_id` | yes | Stable test identifier, unique across the registry |
| `owner` | yes | Team or person who fixes it; not `TBD` / `unknown` |
| `end_date` | yes | ISO `YYYY-MM-DD`; at most 90 days ahead of the review date |
| `ticket_id` | yes | Tracker id (`QA-1234`), `#42`, `org/repo#42`, or URL |
| `reason` | yes | Evidence of non-determinism, at least 10 characters |
| `exit_criteria` | yes | Observable condition that ends the quarantine, at least 10 characters |
| `start_date` | no | ISO date; not after `end_date` |
| `mechanism` | no | `disabled-annotation`, `tag`, or `ci-skip-list` |
| `notes` | no | Free text |

Unknown fields are rejected so typos do not hide a missing field.

## Where records live

A JSON document with optional `quarantines` (records) and `findings` (FINDING-SCHEMA findings).

- **Registry (applied quarantines):** `.qualityai/quarantine/*.json` in the host repo. Markdown files there are checked through their ```json blocks.
- **Recommendation:** a finding with `skill_applied: flaky-quarantine#quarantine` carries the record in a `quarantine` object. A finding without that object is rejected.
- **Not ready yet** (for example no ticket): emit a `flaky-quarantine#detect` finding that names the blocker. It is not a quarantine recommendation, so no record is allowed until the human supplies a ticket id.

## Expiry

A record whose `end_date` is before the review date needs an escalation finding in the same document:

- `skill_applied: flaky-quarantine#expiry-review`
- `severity: high` or `medium`
- text (`finding`, `evidence.note`, `rationale`, or `recommendation`) names the record's `ticket_id`

Examples may set a top-level `as_of` date so they do not expire; the checker honours it only for shipped examples.

## Muted tests in source

A mute annotation (`@Disabled`, `@Ignore`, TestNG `enabled = false`, `@pytest.mark.skip`, `@unittest.skip`, `it.skip(` / `xit(`, `@Tag("quarantine")`) must have a ticket id on the same line or in the comment line directly above. Conditional skips (`skipif`) are not mutes.

## Run

```bash
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --root .
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --root . --source src/test
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py report.json
python3 .qualityai/skills/flaky-quarantine/tooling/validate_quarantine.py --self-check
```

Issue codes: `QUAR_MISSING`, `QUAR_EMPTY`, `QUAR_SHORT`, `QUAR_DATE`, `QUAR_DATE_FAR`, `QUAR_TICKET`, `QUAR_UNKNOWN`, `QUAR_MECHANISM`, `QUAR_DUPLICATE`, `QUAR_EXPIRED`, `QUAR_MUTE`, `QUAR_SHAPE`, `QUAR_JSON`, `QUAR_EXAMPLE`.
