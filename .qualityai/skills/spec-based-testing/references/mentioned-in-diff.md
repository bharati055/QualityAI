# When the diff mentions a case

Set `mentioned_in_diff` to true only when a reviewer can point at the **same behavior** in the feature diff.

Count any of these as a mention:

- A test whose name or assertion states the case outcome
- Production code whose branch or comment states that outcome
- PR or change text that states the case in words a reviewer can quote

Record the pointer in `diff_evidence` (`RefundServiceTest#refundsFullAmount` or `src/RefundService.java` plus a short quote).

Do not count these as a mention:

- The same class or file was edited
- A nearby happy path passes
- The coding agent wrote a test that shares the implementation's assumptions
- A `diff_only` test that matches no `source_ref`

When there is no mention, set `mentioned_in_diff` to false, `diff_evidence` to `""`, and `flags` to `["unmentioned"]`.

`diff_only` is a separate list. Those rows have no spec source. Hand their quality to `testing-patterns`. Do not relabel them as `ac`, `journey`, or `failure_mode`.
