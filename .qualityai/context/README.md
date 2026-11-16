# Host context knowledge

Fill these templated markdown files for your product. They are the AI-readable replacement for scattered Confluence QA pages.

- Humans author and approve.
- AI may propose updates **only via PR** (see `../instructions/AI-HUMAN-BOUNDARY.md`).
- Copy starting forms from `../templates/context/` if a file is empty.

## Layout

| Path | Purpose | Primary role |
|---|---|---|
| `test-strategy.md` | Overall QA approach | Lead / Architect |
| `test-types.md` | When to use each test type | All |
| `test-automation-framework.md` | e.g. Selenium / Playwright | Engineer |
| `performance-testing.md` | e.g. Gatling / JMeter + approach | Architect |
| `quality-gates/` | Stage gates: PR → Prod | Lead |
| `squad/` | Product area + local frameworks | Engineer |
| `journeys/` | Critical user journeys, cross-app deps | Lead |
| `architecture/` | SUT architecture, FMEA, observability | Architect |
