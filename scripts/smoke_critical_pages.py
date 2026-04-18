"""Automated smoke checks for critical rendered pages (post-build)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "reference.html", "engine.html", "registry.html")


def main() -> int:
    failed = False
    for name in PAGES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        issues: list[str] = []
        if 'id="primary-navigation"' not in text:
            issues.append("nav")
        if 'rel="canonical"' not in text:
            issues.append("canonical")
        if "GTM-56J99S4F" not in text:
            issues.append("gtm")
        if "googletagmanager.com/ns.html?id=GTM-56J99S4F" not in text:
            issues.append("gtm-noscript")
        if "<main" not in text:
            issues.append("main")
        if len(text.strip()) < 500:
            issues.append("too-short")
        if issues:
            failed = True
            print(f"[SMOKE_FAIL] {name}: {', '.join(issues)}")
        else:
            print(f"[SMOKE_OK]   {name}")
    if failed:
        print("[SMOKE_BLOCKED] Critical page smoke checks failed.")
        return 1
    print("[SMOKE_PASSED] Critical page smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
