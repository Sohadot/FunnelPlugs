# Category Intelligence Architecture

## FunnelPlugs as a Category Intelligence Factory

FunnelPlugs is not a collection of articles about conversion rate optimization. It is a governed intelligence factory for the category of structural funnel failure.

The distinction matters. A content site produces pages. A category intelligence factory produces a governed system of named types, formal definitions, classification criteria, diagnostic methods, and reference-grade output that practitioners, systems, and future agents can rely on without verification overhead.

Concretely: FunnelPlugs converts structured commercial-path concepts into governed diagnostic intelligence. Given a commercial path exhibiting observable failure signals, the system provides a structural failure classification, an intervention class, and a diagnostic rationale — grounded in the ontology, evaluated against the integrity standard, processed through the protocol, and surfaced via the engine and reference layer.

This is not the same thing as producing CRO tips, generic funnel advice, or AI-generated marketing recommendations. It is the production of governed intelligence at the category level.

---

## The Intelligence Production Chain

The Funnelplugs system is an ordered chain. Each layer receives its inputs from the layer above it and produces outputs for the layer below. The chain does not work if layers are missing, inconsistent, or ungoverned.

### Manifesto

The manifesto defines why the system exists. It establishes the foundational position: revenue is often lost not because traffic is absent, but because the commercial path is structurally incomplete. This is the governing claim. All downstream layers exist to operationalize it.

The manifesto is not a marketing document. It is a commitment to a structural interpretation of commercial failure. Everything the system subsequently produces must be consistent with this position.

### Doctrine

Doctrine is the conceptual elaboration of the manifesto's position. It defines what structural funnel failure is, why it is treated as a classification problem rather than a performance problem, and why the system's approach — naming failure types, defining intervention classes, evaluating against formal integrity conditions — produces more durable diagnostic value than performance-metric interpretation.

Doctrine is preserved in `docs/FOUNDATION_DOCTRINE.md` and the manifesto layer.

### Governance

Governance controls how the system changes. It defines who can authorize changes to which layers, what change categories exist, what documentation is required, and how the historical record is preserved. Without governance, the system's definitions would drift, its terminology would become unstable, and its diagnostic output would lose reliability.

Governance is the meta-layer that makes all other layers trustworthy over time. A category intelligence factory without governance is not a factory — it is a blog with unusually structured posts.

Governance is defined in `docs/GOVERNANCE_CHARTER.md`, `docs/CHANGE_CONTROL.md`, `docs/VERSIONING_POLICY.md`, and `docs/APPEND_ONLY_POLICY.md`.

### Ontology

The ontology defines the failure language. It is the controlled vocabulary of the system: the formal names, identifiers, and definitions for every structural failure type and intervention class the system recognizes. The ontology is what makes Funnelplugs a classification system rather than an opinion platform.

Ontology changes propagate to every downstream layer. A new failure type added to the ontology requires a corresponding entry in the registry, a reference page, and integration into the protocol and engine. Removing or redefining an ontology term requires the deprecation process defined in the append-only policy.

The ontology is governed by `data/leak_taxonomy.json` and `data/plug_taxonomy.json`.

### Standard

The standard defines the integrity conditions. It is the formal specification of what a structurally complete and conversion-capable commercial path requires across its integrity dimensions: trust integrity, flow continuity, and recovery readiness.

The standard is what the protocol evaluates against. Without the standard, the protocol cannot produce objective classifications — it can only produce impressions. The standard converts subjective path evaluation into structured pass/fail determination.

### Protocol

The protocol defines the diagnostic method. It specifies how to apply the standard against an observable commercial path: how to detect the presence of structural failure, how to classify the failure type against the ontology, and how to assign the correct intervention class from the registry.

The protocol is the bridge between the conceptual layers (manifesto, doctrine, ontology, standard) and the operational layers (registry, engine, reference). It is the governing logic that connects what the system knows to what the system produces.

### Registry

The registry defines the intervention classes. Each registry entry corresponds to an ontology-defined failure type and specifies the class of intervention required to restore structural integrity.

The registry does not recommend specific software products. It defines structural categories: what kind of mechanism must be present, what its function must be, and what the integrity condition it restores looks like when correctly met. This abstraction is intentional — it preserves the system's neutrality and diagnostic value across changing product landscapes.

