# DAILY_OPERATION_PROTOCOL.md

## 1) Purpose

This document defines the daily sovereign operating path for all future changes.
It converts discipline into a repeatable execution sequence.

The objective is not only technical correctness.
The objective is to preserve strategic clarity, output integrity, and governance continuity.

---

## 2) Non-Negotiable Rule

No direct work on `main`.
No direct push to `main`.
All meaningful changes move through branch -> checks -> PR -> reviewed merge.

---

## 3) Daily Sovereign Flow (5 Steps)

### Step 1: Create a fresh branch from `main`

- Sync local `main` with `origin/main`
- Create branch using disciplined naming:
  - `feat/...`
  - `fix/...`
  - `docs/...`
  - `chore/...`

### Step 2: Modify source intentionally

- Apply change to source-of-truth files only
- Avoid opportunistic or mixed-scope edits
- Keep each branch focused on one coherent objective

### Step 3: Run governance and quality checks

Run in this order:

1. `python scripts/sovereign_standards_guard.py`
2. `python scripts/check_markdown_links.py`
3. `python scripts/governance_guard.py --base-ref origin/main`
4. `python scripts/quality_gate.py`

Any failure blocks commit until corrected.

### Step 4: Run production build and visual smoke test

Run:

- `python scripts/build.py --mode production`

Then perform a quick visual smoke test on critical pages:

- `/`
- `/reference.html`
- `/engine.html`
- `/registry.html`

Confirm:

- no layout break
- nav is present and usable
- canonical behavior is intact
- GTM inclusion remains intact where required
- no empty or broken content sections

Optional automated pre-check (after the build, before opening the browser):

- `python scripts/smoke_critical_pages.py`

### Step 5: Pre-commit cleanup, then commit and PR

Before commit:

- remove `__pycache__` and temporary files
- verify no unintended generated output noise
- run `git status` and inspect exact staged scope

Then:

- write a disciplined commit message
- push branch
- open PR
- merge only after required checks + CODEOWNERS approval

---

## 4) Pre-Commit Hygiene Gate (Mandatory)

Pre-commit cleanup is required before every commit, not only after merge.

Minimum hygiene:

- no `__pycache__`
- no local temp artifacts
- no accidental test markers
- no unrelated file drift

If `git status` is noisy, stop and clean first.

---

## 5) Source vs Output Policy

Not every generated change should be committed.

### Allowed output commit cases

- output changed because approved source changed
- output changed because intentional release update is being prepared
- output change is part of a deliberate publish cycle

### Output noise cases (do not commit)

- `lastmod` drift caused only by local test execution
- regenerated files with no strategic or source-driven meaning
- side effects from validation runs without approved release intent

### `sitemap.xml` rule

Commit `sitemap.xml` only when output changes are intentionally part of the release.
If change is test-only noise, restore it before commit.

---

## 6) Commit Message Policy

Use structured commit messages for long-term readability.

Preferred patterns:

- `feat(reference): add core reference pages and internal linking`
- `fix(seo): normalize sitemap generation and canonical behavior`
- `chore(governance): tighten validation and guardrails`
- `docs(protocol): update daily sovereign operation rules`

Avoid vague messages such as:

- `update`
- `misc`
- `fix stuff`

---

## 7) PR and Merge Gate

A PR is merge-ready only when all are true:

- required check passes: `Governance, Security, and Markdown Checks`
- branch is up-to-date with `main`
- CODEOWNERS review is approved
- PR scope remains coherent and traceable

---

## 8) Post-Merge Closeout

After merge:

- pull updated `main`
- delete local/remote feature branch
- verify clean working tree

Operational closure is part of sovereign hygiene.

---

## 9) Final Rule

This protocol is not optional process overhead.
It is part of the asset's trust architecture and valuation discipline.
