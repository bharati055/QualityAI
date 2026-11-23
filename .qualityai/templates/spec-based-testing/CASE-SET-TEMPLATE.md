# Spec-based case set

Copy the JSON into the review output (or a file next to the change under review). Replace every placeholder. Then run:

```bash
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py path/to/case-set.json
```

Field rules: `.qualityai/skills/spec-based-testing/references/case-set.md`.

```json
{
  "specs_read_before_diff": true,
  "compared_to_diff": true,
  "sources_consulted": {
    "ac": "present",
    "journey": "out_of_scope",
    "failure_mode": "missing"
  },
  "source_gaps": [
    {
      "source": "failure_mode",
      "note": "context missing — architecture FMEA is still a stub"
    }
  ],
  "skipped": [],
  "cases": [
    {
      "id": "ac-replace-me",
      "source": "ac",
      "source_ref": "AC-1",
      "title": "Replace with the behavior from the criterion",
      "expected": "Replace with the observable outcome",
      "mentioned_in_diff": false,
      "diff_evidence": "",
      "flags": ["unmentioned"],
      "also_from": []
    }
  ],
  "diff_only": []
}
```

This skeleton is an engineer-shaped draft: AC is `present`, journeys are `out_of_scope`, and FMEA is `missing` so the gap stays visible. When a source is really in scope, set it to `present` and add its cases. `source_gaps` lists only `missing` sources.
