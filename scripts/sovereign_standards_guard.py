from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_DOCS = (
    "FOUNDATION_DOCTRINE.md",
    "PROJECT_DOCTRINE.md",
    "ARCHITECTURE.md",
    "SEO_POLICY.md",
    "SITEMAP_POLICY.md",
    "QUALITY_GATE.md",
    "SECURITY_POLICY.md",
    "DECISION_LOG.md",
    "MONETIZATION_PRINCIPLES.md",
    "CHANGELOG.md",
    "ASSET_THESIS.md",
    "DESIGN_RATIONALE.md",
    "THREAT_MODEL.md",
    "INCIDENT_RESPONSE.md",
    "PUBLICATION_GATE_CHECKLIST.md",
)

REQUIRED_CHECKLIST_LINES = (
    "Structural Stability",
    "Conceptual Integrity",
    "Authority Readiness",
    "Revenue Compatibility",
    "Anti-Mobility Discipline",
)


def main() -> int:
    issues: list[str] = []

    if not DOCS.exists():
        print("[SOVEREIGN_STANDARDS_BLOCKED] Missing docs directory.")
        return 1

    for filename in REQUIRED_DOCS:
        path = DOCS / filename
        if not path.exists():
            issues.append(f"Missing required governance document: docs/{filename}")

    checklist = DOCS / "PUBLICATION_GATE_CHECKLIST.md"
    if checklist.exists():
        content = checklist.read_text(encoding="utf-8")
        for line in REQUIRED_CHECKLIST_LINES:
            if line not in content:
                issues.append(
                    "Publication gate checklist missing required line: "
                    + line
                )

    if issues:
        print("[SOVEREIGN_STANDARDS_BLOCKED] Strict standards check failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[SOVEREIGN_STANDARDS_PASSED] Strict standards baseline is complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
