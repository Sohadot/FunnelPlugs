# CHANGELOG.md

## 1) Purpose

This file records the meaningful structural, technical, editorial, and operational changes made to Funnelplugs.com over time.

It exists to preserve change traceability.

Funnelplugs is being built as a sovereign-grade strategic digital asset.
That means the asset must not only document major decisions, but also maintain a clear record of what was actually changed, added, refined, corrected, or removed.

This file is part of the asset’s operational discipline.

---

## 2) Relationship to Other Governance Files

This file does not replace `DECISION_LOG.md`.

The distinction is strict:

- `DECISION_LOG.md` records why major governing decisions were made.
- `CHANGELOG.md` records what changed in the asset as a result of execution.

If a change reflects a major strategic decision, the decision belongs in `DECISION_LOG.md`.
If a change reflects implementation, refinement, correction, or release evolution, it belongs here.

---

## 3) Logging Rule

This file should record meaningful changes, including changes to:

- doctrine files,
- architecture,
- SEO systems,
- sitemap generation,
- quality controls,
- security policy,
- page structure,
- automation,
- templates,
- data structures,
- visual systems,
- and monetization implementation.

Tiny edits, typo-only fixes, or negligible formatting changes do not need detailed entries unless they matter strategically.

The goal is clarity, not noise.

---

## 4) Change Categories

Every meaningful entry should be grouped under one or more of the following categories:

### Added
For new files, systems, layers, pages, scripts, or policies.

### Changed
For modifications to existing systems, structures, logic, or content.

### Fixed
For corrections to broken, weak, malformed, or inconsistent elements.

### Removed
For intentionally deleted files, systems, outputs, or structures.

### Refined
For improvements that increase clarity, authority, quality, coherence, or strategic strength without changing the underlying system category.

---

## 5) Entry Standard

Entries should be chronological and readable.

Use the following structure:

### [YYYY-MM-DD]

#### Added
- [Describe what was added.]

#### Changed
- [Describe what was changed.]

#### Fixed
- [Describe what was fixed.]

#### Removed
- [Describe what was removed.]

#### Refined
- [Describe what was refined.]

Only include categories that are actually relevant for that date.

---

## 6) Initial Changelog Entries

### [2026-04-03]

#### Added
- Created `FOUNDATION_DOCTRINE.md` as the sovereign conceptual foundation of Funnelplugs.com.
- Created `PROJECT_DOCTRINE.md` to define the operating logic of the project.
- Created `ARCHITECTURE.md` to govern page hierarchy, structural spine, repository logic, and build architecture.
- Created `SEO_POLICY.md` to define sovereign SEO rules and indexation discipline.
- Created `SITEMAP_POLICY.md` to define automated sitemap generation standards and inclusion logic.
- Created `QUALITY_GATE.md` to establish strict pre-deployment validation rules.
- Created `SECURITY_POLICY.md` to define security doctrine for the GitHub-first publishing system.
- Created `DECISION_LOG.md` to preserve traceability of high-value strategic decisions.
- Created `MONETIZATION_PRINCIPLES.md` to govern revenue logic without degrading trust or valuation.

#### Changed
- Established the GitHub-first sovereign publishing model as the operating workflow for the asset.
- Formalized the first-release structural spine around Manifesto, Protocol, Funnel Integrity Standard, Plug Registry, and Revenue Leak Engine.

#### Fixed
- Corrected Markdown rendering issues in `DECISION_LOG.md` by removing unsafe nested code block behavior and replacing it with a stable, GitHub-safe template structure.

#### Refined
- Strengthened the internal governance system by separating doctrine, policy, architecture, decision traceability, and monetization logic into distinct files.
- Improved acquisition readability by treating documentation as part of valuation architecture rather than as auxiliary notes.

---

### [2026-04-17]

#### Added
- Added `SECURITY.md` at repository root for standardized vulnerability disclosure and response expectations.
- Added `CODEOWNERS` to enforce ownership on governance-critical files.
- Added `CONTRIBUTING.md` and `.github/pull_request_template.md` with strict sovereign contribution requirements.
- Added `.github/workflows/governance.yml` for governance, markdown, and strict standards CI checks.
- Added `scripts/governance_guard.py` to block governance-critical changes without `docs/DECISION_LOG.md` updates.
- Added `scripts/check_markdown_links.py` to block broken relative markdown links.
- Added `scripts/sovereign_standards_guard.py` to enforce strict baseline doctrine-governance document presence.
- Added `docs/THREAT_MODEL.md`, `docs/INCIDENT_RESPONSE.md`, `docs/DESIGN_RATIONALE.md`, and `docs/PUBLICATION_GATE_CHECKLIST.md`.

#### Changed
- Updated contribution and PR validation flows to include strict sovereign standards checks.
- Extended governance CI to run sovereign strict standards guard in addition to existing checks.

