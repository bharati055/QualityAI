# Bad pattern — cases copied from the diff

## What went wrong

The agent opened `RefundService` first and listed the tests the coding agent had already written:

- `refundsFullAmount`
- `rejectsNonPositiveAmount`

Both rows left `source` blank. AC-2 (partial refund) and FM-14 (retry after an accepted timeout) were in the specs and never appeared. Nothing was flagged `unmentioned`. The report called the change covered because the new tests were green.

That is the shared-assumption miss this skill exists to catch. A green full-refund test does not name AC-2 or FM-14.

## Fragment the validator rejects

```json
{
  "specs_read_before_diff": false,
  "compared_to_diff": true,
  "sources_consulted": {
    "ac": "present",
    "journey": "present",
    "failure_mode": "present"
  },
  "source_gaps": [],
  "skipped": [],
  "cases": [
    {
      "id": "refunds-full-amount",
      "source": "ac",
      "source_ref": "",
      "title": "refundsFullAmount",
      "expected": "test passes",
      "mentioned_in_diff": true,
      "diff_evidence": "",
      "flags": ["unmentioned"],
      "also_from": []
    }
  ],
  "diff_only": []
}
```

The checker rejects this fragment: `specs_read_before_diff` is false, `source_ref` is empty, and a mentioned case still has flag `unmentioned` with no `diff_evidence`. The title `refundsFullAmount` is a test method. Derive would refuse that too — titles come from the spec outcome. The checker does not judge title wording.

## What to do instead

Run `playbook/derive` with the diff closed. Then `playbook/compare`. Use `examples/good-pattern.md`.
