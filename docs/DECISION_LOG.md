# DECISION_LOG.md

## 1) Purpose

This file records the major strategic, structural, technical, and operational decisions behind Funnelplugs.com.

It exists to preserve decision traceability.

Funnelplugs is not being built as random output.
It is being built as a deliberate strategic asset.
That means key decisions must be documented with clarity.

This log is part of the asset’s transfer value.
A future operator, partner, or acquirer should be able to understand:
- what was decided,
- why it was decided,
- what alternatives were rejected,
- and how the decision supports long-term asset value.

---

## 2) Logging Rule

Not every small change belongs here.

This file is for high-value decisions, including decisions related to:
- strategic positioning,
- architecture,
- infrastructure,
- SEO,
- monetization,
- security,
- governance,
- standards,
- taxonomy,
- and asset valuation logic.

Small edits belong in `CHANGELOG.md`.
High-level decisions belong here.

---

## 3) Entry Format

Every decision entry should follow this structure:

### Decision ID
A unique identifier for the decision.

### Date
The date the decision was made.

### Decision
A clear statement of what was decided.

### Context
What problem, need, or strategic condition led to the decision.

### Rationale
Why this decision was selected.

### Alternatives Rejected
What other paths were considered and why they were rejected.

### Strategic Impact
How this decision strengthens the asset.

### Operational Consequence
What changes in execution, structure, process, or workflow follow from this decision.

### Status
Accepted / Revised / Deprecated / Superseded

---

## 4) Decision Entry Template

Use the following structure for all future entries:

    ## DECISION-000
    
    **Date:** YYYY-MM-DD  
    **Status:** Accepted
    
    ### Decision
    [Insert the decision clearly.]
    
    ### Context
    [Explain the strategic or technical context.]
    
    ### Rationale
    [Explain why this path was chosen.]
    
    ### Alternatives Rejected
    - [Alternative 1] — [Reason rejected]
    - [Alternative 2] — [Reason rejected]
    
    ### Strategic Impact
    [Explain how this strengthens authority, trust, valuation, governance, or clarity.]
    
    ### Operational Consequence
    [Explain what must now happen in the project because of this decision.]

---

## 5) Initial Recorded Decisions

## DECISION-001

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
Funnelplugs.com will be built as a sovereign-grade strategic digital asset, not as a conventional website.

### Context
The domain has conceptual potential far beyond a normal content or affiliate site.
The project goal is long-term value creation, recurring revenue, and eventual high-value acquisition positioning.

### Rationale
A conventional website model would underuse the domain’s conceptual strength and reduce the project to ordinary execution.
A sovereign asset model allows the domain to accumulate authority, structure, and transfer value over time.

### Alternatives Rejected
- Generic content website — rejected because it weakens differentiation.
- Affiliate-first review site — rejected because it lowers trust and long-term valuation.
- Trend-driven SEO build — rejected because it creates fragile, low-grade growth.

### Strategic Impact
This decision defines the project at the highest level.
It protects the asset from strategic drift and aligns all future work with long-term value creation.

### Operational Consequence
All future architecture, SEO, monetization, and design decisions must be evaluated against sovereign asset standards.

---

## DECISION-002

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
The core narrative of Funnelplugs will be:

**The Logic of the Missing Plug**

### Context
The project required a conceptual foundation strong enough to elevate the domain beyond utility-only positioning.

### Rationale
This narrative explains revenue leakage as structural incompleteness inside funnels.
It gives Funnelplugs an owned interpretive frame rather than a generic optimization angle.

### Alternatives Rejected
- Generic “conversion optimization” framing — rejected because it is too common and weakly differentiated.
- Tool-discovery framing — rejected because it reduces the asset to a directory.
- Broad marketing-performance framing — rejected because it lacks conceptual sharpness.

### Strategic Impact
This decision establishes the intellectual center of the asset.
It strengthens brand distinction, valuation logic, and future standard-setting potential.

### Operational Consequence
Pages, vocabulary, design, registry logic, and utility tools must all align with this narrative.

---

## DECISION-003

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
GitHub will be the single source of truth for all development, updates, and publishing workflow.

