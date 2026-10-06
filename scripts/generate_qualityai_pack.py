#!/usr/bin/env python3
"""Generate QualityAI v1 agents, gates, and skill pack files."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / ".qualityai"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n") if content.startswith("\n") else content, encoding="utf-8")
    if not content.endswith("\n"):
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")


def playbook(
    skill_id: str,
    display: str,
    phase: str,
    purpose: str,
    when: list[str],
    when_not: list[str],
    inputs: list[tuple[str, str, str]],
    steps: list[tuple[str, list[str]]],
    decisions: list[tuple[str, str]],
    output: list[str],
    examples: list[str],
    related: list[str],
    anti: list[str],
) -> str:
    input_rows = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in inputs)
    step_blocks = []
    for i, (name, bullets) in enumerate(steps, 1):
        body = "\n".join(f"- {b}" for b in bullets)
        step_blocks.append(f"### Step {i}: {name}\n\n{body}")
    steps_text = "\n\n".join(step_blocks)
    dec_rows = "\n".join(f"| {a} | {b} |" for a, b in decisions)
    return f"""# {display}: {phase.replace('-', ' ').title()} Playbook

<!--
skill_id: {skill_id}
phase: {phase}
version: "1.0.0"
-->

## Purpose

{purpose}

## When to Use

{chr(10).join(f"- {w}" for w in when)}

## When NOT to Use

{chr(10).join(f"- {w}" for w in when_not)}

## Inputs

| Input | Required | Description |
|---|---|---|
{input_rows}

## Prerequisites

- Read `../../SKILL.md`
- Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure
- Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md`

## Steps

{steps_text}

## Decision Criteria

| Outcome | When |
|---|---|
{dec_rows}

Severity for findings: high / medium / low per FINDING-SCHEMA.md.

## Output

{chr(10).join(f"- {o}" for o in output)}
- Findings with `skill_applied`: `{skill_id}#{phase}`
- Short summary for the orchestrator

## Examples

{chr(10).join(f"- {e}" for e in examples)}

## Related Skills

{chr(10).join(f"- {r}" for r in related)}

## Anti-Patterns

{chr(10).join(f"- {a}" for a in anti)}

## Notes (optional)

- Language defaults: methodology language-agnostic; Java if code sample needed; Python if script needed
"""


def agent(role: str, title: str, mission: str, skills: list[str], playbooks: list[str]) -> str:
    skill_lines = "\n".join(f"- `{s}` → `.qualityai/skills/{s}/SKILL.md`" for s in skills)
    pb = "\n".join(f"- {p}" for p in playbooks)
    return f"""# qa.{role}.agent

You are the **{title}** for QualityAI.

## Mission

{mission}

## Rules

1. Delegate methodology to the skills listed below. Do **not** invent inline checklists.
2. Follow `.qualityai/instructions/FINDING-SCHEMA.md` for every finding.
3. Recommend only. Do not merge, push, deploy, or silently edit host code as part of review.
4. After your analysis, invite validation by `qa.{role}.agent.feedback.md` (orchestrator may run this).
5. Language-agnostic by default; Java for required code samples; Python for scripts.

## Skills

{skill_lines}

## Typical playbooks

{pb}

## Output

- Findings (schema)
- Brief risk summary for orchestrator / critic
- Explicit confidence on each finding
"""


def feedback(role: str, title: str) -> str:
    return f"""# qa.{role}.agent.feedback

You validate the **{title}** specialist (`qa.{role}.agent.md`).

## Mission

Challenge the primary agent's findings. Reduce false positives and under-claiming.

## Checks (for each finding)

1. Is there concrete **evidence** (file/lines or explicit process gap)?
2. Is **severity** justified by blast radius / business risk?
3. Is **confidence** calibrated (see FINDING-SCHEMA bands)?
4. Does `skill_applied` point at a real skill section?
5. What critical consideration might be **missing**?

## Rules

- Do not re-implement the skill. Point at gaps and ask for skill re-application if needed.
- Prefer adjusting confidence/severity over inventing new unrelated findings.
- Escalate unresolved uncertainty to `qa.critic` / human.

## Output

- Validated findings list (accepted / adjusted / rejected with reason)
- Missing considerations (if any)
- Confidence deltas
"""


def gate(name: str, title: str, skill: str, questions: list[str], fail: str, warn: str, ok: str) -> str:
    qs = "\n".join(f"- {q}" for q in questions)
    return f"""# Gate: {title}

Instruction-level quality gate. Recommendation only — humans decide merge.

## Depends on

- Skill: `{skill}`
- Prior specialist findings for this concern

## Questions

{qs}

## Recommendation

| Result | When |
|---|---|
| fail | {fail} |
| warn | {warn} |
| pass | {ok} |

## Output