#### Refined
- Strengthened doctrine-to-execution enforceability by converting governance expectations into auditable automation controls.

---

### [2026-04-17]

#### Added
- Added `docs/DAILY_OPERATION_PROTOCOL.md` as a mandatory daily sovereign operating path.

#### Changed
- Updated `CONTRIBUTING.md` to require reading `docs/DAILY_OPERATION_PROTOCOL.md`.
- Updated `docs/PROJECT_DOCTRINE.md` to make the daily execution protocol part of governed routine operation.
- Updated `docs/DECISION_LOG.md` with `DECISION-012` to formally adopt daily sovereign execution controls.

#### Refined
- Converted daily execution guidance from informal checklist into a full operating protocol covering pre-commit hygiene, output-noise control, visual smoke tests, and commit-message discipline.

---

### [2026-04-17]

#### Added
- Added `.markdownlint-cli2.yaml` to define a repository-level markdownlint policy baseline compatible with sovereign doctrine documentation style.

#### Changed
- Updated `docs/DECISION_LOG.md` with `DECISION-013` to formalize markdownlint policy governance and CI reliability alignment.

#### Refined
- Reduced markdown formatting false-failure noise in required checks while preserving governance and quality enforcement intent.

---

### [2026-04-17]

#### Changed
- Updated `.markdownlint-cli2.yaml` to disable `MD032` and `MD036` for compatibility with sovereign doctrine-style documents.
- Updated `docs/DECISION_LOG.md` with `DECISION-014` to formalize the policy extension.

#### Refined
- Eliminated remaining markdownlint false blockers affecting `docs/ASSET_THESIS.md` in required CI checks.

---

### [2026-04-17]

#### Changed
- Updated `.markdownlint-cli2.yaml` to disable `MD024` for repeated changelog subsection headings used by design.
- Updated `docs/DECISION_LOG.md` with `DECISION-015` to formalize the policy extension.

#### Refined
- Removed remaining markdownlint false blockers tied to intentional repeated heading labels in `docs/CHANGELOG.md`.

---

### [2026-04-17]

#### Changed
- Updated `.markdownlint-cli2.yaml` to disable `MD041` for legacy doctrine-file title marker format.
- Updated `docs/DECISION_LOG.md` with `DECISION-016` to formalize the policy extension.

#### Refined
- Removed remaining markdownlint false blockers tied to first-line title-marker formatting in sovereign documentation files.

---

### [2026-04-18]

#### Added
- `docs/EXTERNAL_SYSTEMS.md` to govern production systems that exist outside GitHub but materially affect the live asset.
- `docs/REMEDIATION_PLAN.md` as the sequenced sovereign repair and expansion program (security → hardening → UX → authority → verification).
- `404.html` as a governed error surface aligned with the public design system.
- `.github/dependabot.yml` for weekly grouped GitHub Actions update proposals.
- `.gitignore` to reduce repository noise (`__pycache__/`, virtualenvs, local editor artifacts).
- `assets/img/og-default.jpg` so declared Open Graph defaults resolve to a real file.

#### Changed
- `robots.txt` simplified to a minimal crawl policy with reduced speculative path disclosure.
- `.github/workflows/deploy.yml` now runs markdown lint, governance guard, markdown link checks, sovereign standards guard, and an explicit `quality_gate.py` step before staging; third-party actions are pinned to immutable SHAs.
- `.github/workflows/governance.yml` third-party actions pinned to immutable SHAs.
- `scripts/config.py` now documents that inline GTM bootstrap is an intentional governed exception to the “no arbitrary inline scripts” posture enforced in rendered HTML validation.
- `scripts/quality_gate.py` and `scripts/sovereign_standards_guard.py` now require `docs/EXTERNAL_SYSTEMS.md` alongside other foundation governance files.

#### Refined
- `scripts/governance_guard.py` now treats `.github/workflows/governance.yml` as governance-critical alongside `deploy.yml`.

---

## 7) Logging Discipline

The changelog must remain:

- clean,
- chronological,
- factual,
- readable,
- and operationally useful.

It must not become:
- a dump of meaningless micro-edits,
- a duplicate of `DECISION_LOG.md`,
- or a vague summary without execution value.

The purpose is to preserve implementation history with discipline.

---

## 8) Update Rule

This file should be updated whenever meaningful work changes the live asset, the repository structure, the governance layer, the automation system, or the controlled build logic.

If a change would matter to:
- a future maintainer,
- a reviewer,
- a technical auditor,
- or a future acquirer,

it likely belongs here.

---

## 9) Final Rule

Funnelplugs must be able to explain not only why it evolved, but how it evolved.

`DECISION_LOG.md` explains governing intent.
`CHANGELOG.md` explains executed change.

That is the purpose of this file.