### Context
The project required a controlled, transferable, versioned system for building a strategic asset without scattered operational logic.

### Rationale
GitHub provides clear history, disciplined structure, automation compatibility, and acquisition readability.
This reduces operational ambiguity and increases long-term trust in the build system.

### Alternatives Rejected
- Mixed publishing across multiple platforms — rejected because it creates chaos and weakens transferability.
- Cloudflare-centered publishing workflow — rejected because Cloudflare should remain a perimeter layer, not the source of truth.
- Manual patch-based workflow — rejected because it weakens governance and traceability.

### Strategic Impact
This decision strengthens structural control, clarity, and future asset transfer value.

### Operational Consequence
All code, content, architecture, automation, and deployment logic must remain GitHub-centered.

---

## DECISION-004

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
The publishing chain will follow this sequence:

**Local Python generation/update → GitHub Desktop commit/push → GitHub repository → GitHub Actions validation/build/deployment**

### Context
The project required a strict operational model that keeps local generation, source control, and deployment aligned.

### Rationale
This sequence preserves order:
Python handles generation,
GitHub Desktop handles disciplined transfer,
GitHub stores truth,
and GitHub Actions handles automation.

### Alternatives Rejected
- Direct manual file editing in production — rejected because it breaks governance.
- Cloudflare API-based publishing — rejected because it adds unnecessary complexity and violates publishing clarity.
- Multi-path deployment methods — rejected because they reduce operational coherence.

### Strategic Impact
This decision creates a disciplined operational chain and reduces structural risk.

### Operational Consequence
All updates must follow this path.
No bypass is allowed.

---

## DECISION-005

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
Cloudflare will be used only as the DNS, TLS, security, and edge-control layer after nameserver delegation.

### Context
The project needed stronger perimeter control without turning Cloudflare into the publishing engine.

### Rationale
Cloudflare is highly valuable for DNS, protection, and performance, but it should not become the development or publishing center of the asset.

### Alternatives Rejected
- Using Cloudflare as a hidden content workflow layer — rejected because it weakens GitHub sovereignty.
- Depending on Cloudflare API tokens in publishing — rejected because it adds unnecessary coupling and risk.
- Avoiding Cloudflare entirely — rejected because perimeter protection and DNS control are strategically valuable.

### Strategic Impact
This decision preserves publishing clarity while adding strong network control and security posture.

### Operational Consequence
Cloudflare changes are limited to DNS, TLS, security, and edge configuration.
Asset development remains outside Cloudflare.

---

## DECISION-006

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
The first-release structural spine of Funnelplugs will be built around five primary layers:
Manifesto, Protocol, Funnel Integrity Standard, Plug Registry, and Revenue Leak Engine.

### Context
The project required a controlled first-release structure that expresses authority without bloated launch behavior.

### Rationale
These five layers cover doctrine, method, standard, governed reference, and practical utility.
Together they form a strong sovereign spine.

### Alternatives Rejected
- Large article-heavy launch — rejected because it dilutes conceptual clarity.
- Tool-list-first launch — rejected because it weakens authority.
- Minimal brochure-style launch — rejected because it underbuilds the asset.

### Strategic Impact
This decision protects structural clarity and keeps the early asset high-density and high-signal.

### Operational Consequence
All first-release work should reinforce one of these five layers.

---

## DECISION-007

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
The asset will follow a strict quality gate policy before deployment.

### Context
A strategic asset cannot be allowed to degrade through broken pages, weak metadata, or structurally careless output.

### Rationale
A successful compile is not enough.
Publication must be governed by quality, trust, and structural integrity.

### Alternatives Rejected
- Deploy-on-build-success only — rejected because it ignores strategic quality.
- Manual visual checking alone — rejected because it is insufficient and non-scalable.
- SEO-only validation — rejected because the asset requires broader integrity checks.

### Strategic Impact
This decision protects trust, consistency, and acquisition-grade readiness.

### Operational Consequence
Validation scripts and blocking rules must remain part of the publishing pipeline.

---

## DECISION-008

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
Funnelplugs will pursue sovereign SEO, not cheap search growth.

### Context
The project requires search visibility, but low-grade SEO would weaken its authority and conceptual value.

