# SITEMAP_POLICY.md

## 1) Purpose

The sitemap at Funnelplugs is not a technical afterthought.
It is a strategic indexing map.

Its role is to provide search engines with a clean, current, trustworthy representation of the asset’s live, indexable structure.

The sitemap must reflect the real architecture of the asset.
It must not become stale, partial, inflated, or misleading.

---

## 2) Core Rule

The sitemap must be generated automatically.
It must not depend on manual maintenance.
It must always reflect newly created, updated, validated, and index-worthy pages.

If a page is added, updated, or removed, the sitemap logic must recognize that change during generation.

---

## 3) Strategic Principles

### 3.1 Accuracy over volume
Only valid, strategic, indexable pages belong in the sitemap.

### 3.2 Freshness matters
Updated pages must carry updated `lastmod` values when meaningful changes occur.

### 3.3 No low-value noise
The sitemap must not become a dumping ground for every generated file.

### 3.4 Structural truth
The sitemap must reflect the actual public architecture of the asset.

---

## 4) Inclusion Rules

A page may be included in the sitemap only if all of the following are true:

- it is publicly accessible,
- it is intended for indexing,
- it has strategic value,
- it is structurally valid,
- it has passed the quality gate,
- it has a clean canonical target,
- and it is not a duplicate or low-value system state.

---

## 5) Exclusion Rules

The following should generally be excluded unless explicitly justified:

- drafts,
- placeholders,
- thin pages,
- duplicate states,
- internal-only pages,
- test outputs,
- orphan utility states,
- low-context results,
- pages blocked from indexing,
- or pages that failed quality validation.

If a page is `noindex`, it should not be present in the sitemap.

---

## 6) lastmod Policy

### 6.1 lastmod is required where supported by the build system
Each sitemap entry should include a meaningful `lastmod` value.

### 6.2 lastmod must reflect real change
Do not update `lastmod` mechanically if the page content has not meaningfully changed.

### 6.3 lastmod must be generation-aware
The sitemap generator should read from actual file state, structured data, or content timestamps when possible.

False freshness weakens trust.

---

## 7) Canonical and URL Integrity

Every sitemap URL must:
- resolve correctly,
- match the canonical public version,
- avoid duplication,
- avoid malformed structures,
- and align with the intended domain strategy.

No broken URL may appear in the sitemap.
No redirected clutter should be tolerated if the final canonical URL is known.

---

## 8) Domain and Format Consistency

The sitemap must consistently use the correct production domain.

It must not mix:
- staging domains,
- preview domains,
- temporary routes,
- or inconsistent protocol states.

The sitemap must represent the final live asset cleanly.

---

## 9) Generation Workflow

The sitemap must be generated as part of the build process.

Recommended sequence:

1. content and page generation
2. validation pass
3. indexability filtering
4. sitemap generation
5. final quality check
6. deployment

The sitemap must never be generated before page validity is known.

---

## 10) Validation Requirements

The sitemap generation process must verify:
- each included URL exists,
- each included URL is intended for indexing,
- each included URL has valid metadata,
- each included URL has acceptable structural status,
- each included URL belongs to the approved domain,
- and no excluded page leaks into the sitemap.

---

## 11) Relationship to SEO Policy

The sitemap is not a substitute for good SEO.
It is a structural reinforcement layer.

A weak page does not become valuable because it appears in the sitemap.
The sitemap should amplify quality, not disguise weakness.

---

## 12) Automation Rule

Sitemap maintenance must remain fully aligned with the GitHub-first publishing workflow.

That means:
- generated locally through Python or build logic,
- committed via GitHub Desktop,
- validated in GitHub Actions,
- published from GitHub,
- and never manually maintained inside Cloudflare.

Cloudflare has no sitemap governance role.

---

## 13) Failure Rule

If sitemap generation detects:
- broken URLs,
- invalid canonical structure,
- missing metadata,
- structural mismatches,
- or invalid inclusion,

then the build should fail or raise a high-severity warning depending on the system design.

The sitemap must be treated as a trust-bearing asset file.

---

## 14) Final Rule

The Funnelplugs sitemap must always behave like a disciplined index of the asset’s strongest public structure.
It must be current, selective, correct, and worthy of trust.

That is the sitemap standard.
