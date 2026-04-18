# DECISION_LOG.md

## Status
Active governance record.

## Purpose
This file records material decisions that affect the structure, doctrine, governance, deployment posture, measurement posture, indexation workflow, security posture, and sovereign integrity of FunnelPlugs.com.

This is not a changelog.
This is not a scratchpad.
This is not a discussion archive.

This file exists to preserve decision memory at the level of institutional consequence.

If a decision changes how the asset is built, governed, published, secured, measured, or interpreted, it belongs here.

---

## Decision Standard

A decision must be logged here if it affects any of the following:

- repository governance
- source-of-truth doctrine
- deployment architecture
- external production systems
- measurement architecture
- search/indexation workflow
- security posture
- canonical or redirect behavior
- content generation model
- sovereign asset positioning
- monetization boundaries
- operational discipline

Purely cosmetic edits, copy corrections, and minor layout tweaks do not belong here unless they carry structural consequences.

---

## Logging Discipline

Each entry must be:

- decision-level, not task-level
- concise, but not vague
- operationally legible
- written in institutional language
- tied to actual live or repository-level consequences

Each entry should make clear:

- what was decided
- why it was decided
- what it now governs
- what must remain true afterward

---

## Entry Format

Each decision entry should follow this structure:

### [YYYY-MM-DD] Decision Title
**Status**  
Approved | Active | Superseded

**Decision**  
What was decided.

**Rationale**  
Why the decision was necessary.

**Operational Effect**  
What now changes in the repository, production system, or governance model.

**Constraint**  
What must not be violated after this decision.

---

## Decision Register

### [2026-04-18] External production systems brought under repository governance
**Status**  
Approved | Active

**Decision**  
Production-relevant external systems are now formally documented in-repo through `docs/EXTERNAL_SYSTEMS.md`.

The following systems are explicitly brought under repository governance visibility:
- Google Tag Manager
- Google Analytics 4
- Cloudflare
- Google Search Console

**Rationale**  
A governance gap existed between live operational reality and the sovereign source-of-truth doctrine.

The asset was already materially influenced by external systems affecting:
- measurement
- DNS and proxy behavior
- HTTPS enforcement
- redirects
- TLS behavior
- sitemap handling
- indexation monitoring

These systems could not be treated as invisible simply because they lived outside GitHub.

**Operational Effect**  
`docs/EXTERNAL_SYSTEMS.md` is now part of the formal governance surface of the asset.

Any material change to GTM, GA4, Cloudflare, or Search Console must be reflected in-repo.

External production infrastructure is no longer permitted to remain undocumented.

**Constraint**  
External systems may exist outside the repository.  
They may not exist outside governance.

---

### [2026-04-18] GitHub retained as sovereign source of truth for documentation and operational visibility
**Status**  
Approved | Active

**Decision**  
GitHub remains the sovereign source of truth for FunnelPlugs documentation, decision memory, operational visibility, and change discipline.

This principle remains in force even where some production systems necessarily live outside the repository.

**Rationale**  
Without a governing source of truth, the asset fragments into undocumented operational islands, weakening control, continuity, auditability, and institutional readability.

**Operational Effect**  
Repository documentation must reflect the live state of production-relevant systems and decisions.

If production behavior changes and repository documentation does not reflect that change, the asset is considered governance-incomplete.

**Constraint**  
No shadow publishing logic.  
No undocumented production control surfaces.  
No silent divergence between live infrastructure and repository documentation.

---

### [2026-04-18] GTM retained as controlled measurement orchestration layer
**Status**  
Approved | Active

**Decision**  
Google Tag Manager remains the controlled orchestration layer for measurement delivery.

GA4 measurement is governed through GTM rather than duplicated through parallel direct page-level implementations.

**Rationale**  
A duplicated or loosely governed measurement path introduces operational ambiguity, inflates reporting risk, and weakens traceability.

A single governed orchestration path is cleaner and more legible.

**Operational Effect**  
GTM is treated as the authoritative delivery layer for measurement tags.
GA4 receives data through the governed GTM path.
Measurement configuration changes must be documented in `docs/EXTERNAL_SYSTEMS.md`.

**Constraint**  
Duplicate direct tagging must not be introduced casually in templates or page-level markup.

---

### [2026-04-18] Cloudflare recognized as active edge control plane requiring explicit documentation
**Status**  
Approved | Active

