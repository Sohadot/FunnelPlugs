# REMEDIATION_PLAN.md

## Status

Active execution plan.

## Purpose

This document turns sovereign diagnosis into a **sequenced remediation program** for FunnelPlugs.com.

It is not a wish list.
It is not a duplicate of `EXTERNAL_SYSTEMS.md`.

It exists to prevent mixing unrelated work into one undifferentiated change-set, which weakens review, traceability, and asset dignity.

---

## Governance Alignment

This plan follows the Sovereign Asset System discipline:

- Doctrine first (what must remain true)
- Rules and gates (what must be enforced)
- Execution in controlled phases (what ships, when, and why)

Cross-links:

- `docs/EXTERNAL_SYSTEMS.md` — live systems outside GitHub
- `docs/DECISION_LOG.md` — governing decisions
- `docs/CHANGELOG.md` — executed change history

---

## Severity Ladder

Work is grouped by **risk to asset integrity**, not by convenience.

1. **Critical now** — security, supply chain, injection surface, broken public signals
2. **Hardening next** — CI transparency, repository hygiene, edge headers, CSP rollout
3. **UX / reference refinement** — design system documentation, engine UX, mobile polish
4. **Authority build** — methodology, glossary, internal linking fabric, structured data
5. **Verification gates** — smoke checks, performance budgets, periodic external-system review

---

## Phase A — Critical now (3–5 days target)

### A1) Reduce HTML injection surface (`| safe`)

**Scope**

- `templates/base.html` — `extra_head`, `summary.body`
- `templates/page.html` — all `| safe` render paths for sections, cards, and `body_content`

**Rule**

- Prefer escaped output by default.
- Where HTML is required, it must be **governed input** (build-time only), not arbitrary strings.
- `extra_head` should trend toward empty unless explicitly approved fragments exist.

**Exit criteria**

- Inventory complete in a PR checklist.
- Any remaining `| safe` usage is listed with: owner field, threat model note, and validation hook.

### A2) `robots.txt` minimization

**Goal**

- Simple public crawl policy
- No speculative internal path disclosure
- Clear `Sitemap` pointer

**Exit criteria**

- `robots.txt` reviewed against live routes and repository reality.

### A3) Sovereign `404.html`

**Goal**

- Same visual system as the live asset
- `noindex` for error state
- Recovery links to core reference routes

**Exit criteria**

- `404.html` ships in Pages artifact and is manually smoke-tested.

### A4) Repository hygiene (`.gitignore`)

**Goal**

- Exclude `__pycache__/`, `*.pyc`, local editor noise, and accidental artifacts.

**Exit criteria**

- Clean `git status` after a normal build cycle.

### A5) Deploy pipeline transparency

**Goal**

- Markdown + governance scripts + quality gate are **visible steps** on `main` deploy, not implied.

**Exit criteria**

- `.github/workflows/deploy.yml` shows ordered steps with clear failure signals.

---

## Phase B — Hardening next (~1 week after Phase A)

### B1) Edge security headers (Cloudflare)

**Sequence**

1. `X-Content-Type-Options: nosniff`
2. `Referrer-Policy: strict-origin-when-cross-origin`
3. Tight `Permissions-Policy`
4. Frame control (`X-Frame-Options: DENY` or CSP `frame-ancestors 'none'`)
5. `Content-Security-Policy-Report-Only` first, then enforce after violation review

**Exit criteria**

- Values recorded in `docs/EXTERNAL_SYSTEMS.md` under Cloudflare.
- `DECISION_LOG.md` entry when CSP moves from Report-Only to enforce.

### B2) GitHub Actions SHA pinning

**Goal**

- Replace floating tags with immutable SHAs for all third-party actions in `.github/workflows/*`.

**Exit criteria**

- Dependabot can propose SHA bumps via grouped PRs.

### B3) Dependabot

**Goal**

- `.github/dependabot.yml` monitors GitHub Actions (and Python ecosystem if/when dependency files exist).

### B4) Build cleanliness decision

**Goal**

- Decide whether `clean_output_before_build` becomes `True` for production, or an explicit pre-clean step runs before generation.

**Exit criteria**

- Decision recorded in `DECISION_LOG.md` with operational consequence.

---

## Phase C — UX / reference refinement (2–3 weeks)

### C1) Engine page sovereignty

- Reduce payload weight and DOM density
- Improve results hierarchy (diagnostic dossier posture)
- Mobile-first review of the tool surface

### C2) Open Graph sovereignty

- Replace placeholder OG with governed brand imagery (per page type where justified)

### C3) JSON-LD (structured legitimacy)

- Start with `WebSite`, `Organization`, and `WebPage`/`WebApplication` for the engine route

---

## Phase D — Authority build (next month)

### D1) Methodology page

Explain limits, scoring philosophy, and what the engine does not claim.

### D2) Glossary seed

Own the language systematically.

### D3) Internal linking fabric

No orphan reference pages; each page links into the system deliberately.

---

## Phase E — Verification gates (continuous)

### E1) Post-build smoke (manual until automated)

After `python scripts/build.py` (or `python scripts/quality_gate.py` in CI), verify:

- `/`
- `/manifesto.html`
- `/protocol.html`
- `/standard.html`
- `/registry.html`
- `/reference.html`
- `/engine.html`

Checks:

- navigation present
- canonical present
- GTM present where governed
- no empty structural sections
- no broken internal links on sampled pages

### E2) Monthly external-system review

Follow `docs/EXTERNAL_SYSTEMS.md` review standard.

---

## Sovereign Rule

Remediation without sequencing is operational noise.

Sequencing without documentation is hidden risk.

This plan exists to keep both disciplined.