- Gate id: `{name}`
- Recommendation: pass | warn | fail
- Top 3 linked findings (ids or short titles)
- One sentence for the consolidated report
"""


ROLES = [
    (
        "orchestrator",
        "Quality Orchestrator",
        "Parse context, select specialists, merge validated findings, run sequential gates, and produce one consolidated QualityAI report.",
        [
            "requirement-alignment",
            "architecture-patterns",
            "ai-code-detection",
            "testing-patterns",
            "security-patterns",
            "code-quality",
            "performance-validation",
        ],
        [
            "Follow `.qualityai/instructions/REVIEW-FLOW.md`",
            "Do not duplicate specialist analysis; route and consolidate",
        ],
    ),
    (
        "researcher",
        "Requirement Researcher",
        "Assess whether the change matches requirement intent and acceptance criteria.",
        ["requirement-alignment"],
        ["skills/requirement-alignment/playbook/parse|map|validate|gap-analysis"],
    ),
    (
        "architect",
        "Architecture Reviewer",
        "Assess design fitness, boundaries, and architectural drift.",
        ["architecture-patterns", "performance-validation"],
        ["skills/architecture-patterns/playbook/design|review|anti-pattern-detection|refactor"],
    ),
    (
        "tester",
        "Test Quality Reviewer",
        "Assess whether tests meaningfully cover behavior, failure paths, and risk — beyond coverage percentage.",
        ["testing-patterns"],
        ["skills/testing-patterns/playbook/create|plan|review|refactor|update|failure-analysis"],
    ),
    (
        "security-reviewer",
        "Security Reviewer",
        "Assess security and reliability risks: secrets, input handling, auth, unsafe defaults.",
        ["security-patterns"],
        ["skills/security-patterns/playbook/create|review|validate|refactor|failure-analysis"],
    ),
    (
        "code-reviewer",
        "Code Quality Reviewer",
        "Assess maintainability, clarity, duplication, and reviewability of the change.",
        ["code-quality"],
        ["skills/code-quality/playbook/review|refactor|maintainability-assessment"],
    ),
    (
        "ai-detector",
        "AI-Assisted Review Depth Advisor",
        "Apply a review-depth rubric for likely AI-assisted or high-volume generated changes. Do NOT claim which model authored the code.",
        ["ai-code-detection"],
        ["skills/ai-code-detection/playbook/detect|risk-assessment|review-strategy"],
    ),
    (
        "critic",
        "Quality Critic",
        "Reconcile specialist outputs, find blind spots and conflicts, and prioritize business risk.",
        [
            "requirement-alignment",
            "architecture-patterns",
            "ai-code-detection",
            "testing-patterns",
            "security-patterns",
            "code-quality",
            "performance-validation",
        ],
        ["Cross-read specialist + feedback outputs; do not re-run every playbook unless conflict requires it"],
    ),
]


GATES = [
    (
        "requirement",
        "Requirements Gate",
        "requirement-alignment",
        [
            "Is requirement intent clear and testable?",
            "Does the change map to acceptance criteria?",
            "Are gaps or drifts called out with evidence?",
        ],
        "Critical AC unmet or large intent drift with high-severity findings",
        "AC incomplete or partial mapping",
        "Intent clear and change aligned (or N/A with documented reason)",
    ),
    (
        "design",
        "Design Gate",
        "architecture-patterns",
        [
            "Does implementation fit expected architecture/boundaries?",
            "Are anti-patterns or risky drift present?",
        ],
        "High-severity architecture drift on a critical path",
        "Moderate layering/coupling concerns",
        "Design fit acceptable for the change size",
    ),
    (
        "ai-risk",
        "AI-Assisted Risk Gate",
        "ai-code-detection",
        [
            "Does the change warrant elevated review depth?",
            "Were stricter checks applied if yes?",
        ],
        "High review-depth warranted but specialist/security/test gaps remain unaddressed",
        "Elevated depth recommended; residual medium findings",
        "Normal depth sufficient or elevated depth completed cleanly",
    ),
    (
        "test-quality",
        "Test Quality Gate",
        "testing-patterns",
        [
            "Are happy and failure paths covered where risk demands?",
            "Are assertions meaningful (not brittle/vacuous)?",
            "Are skipped/xfailed tests justified?",
        ],
        "Critical path lacks failure-path tests or has hollow assertions",
        "Coverage gaps on non-critical but important paths",
        "Test quality adequate for change risk",
    ),
    (
        "security",
        "Security Gate",
        "security-patterns",
        [
            "Secrets, injection, auth, and validation risks reviewed?",
            "High-severity security findings unresolved?",
        ],
        "Unresolved high-severity security finding",
        "Medium security concerns needing follow-up",
        "No material unresolved security findings",
    ),
    (
        "pr-review",
        "PR Review Gate",
        "code-quality",
        [
            "Is there a high-signal human summary?",
            "Are findings prioritized and actionable?",
        ],
        "Report too noisy or missing critical context for a human reviewer",
        "Summary weak but findings usable",
        "Clear summary and prioritized actions",
    ),
    (
        "deployment-readiness",
        "Deployment Readiness Gate",
        "performance-validation",
        [
            "Cumulative gate recommendations considered?",
            "Any unresolved high risk on critical path?",
            "Perf/reliability risks called out when relevant?",
        ],
        "Any blocking high-risk recommendation remains",
        "Residual medium risks; deploy with caution / follow-ups",
        "No unresolved high risks; residual risk accepted or none",
    ),
]


def skill_readme() -> str:
    return """# Skills

