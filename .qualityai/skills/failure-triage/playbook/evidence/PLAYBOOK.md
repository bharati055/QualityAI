# Failure Triage: Evidence Playbook

<!--
skill_id: failure-triage
phase: evidence
version: "1.0.0"
-->

## Purpose

Collect and cite the proof behind a failure class. A class is only as good as its evidence, so this phase says what to gather for each class, how many independent signals are enough, and how to cite them so a human can re-check in minutes.

## When to Use

- Before or while `classify`, when the class needs proof
- A reviewer challenges a triage finding ("why environment?")
- A finding has confidence below 0.70 and needs a second signal
- When the orchestrator or role-agent routes `failure-triage` / `evidence` work

## When NOT to Use

- No failure exists to explain (a green run) — nothing to prove
- The class is accepted and the open point is the next action — `recommend`
- The evidence needed is a metrics or trace query this pack cannot reach — record the gap and keep the class `unknown`

## Inputs

| Input | Required | Description |
|---|---|---|
| Failure log and run ids | yes | Same set `classify` uses |
| Run history | yes | Pass/fail per run for the `test_id`, with commit SHA |
| Diff or change list | no | Needed for `product_defect` |
| Dependency or runner status | no | Status page, incident log, CI runner notes for the window |
| Policy | yes | `.qualityai/context/suite-trust.md` |

## Prerequisites

- Read `../../SKILL.md`
- A candidate class from `classify` (or a request to test one)
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`
- Obey `.qualityai/instructions/AI-HUMAN-BOUNDARY.md`

## Steps

### Step 1: Pick the evidence set for the class

| Class | Needs at least two of | Cite as |
|---|---|---|
| `product_defect` | Failing assertion maps to a requirement or AC; repro on a clean checkout; the diff or commit that changed the behavior; same failure on 3 or more runs of one SHA | requirement id, repro command, commit SHA, run ids |
| `test_script_issue` | Pass and fail on one SHA; a timing, order, or shared-state flaw visible in the test code; fails alone but passes in a fresh isolated run (or the reverse); no product change in the window | file and lines, run ids, SHA |
| `environment` | Dependency error codes in the log window; incident or status entry for the same window; failure across unrelated tests at the same minute; passes after the dependency recovers with no change | log lines with timestamps, status link, list of other failing `test_id`s |
| `unknown` | Record what was checked and what was missing | the missing input, by name |

### Step 2: Run the cheap checks first

- Re-read the failing assertion and the test setup; do not trust the summary line.
- Compare the failing run with the nearest green run: same SHA, same runner image, same data set?
- Count other failures in the same run and window; a cluster points away from one test.
- If a rerun is allowed, record both outcomes with run ids. Do not trigger runs yourself; ask the human.

### Step 3: Cite exactly

- File findings use `evidence.file`, `evidence.lines`, and a short `code_snippet`.
- Process findings (no file) use `evidence.file: null` and put run ids, SHAs, and timestamps in `evidence.note`.
- Quote at most a few lines of log; link or name the run for the rest.

### Step 4: Rate the evidence

- Two independent signals: confidence 0.85 or higher
- One signal, or two that share a source (two log lines of one run): 0.50 to 0.69
- A guess: record it as a hypothesis in `rationale`, keep the class `unknown`

### Step 5: Hand back

- Return the evidence set to `classify`, or emit it as its own finding with `skill_applied: failure-triage#evidence`.
- List what was not checked so the human knows the limits.

## Decision Criteria

| Outcome | When |
|---|---|
| pass | Each class in scope has the evidence set from Step 1 |
| warn | One signal only, or a required input was unavailable and is named |
| fail | A class was asserted on a critical journey with no evidence, or evidence was dropped to fit a class |

Severity for findings: missing evidence on a critical-journey failure is high; elsewhere medium or low.

## Output

- Evidence list per failing `test_id`: signal, source, run id or SHA, independence (yes/no)
- Confidence per class
- `skill_applied`: `failure-triage#evidence`
- Gaps the human can close

Example evidence note for an `environment` class:

```text
test_id: InventoryApiTest#returnsStock
run 9104 (2026-11-25 02:11 UTC): 502 from stock-service after 30 s timeout
run 9104: 14 other tests calling stock-service failed in the same 4-minute window
status page: stock-service degraded 02:05-02:20 UTC
run 9105, same SHA 51be0aa: green
independent signals: 3 of 3 (log, cluster, status)
```

## Examples

- `../../examples/good-pattern.md` — evidence set per class
- `../../examples/bad-pattern.md` — one log line used as proof

## Related Skills

- `failure-triage#classify` — consumes this evidence
- `failure-triage#recommend` — acts on the class
- `observability` context (`.qualityai/context/observability.md`) — where logs and dashboards live, when filled

## Anti-Patterns

- One log line as the only proof
- "Environment" without a dependency or runner signal
- Evidence from the coding agent's own tests as proof of intent
- Pasting a whole log instead of the failing lines and run id
- Running or re-running builds the human did not approve

## Notes (optional)

- Language defaults: methodology language-agnostic; Java for code samples; Python for scripts
