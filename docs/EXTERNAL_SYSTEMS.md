# EXTERNAL_SYSTEMS.md

## Purpose
This file documents production systems that operate outside the GitHub repository but materially affect FunnelPlugs.com behavior, measurement, security, or indexation.

These systems are external to the repository, but they are not outside governance.
GitHub remains the source of truth for documentation, decision tracking, and operational visibility.

---

## 1. Google Tag Manager

- **System:** Google Tag Manager
- **Container ID:** `GTM-56J99S4F`
- **Purpose:** Tag orchestration and measurement delivery
- **Production Status:** Active
- **Configured Outside Repo:** Yes
- **Repository Dependency:** `templates/base.html` + `assets/js/gtm.js`

### Active Configuration
- **Google tag / GA4 Measurement ID:** `G-7STBKHZN47`
- **Trigger:** All Pages

### Governance Notes
- No unpublished experimental tags should remain in the live container.
- Any production tag change must be reflected in this file.
- Container structure must remain minimal and controlled.

### Last Verified
- **Date:** `2026-04-17`
- **Verified By:** `Ahmed / Sohadot`

---

## 2. Google Analytics 4

- **System:** Google Analytics 4
- **Measurement ID:** `G-7STBKHZN47`
- **Purpose:** Traffic and behavioral measurement
- **Production Status:** Active
- **Stream:** `Funnelplugs Main Website`
- **Configured Outside Repo:** Yes

### Governance Notes
- GA4 receives production data through GTM.
- Direct duplicate tagging must not be introduced in page templates.
- Any stream or measurement ID change must be documented here immediately.

### Last Verified
- **Date:** `2026-04-17`
- **Verified By:** `Ahmed / Sohadot`

---

## 3. Cloudflare

- **System:** Cloudflare
- **Purpose:** DNS, TLS, proxying, redirects, security layer, caching
- **Production Status:** Active
- **Configured Outside Repo:** Yes

### Known Active State
- **DNS proxy:** Active
- **Always Use HTTPS:** Enabled
- **WWW to root redirect:** Enabled
- **TLS mode:** Full
- **Universal SSL:** Active
- **TLS 1.3:** Enabled
- **Automatic HTTPS Rewrites:** Enabled

### To Be Documented Explicitly
- Security headers status
- WAF / bot protections
- Redirect rules inventory
- Cache behavior
- Any custom rules affecting crawlability or routing

### Governance Notes
- Any Cloudflare rule affecting routing, headers, caching, or crawl behavior must be documented here.
- Cloudflare must not become an undocumented shadow control plane.

### Last Verified
- **Date:** `2026-04-17`
- **Verified By:** `Ahmed / Sohadot`

---

## 4. Google Search Console

- **System:** Google Search Console
- **Purpose:** Indexation monitoring and sitemap submission
- **Production Status:** Active
- **Configured Outside Repo:** Yes

### Known Active State
- **Property Type:** Domain Property
- **Verification Status:** Verified
- **Primary Sitemap:** `https://funnelplugs.com/sitemap.xml`

### To Be Documented Explicitly
- Exact property name
- Verification method
- Any URL inspection / validation actions of record
- Indexation anomalies under active review

### Governance Notes
- Search Console status changes do not modify the site directly, but they materially affect indexation workflow and must be tracked.
- Sitemap submissions and validation actions should be reflected in the decision log when materially relevant.

### Last Verified
- **Date:** `2026-04-17`
- **Verified By:** `Ahmed / Sohadot`

---

## Operating Rule

External systems may exist outside the repository, but no production-relevant external system may remain undocumented.

If a system changes production behavior, measurement, crawlability, security posture, or routing, that change must be reflected in:
- `docs/EXTERNAL_SYSTEMS.md`
- `docs/DECISION_LOG.md` when materially relevant

Undocumented production configuration is considered governance debt.
