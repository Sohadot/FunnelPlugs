# THREAT_MODEL.md

## 1) Purpose

This document defines the sovereign threat model for Funnelplugs.com.
It protects trust, continuity, and strategic valuation posture.

The model is focused on realistic threats to a GitHub-first static strategic asset.

---

## 2) Critical Assets to Protect

- source-of-truth repository integrity
- deployment workflow integrity
- canonical domain trust identity
- doctrine and standards fidelity
- public narrative consistency

---

## 3) Threat Classes

### 3.1 Identity and Brand Abuse

- domain impersonation
- lookalike social/account spoofing
- fake mirror pages with altered messaging

### 3.2 Source and Workflow Abuse

- unauthorized repository writes
- malicious workflow modification
- hidden publishing path injection

### 3.3 Supply Chain and Dependency Risk

- compromised third-party action or package
- unreviewed dependency drift
- indirect script execution expansion

### 3.4 Content Integrity Attacks

- unauthorized doctrinal edits
- stealth degradation of standards language
- strategic narrative poisoning

### 3.5 Infrastructure and Availability Risks

- DNS misconfiguration or hijack attempt
- TLS or edge misconfiguration
- origin content mismatch and stale exposure

---

## 4) Threat Severity Model

- **Critical:** public trust or source integrity compromised
- **High:** publication chain or authority posture weakened
- **Medium:** localized integrity weakness without full compromise
- **Low:** non-critical control gap or hygiene issue

---

## 5) Control Matrix

### 5.1 Preventive Controls

- CODEOWNERS on governance-critical files
- pull request template with governance declarations
- mandatory CI checks for governance and markdown integrity
- no secrets in repository policy
- GitHub-first publishing chain only

### 5.2 Detective Controls

- CI failures for governance-critical violations
- markdown link integrity checks
- decision-log traceability requirements
- routine review of workflow and docs drift

### 5.3 Corrective Controls

- incident triage and containment playbook
- rollback to last trusted commit
- credentials rotation if exposure exists
- post-incident decision and changelog updates

---

## 6) Non-Negotiable Security Outcomes

- GitHub remains the only source of truth
- no hidden publishing channels are accepted
- no governance-critical change ships without traceability
- no monetization or growth move degrades authority trust

---

## 7) Review Cadence

- review this model on each major workflow or security change
- update when new threat classes become material
- record major model changes in `DECISION_LOG.md`