**Decision**  
Cloudflare is formally recognized as an active edge control plane affecting FunnelPlugs.com production behavior and therefore requiring explicit repository-level documentation.

**Rationale**  
Cloudflare materially affects:
- DNS resolution
- HTTPS enforcement
- redirect logic
- TLS behavior
- proxy behavior
- edge security posture

This makes it structurally significant, not peripheral.

**Operational Effect**  
Cloudflare rules, settings, and edge behaviors that affect the public asset must be tracked as governed operational state, not treated as informal admin-side configuration.

**Constraint**  
Cloudflare must not become an undocumented parallel architecture.

---

### [2026-04-18] Search Console operational state recognized as part of indexation governance
**Status**  
Approved | Active

**Decision**  
Google Search Console is recognized as part of the governed indexation workflow of the asset.

Its verified property state, sitemap submission state, and material indexation observations are now considered operationally relevant.

**Rationale**  
Search visibility is not produced by code alone.
It is also shaped by submission state, validation state, crawl observations, and canonical enforcement outcomes.

Ignoring Search Console would leave indexation governance incomplete.

**Operational Effect**  
Material Search Console changes and notable indexation-state developments should be reflected in this decision log when they affect live search posture or repository decisions.

**Constraint**  
Search Console may monitor indexation externally, but its operational consequences must remain legible in-repo.

---

### [2026-04-17] Reference-layer expansion established as sovereign authority-building direction
**Status**  
Approved | Active

**Decision**  
FunnelPlugs is not to remain a thin static website centered only on a diagnostic tool.

It is to develop into a governed reference system for funnel integrity through:
- reference pages
- leak-class pages
- plug-class pages
- conceptual papers
- methodology and interpretation layers
- internal linking infrastructure

**Rationale**  
The asset’s long-term strategic value does not come from utility alone.
It comes from authority, framework ownership, doctrinal clarity, and institutional legibility.

**Operational Effect**  
Expansion beyond the initial core pages is not optional polish.
It is part of the asset thesis.

Reference-layer growth, internal linking density, and taxonomy visibility are now aligned with the sovereign build direction.

**Constraint**  
The asset must not regress into a shallow “single-tool website” posture.

---

### [2026-04-17] Sitemap generation aligned with governed page registry
**Status**  
Approved | Active

**Decision**  
Sitemap generation is governed through the repository’s page registry and build system rather than through ad hoc manual URL insertion.

**Rationale**  
A sovereign asset cannot depend on manual sitemap drift.
Its public discovery layer must be generated from the same governed source that defines live page existence.

**Operational Effect**  
Sitemap inclusion is now expected to reflect the governed page register and generated live files.
New reference pages are intended to enter the sitemap through structured generation, not isolated manual edits.

**Constraint**  
Discovery infrastructure must remain aligned with governed page existence.

---

### [2026-04-17] Working tree cleanliness elevated to operational requirement
**Status**  
Approved | Active

**Decision**  
Repository cleanliness is a governance requirement, not a convenience preference.

Generated noise such as `__pycache__`, temporary artifacts, and non-intentional output drift must not remain in the working tree.

**Rationale**  
A polluted working tree weakens judgment, slows review, obscures material changes, and degrades institutional confidence in what is actually being published.

**Operational Effect**  
Temporary Python cache artifacts and non-deliberate file churn must be removed before commit and before merge.

**Constraint**  
A dirty working tree is not an acceptable steady state.

---

### [2026-04-17] Quality gate retained as mandatory publication boundary
**Status**  
Approved | Active

**Decision**  
The quality gate remains a mandatory publication boundary for FunnelPlugs.

No change is considered publication-ready if it crosses governance, structural, or validation boundaries without passing the established checks.

**Rationale**  
The asset’s value depends on disciplined consistency, not raw publishing velocity.

**Operational Effect**  
Governance guards, markdown checks, validation routines, and build checks remain part of the required route to production readiness.

**Constraint**  
No “publish first, clean later” posture is acceptable.

---

## Review Rule

This file must be updated when:
- a production-relevant external system changes
- a governance doctrine changes
- a structural build rule changes
- a search/indexation decision materially changes
- a security or routing decision materially changes
- a sovereign positioning decision changes the development direction of the asset

If a material decision is made and this file is not updated, governance memory has failed.

---

## Sovereign Closing Rule

FunnelPlugs is not governed only by what is deployed.  
It is governed by what is decided, recorded, and kept institutionally legible.

An undocumented material decision is not operational maturity.  
It is hidden instability.
