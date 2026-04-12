from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import get_config


class SiteDataLoadError(Exception):
    """Raised when site.json or its optional bundles cannot be loaded safely."""


CONFIG = get_config()
DATA_DIR = CONFIG.paths.data_dir
SITE_DATA_FILE = DATA_DIR / "site.json"
EXTRA_CORE_PAGES_FILE = DATA_DIR / "extra_core_pages.json"


def load_site_data() -> dict[str, Any]:
    """
    Load site.json and append pages from extra_core_pages.json when present.

    The optional bundle keeps the canonical registry in site.json while allowing
    large reference sets to live in a dedicated file without duplicating loaders.
    """
    if not SITE_DATA_FILE.exists():
        raise SiteDataLoadError(f"Missing required data file: {SITE_DATA_FILE}")

    try:
        data = json.loads(SITE_DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SiteDataLoadError(f"Invalid JSON in {SITE_DATA_FILE}: {exc}") from exc

    if not isinstance(data, dict):
        raise SiteDataLoadError("site.json must contain a top-level JSON object.")

    if EXTRA_CORE_PAGES_FILE.exists():
        try:
            extra_raw = EXTRA_CORE_PAGES_FILE.read_text(encoding="utf-8")
            extra = json.loads(extra_raw)
        except json.JSONDecodeError as exc:
            raise SiteDataLoadError(f"Invalid JSON in {EXTRA_CORE_PAGES_FILE}: {exc}") from exc

        if not isinstance(extra, dict):
            raise SiteDataLoadError("extra_core_pages.json must contain a top-level JSON object.")

        extra_pages = extra.get("pages", [])
        if not isinstance(extra_pages, list):
            raise SiteDataLoadError("extra_core_pages.json 'pages' must be a list.")

        core = data.get("core_pages")
        if not isinstance(core, list):
            raise SiteDataLoadError("site.json must define 'core_pages' as a list before merging extras.")

        data = {**data, "core_pages": [*core, *extra_pages]}

    return data
