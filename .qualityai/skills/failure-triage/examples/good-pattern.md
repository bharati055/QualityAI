# Good Failure Triage

## Scenario

API test fails intermittently at night; same build passes locally; dependency health dashboard showed 502 spike.

## Classification

- Category: `environment`
- Evidence: CI logs + dependency status window matching failure times
- Recommendation: Re-run after dependency stable; do not file product bug yet
- `skill_applied`: `failure-triage#classify`
