from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from config import get_config
from site_data_loader import SiteDataLoadError, load_site_data as load_site_bundle


class ValidationError(Exception):
    """Raised when the sovereign validation pipeline detects blocking issues."""


CONFIG = get_config()
ROOT_DIR = CONFIG.paths.root
DATA_DIR = CONFIG.paths.data_dir
OUTPUT_DIR = CONFIG.paths.output_dir
SITE_DATA_FILE = DATA_DIR / "site.json"

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TITLE_PATTERN = re.compile(r"<title>(.+?)</title>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_PATTERN = re.compile(
    r'<meta\s+name="description"\s+content="([^"]+)"',
    re.IGNORECASE,
)
CANONICAL_PATTERN = re.compile(
    r'<link\s+rel="canonical"\s+href="([^"]+)"',
    re.IGNORECASE,
)
ROBOTS_PATTERN = re.compile(
    r'<meta\s+name="robots"\s+content="([^"]+)"',
    re.IGNORECASE,
)
H1_PATTERN = re.compile(r"<h1\b[^>]*>(.+?)</h1>", re.IGNORECASE | re.DOTALL)

FORBIDDEN_SCAN_SEGMENTS = {
    "assets",
    "data",
    "docs",
    "scripts",
    "templates",
    ".github",
    "__pycache__",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"lorem ipsum", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
)

SHELL_WEAKNESS_PATTERNS = (
    re.compile(r"structured page shell active", re.IGNORECASE),
    re.compile(r"ready to receive validated structured content", re.IGNORECASE),
    re.compile(r"content pending", re.IGNORECASE),
    re.compile(r"\bpending\b", re.IGNORECASE),
)

UNSAFE_URL_AND_HANDLER_PATTERNS = (
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"\bon\w+\s*=", re.IGNORECASE),
)

IFRAME_MARKUP_PATTERN = re.compile(r"<\s*iframe\b", re.IGNORECASE)

# Declared JSON content must not embed iframes; rendered HTML may include the GTM noscript iframe only.
UNSAFE_DECLARED_CONTENT_PATTERNS = UNSAFE_URL_AND_HANDLER_PATTERNS + (IFRAME_MARKUP_PATTERN,)

INLINE_SCRIPT_PATTERN = re.compile(
    r'<\s*script\b(?![^>]*\bsrc=)(?![^>]*\btype=["\']application/json["\'])[^>]*>',
    re.IGNORECASE,
)

ALLOWED_SCRIPT_SRCS = {
    "/assets/js/main.js",
    "/assets/js/engine.js",
    "/assets/js/gtm.js",
}

SITE_CANONICAL_ROOT = CONFIG.site.canonical_url.rstrip("/")
GTM_CONTAINER_ID = "GTM-56J99S4F"
GTM_NS_IFRAME_PATH = f"https://www.googletagmanager.com/ns.html?id={GTM_CONTAINER_ID}"

INLINE_SCRIPT_BLOCK_PATTERN = re.compile(
    r"<\s*script\b(?P<attrs>[^>]*)>(?P<body>.*?)<\s*/\s*script\s*>",
    re.IGNORECASE | re.DOTALL,
)
INLINE_SCRIPT_TYPE_JSON_PATTERN = re.compile(
    r'\btype\s*=\s*["\']application/json["\']',
    re.IGNORECASE,
)
GTM_INLINE_REQUIRED_MARKERS = (
    "window,document,'script','datalayer'",
    "window, document, 'script', 'datalayer'",
    "window,document,\"script\",\"datalayer\"",
    "window, document, \"script\", \"datalayer\"",
)


@dataclass
class Issue:
    severity: str  # ERROR | WARNING
    scope: str
    message: str