Registry entries are append-only. Established categories cannot be silently removed or redefined.

### Engine

The engine operationalizes the system. It receives a structured diagnostic input — signals from a practitioner evaluating a real commercial path — and produces a governed output: the failure classifications present, their integrity dimension assignments, the intervention classes required, and a priority ordering for remediation.

The engine does not produce revenue forecasts, conversion-lift projections, or ROI estimates. It produces structural diagnostic output — governed, reproducible, and grounded in the ontology and standard. This constraint is intentional. Financial projections require assumptions the system cannot make without access to the practitioner's specific context. Structural classifications can be made from observable path properties alone.

The engine is implemented in `assets/js/engine.js` and governed by `data/scoring_rules.json` and `data/decision_logic.json`.

### Reference

The reference layer preserves discoverability, internal memory, and concept navigation. It materializes the ontology and registry as individually addressable, canonically identified, internally linked pages — each covering one failure class, one intervention class, or one conceptual paper.

The reference layer serves three audiences simultaneously: human practitioners navigating the system, search engines indexing the category, and future AI agents or automated systems that need to retrieve governed definitions without parsing unstructured prose.

A well-built reference layer is the system's long-term footprint in the category. It creates the internal link graph that signal to indexing systems — human or machine — that the system has depth, structure, and discoverability at the concept level.

---

## What FunnelPlugs Produces

### Intelligence outputs the system produces

- **Governed failure language**: Precise, stable names for structural failure types that practitioners can rely on across time and context
- **Structural classifications**: Assignment of observable path failure signals to formal failure classes with defined membership criteria
- **Integrity dimensions**: Evaluation of commercial paths against the formal integrity standard's trust, flow, and recovery conditions
- **Diagnostic mappings**: Correspondence between observed failure signals and required intervention classes, mediated by the protocol
- **Intervention class references**: Registry-governed definitions of what must be structurally present to address each failure type
- **Reference-grade explanations**: Individually addressable, canonically identified concept pages that serve as stable reference points
- **Audit-ready conceptual output**: Structured diagnostic results that a practitioner can incorporate into a client audit without translating from informal advice

### What the system does not produce

- **Revenue forecasts**: The system does not predict what fixing a structural failure will do to revenue. That depends on execution quality, market conditions, and factors outside structural classification.
- **ROI guarantees**: No return on investment can be stated without knowledge of the cost of intervention and the specific revenue uplift in the practitioner's context.
- **Conversion-lift promises**: The system classifies what is missing. What happens when what is missing is supplied depends on variables the system does not observe.
- **Black-box decisions**: Every diagnostic output is grounded in a visible chain: signal → failure class → ontology → intervention class → registry. The reasoning is auditable.
- **Vendor-biased recommendations**: The system recommends intervention classes, not products. Vendor-specific recommendations would compromise the system's structural neutrality.
- **Unsupported benchmark claims**: The system does not state that average commercial paths of a given type convert at a specific rate. Such claims require empirical evidence the system does not gather.

---

## Why This Architecture Matters in the AI Era

As commercial systems become more automated, agentic, and AI-assisted, the need for stable diagnostic language increases — not decreases.

When an AI system assists a practitioner in evaluating a commercial path, it needs concepts to work with. If the vocabulary for structural failure is unstable — if "trust collapse" means something different in one context than another, if the definition of "flow break" has been informally modified without documentation — the AI system cannot produce reliable diagnostic assistance. It will either work with inconsistent input or produce inconsistent output.

Funnelplugs positions itself as the governed vocabulary layer for structural funnel failure. The value of this position grows as more systems — human and automated — need to reason about commercial path integrity using structured concepts rather than informal heuristics.

Concretely, the architecture is designed to be readable by:

**Human practitioners**: Navigating concepts, applying the protocol, reading failure class definitions, interpreting engine output. The interface and reference layer serve this audience.

**Search engines**: Indexing the category through stable canonical URLs, structured internal link graphs, individually addressed concept pages, and consistent metadata. The SEO policy and sitemap governance serve this audience.

