# Good pattern — incident becomes a case

A refund change shipped with a green full-refund test. In production the gateway applied the refund, the caller timed out, and the retry sent a second refund. Review never raised failure mode FM-14.

That miss is stored as a pair:

| File | Role |
|---|---|
| `.qualityai/evals/records/rec-refund-double-charge.md` | `incident` record. Target skill `spec-based-testing`. |
| `.qualityai/evals/cases/eval-refund-double-charge.md` | Regression case: input, bad outcome, expected finding |

The case input repeats the AC, the journey step, FM-14, and the Java test that was green. The bad outcome says the engineer treated that test as coverage. The expected finding is the `unmentioned` FM-14 result from `spec-based-testing#compare`. The same record has a second case, `eval-refund-partial`, which locks the unmentioned AC-2.

Two other shipped pairs show the other kinds:

- Revert, aimed at agent `qa.lead`: `.qualityai/evals/cases/eval-checkout-promo-revert.md`
- False positive, aimed at skill `testing-patterns`: `.qualityai/evals/cases/eval-hollow-assert-false-positive.md`

All six files are `example: true`. They teach the shape. A host file for a real miss sets `example: false`.

Check:

```bash
python3 .qualityai/skills/eval-harness/tooling/validate_eval_case.py --root .qualityai/evals
```

`skill_applied`: `eval-harness#case`