class HTMLInspector(HTMLParser):
    """Extract hrefs and inspect script usage from rendered HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.script_srcs: list[str] = []
        self.inline_script_detected = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_lower = tag.lower()
        attr_map = dict(attrs)

        if tag_lower == "a":
            href = attr_map.get("href")
            if href:
                self.hrefs.append(href.strip())

        if tag_lower == "script":
            src = attr_map.get("src")
            if src:
                self.script_srcs.append(src.strip())
            else:
                self.inline_script_detected = True

    def handle_data(self, data: str) -> None:
        if data.strip():
            # Actual inline script bodies are already blocked by handle_starttag
            # when there is no src. Nothing more is needed here.
            return


def load_site_data() -> dict[str, Any]:
    """Load the sovereign site data source."""
    try:
        data = load_site_bundle()
    except SiteDataLoadError as exc:
        raise ValidationError(str(exc)) from exc

    if "core_pages" not in data or not isinstance(data["core_pages"], list):
        raise ValidationError("site.json must define a 'core_pages' list.")

    if "navigation" not in data or not isinstance(data["navigation"], dict):
        raise ValidationError("site.json must define a 'navigation' object.")

    return data


def normalize_whitespace(value: str) -> str:
    """Normalize whitespace for reliable comparisons."""
    return " ".join(value.split())


def iter_live_html_files() -> list[Path]:
    """Return all live candidate HTML files under the root output structure."""
    files: list[Path] = []

    for path in OUTPUT_DIR.rglob("*.html"):
        relative = path.relative_to(OUTPUT_DIR)

        if any(part in FORBIDDEN_SCAN_SEGMENTS for part in relative.parts):
            continue

        if any(part.startswith(".") for part in relative.parts):
            continue

        files.append(path)

    return sorted(files, key=lambda p: p.relative_to(OUTPUT_DIR).as_posix())


def declared_pages_by_file(site_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map declared core pages by their output file names."""
    mapping: dict[str, dict[str, Any]] = {}

    for page in site_data["core_pages"]:
        if not isinstance(page, dict):
            raise ValidationError("Each item in core_pages must be an object.")

        file_value = str(page.get("file", "")).strip()
        if not file_value:
            raise ValidationError("A page in core_pages is missing its 'file' field.")

        if file_value in mapping:
            raise ValidationError(f"Duplicate declared page file detected: '{file_value}'")

        mapping[file_value] = page

    return mapping


