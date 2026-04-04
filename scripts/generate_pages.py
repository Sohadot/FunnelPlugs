from __future__ import annotations
from html import unescape

import json
import re
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
except ImportError as exc:
    raise SystemExit(
        "Jinja2 is required for generate_pages.py. "
        "Install it locally before running the build workflow."
    ) from exc

from config import get_config


class GenerationError(Exception):
    """Raised when the sovereign page generation pipeline detects a blocking issue."""


CONFIG = get_config()
ROOT_DIR = CONFIG.paths.root
DATA_DIR = CONFIG.paths.data_dir
TEMPLATES_DIR = CONFIG.paths.templates_dir
OUTPUT_DIR = CONFIG.paths.output_dir

SITE_DATA_FILE = DATA_DIR / "site.json"

REQUIRED_TOP_LEVEL_KEYS = (
    "site",
    "brand",
    "seo",
    "navigation",
    "core_pages",
)

REQUIRED_PAGE_KEYS = (
    "key",
    "file",
    "title",
    "description",
    "template",
    "page_type",
    "indexable",
    "canonical",
)

FORBIDDEN_OUTPUT_SEGMENTS = {
    "scripts",
    "templates",
    "data",
    "docs",
    ".github",
    "__pycache__",
}

FORBIDDEN_CONTENT_PATTERNS = (
    re.compile(r"<\s*script\b", re.IGNORECASE),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"\bon\w+\s*=", re.IGNORECASE),
    re.compile(r"<\s*iframe\b", re.IGNORECASE),
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"lorem ipsum", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
)

TITLE_PATTERN = re.compile(r"<title>(.+?)</title>", re.IGNORECASE | re.DOTALL)

DESCRIPTION_PATTERN = re.compile(
    r'<meta\s+name="description"\s+content="([^"]+)"',
    re.IGNORECASE,
)

CANONICAL_PATTERN = re.compile(
    r'<link\s+rel="canonical"\s+href="([^"]+)"',
    re.IGNORECASE,
)

H1_PATTERN = re.compile(
    r"<h1\b[^>]*>(.+?)</h1>",
    re.IGNORECASE | re.DOTALL,
)


RENDER_VALIDATION_PATTERNS = {
    "title": re.compile(r"<title>.+?</title>", re.IGNORECASE | re.DOTALL),
    "description": re.compile(
        r'<meta\s+name="description"\s+content="[^"]+">',
        re.IGNORECASE,
    ),
    "canonical": re.compile(
        r'<link\s+rel="canonical"\s+href="https://[^"]+">',
        re.IGNORECASE,
    ),
    "h1": re.compile(r"<h1\b[^>]*>.+?</h1>", re.IGNORECASE | re.DOTALL),
}

CURRENT_YEAR = str(datetime.now(timezone.utc).year)


def dataclass_to_dict(value: Any) -> Any:
    """Safely convert dataclass-based config objects into plain dictionaries."""
    if is_dataclass(value):
        return asdict(value)
    return value


def load_site_data() -> dict[str, Any]:
    """Load and validate the sovereign site data source."""
    if not SITE_DATA_FILE.exists():
        raise GenerationError(f"Missing required data file: {SITE_DATA_FILE}")

    try:
        raw = SITE_DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GenerationError(f"Invalid JSON in {SITE_DATA_FILE}: {exc}") from exc

    if not isinstance(data, dict):
        raise GenerationError("site.json must contain a top-level JSON object.")

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            raise GenerationError(f"site.json is missing required top-level key: '{key}'")

    if not isinstance(data["core_pages"], list) or not data["core_pages"]:
        raise GenerationError("site.json must include a non-empty 'core_pages' array.")

    return data


