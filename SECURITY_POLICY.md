# SECURITY_POLICY.md

## 1) Purpose

Security at Funnelplugs is not a patching activity.
It is a structural requirement.

The purpose of this policy is to ensure that Funnelplugs.com is built, published, and maintained as a secure, controlled, and trustworthy strategic digital asset.

Security must protect:
- the integrity of the asset,
- the trustworthiness of the publishing system,
- the cleanliness of the production surface,
- and the long-term valuation strength of the project.

---

## 2) Core Rule

Security must be designed into the asset from the beginning.

It must not be treated as:
- a later fix,
- a reactive patch cycle,
- or a cosmetic compliance layer.

Every technical and structural decision must reduce unnecessary exposure.

---

## 3) Security Principle

Funnelplugs is a **GitHub-first static strategic asset** with a controlled publishing chain.

That means security is built through:
- architectural simplicity,
- versioned control,
- limited attack surface,
- controlled dependencies,
- disciplined deployment,
- and strong network perimeter protection.

The safest system is the one that exposes the least unnecessary complexity.

---

## 4) Official Publishing Security Chain

The approved operational chain is:

**Local Python generation/update → GitHub Desktop commit/push → GitHub repository → GitHub Actions validation/build/deployment → live asset**

### Security meaning of this chain
- Development happens locally in a controlled environment.
- GitHub is the single source of truth.
- GitHub Actions handles automation and deployment logic.
- Cloudflare is used only for DNS, TLS, security, and edge control after nameserver delegation.
- Cloudflare is not part of the content publishing workflow.
- No Cloudflare API token is required for publishing.

Any workflow that bypasses this chain is non-compliant.

---

## 5) Source-of-Truth Protection

### 5.1 GitHub is the only source of truth
No production changes may be made through scattered platforms or undocumented manual interventions.

### 5.2 No shadow publishing
No hidden deployment paths.
No unofficial copies.
No side-channel content updates.

### 5.3 Version traceability is mandatory
All meaningful changes must remain traceable through Git history.

---

## 6) Secrets and Credentials Policy

### 6.1 No secrets in the repository
The repository must never contain:
- API keys,
- tokens,
- credentials,
- private certificates,
- environment secrets,
- or hidden operational passwords.

### 6.2 No hardcoded secrets in code
No credentials may appear in Python scripts, JavaScript files, templates, or configuration committed to GitHub.

### 6.3 GitHub secrets only where truly required
If the workflow later needs secrets, they must be stored only in approved GitHub repository or environment secrets.

### 6.4 Cloudflare token restriction
No Cloudflare API token is part of the publishing workflow.
This is a deliberate security simplification rule.

---

## 7) Static Asset Security Discipline

Funnelplugs should remain structurally simple wherever possible.

### Required principles
- prefer static generation over unnecessary runtime complexity,
- avoid server-side attack surface unless strategically necessary,
- minimize external execution dependencies,
- keep production output transparent and inspectable.

Static clarity is part of security strength.

---

## 8) Dependency Policy

### 8.1 Minimal dependency doctrine
Do not introduce packages, libraries, frameworks, or scripts unless they are clearly justified.

### 8.2 Stable dependency preference
Prefer mature, necessary, well-understood dependencies over fashionable complexity.

### 8.3 No dependency sprawl
Every dependency increases risk.
Unnecessary dependencies are forbidden.

### 8.4 Dependency review discipline
Any added dependency must be reviewed for:
- necessity,
- maintenance quality,
- security reputation,
- and architectural fit.

---

## 9) JavaScript and Client-Side Security Policy

### 9.1 Only necessary client-side code
No unnecessary JavaScript.
No decorative script bloat.
No third-party script clutter.

### 9.2 No unsafe inline logic where avoidable
Client-side behavior should remain clean, minimal, and reviewable.

### 9.3 No untrusted script inclusion
Do not include third-party scripts without strategic and security justification.

### 9.4 Avoid risky browser-side patterns
Do not expose internal logic, unsafe debug helpers, sensitive identifiers, or fragile public-side mechanisms.

---

## 10) Content and File Exposure Policy

### 10.1 No internal-only documents in production
The live asset must not expose:
- internal notes,
- hidden decision files,
- draft documents,
- development leftovers,
- raw data not intended for public access,
- or internal process artifacts.

### 10.2 No debug residue
No debug files, temporary outputs, or test states may remain in production.

### 10.3 Public output must be intentional
Anything published must be assumed public, indexable if not blocked, and inspectable.

---

## 11) Form, Input, and External Interaction Policy

If the asset later introduces forms, calculators, or user input systems:

### 11.1 Input must be treated as untrusted
All inputs must be validated and constrained.

### 11.2 Minimize collection
Do not collect unnecessary user data.

### 11.3 No uncontrolled integrations
No external collection or processing service should be added casually.

### 11.4 Utility must not become an attack surface
Tools must remain bounded, controlled, and strategically justified.

---

## 12) Cloudflare Security Role

Cloudflare is the network perimeter security layer after nameserver delegation.

### Approved Cloudflare role
- DNS authority
- TLS/SSL enforcement
- edge security
- WAF
- bot management where appropriate
- rate limiting where appropriate
- caching and edge rules where appropriate

### Forbidden role
Cloudflare must not become:
- the asset publishing engine,
- the content update path,
- the hidden source of truth,
- or a replacement for GitHub governance.

Cloudflare protects the perimeter.
It does not govern the asset’s internal publishing logic.

---

## 13) GitHub Actions Security Role

GitHub Actions is the approved automation layer.

### Security expectations
- workflows must be minimal and controlled,
- actions used should be trusted and necessary,
- permissions should be limited where possible,
- deployment should depend on validation and quality checks,
- and workflow logic must not expose secrets carelessly.

Automation must strengthen control, not weaken it.

---

## 14) Security Headers and Transport Discipline

Production delivery should enforce strong transport and browser-level security where supported by the platform stack.

This includes, where appropriate:
- HTTPS enforcement,
- clean TLS configuration,
- secure transport expectations,
- and suitable browser security headers.

These controls should be configured through the approved infrastructure layer, especially via Cloudflare or hosting controls when applicable.

---

## 15) Access Control Policy

### 15.1 Repository access must be limited
Only trusted operators should have write access.

### 15.2 Publishing authority must be controlled
No uncontrolled collaborator publishing.

### 15.3 Principle of minimal access
People and systems should only have the access they actually require.

---

## 16) Monitoring and Detection

Security issues should be made visible early.

The build and review process should help detect:
- exposed internal files,
- invalid asset references,
- accidental publication of protected material,
- dependency risk where checks exist,
- and structural conditions that create avoidable exposure.

Where possible, automated checks should support this.

---

## 17) Incident Response Principle

If a security issue is detected:

1. stop unsafe deployment if necessary,
2. identify scope,
3. remove exposure,
4. rotate affected secrets if any exposure occurred,
5. correct the structural cause,
6. log the event in the decision or incident record,
7. redeploy only after verification.

The objective is not cosmetic recovery.
The objective is restored trust integrity.

---

## 18) Security and Valuation Relationship

Security is part of acquisition strength.

A strategic acquirer should see:
- controlled infrastructure,
- minimal exposure,
- disciplined publishing,
- clean operational logic,
- and a low-chaos technical environment.

Security is not only protection.
It is part of the asset’s credibility and transfer value.

---

## 19) Final Rule

Nothing insecure, uncontrolled, overexposed, or structurally careless should enter production.

Funnelplugs must remain:
- clean,
- controlled,
- minimal in exposure,
- and secure by design.

That is the security standard.
