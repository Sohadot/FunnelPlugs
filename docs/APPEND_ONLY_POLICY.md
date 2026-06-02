# Append-Only Policy

## The Principle

Terminology published by a reference system becomes load-bearing the moment practitioners begin using it. A practitioner who has built a diagnostic workflow around a term, a category, or a class definition is now dependent on that definition remaining stable.

Silent rewrites break that dependency without warning. They invalidate existing work without leaving a record of what changed or why. They erode the trust that makes a reference system worth consulting.

The append-only policy exists to protect the structural integrity of terms that have been published and relied upon.

---

## Records That Must Be Preserved Historically

The following records are governed as historically preserved. Once published, they may be extended or deprecated but not silently modified or deleted:

1. **Plug ontology class entries** — Each plug class published in `data/plug_taxonomy.json` and its corresponding reference page
2. **Leak ontology class entries** — Each leak class published in `data/leak_taxonomy.json` and its corresponding reference page
3. **Registry category definitions** — Each category in the plug registry as published in `registry.html` and its governing data
4. **Standard version definitions** — Each published version of the Funnel Integrity Standard, including its formal integrity dimensions and their definitions
5. **Protocol version definitions** — Each published version of the FunnelPlugs Protocol, including its stage names, sequence, and classification criteria
6. **Decision log entries** — All entries in `docs/DECISION_LOG.md` once written; the log accumulates forward

---

## How Deprecated Terms Are Handled

A term that is no longer structurally correct or has been superseded by a more precise definition is deprecated, not deleted.

**Deprecation process:**

1. The term's entry in the governing data file is updated with a `deprecated: true` flag and a `deprecated_reason` field explaining why the term is no longer current
2. A `successor` field is added pointing to the term or class that replaces it, if one exists
3. The term's reference page (if it has one) is updated to include a deprecation notice at the top, stating: the term is deprecated, the date of deprecation, the reason, and the successor term if applicable
4. The deprecation is recorded in `docs/DECISION_LOG.md` with full rationale
5. The term is NOT removed from the data file and NOT deleted from the file system
6. Internal links pointing to the deprecated term's page are evaluated: links that serve historical context may remain; links that would mislead current practitioners are updated to point to the successor

---

## How Renamed Classes Are Handled

A class that is renamed is treated as a deprecation of the original name and an addition of a new name — not as a modification of an existing entry.

**Rename process:**

1. The original class entry is deprecated using the deprecation process above
2. A new class entry is created with the new name, a new identifier, and all governing definition fields
3. The original class's reference page is updated with a deprecation notice pointing to the new class page
4. The new class receives its own reference page
5. Internal links are updated to point to the new class page
6. The rename is recorded in `docs/DECISION_LOG.md` with the rationale for why the original name was insufficient and what the new name more precisely captures

The original identifier is retained in the data file indefinitely. It is not reassigned.

---

## How Old Standard and Protocol Versions Are Preserved

When the Funnel Integrity Standard or the FunnelPlugs Protocol undergoes a MAJOR version increment:

1. The content of the current published version is archived before the new version replaces it
2. The archived version is stored in `docs/archive/` under a versioned filename (e.g., `FUNNEL_INTEGRITY_STANDARD_v1.md`)
3. The new version is published as the current authoritative version
4. The archived version is not edited after archiving
5. If the new version makes the archived version substantially incorrect in ways that could mislead practitioners, a note is added to the top of the archived version stating that it has been superseded and pointing to the current version

The archive directory is a governance record, not a public-facing resource. Archived versions are not linked from the public navigation.

---

## How the System Avoids Silent Conceptual Rewrites

The following practices prevent silent conceptual drift:

**Version increment requirement**

Any change to a formal definition, classification criterion, or ontology term must increment the version of the affected layer. Version increments are visible in the decision log. A layer that has not been version-incremented has not changed its formal definitions — this is a guarantee, not an aspiration.

**Decision log requirement**

Any change that modifies how the system classifies, names, or evaluates a structural concept must be documented in `docs/DECISION_LOG.md` before or at the time it is published. The log is a continuous written record. Its absence for a given change indicates that the change was not made through the governed process.

**Data-layer authority**

The ontology and registry are governed by data files (`data/plug_taxonomy.json`, `data/leak_taxonomy.json`), not by the rendered HTML. Changing a term in a rendered HTML file without changing its governing data file creates a discrepancy between the system's formal record and its public presentation. The quality gate does not catch all such discrepancies — therefore, changes to definitions must always originate in the data layer.

**Governance guard enforcement**

`scripts/governance_guard.py` enforces that changes to governance-critical files are accompanied by a decision log update. This is a CI-enforced rule, not a convention. It creates an automated barrier against casual modification of the system's governing documents without documentation.

**Append-only log**

The decision log is itself governed as append-only. An entry may not be deleted or retroactively edited once the change it documents has been published. If an entry was incorrect, a new entry is added to clarify or correct it — the original entry remains.