### Rationale
Search must strengthen discoverability without damaging trust or turning the asset into a spam-adjacent property.

### Alternatives Rejected
- Keyword-stuffing growth model — rejected because it weakens quality signals.
- Thin-page scale tactics — rejected because they undermine long-term authority.
- SEO as the primary identity of the asset — rejected because SEO is a support system, not the core identity.

### Strategic Impact
This decision aligns search growth with trust, authority, and valuation logic.

### Operational Consequence
Only strategically strong, index-worthy, high-quality pages should be allowed into the SEO surface.

---

## DECISION-009

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
The sitemap must be generated automatically and must reflect newly created or updated valid pages.

### Context
A sovereign asset requires a trustworthy indexing map that remains current without manual fragility.

### Rationale
Manual sitemap maintenance is error-prone and weakens structural reliability.
Automation preserves freshness and consistency.

### Alternatives Rejected
- Manual sitemap editing — rejected because it does not scale and invites errors.
- Including every generated page by default — rejected because it creates low-value noise.
- Ignoring `lastmod` integrity — rejected because false freshness weakens trust.

### Strategic Impact
This decision strengthens crawl clarity, search trust, and structural coherence.

### Operational Consequence
Sitemap generation must be part of the controlled build flow and tied to validation logic.

---

## DECISION-010

**Date:** 2026-04-03  
**Status:** Accepted

### Decision
Meta-documentation is part of the asset’s valuation architecture.

### Context
The project is being built for long-term transferability, readability, and acquisition-grade credibility.

### Rationale
Documenting why decisions were made transforms the asset from output into system.
That increases strategic legibility and transfer value.

### Alternatives Rejected
- No decision archive — rejected because it weakens continuity and acquisition clarity.
- Only technical changelogs — rejected because they record what changed, not why.
- Memory-based governance — rejected because it does not scale and is not transferable.

### Strategic Impact
This decision increases the asset’s intellectual and operational readability.

### Operational Consequence
Major decisions must continue to be recorded here as the project evolves.

---

## DECISION-011

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Adopt a strict sovereign standards enforcement layer in repository governance.

### Context
Core doctrine and quality rules were strong, but enforcement needed stricter operational guarantees to reduce governance drift risk as the asset evolves.

### Rationale
A sovereign-grade asset requires mandatory controls, not advisory-only guidance.
Enforcement now includes stricter standards checks plus dedicated doctrine-adjacent documents for threat modeling, incident response, publication gate execution, and design rationale continuity.

### Alternatives Rejected
- Governance by documentation only — rejected because it relies too heavily on memory and manual discipline.
- Security-only hardening without doctrine controls — rejected because it leaves strategic integrity exposed.
- Deferred strict governance to later phase — rejected because early drift compounds quickly.

### Strategic Impact
This decision improves defensibility, trust continuity, and acquisition readability by proving that doctrine-to-execution controls are active and auditable.

### Operational Consequence
Pull requests and CI must now satisfy sovereign strict standards checks, and governance baseline documents must remain present and complete.

---

## DECISION-012

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Adopt a mandatory daily sovereign execution protocol and make it part of governed project operation.

### Context
Existing governance controls were strong, but daily execution needed a complete operating path that explicitly covers pre-commit cleanup, source-versus-output policy, visual smoke testing, and commit message discipline.

### Rationale
Without a strict daily path, technically valid work can still introduce output noise, weak traceability, or operational ambiguity.
The daily protocol closes these gaps and keeps future execution aligned with sovereign standards under branch protection.

### Alternatives Rejected
- Keep guidance only in chat or memory — rejected because it is non-transferable and fragile.
- Keep CONTRIBUTING as the only execution reference — rejected because it is too brief for full sovereign daily operation.
- Enforce technical checks only — rejected because visual and output-governance controls are also required.

### Strategic Impact
This decision strengthens repeatability, reduces drift risk, and improves long-horizon operating reliability for maintainers and future acquirers.

### Operational Consequence
Daily work must follow `docs/DAILY_OPERATION_PROTOCOL.md`, and core governance references now explicitly point to that protocol.

---

