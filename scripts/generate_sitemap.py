from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from config import get_config


class SitemapError(Exception):
    """Raised when sitemap generation detects a blocking structural issue."""


CONFIG = get_config()
ROOT_DIR = CONFIG.paths.root
DATA_DIR = CONFIG.paths.data_dir
OUTPUT_DIR = CONFIG.paths.output_dir
SITE_DATA_FILE = DATA_DIR / "site.json"
SITEMAP_OUTPUT = OUTPUT_DIR / CONFIG.seo.sitemap_filename

FORBIDDEN_SCAN_SEGMENTS = {
    "assets",
    "data",
    "docs",
    "scripts",
    "templates",
    ".github",
    "__pycache__",
}

REQUIRED_META_PATTERNS = {
    "title": re.compile(r"<title>.+?</title>", re.IGNORECASE | re.DOTALL),
    "canonical": re.compile(
        r'<link\s+rel="canonical"\s+href="([^"]+)"',
        re.IGNORECASE,
    ),
    "robots": re.compile(
        r'<meta\s+name="robots"\s+content="([^"]+)"',
        re.IGNORECASE,
    ),
}

TITLE_EXTRACT_PATTERN = re.compile(r"<title>(.+?)</title>", re.IGNORECASE | re.DOTALL)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"lorem ipsum", re.IGNORECASE),
    re.compile(r"structured page shell active", re.IGNORECASE),
    re.compile(r"ready to receive validated structured content", re.IGNORECASE),
)

CANONICAL_ROOT = CONFIG.site.canonical_url.rstrip("/")