Canonical skill IDs (stable):

| ID | Purpose |
|---|---|
| `requirement-alignment` | Intent vs change |
| `architecture-patterns` | Design fit and drift |
| `ai-code-detection` | Review-depth rubric (not authorship claims) |
| `testing-patterns` | Test quality beyond coverage |
| `security-patterns` | Security and unsafe defaults |
| `code-quality` | Maintainability and reviewability |
| `performance-validation` | Perf/reliability risk |

Each skill: `SKILL.md`, `playbook/`, `coverage/`, `examples/`, `references/`.

All playbooks follow `../templates/PLAYBOOK-TEMPLATE.md`.
"""


SKILLS_META = {
    "requirement-alignment": {
        "desc": "Parse requirements, map them to changes, validate alignment, and find gaps.",
        "domain": "quality",
        "tags": ["requirements", "traceability", "acceptance-criteria"],
        "covers": [
            "Extracting intent and AC from text",
            "Mapping code/diff to requirements",
            "Detecting drift and missing AC",
            "Flagging untestable or vague requirements",
        ],
        "not_covers": [
            "Jira API sync (later addon)",
            "Writing product requirements for the business",
            "Project management / sprint planning",
        ],
        "agents": "qa.researcher",
        "phases": {
            "parse": (
                "Extract clear intent, acceptance criteria, and constraints from requirement text.",
                ["Requirement text exists or is claimed missing"],
                ["Do not invent product requirements when none were provided — record the gap"],
                [
                    (
                        "Inventory sources",
                        [
                            "Collect PR description, ticket paste, in-repo docs, user-stated AC",
                            "If none: emit a finding that requirements are missing",
                        ],
                    ),
                    (
                        "Normalize AC",
                        [
                            "List discrete acceptance criteria",
                            "Mark vague items (untestable language)",
                            "Note constraints (security, perf, compliance) called out in text",
                        ],
                    ),
                    (
                        "Publish intent summary",
                        ["Write a short intent paragraph and AC checklist for downstream playbooks"],
                    ),
                ],
            ),
            "map": (
                "Map each acceptance criterion to evidence in the change (or mark unmapped).",
                ["Parse playbook completed or AC list available"],
                ["Do not judge test quality here — hand off to testing-patterns"],
                [
                    (
                        "Build matrix",
                        ["For each AC, note supporting files/behaviors or UNMAPPED"],
                    ),
                    (
                        "Check partial maps",
                        ["Flag AC only partially addressed"],
                    ),
                    (
                        "Surface orphans",
                        ["Large change areas with no AC mapping — possible scope creep"],
                    ),
                ],
            ),
            "validate": (
                "Decide whether the change satisfies stated intent with evidence.",
                ["Map playbook completed"],
                ["Do not deep-dive security/perf — related skills"],
                [
                    (
                        "Verify mapped AC",
                        ["Confirm evidence actually implements the AC"],
                    ),
                    (
                        "Score alignment",
                        ["pass / warn / fail recommendation for requirement fit"],
                    ),
                    (
                        "Emit findings",
                        ["Use schema; skill_applied requirement-alignment#validate"],
                    ),
                ],
            ),
            "gap-analysis": (
                "List missing requirements, missing implementation, and missing validation.",
                ["After validate, or when user asks what is missing"],
                ["Do not fill gaps by writing code unless user asks outside review"],
                [
                    (
                        "Gap catalog",
                        ["Missing AC", "AC without code", "Code without AC", "Untestable AC"],
                    ),
                    (
                        "Prioritize",
                        ["Order by business risk"],
                    ),
                    (
                        "Recommend",
                        ["Concrete human actions to close gaps"],
                    ),
                ],
            ),
        },
        "examples": [
            ("clear-requirement.md", "Well-formed AC and how to parse them"),
            ("vague-requirement.md", "Untestable language and how to flag it"),
            ("well-aligned-code.md", "Change that maps cleanly to AC"),
            ("drifted-code.md", "Implementation that diverges from intent"),
        ],
        "refs": [
            ("acceptance-criteria-format.md", "What good AC look like"),
            ("traceability-model.md", "AC ↔ change ↔ tests conceptual model"),
            ("jira-integration.md", "Later addon note; v1 uses pasted/in-repo text"),
        ],
    },
    "architecture-patterns": {
        "desc": "Review design fitness, layering, coupling, and architectural drift.",
        "domain": "architecture",
        "tags": ["architecture", "design", "coupling"],
        "covers": [
            "Boundary and layering checks",
            "Coupling/cohesion smells",
            "Anti-pattern detection at design level",
            "Refactor guidance for structure",
        ],
        "not_covers": [
            "Full system redesign",
            "Infrastructure-as-code deep review (unless change includes it)",
            "Micro-optimizations (see performance-validation)",
        ],
        "agents": "qa.architect",
        "phases": {
            "design": (
                "Guide design choices for a change before or during implementation.",
                ["New feature or structural change"],
                ["Do not replace domain product decisions"],
                [
                    ("Identify boundaries", ["Modules, APIs, data ownership"]),
                    ("Choose patterns", ["Fit existing architecture; avoid inventing new layers without need"]),
                    ("Document risks", ["Where design could drift"]),
                ],
            ),
            "review": (
                "Review the change against expected architecture.",
                ["PR or diff review"],
                ["Style-only nits belong in code-quality"],
                [
                    ("Locate touch points", ["Packages/modules changed"]),
                    ("Check boundaries", ["Dependency direction, leakage of internals"]),
                    ("Emit findings", ["Evidence-backed drift or violations"]),
                ],
            ),
            "anti-pattern-detection": (
                "Identify architectural smells in the change.",
                ["Suspected god objects, circular deps, leaky abstractions"],
                ["Do not flag every large class without risk rationale"],
                [
                    ("Scan for smells", ["Tight coupling, circular deps, shared mutable globals"]),
                    ("Assess blast radius", ["Who depends on this?"]),
                    ("Recommend", ["Minimal structural fix direction"]),
                ],
            ),
            "refactor": (
                "Propose structural improvements without rewriting the product.",
                ["After review findings"],
                ["Do not apply refactors during read-only review unless user asks"],
                [
                    ("Prioritize", ["High-risk smells first"]),
                    ("Plan steps", ["Incremental, testable moves"]),
                    ("Guardrails", ["Keep behavior; point to testing-patterns for coverage"]),
                ],
            ),
        },
        "examples": [
            ("monolithic-good.md", "Clear modular monolith boundaries"),
            ("monolithic-bad.md", "Boundary leakage"),
            ("microservice-good.md", "Sensible service boundaries"),
            ("coupling-anti-pattern.md", "Tight coupling example"),
        ],
        "refs": [
            ("SOLID-principles.md", "SOLID as review lenses"),
            ("clean-architecture.md", "Dependency rule"),
            ("coupling-cohesion.md", "Coupling/cohesion checks"),
            ("domain-driven-design.md", "Bounded context hints"),
        ],
    },
    "ai-code-detection": {
        "desc": "Review-depth rubric for likely AI-assisted or high-volume generated changes — not authorship detection.",
        "domain": "quality",
        "tags": ["ai-assisted", "review-depth", "risk"],
        "covers": [
            "Signals that warrant deeper review (size, generic structure, missing edge cases)",
            "Risk/review-depth assessment",
            "Strategy for stricter review without authorship claims",
        ],
        "not_covers": [
            "Claiming Copilot vs Claude vs human authorship as fact",
            "Blocking merges solely on 'looks AI-generated'",
            "Plagiarism detection products",
        ],
        "agents": "qa.ai-detector",
        "phases": {
            "detect": (
                "Decide whether elevated review depth is warranted. Never assert which model wrote the code.",
                ["Large or generic-looking diffs; user suspects AI-assisted generation"],
                ["Do not output 'written by X model' as a finding"],
                [
                    (
                        "Collect signals",
                        [
                            "Diff size/complexity",
                            "Generic names, missing edge cases, boilerplate patterns",
                            "User/PR statements about AI assistance",
                        ],
                    ),
                    (
                        "Classify depth",
                        ["normal | elevated | high — based on signals, not authorship"],
                    ),
                    (
                        "Document rationale",
                        ["Evidence = signals; confidence reflects signal strength"],
                    ),
                ],
            ),
            "risk-assessment": (
                "Translate review-depth into risk focus areas for other specialists.",
                ["After detect"],
                ["Do not replace security-patterns or testing-patterns"],
                [
                    ("Map depth to checks", ["Which gates/skills must be thorough"]),
                    ("Call out blind spots", ["Likely missing validation, tests, error paths"]),
                    ("Set expectations", ["What 'done' means for elevated review"]),
                ],
            ),
            "review-strategy": (
                "Provide a concrete stricter review plan for the orchestrator.",
                ["Elevated or high depth"],
                ["Do not run unrelated skills yourself — recommend them"],
                [
                    ("Sequence checks", ["security, tests, requirements, architecture as needed"]),
                    ("Human attention", ["What a human must still verify"]),
                    ("Exit criteria", ["When elevated review can recommend pass/warn/fail"]),
                ],
            ),
        },
        "examples": [
            ("high-volume-generic-diff.md", "Signals for elevated depth"),
            ("missing-edge-cases.md", "Generated-looking happy-path-only change"),
            ("mixed-generated-human.md", "Mixed change; still no authorship claim"),
            ("well-reviewed-assisted-change.md", "Elevated depth completed well"),
        ],
        "refs": [
            ("review-depth-rubric.md", "normal / elevated / high criteria"),
            ("high-volume-change-signals.md", "Signal catalog"),
            ("false-positive-mitigation.md", "Avoid authorship claims"),
        ],
    },
    "testing-patterns": {
        "desc": "Design and review tests for meaningful coverage of behavior, failures, and edge cases.",
        "domain": "testing",
        "tags": ["testing", "edge-cases", "assertions"],
        "covers": [
            "Unit/integration test design",
            "Happy, failure, and edge paths",
            "Assertion quality and brittleness",
            "Failure analysis of tests",
        ],
        "not_covers": [
            "Performance/load testing (performance-validation)",
            "Security testing methodology (security-patterns)",
            "Choosing a specific framework as dogma",
        ],
        "agents": "qa.tester",
        "phases": {
            "create": (
                "Design a test strategy for a feature or change.",
                ["New feature or major behavior change"],
                ["Do not implement production code here"],
                [
                    ("Understand behavior", ["AC, failure modes, edge cases"]),
                    ("Choose layers", ["unit vs integration vs e2e — justify"]),
                    ("List scenarios", ["Happy, error, boundary, null/empty"]),
                ],
            ),
            "plan": (
                "Plan execution order, fixtures, and data for tests.",
                ["Strategy exists"],
                ["Do not skip risk-based prioritization"],
                [
                    ("Prioritize", ["Critical path first"]),
                    ("Fixtures", ["Factories over hardcoded opaque IDs"]),
                    ("Definition of done", ["Which scenarios must pass before merge recommendation"]),
                ],
            ),
            "review": (
                "Review existing tests for quality beyond coverage percentage.",
                ["PR adds/changes tests or claims coverage"],
                ["Do not equate line coverage with quality"],
                [
                    ("Map tests to AC/risk", ["Missing failure paths?"]),
                    ("Inspect assertions", ["Vacuous or brittle asserts"]),
                    ("Flag skips", ["skipped/xfailed without justification"]),
                ],
            ),
            "refactor": (
                "Improve weak tests while preserving intent.",
                ["After review findings"],
                ["Do not delete coverage without replacement"],
                [
                    ("Target brittle tests", ["Time, order, hardcoded env"]),
                    ("Strengthen asserts", ["Behavior outcomes, not implementation trivia"]),
                    ("Keep signal", ["Prefer fewer strong tests over many weak ones"]),
                ],
            ),
            "update": (
                "Update tests when production behavior changes.",
                ["Code change invalidates old tests"],
                ["Do not blindly update asserts to make red tests green without understanding"],
                [
                    ("Diff behavior", ["What actually changed?"]),
                    ("Adjust scenarios", ["Add/remove/rename tests intentionally"]),
                    ("Re-check failure paths", ["Still covered?"]),
                ],
            ),
            "failure-analysis": (
                "Analyze why tests failed and whether the test or code is wrong.",
                ["Failing tests / flakes"],
                ["Do not silence failures"],
                [
                    ("Reproduce", ["Isolate failing case"]),
                    ("Classify", ["Product bug vs bad test vs env flake"]),
                    ("Recommend fix path", ["Code, test, or infra"]),
                ],
            ),
        },
        "examples": [
            ("good-test-example.md", "Strong happy + failure coverage"),
            ("bad-test-example.md", "Brittle / hollow assertions"),
            ("edge-case-example.md", "Boundary and null handling"),
            ("async-handling-example.md", "Timeouts and concurrency notes"),
        ],
        "refs": [
            ("edge-case-taxonomy.md", "Common edge cases"),
            ("assertion-patterns.md", "What to assert"),
            ("mock-vs-stub.md", "Mocking decision tree"),
            ("performance-considerations.md", "When tests intersect perf"),
        ],
    },
    "security-patterns": {
        "desc": "Review for secrets, injection, auth/session issues, and unsafe defaults.",
        "domain": "security",
        "tags": ["security", "validation", "secrets"],
        "covers": [
            "Secret leakage patterns",
            "Input validation / injection risks",
            "AuthZ/AuthN footguns at code level",
            "Unsafe defaults and error handling that leaks data",
        ],
        "not_covers": [
            "Full penetration testing",
            "Cloud IAM redesign",
            "Compliance certification",
        ],
        "agents": "qa.security-reviewer",
        "phases": {
            "create": (
                "Design secure approach for a feature touching trust boundaries.",
                ["New API, auth, payment, or PII path"],
                ["Do not invent crypto algorithms"],
                [
                    ("Threat sketch", ["Assets, attackers, entry points"]),
                    ("Controls", ["Validation, authz, secrets handling"]),
                    ("Test plan link", ["Point to testing-patterns for security-relevant tests"]),
                ],
            ),
            "review": (
                "Review the change for security issues with evidence.",
                ["Any change on trust boundary or user input"],
                ["Do not spam low-value style findings"],
                [
                    ("Trust boundaries", ["Inputs, outputs, auth, data stores"]),
                    ("Check patterns", ["Secrets, injection, authz gaps, unsafe defaults"]),
                    ("Emit findings", ["High severity for exploitable paths"]),
                ],
            ),
            "validate": (
                "Validate that claimed security controls exist and are wired.",
                ["After fixes or when PR claims 'secured'"],
                ["Do not assume a library = correct usage"],
                [
                    ("Trace control", ["From entry to enforcement"]),
                    ("Negative cases", ["Unauthorized / invalid input paths"]),
                    ("Residual risk", ["Document what remains"]),
                ],
            ),
            "refactor": (
                "Propose secure refactors that preserve behavior.",
                ["After high/medium findings"],
                ["Do not apply patches in read-only review unless asked"],
                [
                    ("Prefer standard libs", ["Known validators/auth frameworks"]),
                    ("Least privilege", ["Narrow trust"]),
                    ("Verify with tests", ["Hand off scenarios to testing-patterns"]),
                ],
            ),
            "failure-analysis": (
                "Analyze a security incident or near-miss for systemic gaps.",
                ["Incident, bug bounty, or failed security test"],
                ["Do not blame individuals"],
                [
                    ("Timeline", ["What failed when"]),
                    ("Root cause classes", ["Missing control vs broken control vs misuse"]),
                    ("Prevent recurrence", ["Skill/playbook updates + tests"]),
                ],
            ),
        },
        "examples": [
            ("secure-auth-flow.md", "Sane authz checks"),
            ("insecure-auth-flow.md", "Missing authz"),
            ("secret-detection-example.md", "Hardcoded secret pattern"),
            ("input-validation-example.md", "Validated vs raw input (Java sample ok)"),
        ],
        "refs": [
            ("owasp-top-10.md", "Map findings to OWASP themes"),
            ("secret-patterns.md", "Secret shapes to watch"),
            ("input-validation-rules.md", "Validation expectations"),
            ("output-encoding.md", "Encoding notes"),
            ("threat-model.md", "Lightweight threat sketch"),
        ],
    },
    "code-quality": {
        "desc": "Review maintainability, clarity, duplication, and change reviewability.",
        "domain": "quality",
        "tags": ["maintainability", "readability", "complexity"],
        "covers": [
            "Naming and structure for reviewability",
            "Complexity and duplication signals",
            "Comment quality (signal vs noise)",
            "Maintainability assessment",
        ],
        "not_covers": [
            "Formatter/linter config wars",
            "Security issues (security-patterns)",
            "Requirement fit (requirement-alignment)",
        ],
        "agents": "qa.code-reviewer",
        "phases": {
            "review": (
                "Deep but prioritized code review for maintainability.",
                ["PR review"],
                ["Do not drown the report in nits"],
                [
                    ("Scan for hotspots", ["Complex methods, duplication, unclear names"]),
                    ("Assess reviewability", ["Can a human safely change this later?"]),
                    ("Emit few high-signal findings", ["Tie to risk of future defects"]),
                ],
            ),
            "refactor": (
                "Propose maintainability refactors.",
                ["After review"],
                ["Do not rewrite for taste alone"],
                [
                    ("Smallest safe step", ["Extract, rename, dedupe"]),
                    ("Preserve behavior", ["Require tests via testing-patterns"]),
                    ("Avoid drive-by", ["Stay in changed area unless risk demands"]),
                ],
            ),
            "maintainability-assessment": (
                "Judge whether the change is maintainable enough for the criticality of the path.",
                ["Critical modules or large diffs"],
                ["Do not block solely on style"],
                [
                    ("Criticality", ["Payment/auth/data integrity?"]),
                    ("Debt introduced", ["What future cost?"]),
                    ("Recommendation", ["pass/warn/fail with rationale"]),
                ],
            ),
        },
        "examples": [
            ("readable-function.md", "Clear structure"),
            ("unreadable-function.md", "Dense logic without seams"),
            ("complex-logic.md", "Complexity hotspot"),
            ("well-commented-function.md", "Comments that add signal"),
        ],
        "refs": [
            ("naming-conventions.md", "Naming guidance"),
            ("cyclomatic-complexity.md", "Complexity as a signal"),
            ("function-sizing.md", "Size heuristics"),
            ("comment-best-practices.md", "When to comment"),
        ],
    },
    "performance-validation": {
        "desc": "Plan and assess performance/reliability risk; later pairs with GCO metrics for SLOs, load, and RCA.",
        "domain": "quality",
        "tags": ["performance", "reliability", "load"],
        "covers": [
            "Perf test planning and baselines",
            "Regression detection mindset",
            "Bottleneck hypotheses from code/diff",
            "Linking to future GCO metrics (SLOs, load reqs, RCA)",
        ],
        "not_covers": [
            "Running GCO itself in v1",
            "Full capacity planning projects",
            "Micro-benchmark fetishism without risk",
        ],
        "agents": "qa.architect / qa.tester (as routed)",
        "phases": {
            "plan": (
                "Plan performance validation for a change.",
                ["Latency/throughput/resource-sensitive change"],
                ["Do not require load tests for trivial UI copy changes"],
                [
                    ("Identify SLIs", ["Latency, error rate, saturation"]),
                    ("Define scenarios", ["Load profile hypotheses"]),
                    ("Note GCO later", ["Which metrics would validate in GCP Monitoring"]),
                ],
            ),
            "baseline": (
                "Establish or reference a performance baseline.",
                ["Before claiming improvement/regression"],
                ["Do not invent numbers without source"],
                [
                    ("Source baseline", ["Existing tests, docs, or GCO history when available"]),
                    ("Record conditions", ["Data size, env, version"]),
                    ("Gaps", ["If no baseline, say so"]),
                ],
            ),
            "execute": (
                "Execute or specify how to execute perf checks.",
                ["Plan ready"],
                ["v1 may specify Python scripts/scenarios without running infra"],
                [
                    ("Run or describe", ["Commands/scripts (Python preferred)"]),
                    ("Capture results", ["Raw metrics + context"]),
                    ("Stop conditions", ["When to abort"]),
                ],
            ),
            "analyze": (
                "Interpret results against requirements and risk.",
                ["Results available"],
                ["Do not overfit noise"],
                [
                    ("Compare to baseline/reqs", ["Regression?"]),
                    ("Hypothesize bottlenecks", ["Code evidence"]),
                    ("Recommend", ["Fix, accept, or gather more data"]),
                ],
            ),
            "regression-detection": (
                "Detect performance regressions in a change.",
                ["Diff touches hot path"],
                ["Do not fail solely on micro noise"],
                [
                    ("Hot path review", ["N+1, unbounded loops, sync over async I/O"]),
                    ("Compare signals", ["Tests or metrics if present"]),
                    ("Emit findings", ["Tie to user-visible impact"]),
                ],
            ),
            "refactor": (
                "Propose performance-oriented refactors.",
                ["After confirmed issue"],
                ["Do not premature-optimize"],
                [
                    ("Biggest win first", ["Measured or strongly evidenced"]),
                    ("Keep correctness", ["testing-patterns"]),
                    ("Re-measure", ["baseline/analyze loop"]),
                ],
            ),
        },
        "examples": [
            ("good-performance.md", "Bounded work on hot path"),
            ("performance-regression.md", "N+1 / unbounded pattern"),
            ("optimization-opportunity.md", "Safe optimization candidate"),
            ("load-test-analysis.md", "Reading load results"),
        ],
        "refs": [
            ("performance-metrics.md", "What to measure"),
            ("baseline-strategy.md", "Baselines"),
            ("load-testing-patterns.md", "Load patterns"),
            ("common-bottlenecks.md", "Common smells"),
            ("gco-use-cases.md", "SLOs/alerts, load reqs, RCA via GCP Monitoring"),
        ],
    },
}


def emit_skill(skill_id: str, meta: dict) -> None:
    base = QA / "skills" / skill_id
    display = skill_id.replace("-", " ").title()
    playbook_links = "\n".join(
        f"- `playbook/{phase}/PLAYBOOK.md` — {meta['phases'][phase][0]}" for phase in meta["phases"]
    )
    example_links = "\n".join(f"- `examples/{name}` — {desc}" for name, desc in meta["examples"])
    ref_links = "\n".join(f"- `references/{name}` — {desc}" for name, desc in meta["refs"])

    write(
        base / "SKILL.md",
        f"""---
