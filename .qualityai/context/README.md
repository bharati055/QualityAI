# Host context knowledge

Fill these templated markdown files for your product. They are the AI-readable replacement for scattered Confluence QA pages.

- Humans author and approve.
- AI may propose updates **only via PR** (see `../instructions/AI-HUMAN-BOUNDARY.md`).
- Copy starting forms from `../templates/context/` if needed.
- **Stub files** are marked with a **STUB — implement as needed** banner and `status: stub` in frontmatter. Do **not** treat TODO/empty stubs as product truth; agents should report "context missing" until filled.

## Core (fill for pilot — P0/P1)

| Path | Purpose | Primary role |
|---|---|---|
| `test-strategy.md` | Overall QA approach | Lead / Architect |
| `test-types.md` | Definitions and when to use each type | All |
| `test-automation-framework.md` | e.g. Selenium / Playwright | Engineer |
| `performance-testing.md` | e.g. Gatling / JMeter + approach | Architect |
| `quality-gates/` | Stage gates: PR → Prod | Lead |
| `squad/` | Product area + local frameworks | Engineer |
| `journeys/` | Critical user journeys + **per-journey SLIs/NFRs** (see `templates/context/JOURNEY-TEMPLATE.md`) | Lead |
| `architecture/` | SUT architecture, FMEA, observability | Architect |
| `suite-trust.md` | Flake thresholds, quarantine fields, expiry, allowed mutes (defaults shipped; tune per project) | Lead |

## P2 stubs (implement as needed)

These ship as **explicit stubs**. Implement when the related workflow starts failing from missing knowledge. Leaving them as stubs is fine.

| Path | Purpose | Primary role | Typical trigger to fill |
|---|---|---|---|
| `environments.md` | Env URLs, data, quirks | Lead | Mis-triage of CI failures |
| `test-data.md` | Fixtures, PII, factories | Engineer | Flaky or unsafe data |
| `security-testing.md` | Auth/trust boundaries | Architect | Security skill noise |
| `api-and-contracts.md` | Specs + contract repos | Lead | API/contract gaps |
| `observability.md` | Logs/metrics/traces | Architect | RCA / GCO prep |
| `nfr.md` | **Defaults + cross-cutting only** (journey SLIs live under `journeys/`) | Architect | Missing system defaults / a11y / compliance |
| `glossary.md` | Domain terms | Shared | Ambiguous product language |

Stub banner standard: `../templates/context/STUB-BANNER.md`.
