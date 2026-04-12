from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from config import get_config
from site_data_loader import SiteDataLoadError, load_site_data as load_site_bundle


CONFIG = get_config()
ROOT_DIR = CONFIG.paths.root
DATA_DIR = CONFIG.paths.data_dir
TEMPLATES_DIR = CONFIG.paths.templates_dir
ASSETS_DIR = CONFIG.paths.assets_dir
DOCS_DIR = CONFIG.paths.docs_dir
SCRIPTS_DIR = CONFIG.paths.scripts_dir
OUTPUT_DIR = CONFIG.paths.output_dir

SITE_DATA_FILE = DATA_DIR / "site.json"
SITEMAP_FILE = OUTPUT_DIR / CONFIG.seo.sitemap_filename
ROBOTS_FILE = OUTPUT_DIR / "robots.txt"
FAVICON_FILE = OUTPUT_DIR / "favicon.ico"

REQUIRED_SCRIPT_FILES = (
    "config.py",
    "site_data_loader.py",
    "generate_pages.py",
    "generate_sitemap.py",
    "validate_content.py",
    "quality_gate.py",
)

REQUIRED_TEMPLATE_FILES = (
    "base.html",
    "page.html",
)

REQUIRED_DOC_FILES = (
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
)

REQUIRED_ASSET_FILES = (
    "assets/css/main.css",
    "assets/js/main.js",
)

XML_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@dataclass
class GateIssue:
    severity: str  # ERROR | WARNING
    scope: str
    message: str


@dataclass
class GateResult:
    issues: list[GateIssue] = field(default_factory=list)

    def add_error(self, scope: str, message: str) -> None:
        self.issues.append(GateIssue("ERROR", scope, message))

    def add_warning(self, scope: str, message: str) -> None:
        self.issues.append(GateIssue("WARNING", scope, message))

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "ERROR" for issue in self.issues)

    def print(self) -> None:
        errors = [issue for issue in self.issues if issue.severity == "ERROR"]
        warnings = [issue for issue in self.issues if issue.severity == "WARNING"]

        if errors:
            print("Blocking quality gate issues:")
            for issue in errors:
                print(f"  [ERROR] {issue.scope} :: {issue.message}")

        if warnings:
            print("Non-blocking quality gate warnings:")
            for issue in warnings:
                print(f"  [WARNING] {issue.scope} :: {issue.message}")

        if not self.issues:
            print("Quality gate completed successfully with no issues.")


class QualityGateError(Exception):
    """Raised when the sovereign quality gate cannot continue safely."""


def load_site_data() -> dict[str, Any]:
    """Load the sovereign site data source."""
    try:
        return load_site_bundle()
    except SiteDataLoadError as exc:
        raise QualityGateError(str(exc)) from exc


def require_foundation_inputs(result: GateResult, site_data: dict[str, Any]) -> None:
    """Check that the required foundation inputs exist before deeper validation."""
    if not DATA_DIR.exists():
        result.add_error("foundation", f"Missing data directory: {DATA_DIR}")
    if not TEMPLATES_DIR.exists():
        result.add_error("foundation", f"Missing templates directory: {TEMPLATES_DIR}")
    if not SCRIPTS_DIR.exists():
        result.add_error("foundation", f"Missing scripts directory: {SCRIPTS_DIR}")
    if not ASSETS_DIR.exists():
        result.add_error("foundation", f"Missing assets directory: {ASSETS_DIR}")

    for filename in REQUIRED_SCRIPT_FILES:
        path = SCRIPTS_DIR / filename
        if not path.exists():
            result.add_error("scripts", f"Missing required script file: {path.relative_to(ROOT_DIR)}")

    for filename in REQUIRED_TEMPLATE_FILES:
        path = TEMPLATES_DIR / filename
        if not path.exists():
            result.add_error("templates", f"Missing required template file: {path.relative_to(ROOT_DIR)}")

    for relative in REQUIRED_ASSET_FILES:
        path = ROOT_DIR / relative
        if not path.exists():
            result.add_error("assets", f"Missing required asset file: {path.relative_to(ROOT_DIR)}")

    if not DOCS_DIR.exists():
        result.add_error("docs", f"Missing required docs directory: {DOCS_DIR.relative_to(ROOT_DIR)}")
    else:
        for filename in REQUIRED_DOC_FILES:
            path = DOCS_DIR / filename
            if not path.exists():
                result.add_error("docs", f"Missing required governance file: {path.relative_to(ROOT_DIR)}")

    validate_site_declared_assets(site_data, result)


def validate_site_declared_assets(site_data: dict[str, Any], result: GateResult) -> None:
    """Ensure asset paths declared in site.json exist where required."""
    seo = site_data.get("seo", {})
    organization = site_data.get("organization", {})

    default_og = str(seo.get("default_og_image", "")).strip()
    if default_og:
        path = resolve_root_relative_asset(default_og)
        if not path.exists():
            result.add_error("site.json:seo.default_og_image", f"Declared OG image missing: {path.relative_to(ROOT_DIR)}")

    logo = str(organization.get("logo", "")).strip()
    if logo:
        path = resolve_root_relative_asset(logo)
        if not path.exists():
            result.add_error("site.json:organization.logo", f"Declared logo asset missing: {path.relative_to(ROOT_DIR)}")


def resolve_root_relative_asset(asset_path: str) -> Path:
    """Resolve a root-relative asset path safely under the sovereign root."""
    normalized = asset_path.lstrip("/")
    resolved = (ROOT_DIR / normalized).resolve()

    try:
        resolved.relative_to(ROOT_DIR.resolve())
    except ValueError as exc:
        raise QualityGateError(f"Asset path escapes the sovereign root: {asset_path}") from exc

    return resolved


