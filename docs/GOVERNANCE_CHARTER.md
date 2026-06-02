# Governance Charter

## System Definition

Funnelplugs is a governed reference system for structural funnel failure and missing intervention layers. It is not a generic marketing resource. It is a classification infrastructure for identifying where digital commercial paths fail, naming the failure type, and defining the intervention layer required to restore flow.

The governing obligation of Funnelplugs is structural correctness. Every term published, every class defined, every claim advanced must be accurate, defensible, and stable enough for practitioners to rely on it.

---

## System Layers and Their Relationships

Funnelplugs operates across seven distinct layers. Each layer has a defined role and a governed relationship to the others. No layer may be changed without considering its effect on the layers it supports and the layers that support it.

### Ontology

The controlled vocabulary of the system. Defines the formal types, classes, identifiers, and naming conventions for all structural concepts. All other layers are downstream of the ontology. Ontology changes propagate to every layer.

### Standard

The formal specification of what constitutes a structurally sound commercial path. Defines integrity dimensions, pass/fail criteria, and the measurable conditions of completeness. The standard is the evaluative benchmark. Protocol and Engine reference it directly.

### Protocol

The methodological system for applying the standard diagnostically. Defines how to detect, classify, and assign intervention types. The protocol references the standard and the ontology. Registry entries are organized according to protocol categories.

### Registry

The governed catalog of intervention classes and plug categories. All registry entries are governed by ontology naming and organized by protocol classification. The registry is append-only for established entries.

### Reference

The public reference layer: individual pages for each defined leak class, plug class, and conceptual paper. The reference layer materializes the ontology and registry as publicly accessible, indexed documents.

### Engine

The diagnostic utility layer. Translates the protocol and standard into a structured evaluation interface. Engine logic references the ontology, standard, protocol, and scoring rules. Engine outputs reference registry categories.

### Governance

The meta-layer that controls how all other layers change, who may authorize changes, what triggers documentation requirements, and how the system preserves its historical record. Governance is the only layer with authority over all others.

---

## Decision Authority

### Doctrine-Level Changes

Changes to the governing thesis, the foundational ontology structure, or the formal integrity standard require explicit decision authority. These changes must be initiated through a formal decision proposal, reviewed against the append-only policy, documented in `docs/DECISION_LOG.md` with full rationale, and treated as major version increments.

No doctrine-level change may be made silently or as a side effect of a lower-priority edit.

### Major Changes

Changes that alter the classification structure, add or remove formal categories, modify scoring rules, change protocol stages, or affect how the engine produces outputs are major changes. Major changes require:
- A proposal documented before the change is made
- Validation that the change is consistent with the governing thesis
- A decision log entry with rationale
- Version increment in the affected layer

### Minor Changes

Changes that improve the precision of existing descriptions without altering their structural meaning, fix errors in rendering or formatting, add new reference entries within existing categories, or update metadata are minor changes. Minor changes require:
- No formal proposal
- No decision log entry unless the change touches a governance-critical file
- No version increment unless the affected layer policy requires one

---

## What Requires Documented Rationale

The following changes require a written rationale entry in `docs/DECISION_LOG.md` before or at the time of publication:

1. Renaming any formally defined class, category, or ontology term
2. Deprecating any established leak class, plug class, or registry category
3. Changing the formal definition of any integrity dimension
4. Modifying scoring rules, weighting factors, or integrity band thresholds
5. Adding a new top-level category to the plug or leak ontology
6. Removing any content layer from the public reference
7. Changing canonical URL structure for any declared page
8. Changing the formal standard version number
9. Altering the governance charter itself

---

## What Cannot Be Changed Without Version Increment

The following cannot be silently modified. Any change requires a version increment in the affected layer:

- Ontology class identifiers (IDs are permanent; renaming requires a new ID with the old one deprecated)
- Standard integrity dimensions
- Protocol stage names and sequence
- Scoring rule structure (new dimensions, changed weights, altered band thresholds)
- Engine decision logic identifiers
- Governance charter version

---

## Append-Only Layers

The following layers are governed as append-only or historically preserved. See `docs/APPEND_ONLY_POLICY.md` for full rules.

- Plug ontology class registry
- Leak ontology class registry
- Published standard versions
- Published protocol versions
- Decision log

Entries may be deprecated but not deleted. Versions may be superseded but not erased. The historical record of what was published, when, and why is a governance asset.

---

## Claims Restraint

Funnelplugs makes no unsupported revenue, ROI, or conversion-lift claims.

The following are permanently prohibited:
- Specific revenue percentage improvements attributed to any plug class
- Guaranteed conversion lift claims tied to any intervention
- ROI projections not derived from the user's own data
- Comparison claims against competitor tools or approaches

Claims within the system are structural and diagnostic: this class of failure exists, it follows this pattern, this type of intervention addresses it. The outcome of applying an intervention depends on the specific system being corrected and is not within the scope of this reference.

---

## Quality Posture

Funnelplugs maintains the following minimum quality standards. These are not aspirational targets — they are conditions of publication.

- No page may be published without a complete title, description, canonical, and H1
- No page may contain structurally empty content shells
- No internal links may be broken
- No page may contain structurally unsupported claims
- No page may be published as a structural shell awaiting content
- Publishing access is controlled: no unreviewed content may enter the public reference layer
- All new entries to the registry must meet the formal entry criteria documented in the registry governance