name: {skill_id}
description: {meta['desc']}
version: "1.0.0"
created: 2026-10-06
authors: [qa-lead]
tags: {meta['tags']}
domain: {meta['domain']}
languages: [language-agnostic, java, python]
---

## When to Use

Use this skill when the review concern matches: **{meta['desc']}**

## What This Skill Covers

{chr(10).join(f"- {c}" for c in meta['covers'])}

## What This Skill Does NOT Cover

{chr(10).join(f"- {c}" for c in meta['not_covers'])}

See `coverage/GAPS.md`.

## How to Use This Skill

1. Read this file.
2. Choose the phase playbook under `playbook/`.
3. Follow `.qualityai/templates/PLAYBOOK-TEMPLATE.md` structure (already applied in each playbook).
4. Emit findings per `.qualityai/instructions/FINDING-SCHEMA.md` with `skill_applied: {skill_id}#...`.

## Playbooks

{playbook_links}

## Examples

{example_links}

## Tooling

Optional. Not required for v1.

## References

{ref_links}

## How Agents Use This Skill

Primary agent: `{meta['agents']}`.

Delegate here; do not copy this methodology into the agent file.
""",
    )

    write(
        base / "PLAYBOOK.md",
        f"""# {display} — Quick Start

1. Open `SKILL.md`.
2. Pick a phase under `playbook/`.
3. Default for PR review: use the `review` playbook if present; otherwise `validate`, `detect`, or `analyze` as appropriate.
4. All playbooks follow `../../templates/PLAYBOOK-TEMPLATE.md`.
""",
    )

    write(
        base / "coverage" / "COVERAGE.md",
        f"""# {display}: Coverage

