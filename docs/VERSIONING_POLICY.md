# Versioning Policy

## Purpose

This document defines how version numbers are assigned, incremented, and recorded for each layer of the Funnelplugs system. Versioning is a governance function, not an administrative convention. It creates a traceable record of when the system changed and what changed, allowing practitioners and downstream references to reason about stability.

---

## Version Format

All versioned layers use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Structural change to the layer's governing logic, formal definitions, or classification architecture. Downstream layers may be affected. Change requires full documentation in `docs/DECISION_LOG.md`.
- **MINOR**: Addition of new entries, categories, or content within the existing structure. Does not alter existing definitions or classifications. May require a decision log note if the addition is non-trivial.
- **PATCH**: Precision improvement, error correction, or metadata update within existing content. No structural change. No decision log entry required.

---

## Layer Versioning Rules

### Plug Ontology

**Current authority:** `data/plug_taxonomy.json`

**Increment triggers:**
- MAJOR: Addition of a new top-level plug class category, deprecation of an existing category, or restructuring of the category hierarchy
- MINOR: Addition of a new plug class entry within an existing category
- PATCH: Correction of a description, identifier cross-reference, or metadata field for an existing entry

**Constraint:** Plug class IDs are permanent once published. An ID assigned to a class cannot be reassigned to a different class. Deprecated IDs must be retained in the taxonomy with a deprecation flag and a pointer to the successor.

---

### Funnel Integrity Standard

**Current authority:** `docs/FOUNDATION_DOCTRINE.md` and the formal standard page

**Increment triggers:**
- MAJOR: Changing the number, names, or formal definitions of the integrity dimensions; changing the pass criteria for any dimension; modifying the integrity band definitions
- MINOR: Adding clarifying language, examples, or supporting rationale without altering formal definitions
- PATCH: Correcting typographic errors, formatting, or cross-reference accuracy

**Constraint:** Each published version of the Standard must be preserved. When a MAJOR increment occurs, the previous version is archived under its version number and remains accessible. No retroactive editing of published versions is permitted.

---

### FunnelPlugs Protocol

**Current authority:** `protocol.html` and associated data in `data/site.json`

**Increment triggers:**
- MAJOR: Changing the stage names, stage sequence, or formal classification criteria within any stage
- MINOR: Adding interpretive guidance, edge case handling, or worked examples without altering stage definitions
- PATCH: Formatting, cross-reference, or precision corrections

**Constraint:** The protocol version is displayed in the protocol page metadata. When a MAJOR increment occurs, the previous version is archived. Practitioners referencing the protocol by version must be able to retrieve what was published at that version.

---

### Plug Registry

**Current authority:** `registry.html`, `data/plug_taxonomy.json`, and individual plug class pages

**Increment triggers:**
- MAJOR: Addition or deprecation of a registry category; restructuring of category organization
- MINOR: Addition of new entries within existing categories; addition of supporting reference material for existing entries
- PATCH: Correction of descriptions, cross-references, or metadata

**Constraint:** Registry entries are append-only. An entry that has been published cannot be silently removed. Superseded entries are deprecated with a deprecation notice and a pointer to the replacement. See `docs/APPEND_ONLY_POLICY.md`.

---

### Diagnostic Engine Logic

**Current authority:** `data/decision_logic.json`, `data/scoring_rules.json`, `assets/js/engine.js`

**Increment triggers:**
- MAJOR: Changes to scoring weights, band thresholds, decision logic identifiers, or the diagnostic output model
- MINOR: Addition of new diagnostic signals, questions, or dimension mappings within the existing scoring structure
- PATCH: Correction of mapping errors, label precision, or metadata

**Constraint:** Engine logic versioning must be synchronized with the scoring rules and tool questions data files. A change to any of these three files that alters diagnostic outputs requires a MAJOR increment.

---

### Public Reference Pages

**Current authority:** Individual HTML pages generated from `data/site.json`, `data/extra_core_pages.json`, and associated taxonomy data

**Increment triggers:**
- MAJOR: Restructuring the page's conceptual framing, changing its governing definition, or substantially altering its classification content
- MINOR: Addition of related entries, supporting sections, or expanded explanatory content
- PATCH: Metadata corrections, link repairs, formatting improvements

**Constraint:** Reference pages are governed by the pages governance check pipeline. Changes to declared pages regenerate the HTML output from the data layer. Direct edits to generated HTML are overwritten on the next build. Changes to reference page content must be made in the data layer, not the rendered output.

---

### Governance Documents

**Current authority:** All files in `docs/`

**Increment triggers:**
- MAJOR: Changes to charter provisions, policy rules, or formal definitions within governance documents
- MINOR: Addition of clarifying sections, examples, or supporting rationale
- PATCH: Corrections to formatting, cross-references, or typographic errors

**Constraint:** Changes to governance-critical documents (`docs/PROJECT_DOCTRINE.md`, `docs/FOUNDATION_DOCTRINE.md`, `docs/SECURITY_POLICY.md`) must be accompanied by a `docs/DECISION_LOG.md` entry per `governance_guard.py` enforcement. Changes to other governance documents do not require a decision log entry unless they alter formal policy provisions.

---

## Version Record Keeping

The current version of each layer is recorded in `docs/DECISION_LOG.md` as part of any MAJOR change entry. The version history is not stored as a structured data field accessible to the build system — it is maintained in the decision log as a human-readable record.

When a MAJOR increment occurs for any layer:

1. Record the previous version, current version, date, and rationale in `docs/DECISION_LOG.md`
2. Archive the previous version's defining content if it is a versioned artifact (standard version, protocol version)
3. Update any cross-references within the system that cite the versioned layer by version number
