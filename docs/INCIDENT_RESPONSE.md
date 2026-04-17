# INCIDENT_RESPONSE.md

## 1) Purpose

This document defines the incident response procedure for Funnelplugs.com.
The objective is trusted recovery with minimal strategic damage.

---

## 2) Incident Types

- source integrity incident
- workflow/deployment incident
- security exposure incident
- public trust narrative incident
- infrastructure/DNS/TLS incident

---

## 3) Severity Levels

- **SEV-1:** active compromise or major trust break
- **SEV-2:** high-risk exposure without confirmed full compromise
- **SEV-3:** contained issue with moderate operational risk
- **SEV-4:** low-severity hygiene issue

---

## 4) Response Sequence

### Step 1: Detect and Classify

- identify incident class and severity
- capture initial evidence and scope

### Step 2: Contain

- pause deployment if risk is active
- isolate affected workflow, files, or infrastructure path

### Step 3: Eradicate

- remove malicious or unsafe changes
- revoke or rotate affected secrets if exposure exists
- remove unauthorized access paths

### Step 4: Recover

- restore last trusted state
- re-run quality and governance checks
- redeploy only after controls pass

### Step 5: Learn and Harden

- document root cause
- add preventive control if missing
- log strategic implications in `DECISION_LOG.md`

---

## 5) Communication Rule

- internal communication must remain precise and factual
- external communication (if needed) must be controlled and trust-preserving
- no speculative public statements during active triage

---

## 6) Recovery Gate

No incident is considered closed until:

- root cause is identified
- corrective change is merged and validated
- recurrence control is documented
- changelog and decision traceability are updated

---

## 7) Final Rule

Speed matters, but trust restoration quality matters more.
Recovery is complete only when integrity is operationally re-proven.