def run_subprocess(script_name: str) -> None:
    """Run a required validation/build script and fail loudly if it exits non-zero."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        raise QualityGateError(f"Cannot run missing script: {script_path}")

    print(f"[QUALITY_GATE] Running {script_name} ...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        check=False,
        text=True,
    )

    if result.returncode != 0:
        raise QualityGateError(f"Script failed during quality gate: {script_name}")


def ensure_live_outputs_exist(result: GateResult, site_data: dict[str, Any]) -> None:
    """Ensure required live outputs exist after generation."""
    for filename in CONFIG.pages.required_core_pages:
        path = OUTPUT_DIR / filename
        if not path.exists():
            result.add_error("live-output", f"Missing required core page: {path.relative_to(ROOT_DIR)}")

    if not SITEMAP_FILE.exists():
        result.add_error("live-output", f"Missing generated sitemap: {SITEMAP_FILE.relative_to(ROOT_DIR)}")

    if not ROBOTS_FILE.exists():
        result.add_warning("live-output", f"robots.txt is missing at root: {ROBOTS_FILE.relative_to(ROOT_DIR)}")

    if not FAVICON_FILE.exists():
        result.add_warning("live-output", f"favicon.ico is missing at root: {FAVICON_FILE.relative_to(ROOT_DIR)}")

    for page in site_data.get("core_pages", []):
        file_value = str(page.get("file", "")).strip()
        if not file_value:
            continue
        path = OUTPUT_DIR / file_value
        if not path.exists():
            result.add_error("live-output", f"Declared page missing after generation: {path.relative_to(ROOT_DIR)}")


def validate_sitemap_integrity(site_data: dict[str, Any], result: GateResult) -> None:
    """Parse sitemap.xml and ensure it reflects the sovereign live root correctly."""
    if not SITEMAP_FILE.exists():
        result.add_error("sitemap", "sitemap.xml does not exist.")
        return

    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
    except ET.ParseError as exc:
        result.add_error("sitemap", f"Invalid XML in sitemap.xml: {exc}")
        return

    url_nodes = root.findall("sm:url", XML_NS)
    if not url_nodes:
        result.add_error("sitemap", "sitemap.xml contains no <url> entries.")
        return

    locs: list[str] = []
    for node in url_nodes:
        loc = node.findtext("sm:loc", default="", namespaces=XML_NS).strip()
        lastmod = node.findtext("sm:lastmod", default="", namespaces=XML_NS).strip()

        if not loc:
            result.add_error("sitemap", "A sitemap entry is missing <loc>.")
            continue

        if not loc.startswith(CONFIG.site.canonical_url.rstrip("/")):
            result.add_error("sitemap", f"Sitemap loc escapes the sovereign domain: {loc}")

        if CONFIG.seo.enforce_lastmod and not lastmod:
            result.add_error("sitemap", f"Sitemap entry is missing lastmod: {loc}")

        locs.append(loc)

    expected_canonicals = {
        str(page.get("canonical", "")).strip()
        for page in site_data.get("core_pages", [])
        if page.get("indexable") is True
    }

    for canonical in sorted(expected_canonicals):
        if canonical and canonical not in locs:
            result.add_error("sitemap", f"Declared indexable page missing from sitemap: {canonical}")

    if len(locs) != len(set(locs)):
        result.add_error("sitemap", "Duplicate loc entries detected in sitemap.xml.")


def validate_root_integrity(site_data: dict[str, Any], result: GateResult) -> None:
    """Perform final sovereign root checks after generation and validation scripts."""
    for page in site_data.get("core_pages", []):
        file_value = str(page.get("file", "")).strip()
        if not file_value:
            continue

        path = OUTPUT_DIR / file_value
        if not path.exists():
            continue

        html = path.read_text(encoding="utf-8")

        if "{{" in html or "{%" in html or "{#" in html:
            result.add_error(
                "render",
                f"Unresolved template syntax found in rendered file: {path.relative_to(ROOT_DIR)}",
            )

        if "structured page shell active" in html.lower():
            result.add_error(
                "render",
                f"Rendered page still contains shell fallback language: {path.relative_to(ROOT_DIR)}",
            )

        if "ready to receive validated structured content" in html.lower():
            result.add_error(
                "render",
                f"Rendered page still contains placeholder shell messaging: {path.relative_to(ROOT_DIR)}",
            )


def run_quality_gate() -> int:
    """Run the sovereign quality gate and return an exit status code."""
    result = GateResult()

    try:
        site_data = load_site_data()
    except QualityGateError as exc:
        print(f"[QUALITY_GATE_ERROR] {exc}")
        return 1

    require_foundation_inputs(result, site_data)
    if result.has_errors:
        result.print()
        return 1

    try:
        run_subprocess("generate_pages.py")
        run_subprocess("generate_sitemap.py")
        run_subprocess("validate_content.py")
    except QualityGateError as exc:
        print(f"[QUALITY_GATE_ERROR] {exc}")
        return 1

    ensure_live_outputs_exist(result, site_data)
    validate_sitemap_integrity(site_data, result)
    validate_root_integrity(site_data, result)

    result.print()

    if result.has_errors:
        print("[QUALITY_GATE_BLOCKED] Deployment permission denied.")
        return 1

    print("[QUALITY_GATE_PASSED] Deployment permission granted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_quality_gate())