def validate_site_json_structure(site_data: dict[str, Any]) -> list[Issue]:
    """Validate declared site data before comparing against rendered output."""
    issues: list[Issue] = []
    pages = site_data["core_pages"]

    seen_keys: set[str] = set()
    seen_files: set[str] = set()
    seen_slugs: set[str] = set()
    seen_canonicals: set[str] = set()

    for page in pages:
        scope = f"page:{page.get('key', 'unknown')}"

        for field in (
            "key",
            "file",
            "title",
            "description",
            "template",
            "page_type",
            "indexable",
            "canonical",
        ):
            if field not in page:
                issues.append(Issue("ERROR", scope, f"Missing required field '{field}' in site.json."))
                continue

        key = str(page.get("key", "")).strip()
        file_value = str(page.get("file", "")).strip()
        slug = str(page.get("slug", "")).strip()
        title = str(page.get("title", "")).strip()
        description = str(page.get("description", "")).strip()
        canonical = str(page.get("canonical", "")).strip()
        indexable = page.get("indexable")

        if not key:
            issues.append(Issue("ERROR", scope, "Page key must be a non-empty string."))
        elif key in seen_keys:
            issues.append(Issue("ERROR", scope, f"Duplicate page key detected: '{key}'"))
        else:
            seen_keys.add(key)

        if not file_value:
            issues.append(Issue("ERROR", scope, "Page file must be a non-empty string."))
        elif file_value in seen_files:
            issues.append(Issue("ERROR", scope, f"Duplicate page file detected: '{file_value}'"))
        else:
            seen_files.add(file_value)

        if key == "home":
            if file_value != "index.html":
                issues.append(Issue("ERROR", scope, "The home page must render to index.html."))
            if slug:
                issues.append(Issue("ERROR", scope, "The home page slug must remain empty."))
        else:
            if not slug:
                issues.append(Issue("ERROR", scope, "Non-home pages must define a non-empty slug."))
            elif not SLUG_PATTERN.fullmatch(slug):
                issues.append(Issue("ERROR", scope, f"Invalid slug format: '{slug}'"))
            elif slug in seen_slugs:
                issues.append(Issue("ERROR", scope, f"Duplicate slug detected: '{slug}'"))
            else:
                seen_slugs.add(slug)

            expected_file = f"{slug}.html"
            if file_value and file_value != expected_file:
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Non-home page file '{file_value}' must match slug-based convention '{expected_file}'.",
                    )
                )

        if not title:
            issues.append(Issue("ERROR", scope, "Page title must be non-empty."))
        if not description:
            issues.append(Issue("ERROR", scope, "Page description must be non-empty."))

        if not isinstance(indexable, bool):
            issues.append(Issue("ERROR", scope, "Page indexable field must be a boolean."))

        if not canonical:
            issues.append(Issue("ERROR", scope, "Canonical URL must be non-empty."))
        else:
            if canonical in seen_canonicals:
                issues.append(Issue("ERROR", scope, f"Duplicate canonical detected: '{canonical}'"))
            else:
                seen_canonicals.add(canonical)

            if not canonical.startswith("https://"):
                issues.append(Issue("ERROR", scope, f"Canonical must use HTTPS: '{canonical}'"))
            if not canonical.startswith(SITE_CANONICAL_ROOT):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Canonical must remain within the sovereign root '{SITE_CANONICAL_ROOT}': '{canonical}'",
                    )
                )

        for label, value in (("title", title), ("description", description)):
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.search(value):
                    issues.append(
                        Issue(
                            "ERROR",
                            scope,
                            f"Placeholder pattern detected in declared {label}: '{value}'",
                        )
                    )

        validate_declared_page_content_quality(page, issues)

    required_files = set(CONFIG.pages.required_core_pages)
    declared_files = {str(page.get("file", "")).strip() for page in pages}
    missing_required = sorted(required_files - declared_files)
    if missing_required:
        issues.append(
            Issue(
                "ERROR",
                "site.json",
                f"Missing required core pages declared in config.py: {missing_required}",
            )
        )

    issues.extend(validate_navigation_declared_targets(site_data))
    return issues


def validate_declared_page_content_quality(page: dict[str, Any], issues: list[Issue]) -> None:
    """Validate that the declared page has real structured content and no obvious weak shell."""
    scope = f"page:{page.get('key', 'unknown')}"

    if not any(page.get(field) for field in ("hero", "summary", "sections", "body")):
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Page must define at least one structured content layer: hero, summary, sections, or body.",
            )
        )

    for pattern in SHELL_WEAKNESS_PATTERNS:
        for field_name in ("title", "description"):
            value = str(page.get(field_name, ""))
            if pattern.search(value):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Weak shell language detected in declared {field_name}: '{value}'",
                    )
                )

    scan_nested_content_for_patterns(page, scope, issues)


def scan_nested_content_for_patterns(node: Any, scope: str, issues: list[Issue], path: str = "") -> None:
    """Recursively inspect declared content for placeholders, unsafe markup, and weak shell text."""
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = f"{path}.{key}" if path else key
            scan_nested_content_for_patterns(value, scope, issues, next_path)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            next_path = f"{path}[{index}]"
            scan_nested_content_for_patterns(item, scope, issues, next_path)
    elif isinstance(node, str):
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(node):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Placeholder pattern detected in declared content at '{path}'.",
                    )
                )

        for pattern in SHELL_WEAKNESS_PATTERNS:
            if pattern.search(node):
                issues.append(
                    Issue(
                        "WARNING",
                        scope,
                        f"Potential shell weakness language detected in declared content at '{path}'.",
                    )
                )

        for pattern in UNSAFE_DECLARED_CONTENT_PATTERNS:
            if pattern.search(node):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Unsafe markup pattern detected in declared content at '{path}'.",
                    )
                )