def validate_top_level_data(data: dict[str, Any]) -> None:
    """Validate core global structures before page generation begins."""
    site = data["site"]
    seo = data["seo"]
    navigation = data["navigation"]
    core_pages = data["core_pages"]

    if site.get("canonical_url") != CONFIG.site.canonical_url:
        raise GenerationError(
            "site.json canonical_url does not match config.py canonical_url. "
            "The source of truth must remain consistent."
        )

    if seo.get("preferred_protocol") != "https":
        raise GenerationError("preferred_protocol must be 'https' for sovereign production output.")

    if not isinstance(navigation, dict) or "header" not in navigation:
        raise GenerationError("navigation.header is required.")

    if not isinstance(navigation["header"], list):
        raise GenerationError("navigation.header must be a list.")

    if not isinstance(core_pages, list):
        raise GenerationError("core_pages must be a list.")

    validate_navigation_targets(data)
    validate_required_core_pages(data)


def validate_required_core_pages(data: dict[str, Any]) -> None:
    """Ensure all required core files defined in config exist in site.json."""
    files = {str(page.get("file", "")).strip() for page in data["core_pages"]}
    missing = [page for page in CONFIG.pages.required_core_pages if page not in files]
    if missing:
        raise GenerationError(
            f"site.json is missing required core pages defined in config.py: {missing}"
        )


def validate_navigation_targets(data: dict[str, Any]) -> None:
    """Ensure every public navigation target points to an existing declared page."""
    known_hrefs = {normalize_href_for_match(page.get("file", "")) for page in data["core_pages"]}

    for item in data["navigation"].get("header", []):
        href = str(item.get("href", "")).strip()
        if not href:
            raise GenerationError("A navigation.header entry is missing its href.")
        if normalize_href_for_match(href) not in known_hrefs:
            raise GenerationError(
                f"Navigation target '{href}' does not match any declared core page file."
            )


def normalize_href_for_match(value: str) -> str:
    """Normalize hrefs like /manifesto.html and manifesto.html for matching."""
    return value.lstrip("/").strip()