def load_site_data() -> dict[str, Any]:
    """Load the sovereign site data source."""
    if not SITE_DATA_FILE.exists():
        raise SitemapError(f"Missing required data file: {SITE_DATA_FILE}")

    try:
        data = json.loads(SITE_DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SitemapError(f"Invalid JSON in {SITE_DATA_FILE}: {exc}") from exc

    if not isinstance(data, dict):
        raise SitemapError("site.json must contain a top-level JSON object.")

    if "core_pages" not in data or not isinstance(data["core_pages"], list):
        raise SitemapError("site.json must define a 'core_pages' array.")

    return data


def declared_pages_by_file(site_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map declared core pages by their output file names."""
    mapping: dict[str, dict[str, Any]] = {}
    for page in site_data["core_pages"]:
        if not isinstance(page, dict):
            raise SitemapError("Each item in core_pages must be an object.")
        file_value = str(page.get("file", "")).strip()
        if not file_value:
            raise SitemapError("A declared core page is missing its 'file' field.")
        if file_value in mapping:
            raise SitemapError(f"Duplicate declared page file in site.json: '{file_value}'")
        mapping[file_value] = page
    return mapping


def ensure_required_core_pages_exist() -> None:
    """Ensure the required core output pages are present before sitemap generation."""
    missing = []
    for filename in CONFIG.pages.required_core_pages:
        if not (OUTPUT_DIR / filename).exists():
            missing.append(filename)

    if missing:
        raise SitemapError(
            f"Required core pages are missing from the live root output: {missing}"
        )


def iter_live_html_files() -> list[Path]:
    """Return all live candidate HTML files under the root output structure."""
    html_files: list[Path] = []

    for path in OUTPUT_DIR.rglob("*.html"):
        relative = path.relative_to(OUTPUT_DIR)

        if is_in_forbidden_area(relative):
            continue

        if any(part.startswith(".") for part in relative.parts):
            continue

        html_files.append(path)

    if not html_files:
        raise SitemapError("No live HTML files were found for sitemap generation.")

    return sorted(html_files, key=lambda p: p.relative_to(OUTPUT_DIR).as_posix())


def is_in_forbidden_area(relative_path: Path) -> bool:
    """Block scanning of internal or non-public directories."""
    return any(part in FORBIDDEN_SCAN_SEGMENTS for part in relative_path.parts)


def extract_page_metadata(html: str, source: Path) -> dict[str, str]:
    """Extract and validate key metadata directly from rendered HTML."""
    title_match = TITLE_EXTRACT_PATTERN.search(html)
    canonical_match = REQUIRED_META_PATTERNS["canonical"].search(html)
    robots_match = REQUIRED_META_PATTERNS["robots"].search(html)

    if not title_match:
        raise SitemapError(f"Missing <title> in rendered page: {source.relative_to(ROOT_DIR)}")
    if not canonical_match:
        raise SitemapError(
            f"Missing canonical link in rendered page: {source.relative_to(ROOT_DIR)}"
        )

    title = normalize_whitespace(title_match.group(1))
    canonical = canonical_match.group(1).strip()
    robots = normalize_whitespace(robots_match.group(1)) if robots_match else CONFIG.seo.robots_default

    if not title:
        raise SitemapError(f"Empty title detected in rendered page: {source.relative_to(ROOT_DIR)}")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(title):
            raise SitemapError(
                f"Placeholder or weak title detected in rendered page: {source.relative_to(ROOT_DIR)}"
            )

    return {
        "title": title,
        "canonical": canonical,
        "robots": robots,
    }


def normalize_whitespace(value: str) -> str:
    """Normalize whitespace for comparison and validation."""
    return " ".join(value.split())


def validate_live_page(
    file_path: Path,
    metadata: dict[str, str],
    declared_page: dict[str, Any] | None,
) -> bool:
    """
    Validate a rendered page for sitemap inclusion.

    Returns True if the page is indexable and should be included.
    Returns False if the page is intentionally non-indexable.
    """
    relative = file_path.relative_to(OUTPUT_DIR).as_posix()
    canonical = metadata["canonical"]
    robots = metadata["robots"].lower()

    if not canonical.startswith("https://"):
        raise SitemapError(f"Canonical must use HTTPS: {relative}")

    if not canonical.startswith(CANONICAL_ROOT):
        raise SitemapError(
            f"Canonical points outside the sovereign root for '{relative}': {canonical}"
        )

    if declared_page:
        declared_canonical = str(declared_page.get("canonical", "")).strip()
        if declared_canonical and declared_canonical != canonical:
            raise SitemapError(
                f"Canonical mismatch for '{relative}'. "
                f"Rendered='{canonical}' Declared='{declared_canonical}'"
            )

    if "noindex" in robots:
        return False

    if declared_page is not None:
        declared_indexable = declared_page.get("indexable")
        if declared_indexable is not True:
            raise SitemapError(
                f"Declared core page '{relative}' is not indexable but rendered robots does not mark it noindex."
            )

    return True


def build_url_entry(file_path: Path, canonical: str) -> dict[str, str]:
    """Build a single sitemap URL entry using the live file state."""
    stat = file_path.stat()
    lastmod = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).date().isoformat()

    return {
        "loc": canonical,
        "lastmod": lastmod,
        "file": file_path.relative_to(OUTPUT_DIR).as_posix(),
    }


def sort_entries(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    """Sort entries with required core pages first, then all others."""
    core_order = {name: index for index, name in enumerate(CONFIG.pages.required_core_pages)}

    def sort_key(entry: dict[str, str]) -> tuple[int, str]:
        file_name = entry["file"]
        priority = core_order.get(file_name, 10_000)
        return (priority, file_name)

    return sorted(entries, key=sort_key)


def render_sitemap_xml(entries: list[dict[str, str]]) -> str:
    """Render the sitemap XML in a clean, deterministic format."""
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for entry in entries:
        url_el = SubElement(urlset, "url")
        loc_el = SubElement(url_el, "loc")
        loc_el.text = entry["loc"]

        if CONFIG.seo.enforce_lastmod:
            lastmod_el = SubElement(url_el, "lastmod")
            lastmod_el.text = entry["lastmod"]

    rough_xml = tostring(urlset, encoding="utf-8")
    pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ", encoding="utf-8")
    return pretty_xml.decode("utf-8")


def write_sitemap(xml_content: str) -> None:
    """Write sitemap.xml to the sovereign root output."""
    SITEMAP_OUTPUT.write_text(xml_content, encoding="utf-8", newline="\n")


def main() -> None:
    """Run the sovereign sitemap generation pipeline."""
    site_data = load_site_data()
    declared_pages = declared_pages_by_file(site_data)

    ensure_required_core_pages_exist()

    entries: list[dict[str, str]] = []
    html_files = iter_live_html_files()

    for file_path in html_files:
        html = file_path.read_text(encoding="utf-8")
        metadata = extract_page_metadata(html, file_path)

        declared = declared_pages.get(file_path.relative_to(OUTPUT_DIR).as_posix())
        should_include = validate_live_page(file_path, metadata, declared)

        if not should_include:
            continue

        entries.append(build_url_entry(file_path, metadata["canonical"]))

    if not entries:
        raise SitemapError("No valid indexable pages qualified for sitemap inclusion.")

    entries = sort_entries(entries)
    xml_content = render_sitemap_xml(entries)
    write_sitemap(xml_content)

    print("Sovereign sitemap generation completed successfully.")
    print(f"  - {SITEMAP_OUTPUT.relative_to(ROOT_DIR)}")
    print(f"  - Included URLs: {len(entries)}")


if __name__ == "__main__":
    try:
        main()
    except SitemapError as exc:
        raise SystemExit(f"[GENERATE_SITEMAP_ERROR] {exc}") from exc