## DECISION-013

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Adopt an explicit markdownlint policy baseline aligned with sovereign documentation style.

### Context
The required governance check enforced markdownlint defaults that conflicted with legacy doctrine-format files (long-form prose style, numbering conventions, and controlled structural spacing), causing PR checks to fail independently of real governance quality.

### Rationale
The repository's strategic documentation is doctrine-first rather than markdown-style-first.
A formal lint policy prevents false negatives while preserving strict checks for meaningful governance and integrity controls.

### Alternatives Rejected
- Reformat all legacy doctrine files immediately — rejected because it is high-noise and low-strategic-yield for current release flow.
- Disable markdownlint entirely — rejected because a markdown hygiene guard is still valuable.
- Keep default markdownlint rules — rejected because it blocks valid sovereign docs for non-strategic formatting reasons.

### Strategic Impact
This decision stabilizes CI reliability, protects review focus on material quality, and prevents operational bottlenecks caused by formatting-only false failures.

### Operational Consequence
Markdownlint now runs with a repository-level policy baseline defined in `.markdownlint-cli2.yaml`.

---

## DECISION-014

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Extend the markdownlint policy baseline to disable `MD032` and `MD036` for doctrine-style strategic docs.

### Context
After baseline lint policy adoption, required checks still failed on legacy doctrine documents due to strict list-spacing and emphasis-as-heading rules that conflict with established repository writing style.

### Rationale
This adjustment removes formatting-only false blockers while maintaining governance and quality enforcement where it matters operationally.

### Alternatives Rejected
- Rewrite all doctrine files to satisfy strict default markdown style immediately — rejected due to high noise and low strategic value.
- Keep failing checks and bypass manually — rejected because branch protection forbids this and it weakens process reliability.

### Strategic Impact
Stabilizes required CI checks and keeps review attention on substantive quality, governance, and security signals.

### Operational Consequence
Repository markdownlint policy now explicitly disables `MD032` and `MD036` in `.markdownlint-cli2.yaml`.

---

## DECISION-015

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Disable markdownlint rule `MD024` for sovereign changelog and doctrine heading patterns.

### Context
Required CI checks continued to fail due to repeated section labels (such as Added/Changed/Fixed/Refined) used intentionally across dated changelog entries.

### Rationale
The repository uses a structured repeatable changelog format where repeated subsection names are expected behavior, not an authoring defect.
Disabling `MD024` removes false blockers while preserving governance integrity controls.

### Alternatives Rejected
- Rewrite changelog taxonomy to unique per-entry heading names — rejected because it hurts readability and deviates from established operating format.
- Keep default `MD024` and accept recurring check failures — rejected because it breaks required check reliability.

### Strategic Impact
Improves CI signal quality by preventing non-material lint failures from blocking governed delivery.

### Operational Consequence
Markdownlint policy in `.markdownlint-cli2.yaml` now also disables `MD024`.

---

## DECISION-016

**Date:** 2026-04-17  
**Status:** Accepted

### Decision
Disable markdownlint rule `MD041` for legacy sovereign doctrine files.

### Context
Required CI checks still failed on strategic governance files whose first line is a document identity marker rather than an ATX H1 heading.

### Rationale
Legacy doctrine files intentionally preserve title-marker-first formatting.
Disabling `MD041` avoids format-only check failures without weakening governance controls.

### Alternatives Rejected
- Rewrite all legacy doctrine files to start with H1 — rejected due to unnecessary formatting churn and low strategic benefit.
- Keep `MD041` active and accept recurring false blockers — rejected because it undermines CI reliability.

### Strategic Impact
Completes markdownlint policy alignment with sovereign documentation style and removes a non-material blocker from required checks.

### Operational Consequence
Markdownlint policy in `.markdownlint-cli2.yaml` now also disables `MD041`.

---

## 6) Maintenance Rule

This file must be updated whenever a major governing decision is made or materially revised.

The log must remain:
- clean,
- readable,
- accurate,
- and strategically useful.

It is not a dumping ground.
It is a record of governing intent.

---

## 7) Final Rule

Funnelplugs must be able to explain itself.
Not only through what exists,
but through why it exists.

That is the purpose of this log.