def validate_page_definitions(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate page-level rules before rendering."""
    pages = deepcopy(data["core_pages"])

    seen_keys: set[str] = set()
    seen_files: set[str] = set()
    seen_slugs: set[str] = set()
    seen_canonicals: set[str] = set()

    for page in pages:
        if not isinstance(page, dict):
            raise GenerationError("Each item in core_pages must be an object.")

        for key in REQUIRED_PAGE_KEYS:
            if key not in page:
                raise GenerationError(
                    f"A page is missing required field '{key}'. Page data: {page}"
                )

        page_key = require_non_empty_string(page, "key")
        page_file = require_non_empty_string(page, "file")
        page_title = require_non_empty_string(page, "title")
        page_description = require_non_empty_string(page, "description")
        page_template = require_non_empty_string(page, "template")
        page_type = require_non_empty_string(page, "page_type")
        page_canonical = require_non_empty_string(page, "canonical")

        if page_key in seen_keys:
            raise GenerationError(f"Duplicate page key detected: '{page_key}'")
        seen_keys.add(page_key)

        if page_file in seen_files:
            raise GenerationError(f"Duplicate page file detected: '{page_file}'")
        seen_files.add(page_file)

        slug = str(page.get("slug", "")).strip()
        if slug:
            if slug in seen_slugs:
                raise GenerationError(f"Duplicate page slug detected: '{slug}'")
            seen_slugs.add(slug)

        if page_canonical in seen_canonicals:
            raise GenerationError(f"Duplicate canonical URL detected: '{page_canonical}'")
        seen_canonicals.add(page_canonical)

        validate_page_file(page_file)
        validate_template_exists(page_template)
        validate_page_canonical(page_canonical)
        validate_page_indexability(page)
        validate_page_text_quality(page_title, "page title")
        validate_page_text_quality(page_description, "page description")
        validate_page_content_safety(page)

        page["year"] = CURRENT_YEAR
        page.setdefault("language", data["site"].get("language", "en"))
        page.setdefault("direction", data["site"].get("direction", "ltr"))
        page.setdefault("robots", data["seo"].get("robots_default", "index, follow"))
        page.setdefault("og_image", data["seo"].get("default_og_image", ""))

        if page_key == "home":
            if page_file != "index.html":
                raise GenerationError("The home page must render to index.html.")
            if slug:
                raise GenerationError("The home page slug must be empty.")
            if page_canonical.rstrip("/") != CONFIG.site.canonical_url.rstrip("/"):
                raise GenerationError(
                    "The home page canonical must match the site canonical_url exactly."
                )
        else:
            if not slug:
                raise GenerationError(f"Non-home page '{page_key}' must define a non-empty slug.")

    return pages


def require_non_empty_string(page: dict[str, Any], field_name: str) -> str:
    """Require a non-empty string field on a page."""
    value = page.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise GenerationError(f"Page '{page.get('key', 'unknown')}' has invalid '{field_name}'.")
    return value.strip()


def validate_page_file(file_value: str) -> None:
    """Ensure the target output file is safe and root-governed."""
    path = Path(file_value)

    if path.is_absolute():
        raise GenerationError(f"Absolute output paths are forbidden: '{file_value}'")

    if any(part in {"..", ""} for part in path.parts[:-1]):
        raise GenerationError(f"Unsafe relative file path detected: '{file_value}'")

    if path.suffix.lower() != ".html":
        raise GenerationError(f"Generated page files must end in .html: '{file_value}'")

    if any(part in FORBIDDEN_OUTPUT_SEGMENTS for part in path.parts):
        raise GenerationError(
            f"Generated pages may not target protected system directories: '{file_value}'"
        )

    target = (OUTPUT_DIR / path).resolve()
    root = OUTPUT_DIR.resolve()

    if not str(target).startswith(str(root)):
        raise GenerationError(f"Output path escapes the root directory: '{file_value}'")


def validate_template_exists(template_name: str) -> None:
    """Ensure the referenced Jinja template exists."""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise GenerationError(f"Missing template referenced by page: '{template_name}'")


def validate_page_canonical(canonical: str) -> None:
    """Ensure canonical URLs are sovereign, secure, and root-aligned."""
    if CONFIG.security.require_https_urls and not canonical.startswith("https://"):
        raise GenerationError(f"Canonical URL must use HTTPS: '{canonical}'")

    if not canonical.startswith(CONFIG.site.canonical_url):
        raise GenerationError(
            "Canonical URL must remain within the sovereign site canonical root: "
            f"'{canonical}'"
        )


def validate_page_indexability(page: dict[str, Any]) -> None:
    """Ensure indexability is explicitly declared and coherent."""
    indexable = page.get("indexable")
    if not isinstance(indexable, bool):
        raise GenerationError(
            f"Page '{page.get('key', 'unknown')}' must declare a boolean 'indexable' field."
        )

    robots = str(page.get("robots", "")).lower()
    if not indexable and "noindex" not in robots and robots:
        raise GenerationError(
            f"Page '{page.get('key', 'unknown')}' is non-indexable but robots does not contain 'noindex'."
        )


def validate_page_text_quality(value: str, label: str) -> None:
    """Block obviously weak or placeholder text."""
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(value):
            raise GenerationError(f"Forbidden placeholder pattern detected in {label}: '{value}'")


def validate_page_content_safety(page: dict[str, Any]) -> None:
    """Recursively scan page data for unsafe inline scripting patterns."""
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else key)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")
        elif isinstance(node, str):
            for pattern in FORBIDDEN_CONTENT_PATTERNS:
                if pattern.search(node):
                    raise GenerationError(
                        f"Unsafe content pattern detected in page '{page.get('key')}' at '{path}'."
                    )

    walk(page, page.get("key", "page"))


def build_jinja_environment() -> Environment:
    """Create a strict Jinja rendering environment."""
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def build_global_context(data: dict[str, Any]) -> dict[str, Any]:
    """Build the cross-page global context passed into every template."""
    return {
        "site": data["site"],
        "brand": data["brand"],
        "seo": data["seo"],
        "navigation": data["navigation"],
        "organization": data.get("organization", {}),
        "system_metadata": data.get("system_metadata", {}),
    }


def render_pages(pages: list[dict[str, Any]], global_context: dict[str, Any]) -> list[Path]:
    """Render each sovereign page into the live root structure."""
    env = build_jinja_environment()
    written_files: list[Path] = []

    for page in pages:
        template = env.get_template(page["template"])
        context = {
            **global_context,
            "page": page,
        }

        rendered = template.render(**context)
        validate_rendered_html(page, rendered)

        output_path = safe_output_path(page["file"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8", newline="\n")
        written_files.append(output_path)

    return written_files


def safe_output_path(file_value: str) -> Path:
    """Resolve a safe final output path under the root live asset directory."""
    output_path = (OUTPUT_DIR / file_value).resolve()
    if not str(output_path).startswith(str(OUTPUT_DIR.resolve())):
        raise GenerationError(f"Blocked unsafe output path resolution: '{file_value}'")
    return output_path


def validate_rendered_html(page: dict[str, Any], html: str) -> None:
    """Validate critical output integrity after rendering."""
    if not html.strip():
        raise GenerationError(f"Rendered output is empty for page '{page['key']}'.")

    if "{{" in html or "{%" in html or "{#" in html:
        raise GenerationError(
            f"Unresolved template syntax detected in rendered page '{page['key']}'."
        )

    for label, pattern in RENDER_VALIDATION_PATTERNS.items():
        if not pattern.search(html):
            raise GenerationError(
                f"Rendered page '{page['key']}' failed output validation: missing {label}."
            )

    title_match = TITLE_PATTERN.search(html)
    description_match = DESCRIPTION_PATTERN.search(html)
    canonical_match = CANONICAL_PATTERN.search(html)
    h1_match = H1_PATTERN.search(html)

    rendered_title = normalize_whitespace(unescape(title_match.group(1))) if title_match else ""
    rendered_description = (
        normalize_whitespace(unescape(description_match.group(1)))
        if description_match else ""
    )
    rendered_canonical = canonical_match.group(1).strip() if canonical_match else ""
    rendered_h1 = normalize_whitespace(unescape(h1_match.group(1))) if h1_match else ""

    declared_title = normalize_whitespace(page["title"])
    declared_description = normalize_whitespace(page["description"])
    declared_canonical = page["canonical"].strip()

    if rendered_title != declared_title:
        raise GenerationError(
            f"Rendered page '{page['key']}' title mismatch. "
            f"Rendered='{rendered_title}' Declared='{declared_title}'"
        )

    if rendered_description != declared_description:
        raise GenerationError(
            f"Rendered page '{page['key']}' description mismatch. "
            f"Rendered='{rendered_description}' Declared='{declared_description}'"
        )

    if rendered_canonical != declared_canonical:
        raise GenerationError(
            f"Rendered page '{page['key']}' canonical mismatch. "
            f"Rendered='{rendered_canonical}' Declared='{declared_canonical}'"
        )

    if not rendered_h1:
        raise GenerationError(
            f"Rendered page '{page['key']}' does not contain a valid H1."
        )

def post_render_integrity_check(written_files: list[Path]) -> None:
    """Perform final output sanity checks across the generated page set."""
    if not written_files:
        raise GenerationError("No pages were rendered. The generation pipeline produced nothing.")

    for required_file in CONFIG.pages.required_core_pages:
        expected = OUTPUT_DIR / required_file
        if not expected.exists():
            raise GenerationError(f"Required core output page missing after rendering: '{required_file}'")


def main() -> None:
    """Run the sovereign page generation pipeline."""
    data = load_site_data()
    validate_top_level_data(data)
    pages = validate_page_definitions(data)
    global_context = build_global_context(data)
    written_files = render_pages(pages, global_context)
    post_render_integrity_check(written_files)

    print("Sovereign page generation completed successfully.")
    for path in written_files:
        print(f"  - {path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    try:
        main()
    except GenerationError as exc:
        raise SystemExit(f"[GENERATE_PAGES_ERROR] {exc}") from exc