def validate_navigation_declared_targets(site_data: dict[str, Any]) -> list[Issue]:
    """Validate navigation targets against declared pages in site.json."""
    issues: list[Issue] = []

    declared_files = {str(page.get("file", "")).strip() for page in site_data["core_pages"]}
    known_hrefs = {f"/{file_name}" for file_name in declared_files}

    for group_name in ("header", "footer"):
        group = site_data["navigation"].get(group_name, [])
        if not isinstance(group, list):
            issues.append(Issue("ERROR", f"navigation.{group_name}", "Navigation group must be a list."))
            continue

        seen_keys: set[str] = set()

        for item in group:
            if not isinstance(item, dict):
                issues.append(Issue("ERROR", f"navigation.{group_name}", "Navigation item must be an object."))
                continue

            label = str(item.get("label", "")).strip()
            href = str(item.get("href", "")).strip()
            key = str(item.get("key", "")).strip()

            scope = f"navigation.{group_name}:{label or key or 'item'}"

            if not label:
                issues.append(Issue("ERROR", scope, "Navigation item label must be non-empty."))
            if not href:
                issues.append(Issue("ERROR", scope, "Navigation item href must be non-empty."))

            if key:
                if key in seen_keys:
                    issues.append(Issue("ERROR", scope, f"Duplicate navigation key detected: '{key}'"))
                else:
                    seen_keys.add(key)

            public = item.get("public", True)
            if public and href not in known_hrefs:
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Public navigation target '{href}' does not match any declared page file.",
                    )
                )

    return issues


def extract_rendered_metadata(html: str) -> dict[str, str]:
    """Extract key metadata from rendered HTML."""
    title_match = TITLE_PATTERN.search(html)
    description_match = DESCRIPTION_PATTERN.search(html)
    canonical_match = CANONICAL_PATTERN.search(html)
    robots_match = ROBOTS_PATTERN.search(html)
    h1_match = H1_PATTERN.search(html)

    return {
        "title": normalize_whitespace(unescape(title_match.group(1))) if title_match else "",
        "description": normalize_whitespace(unescape(description_match.group(1))) if description_match else "",
        "canonical": canonical_match.group(1).strip() if canonical_match else "",
        "robots": normalize_whitespace(unescape(robots_match.group(1))) if robots_match else "",
        "h1": normalize_whitespace(unescape(h1_match.group(1))) if h1_match else "",
    }


def inspect_rendered_html(html: str) -> HTMLInspector:
    """Inspect rendered HTML for links and script usage."""
    inspector = HTMLInspector()
    inspector.feed(html)
    return inspector


def extract_internal_links(html: str) -> list[str]:
    """Extract internal hrefs from rendered HTML."""
    inspector = inspect_rendered_html(html)

    internal: list[str] = []
    for href in inspector.hrefs:
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        internal.append(href)

    return internal


def validate_script_security(scope: str, html: str, issues: list[Issue]) -> None:
    """Allow only approved external scripts and forbid inline scripts."""
    inspector = inspect_rendered_html(html)

    for match in INLINE_SCRIPT_BLOCK_PATTERN.finditer(html):
        script_attrs = match.group("attrs") or ""
        script_body = (match.group("body") or "").strip()
        script_tag = match.group(0)
        has_src = re.search(r"\bsrc\s*=", script_attrs, re.IGNORECASE) is not None
        is_json_data = INLINE_SCRIPT_TYPE_JSON_PATTERN.search(script_attrs) is not None

        if not has_src and not is_json_data and not is_allowed_gtm_inline_script(script_body):
            issues.append(
                Issue(
                    "ERROR",
                    scope,
                    f"Rendered page contains inline script markup, which is not permitted. Tag: {script_tag}",
                )
            )
            break

    for src in inspector.script_srcs:
        if src not in ALLOWED_SCRIPT_SRCS:
            issues.append(
                Issue(
                    "ERROR",
                    scope,
                    f"Rendered page references a non-approved script source: '{src}'.",
                )
            )

    for pattern in UNSAFE_URL_AND_HANDLER_PATTERNS:
        if pattern.search(html):
            issues.append(
                Issue(
                    "ERROR",
                    scope,
                    "Rendered page contains unsafe markup patterns.",
                )
            )

    validate_iframe_security(scope, html, issues)


