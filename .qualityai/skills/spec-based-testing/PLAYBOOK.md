# Spec-Based Testing — Quick Start

1. Open `SKILL.md`.
2. Run phases in order: `playbook/derive` → `playbook/compare` → `playbook/report`.
3. Do not open the feature diff during `derive`.
4. Every case names `source` (`ac`, `journey`, or `failure_mode`) and `source_ref`.
5. `compare` adds flag `unmentioned` when the change never mentions the case.
6. Check the finished JSON:

```bash
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py path/to/case-set.json
```