## What This Skill Covers

{chr(10).join(f"- {c}" for c in meta['covers'])}

## Known Limitations

- v1 is markdown methodology executed by a coding agent; results are not fully deterministic across models.
- Language-agnostic guidance; Java samples and Python scripts only when needed.
""",
    )

    write(
        base / "coverage" / "GAPS.md",
        f"""# {display}: Gaps

## What This Skill Does NOT Cover

{chr(10).join(f"- {c}" for c in meta['not_covers'])}

## Future

- Deeper tooling and CI adapters as QualityAI addons.
""",
    )

    for phase, (purpose, when, when_not, steps) in meta["phases"].items():
        content = playbook(
            skill_id=skill_id,
            display=display,
            phase=phase,
            purpose=purpose,
            when=when,
            when_not=when_not,
            inputs=[
                ("Change / diff", "yes", "Files or PR under review"),
                ("Requirement text", "no", "AC or ticket text when relevant"),
                ("Prior findings", "no", "From other agents"),
            ],
            steps=steps,
            decisions=[
                ("pass", "No material issues for this phase"),
                ("warn", "Gaps exist but not critical-path blockers"),
                ("fail", "Critical-path gaps with evidence"),
            ],
            output=[
                "Phase recommendation: pass | warn | fail",
                "Findings list (may be empty)",
            ],
            examples=[f"`../../examples/{n}` — {d}" for n, d in meta["examples"][:2]],
            related=["See SKILL.md Related concerns via orchestrator routing"],
            anti=[
                "Duplicating another skill's checklist",
                "Findings without evidence",
                "Authorship claims (especially for ai-code-detection)",
            ],
        )
        write(base / "playbook" / phase / "PLAYBOOK.md", content)

    for name, desc in meta["examples"]:
        path = base / "examples" / name
        if path.exists() and "```" in path.read_text(encoding="utf-8"):
            continue  # keep hand-enriched examples (e.g. Java samples)
        write(
            path,
            f"""# Example: {name.replace('.md', '').replace('-', ' ').title()}