def is_allowed_gtm_inline_script(script_body: str) -> bool:
    """Allow only the constrained GTM inline bootstrap snippet."""
    if not script_body:
        return False

    normalized = re.sub(r"\s+", " ", script_body).strip().lower()
    has_gtm_loader = "googletagmanager.com/gtm.js?id=" in normalized
    has_container_id = GTM_CONTAINER_ID.lower() in normalized
    has_data_layer_start = "gtm.start" in normalized and "event" in normalized and "gtm.js" in normalized
    has_bootstrap_signature = any(marker in normalized for marker in GTM_INLINE_REQUIRED_MARKERS)

    return has_gtm_loader and has_container_id and has_data_layer_start and has_bootstrap_signature


def validate_iframe_security(scope: str, html: str, issues: list[Issue]) -> None:
    """Allow only the Google Tag Manager noscript iframe used for this site."""
    for match in re.finditer(r"<\s*iframe\b[^>]*>", html, re.IGNORECASE):
        tag = match.group(0)
        normalized = tag.replace("'", '"').lower()
        if GTM_NS_IFRAME_PATH.lower() in normalized:
            continue
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Rendered page contains a forbidden iframe (only the GTM noscript fallback is permitted).",
            )
        )
        return


def resolve_internal_href(href: str, current_file: Path) -> Path | None:
    """Resolve a relative internal href to a live filesystem path under the root."""
    href = href.strip()
    if not href or href.startswith("#"):
        return None

    if "://" in href or href.startswith(("mailto:", "tel:")):
        return None

    path_part = href.split("?", 1)[0].split("#", 1)[0].strip()

    if not path_part:
        return None

    if path_part.startswith("/"):
        target = (OUTPUT_DIR / path_part.lstrip("/")).resolve()
    else:
        target = (current_file.parent / path_part).resolve()

    try:
        target.relative_to(OUTPUT_DIR.resolve())
    except ValueError:
        raise ValidationError(
            f"Internal href '{href}' resolves outside the sovereign root from '{current_file.relative_to(ROOT_DIR)}'."
        )

    return target


def validate_rendered_pages(site_data: dict[str, Any]) -> list[Issue]:
    """Validate live rendered HTML pages against doctrine and declared data."""
    issues: list[Issue] = []

    declared = declared_pages_by_file(site_data)
    html_files = iter_live_html_files()

    if not html_files:
        issues.append(Issue("ERROR", "render", "No live HTML files were found in the root structure."))
        return issues

    seen_rendered_files = {path.relative_to(OUTPUT_DIR).as_posix() for path in html_files}
    for required_file in CONFIG.pages.required_core_pages:
        if required_file not in seen_rendered_files:
            issues.append(Issue("ERROR", "render", f"Required core rendered page missing: '{required_file}'"))

    for file_path in html_files:
        relative = file_path.relative_to(OUTPUT_DIR).as_posix()
        scope = f"render:{relative}"

        html = file_path.read_text(encoding="utf-8")
        metadata = extract_rendered_metadata(html)
        page_declared = declared.get(relative)

        if not metadata["title"]:
            issues.append(Issue("ERROR", scope, "Rendered page is missing <title>."))
        if not metadata["description"]:
            issues.append(Issue("ERROR", scope, "Rendered page is missing meta description."))
        if not metadata["canonical"]:
            issues.append(Issue("ERROR", scope, "Rendered page is missing canonical link."))
        if not metadata["robots"]:
            issues.append(Issue("ERROR", scope, "Rendered page is missing robots meta tag."))
        if not metadata["h1"]:
            issues.append(Issue("ERROR", scope, "Rendered page is missing a visible H1 heading."))

        if metadata["canonical"]:
            if not metadata["canonical"].startswith("https://"):
                issues.append(Issue("ERROR", scope, f"Canonical must use HTTPS: '{metadata['canonical']}'"))
            if not metadata["canonical"].startswith(SITE_CANONICAL_ROOT):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        f"Canonical escapes the sovereign domain root: '{metadata['canonical']}'",
                    )
                )

        if page_declared:
            compare_declared_to_rendered(page_declared, metadata, scope, issues)

        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(html):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        "Rendered page contains placeholder language.",
                    )
                )

        for pattern in SHELL_WEAKNESS_PATTERNS:
            if pattern.search(html):
                issues.append(
                    Issue(
                        "ERROR",
                        scope,
                        "Rendered page contains shell weakness language and is not ready for production.",
                    )
                )

        validate_script_security(scope, html, issues)
        validate_internal_links(relative, html, file_path, issues)

    return issues


