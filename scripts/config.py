from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final


@dataclass(frozen=True)
class SiteIdentity:
    name: str
    domain: str
    canonical_url: str
    language: str
    locale: str
    title_default: str
    description_default: str


@dataclass(frozen=True)
class PathConfig:
    root: Path
    assets_dir: Path
    css_dir: Path
    js_dir: Path
    img_dir: Path
    icons_dir: Path
    data_dir: Path
    templates_dir: Path
    scripts_dir: Path
    docs_dir: Path
    github_dir: Path
    workflows_dir: Path
    output_dir: Path


@dataclass(frozen=True)
class PageConfig:
    required_core_pages: tuple[str, ...]
    indexable_extensions: tuple[str, ...]
    excluded_output_names: tuple[str, ...]
    reserved_routes: tuple[str, ...]


@dataclass(frozen=True)
class SeoConfig:
    robots_default: str
    sitemap_filename: str
    min_title_length: int
    max_title_length: int
    min_description_length: int
    max_description_length: int
    enforce_canonical: bool
    enforce_lastmod: bool
    allow_noindex_in_sitemap: bool


@dataclass(frozen=True)
class QualityConfig:
    block_on_missing_title: bool
    block_on_missing_description: bool
    block_on_empty_slug: bool
    block_on_broken_internal_links: bool
    block_on_missing_core_page: bool
    block_on_invalid_sitemap: bool
    block_on_orphan_core_page: bool
    block_on_placeholder_content: bool


@dataclass(frozen=True)
class SecurityConfig:
    allow_inline_scripts: bool
    allow_unapproved_external_scripts: bool
    expose_internal_docs_in_output: bool
    expose_raw_data_in_output: bool
    require_https_urls: bool


@dataclass(frozen=True)
class BuildConfig:
    environment: str
    github_branch: str
    generate_sitemap: bool
    run_validation: bool
    run_quality_gate: bool
    clean_output_before_build: bool


@dataclass(frozen=True)
class FunnelPlugsConfig:
    site: SiteIdentity
    paths: PathConfig
    pages: PageConfig
    seo: SeoConfig
    quality: QualityConfig
    security: SecurityConfig
    build: BuildConfig
    version: str = field(default="0.1.0")


ROOT_DIR: Final[Path] = Path(__file__).resolve().parents[1]
OUTPUT_DIR: Final[Path] = ROOT_DIR

CONFIG: Final[FunnelPlugsConfig] = FunnelPlugsConfig(
    site=SiteIdentity(
        name="Funnelplugs",
        domain="funnelplugs.com",
        canonical_url="https://funnelplugs.com",
        language="en",
        locale="en_US",
        title_default="Funnelplugs — The Logic of the Missing Plug",
        description_default=(
            "Funnelplugs is a sovereign-grade reference system for funnel integrity, "
            "commercial leakage logic, and the intervention layers required to restore flow, trust, and conversion."
        ),
    ),
    paths=PathConfig(
        root=ROOT_DIR,
        assets_dir=ROOT_DIR / "assets",
        css_dir=ROOT_DIR / "assets" / "css",
        js_dir=ROOT_DIR / "assets" / "js",
        img_dir=ROOT_DIR / "assets" / "img",
        icons_dir=ROOT_DIR / "assets" / "icons",
        data_dir=ROOT_DIR / "data",
        templates_dir=ROOT_DIR / "templates",
        scripts_dir=ROOT_DIR / "scripts",
        docs_dir=ROOT_DIR / "docs",
        github_dir=ROOT_DIR / ".github",
        workflows_dir=ROOT_DIR / ".github" / "workflows",
        output_dir=OUTPUT_DIR,
    ),
    pages=PageConfig(
        required_core_pages=(
            "index.html",
            "manifesto.html",
            "protocol.html",
            "standard.html",
            "registry.html",
            "engine.html",
        ),
        indexable_extensions=(".html",),
        excluded_output_names=(
            "README.md",
            "robots.txt",
            "sitemap.xml",
        ),
        reserved_routes=(
            "",
            "index",
            "manifesto",
            "protocol",
            "standard",
            "registry",
            "engine",
        ),
    ),
    seo=SeoConfig(
        robots_default="index, follow",
        sitemap_filename="sitemap.xml",
        min_title_length=20,
        max_title_length=70,
        min_description_length=70,
        max_description_length=170,
        enforce_canonical=True,
        enforce_lastmod=True,
        allow_noindex_in_sitemap=False,
    ),
    quality=QualityConfig(
        block_on_missing_title=True,
        block_on_missing_description=True,
        block_on_empty_slug=True,
        block_on_broken_internal_links=True,
        block_on_missing_core_page=True,
        block_on_invalid_sitemap=True,
        block_on_orphan_core_page=True,
        block_on_placeholder_content=True,
    ),
    security=SecurityConfig(
        # GTM bootstrap is intentionally inline in `templates/base.html` (governed exception).
        # All other inline scripts remain forbidden in rendered HTML via `validate_content.py`.
        allow_inline_scripts=True,
        allow_unapproved_external_scripts=False,
        expose_internal_docs_in_output=False,
        expose_raw_data_in_output=False,
        require_https_urls=True,
    ),
    build=BuildConfig(
        environment="production",
        github_branch="main",
        generate_sitemap=True,
        run_validation=True,
        run_quality_gate=True,
        clean_output_before_build=False,
    ),
)


def get_config() -> FunnelPlugsConfig:
    """
    Return the single source of truth configuration for the Funnelplugs asset.
    """
    return CONFIG
