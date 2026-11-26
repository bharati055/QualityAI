# Good Failure Triage

Three failures from one nightly run, each with a class, two independent signals, and an owner.

## 1. Environment

API test fails intermittently at night; same build passes locally; dependency health dashboard showed 502 spike.

- Category: `environment`
- Evidence: CI log shows 502 from `stock-service` at 02:11 UTC; 14 other tests that call it failed in the same 4-minute window; status page lists the degradation 02:05-02:20; next run on the same SHA is green
- Recommendation: re-run after the dependency is stable; do not file a product bug yet; ask the platform owner for the cause
- `skill_applied`: `failure-triage#classify`

## 2. Test script issue

`CheckoutIT#shouldConfirmBooking` fails on the confirm click.

- Category: `test_script_issue`
- Evidence: run 8812 fails, run 8813 passes on the same SHA `3fa9c1d`; `Thread.sleep(500)` before `page.click("#confirm")` at lines 88-94; no product change in the window
- Recommendation: `@squad-payments` replaces the sleep with an explicit wait and shows 10 green runs; quarantine only if it fails 3 times in 7 days (`suite-trust.md`)
- `skill_applied`: `failure-triage#recommend`

## 3. Product defect

`RefundApiTest#refundsFullAmount` fails on every run since commit `b71e0aa`.

- Category: `product_defect`
- Evidence: assertion expects `refunded == 100.00`, response returns `80.00`; the commit changed fee handling; AC-2 says full refund; fails on a clean checkout
- Recommendation: test stays active; human files the defect with the repro; gate is blocked until fixed
- `skill_applied`: `failure-triage#classify`