def compare_declared_to_rendered(
    page_declared: dict[str, Any],
    metadata: dict[str, str],
    scope: str,
    issues: list[Issue],
) -> None:
    """Ensure rendered metadata reflects declared sovereign page intent."""
    declared_title = normalize_whitespace(str(page_declared.get("title", "")))
    declared_description = normalize_whitespace(str(page_declared.get("description", "")))
    declared_canonical = str(page_declared.get("canonical", "")).strip()
    declared_indexable = bool(page_declared.get("indexable", False))

    if declared_title and metadata["title"] != declared_title:
        issues.append(
            Issue(
                "ERROR",
                scope,
                f"Rendered title does not match declared title. Rendered='{metadata['title']}' Declared='{declared_title}'",
            )
        )

    if declared_description and metadata["description"] != declared_description:
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Rendered meta description does not match declared description.",
            )
        )

    if declared_canonical and metadata["canonical"] != declared_canonical:
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Rendered canonical does not match declared canonical.",
            )
        )

    robots = metadata["robots"].lower()
    if declared_indexable and "noindex" in robots:
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Declared indexable page is rendered with noindex robots policy.",
            )
        )
    if not declared_indexable and "noindex" not in robots:
        issues.append(
            Issue(
                "ERROR",
                scope,
                "Declared non-indexable page is missing noindex in rendered robots policy.",
            )
        )


def validate_internal_links(
    relative_file: str,
    html: str,
    current_file: Path,
    issues: list[Issue],
) -> None:
    """Validate that internal links resolve to real public files."""
    scope = f"render:{relative_file}"
    hrefs = extract_internal_links(html)

    for href in hrefs:
        try:
            target = resolve_internal_href(href, current_file)
        except ValidationError as exc:
            issues.append(Issue("ERROR", scope, str(exc)))
            continue

        if target is None:
            continue

        if target.suffix == "":
            target = target / "index.html"

        if not target.exists():
            issues.append(
                Issue(
                    "ERROR",
                    scope,
                    f"Internal href '{href}' resolves to a missing file: '{target.relative_to(ROOT_DIR)}'",
                )
            )


def print_issues(issues: list[Issue]) -> None:
    """Print issues in a readable and auditable form."""
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    warnings = [issue for issue in issues if issue.severity == "WARNING"]

    if not issues:
        print("Content validation completed successfully.")
        print("  - No blocking issues detected.")
        return

    if errors:
        print("Blocking validation issues:")
        for issue in errors:
            print(f"  [ERROR] {issue.scope} :: {issue.message}")

    if warnings:
        print("Non-blocking validation warnings:")
        for issue in warnings:
            print(f"  [WARNING] {issue.scope} :: {issue.message}")


def main() -> None:
    """Run the sovereign content validation pipeline."""
    site_data = load_site_data()

    issues: list[Issue] = []
    issues.extend(validate_site_json_structure(site_data))
    issues.extend(validate_rendered_pages(site_data))

    print_issues(issues)

    if any(issue.severity == "ERROR" for issue in issues):
        raise SystemExit("[VALIDATE_CONTENT_ERROR] Blocking validation issues detected.")

    print("Sovereign content validation passed.")


if __name__ == "__main__":
    main()
