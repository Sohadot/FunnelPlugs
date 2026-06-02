# Ontology Class Page Standard

## Purpose

This document defines the structural standard for standalone reference pages
covering individual Plug Ontology failure classes. Pages built to this standard
constitute the governed reference layer for the ontology, translating the
controlled vocabulary defined in `ontology.html` into individually addressable,
internally linked, concept-depth pages.

---

## Applicability

This standard applies to every HTML page published at a URL of the form
`/{slug}.html` where the slug is the kebab-case identifier of a Plug Ontology
failure class. The current class inventory is defined in `ontology.html`.

---

## Required Page Sections

Each ontology class page must contain all fifteen of the following sections, in
the order listed. Sections may not be omitted. Content may not be synthetic,
vague, or duplicated verbatim from the class definition in `ontology.html` — it
must extend the definition with structural meaning, diagnostic logic, and
governed claim boundaries.

### 1. Formal Class Identifier Block

A metadata block visible at the page's opening that displays:

- **CLASS**: The zero-padded two-digit class number (e.g. `01`)
- **IDENTIFIER**: The full kebab-case slug
- **INTEGRITY DIMENSION**: The Funnel Integrity Standard dimension this class
  violates (Trust Integrity, Flow Continuity, or Recovery Readiness)
- **PROTOCOL STAGE**: The FunnelPlugs Protocol stage at which this class is
  first detected

This block provides machine-readable and human-readable classification anchors
without prose.

### 2. Lead Statement

A single sentence or tight paragraph that states what the failure is, at the
level of structural mechanism. The lead does not summarise the page. It
identifies the failure from the perspective of structural path mechanics.

### 3. Summary Block (Summary section)

A short paragraph (2–4 sentences) that defines the failure class at the level
required for a practitioner to confirm or exclude it during initial path
review. The summary is the minimum complete definition of the class.

### 4. Formal Definition

The governing definition of the class in precise, claim-bounded language. The
formal definition is the canonical statement of what this failure type is. It
is the definition that would appear in a governed ontology export or an API
response for this class. It must be internally consistent with the definition
in `ontology.html`.

### 5. Structural Meaning

An explanation of why this failure is structural rather than presentational.
This section answers: why cannot this failure be corrected by a cosmetic or
content change alone? What architectural property of the path must change for
the failure to be resolved? This section defends the failure's classification
as a structural type rather than a performance metric.

### 6. Where It Appears

A description of which layers, transitions, or zones of the commercial path
are the typical sites of this failure class. Must be specific to path
architecture — not generic advice about marketing channels.

### 7. What It Damages

A structural account of the integrity conditions this failure violates and the
downstream path consequences of those violations. Revenue language is not used.
The account is structural: what does this failure prevent the path from doing,
and what does that prevention cost at the path architecture level?

### 8. Typical Symptoms

An observable-signals list. Symptoms must be:

- Observable from path analytics or practitioner audit without revenue data
- Specific enough to distinguish this class from adjacent classes
- Not circular (do not define the symptom as the failure itself)

Minimum three symptoms. Presented as a prose list or structured paragraph.

### 9. Diagnostic Logic

A step-by-step description of how to confirm the presence of this failure class
in a commercial path under evaluation. The logic must be:

- Executable by a practitioner with access to standard path analytics
- Bounded: it terminates in a classification decision, not an open-ended review
- Discriminating: it references the signals that distinguish this class from
  structurally adjacent classes

### 10. Plug Logic

A description of the structural intervention class required to address this
failure. Must state:

- What the intervention must structurally achieve (not what software to use)
- What condition the path must satisfy after intervention for the failure class
  to no longer apply
- Why the intervention class is structural rather than tactical

### 11. Standard Dimension Mapping

An explicit mapping of this failure class to the Funnel Integrity Standard
integrity dimension it violates. Must include:

- The dimension name
- An explanation of which integrity condition within that dimension is violated
- An internal link to `/standard.html`

### 12. Protocol Stage Mapping

An explicit mapping of this failure class to the FunnelPlugs Protocol stage at
which it is detected and classified. Must include:

- The stage name
- An explanation of what the protocol does at that stage to surface this failure
- An internal link to `/protocol.html`

### 13. Engine Integration

A description of how the Revenue Leak Diagnostic Engine processes signals that
correspond to this failure class. Must include:

- What input signals route toward this class
- What the engine produces as output when this class is detected
- An internal link to `/engine.html`

This section does not make revenue or conversion-lift claims.

### 14. Registry Integration

A description of how the Plug Registry organises the intervention classes that
address this failure. Must include:

- The registry category that contains the relevant plug interventions
- An explanation of what the registry defines for this failure type
- An internal link to `/registry.html`

### 15. Related Concepts Navigation

A set of navigation cards linking to related failure classes, related
intervention classes, and the ontology index. Minimum three cards. Each card
must include:

- A category label (e.g. "Related Failure Class", "Related Plug Class",
  "Ontology Index")
- A title
- A short description
- An internal link

---

## Metadata Requirements

Every ontology class page must include:

- `<title>`: Format: `{Class Name} — Ontology Class {NN} | Funnelplugs`
- `<meta name="description">`: Describes the failure class definition and its
  structural meaning in 140–160 characters
- `<meta name="keywords">`: Includes the class slug, the class name, and the
  generic term "structural funnel failure"
- `<link rel="canonical">`: The absolute URL at
  `https://funnelplugs.com/{slug}.html`
- Open Graph tags: `og:title`, `og:description`, `og:type` (article),
  `og:url`, `og:image`, `og:image:alt`
- Twitter Card tags: `twitter:card` (summary_large_image), `twitter:title`,
  `twitter:description`, `twitter:image`

---

## Internal Linking Requirements

Each page must link internally to:

- `/ontology.html` (ontology index — the governing vocabulary source)
- `/standard.html` (within the Standard Dimension Mapping section)
- `/protocol.html` (within the Protocol Stage Mapping section)
- `/engine.html` (within the Engine Integration section)
- `/registry.html` (within the Registry Integration section)
- At least two other ontology class pages (within Related Concepts Navigation)

External links are not required and should not be added unless governing
external documents are referenced.

---

## Claims Boundary

Ontology class pages are structural reference documents. The following claim
types are unconditionally prohibited:

- Statements that applying the plug intervention will produce a specific revenue
  improvement
- Statements that this failure class affects a specific percentage of commercial
  paths
- Conversion-lift projections of any kind
- Comparisons to competitor tools or approaches
- Statements about average or typical conversion rates

---

## Quality Gate Compliance

Ontology class pages must pass all conditions of the FunnelPlugs quality gate
before publication. Specifically:

- No forbidden content patterns (no `placeholder`, no unsupported benchmark
  claims, no revenue percentage claims)
- All internal links must resolve to existing files
- Metadata must be complete and non-generic
- GTM bootstrap script must be present in `<head>`
- GTM noscript fallback must be the first element in `<body>`
- `<link rel="canonical">` must match the page's declared URL

---

## Versioning

This standard is governed by the FunnelPlugs versioning policy
(`docs/VERSIONING_POLICY.md`). Changes to the required sections, metadata
requirements, or claims boundary trigger a MINOR version increment. Changes to
the formal definition structure or internal linking requirements trigger a
MAJOR version increment. The decision log entry must reference this document
when changes are made.

**Current version:** 1.0