## What this teaches

{desc}

## Notes

- Keep examples language-agnostic unless a snippet is required.
- If a code snippet is required, prefer **Java**.
- If a script is required, prefer **Python**.

## Sketch

Describe the scenario, what good/bad looks like, and the expected finding (`skill_applied: {skill_id}#...`).
""",
        )

    for name, desc in meta["refs"]:
        path = base / "references" / name
        if path.exists() and name == "gco-use-cases.md" and "SLOs and alerts" in path.read_text(encoding="utf-8"):
            continue
        extra = ""
        if name == "gco-use-cases.md":
            extra = """
## GCO (GCP Monitoring / Console) — later addon

1. **SLOs and alerts** — define SLOs/alerts from reliability signals.
2. **Performance and load requirements** — derive load/perf expectations from service metrics.
3. **Test-failure RCA** — correlate metrics with failing tests for root-cause reports.

v1 documents the intent; wiring to GCP is phase 2.
"""
        write(
            path,
            f"""# {name.replace('.md', '').replace('-', ' ').title()}

{desc}
{extra}
""",
        )


def main() -> None:
    # Agents
    for role, title, mission, skills, pbs in ROLES:
        write(QA / "agents" / f"qa.{role}.agent.md", agent(role, title, mission, skills, pbs))
        write(QA / "agents" / f"qa.{role}.agent.feedback.md", feedback(role, title))

    # Gates
    for gid, title, skill, questions, fail, warn, ok in GATES:
        write(
            QA / "agents" / "gates" / f"{gid}-gate.md",
            gate(gid, title, skill, questions, fail, warn, ok),
        )

    write(QA / "skills" / "README.md", skill_readme())

    for skill_id, meta in SKILLS_META.items():
        emit_skill(skill_id, meta)

    print("Generated agents, gates, and skills under", QA)


if __name__ == "__main__":
    main()
