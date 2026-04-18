# EXTERNAL_SYSTEMS.md

## Status

Active governance document.

## Purpose

This document records production systems that operate outside the GitHub repository but materially affect FunnelPlugs.com behavior, measurement, routing, security posture, or indexation.

These systems are external to the repository, but they are not outside governance.

GitHub remains the sovereign source of truth for:

- documentation
- operational visibility
- decision logging
- change discipline

Any production-relevant external system that affects the live asset must be documented here.

---

## Governance Principle

FunnelPlugs does not permit shadow operational infrastructure.

If a system changes any of the following, it must be tracked in-repo:

- measurement
- DNS or routing
- HTTPS behavior
- redirects
- crawlability or indexation
- headers or security posture
- deployment-adjacent production behavior

Undocumented live configuration is governance debt.

---

## Documentation Boundary

This file documents only:

- identifiers
- current status
- purpose
- operational configuration
- last verification state

This file must never contain:

- passwords
- API tokens
- login emails
- recovery codes
- private account details
- secret keys
- billing details

---

## System Register

### 1) Google Tag Manager

**System**  
Google Tag Manager

**Container ID**  
`GTM-56J99S4F`

**Purpose**  
Tag orchestration and controlled delivery of measurement logic.

**Production Status**  
Active

**Configured Outside Repo**  
Yes

**Repository Dependency**

- `templates/base.html` (GTM bootstrap inline; `noscript` iframe)
- `assets/js/gtm.js` (optional legacy loader; production pages use inline bootstrap in the template)

**Known Live Configuration**

- Google tag deployed through GTM
- Primary measurement delivery active
- Current production use is limited and controlled

**Governance Notes**

- No experimental or unpublished production-affecting tags should remain in the live container
- Any tag, trigger, or measurement-path change affecting production behavior must be reflected in this file
- GTM must remain operationally minimal and tightly governed

**Last Verified**

- Date: `2026-04-18`
- Status: Verified active

---

### 2) Google Analytics 4

**System**  
Google Analytics 4

**Measurement ID**  
`G-7STBKHZN47`

**Purpose**  
Traffic and behavioral measurement for FunnelPlugs.com.

**Production Status**  
Active

**Configured Outside Repo**  
Yes

**Known Live Configuration**

- GA4 receives production data
- Delivery path is governed through GTM
- Duplicate direct page-level tagging must not be introduced

**Governance Notes**

- GA4 exists for measurement only, not indexation
- Any change to measurement ID, stream structure, or tag delivery logic must be documented here
- GA4 and GTM must not be configured in a way that produces duplicate pageview reporting

**Last Verified**

- Date: `2026-04-18`
- Status: Receiving data

---

### 3) Cloudflare

**System**  
Cloudflare

**Purpose**  
DNS, proxying, HTTPS enforcement, redirect control, TLS handling, and edge security layer.

**Production Status**  
Active

**Configured Outside Repo**  
Yes

**Known Live Configuration**

- DNS setup: Full
- Apex records proxied through Cloudflare
- `www` CNAME present and proxied
- Redirect rule active: `www` to root
- Always Use HTTPS: Enabled
- TLS mode: Full
- Universal SSL: Active
- TLS 1.3: Enabled
- Automatic HTTPS Rewrites: Enabled
- Bot Fight Mode: Enabled
- Client-side security: Enabled

**Known Not Yet Confirmed as Fully Governed in Repo**

- Full security headers inventory
- WAF rule inventory
- Cache-control policy inventory
- Rate limiting inventory
- HSTS final policy state
- Content-Security-Policy (Report-Only then enforce) rollout plan — see `docs/REMEDIATION_PLAN.md` Phase B

**Governance Notes**

- Cloudflare must not function as an undocumented shadow control plane
- Any rule affecting routing, headers, crawl behavior, or cache behavior must be recorded here
- Any redirect introduced at the edge must be treated as a production architecture change

**Last Verified**

- Date: `2026-04-18`
- Status: Active, partially documented

---

### 4) Google Search Console

**System**  
Google Search Console

**Purpose**  
Indexation monitoring, sitemap submission, validation tracking, and search visibility review.

**Production Status**  
Active

**Configured Outside Repo**  
Yes

**Known Live Configuration**

- Property type: Domain property
- Verification status: Verified
- Primary sitemap submitted: `https://funnelplugs.com/sitemap.xml`
- Sitemap discovery count observed: 30 URLs
- Indexation state: In progress
- Legacy non-canonical variants observed in historical indexation views:
  - `http://funnelplugs.com/`
  - `http://www.funnelplugs.com/`

**Governance Notes**

- Search Console does not publish the site, but it materially affects indexation workflow and operational visibility
- Material validation actions, sitemap changes, and indexation anomalies should be reflected in `docs/DECISION_LOG.md`
- Canonical enforcement and redirect behavior must remain aligned with Search Console findings

**Last Verified**

- Date: `2026-04-18`
- Status: Verified, sitemap active, indexation under observation

---

## Current Governance Gap Status

The following external systems are now identified and tracked in-repo:

- Google Tag Manager
- Google Analytics 4
- Cloudflare
- Google Search Console

This closes the documentation gap between:

- live operational reality
- and the sovereign source-of-truth doctrine

The gap is reduced, but not fully closed until Cloudflare rules and Search Console operational notes are documented at a deeper level.

---

## Operational Discipline

A material change to any external system above requires all of the following:

1. Update `docs/EXTERNAL_SYSTEMS.md`
2. Update `docs/DECISION_LOG.md` if the change affects production behavior, measurement, routing, security posture, or indexation
3. Re-check site behavior after deployment
4. Confirm that repository documentation still matches live infrastructure

Examples of material changes:

- new GTM tags or triggers
- GA4 measurement path changes
- Cloudflare redirect or security rule changes
- Search Console property or sitemap changes
- HTTPS, TLS, or canonical behavior changes

---

## Review Standard

This document should be reviewed whenever:

- a production system is added
- a measurement or security tool changes
- Cloudflare behavior changes
- search indexation behavior materially changes
- governance documentation is updated

Minimum review cadence:

- on every material infrastructure change
- otherwise at least once per month during active build periods

---

## Sovereign Rule

External systems may exist outside the repository.  
They may not exist outside governance.

If live infrastructure affects FunnelPlugs.com and is not documented here, the repository is operationally incomplete.

For sequenced repair work across security, CI, UX, and authority layers, see `docs/REMEDIATION_PLAN.md`.
