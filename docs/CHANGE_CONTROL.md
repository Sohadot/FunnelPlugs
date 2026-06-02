# Change Control

## Purpose

This document defines the process for making governed changes to the Funnelplugs system. It applies to all changes that affect the public reference layer, the ontology, the standard, the protocol, the registry, or the governance documents themselves.

The process exists to prevent silent conceptual drift, protect the stability of terminology that practitioners rely on, and maintain an auditable record of why the system is the way it is.

---

## Change Classifications

Changes fall into three classes defined in `docs/GOVERNANCE_CHARTER.md`:

- **Doctrine-level**: Changes to governing thesis, ontology structure, integrity standard definitions
- **Major**: Changes to classification structure, scoring rules, protocol stages, category hierarchy
- **Minor**: Precision improvements, new entries within existing categories, metadata corrections

The class determines which process stages are required. All three classes follow the same stage sequence; the requirements at each stage differ.

---

## Process Stages

### Stage 1: Proposal

**Required for:** Doctrine-level and major changes. Optional for minor changes where the intent is unambiguous.

A proposal is a written statement that describes:
- What is being changed
- Which layer is affected
- Why the change is necessary
- What would break or become inaccurate without the change
- Whether the change affects any other layer (downstream or upstream)

Proposals for doctrine-level changes must also state:
- Which existing doctrine provision the change modifies or supersedes
- What the change means for existing practitioners using the current version

Proposals do not need to be formal documents. A clear entry in `docs/DECISION_LOG.md` noting the above points is sufficient.

---

### Stage 2: Review

**Required for:** All doctrine-level and major changes. Optional for minor changes.

Review is the process of checking the proposal against the system's existing structure:

1. **Consistency check**: Does the proposed change contradict any existing formal definition in another layer?
2. **Downstream impact check**: If this change is made, which other pages, categories, or definitions must be updated to remain consistent?
3. **Claims check**: Does the proposed change introduce any claim that is not structurally supported by the existing ontology or evidence base?
4. **Append-only check**: Does the proposed change attempt to silently remove or rewrite an existing established entry? If so, it must follow the deprecation process in `docs/APPEND_ONLY_POLICY.md` instead.

A change that fails any of these checks must be revised before proceeding.

---

### Stage 3: Validation

**Required for:** All changes that affect public-facing HTML, ontology data files, or sitemap.

Before a change is published, it must pass the full quality gate:

```bash
cd scripts && python quality_gate.py
```

The quality gate runs:
- `generate_pages.py` — regenerates all declared pages from the data layer
- `generate_sitemap.py` — regenerates sitemap.xml
- `validate_content.py` — validates all rendered HTML pages

Additionally:
- `python check_markdown_links.py` — validates relative links in all markdown files
- `python sovereign_standards_guard.py` — validates required governance document presence
- `python governance_guard.py` — validates that governance-critical file changes are accompanied by a decision log entry

All scripts must exit zero. Any failure is a blocking issue.

---

### Stage 4: Decision Log

**Required for:** All doctrine-level and major changes, and any change to governance-critical files as defined in `governance_guard.py`.

Entry format in `docs/DECISION_LOG.md`:

```text
## [Date] — [Layer] [Version increment if applicable]

**Change:** [What changed]
**Rationale:** [Why it was necessary]
**Downstream effects:** [What else was updated as a result]
**Approved by:** [Role or person]
```

The decision log is append-only. Existing entries must not be edited or removed after the change is published.

---

### Stage 5: Publication

Publication means merging the change to the `main` branch via the governed workflow. The Sovereign Pages Deploy workflow runs on push to `main` and executes the full quality gate in CI before deploying.

A change is not published until it has passed CI. A CI failure after the change is merged is a blocking incident requiring immediate remediation.

For major and doctrine-level changes, the publication step must also:
- Archive the previous version of any versioned artifact (standard, protocol version)
- Update any internal cross-references that cite the modified layer by version number

---

### Stage 6: Post-Publication Verification

After a change is live, verify:

1. **Canonical URL resolution**: The affected page is accessible at its declared canonical URL
2. **Sitemap inclusion**: The affected page appears in `sitemap.xml` with the correct canonical
3. **Internal link integrity**: No pages in the system now have broken links to the changed content
4. **Metadata accuracy**: The page's title, description, and H1 accurately reflect the updated content
5. **Cross-reference accuracy**: Any page that links to the changed content still links correctly

If the change involved a rename or deprecation, also verify that the deprecated term's page (or deprecation notice) is live and accessible at the old URL or is correctly redirected.

Post-publication verification does not need to be a formal report. It is a checklist check against the above points. Issues found during post-publication verification are treated as bugs and corrected immediately.

---

## Emergency Changes

A change required to correct a live error — broken link, incorrect metadata, failed validation — may skip Stage 1 (proposal) and Stage 2 (review) and proceed directly to Stage 3 (validation). The rationale must still be documented in Stage 4 (decision log), noting that the change was made as an emergency correction.

Emergency changes do not bypass the CI quality gate.

---

## Changes That Cannot Be Made

The following are unconditionally blocked and cannot proceed through any change control path:

- Direct edits to generated HTML files for content that must be changed in the data layer
- Silent removal of established ontology terms or registry entries (must use the deprecation process)
- Modifications to published standard or protocol versions (must use the archive-and-supersede process)
- Changes to `scripts/quality_gate.py` or `scripts/validate_content.py` that weaken validation rules without a documented rationale and decision log entry
- Publishing a page that fails validation