**Future AI agents**: Retrieving governed definitions, following internal links to related concepts, building structured knowledge about the category from a stable, versioned reference layer. The reference architecture, ontology data structure, and canonical URL scheme serve this audience.

**Strategic buyers**: Evaluating the asset's position in the category, the depth of its reference layer, the defensibility of its classification system, the quality of its interface, and the governance that makes all of these durable. The entire architecture serves this audience.

**Internal governance validators**: Running the quality gate, verifying structural integrity, checking that all declared pages exist, all links resolve, all metadata is complete, and no unsupported claims are present. The build pipeline serves this audience.

This multi-audience readability is not accidental. It is a design requirement. An asset that is legible to only one of these audiences is incomplete. An asset that is legible to all five is a category infrastructure component.

---

## Buyer Logic

A strategic buyer evaluating FunnelPlugs should see a category infrastructure asset, not a content site. The following components constitute the buyer's case.

### Domain name

`funnelplugs.com` names the category concept directly. The domain is the first signal that this asset has a structural claim to the vocabulary of the domain.

### Category language

The governed vocabulary — leak classes, plug classes, integrity dimensions, protocol stages, intervention categories — is a language asset. A buyer who acquires Funnelplugs acquires the definitional authority over how structural funnel failure is named and classified within the system.

### Ontology

The formal ontology (leak taxonomy, plug taxonomy) is a machine-readable, versioned knowledge asset. It can be extended, licensed, or integrated into downstream systems. Its value increases as more practitioners and systems adopt its vocabulary.

### Standard

The Funnel Integrity Standard is a formal specification asset. It defines the evaluation criteria for commercial path integrity. As the category develops, the standard becomes the benchmark that other tools and practitioners either adopt or position against.

### Protocol

The protocol is the methodological asset. It defines the diagnostic process in a form that is teachable, auditable, and systematizable. A buyer can operationalize the protocol into their own diagnostic offering with a clear reference point.

### Diagnostic engine

The engine is the interactive utility layer. It converts the system's conceptual architecture into a practitioner-facing diagnostic interface. Its output is governed by the ontology and standard — not by heuristics or generic scoring. This makes the engine's output more defensible than comparable tools.

### Governance

The governance layer (charter, change control, versioning policy, append-only policy) is the infrastructure that makes every other asset durable. A buyer acquires not just current content but a governed system for producing future content without quality degradation.

### Reference footprint

The reference layer's individual concept pages create a compounding footprint in the category. Each page, properly indexed and linked, contributes to the system's discoverability and authority. This footprint grows with time and is difficult to replicate quickly.

### Interface thesis

The interface communicates institutional weight before a word is read. A well-governed interface signals that the underlying system is serious. This reduces the buyer's integration cost — the asset fits within an institutional portfolio without requiring interface rehabilitation.

### Future report and API potential

The architecture supports extensions: structured diagnostic reports, API access to the ontology and classification layer, agent-readable output endpoints. These are not implemented — they are possible because the underlying architecture is structured, versioned, and governed. A buyer does not need to rebuild the foundation to add these extensions.

---

## Architectural Integrity Requirements

For FunnelPlugs to function as a category intelligence factory, the following architectural conditions must be maintained:

1. **Stable canonical URLs**: Every concept page must be reachable at a predictable, permanent URL. URL changes break links and degrade the reference footprint.
2. **Clear titles and descriptions**: Every page must have a precise, non-generic title and description that accurately identifies the concept it covers.
3. **Internally linked concepts**: Failure class pages link to their intervention class counterparts. Protocol links to standard. Standard links to registry. The internal link graph is the system's navigational memory.
4. **Versioned reference layers**: Changes to definitions are versioned and documented. The historical record is preserved.
5. **No thin pages**: Every page must have substantive content that justifies its existence in the reference layer.
6. **No broken links**: A broken link in the reference layer is a gap in the system's navigational memory.
7. **Restrained claims**: Claims within the system are structural and diagnostic. Financial, ROI, or conversion-lift claims are unconditionally prohibited.
8. **Structured conceptual relationships**: The relationships between failure classes, intervention classes, integrity dimensions, and protocol stages must be explicitly represented in the data layer — not just implied in prose.
