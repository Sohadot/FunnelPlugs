from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from config import get_config


class BuildError(Exception):
    """Raised when the sovereign build pipeline cannot continue safely."""


CONFIG = get_config()
ROOT_DIR = CONFIG.paths.root
SCRIPTS_DIR = CONFIG.paths.scripts_dir

REQUIRED_SCRIPT_FILES = (
    "config.py",
    "site_data_loader.py",
    "generate_pages.py",
    "generate_sitemap.py",
    "validate_content.py",
    "quality_gate.py",
    "build.py",
)


def utc_now_iso() -> str:
    """Return a stable UTC timestamp for build logging."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_build_prerequisites() -> None:
    """Ensure the sovereign build layer itself is intact before execution."""
    if not ROOT_DIR.exists():
        raise BuildError(f"Root directory does not exist: {ROOT_DIR}")

    if not SCRIPTS_DIR.exists():
        raise BuildError(f"Scripts directory does not exist: {SCRIPTS_DIR}")

    missing = []
    for filename in REQUIRED_SCRIPT_FILES:
        path = SCRIPTS_DIR / filename
        if not path.exists():
            missing.append(path.relative_to(ROOT_DIR).as_posix())

    if missing:
        raise BuildError(
            "The sovereign build pipeline is incomplete. "
            f"Missing required script files: {missing}"
        )


def run_script(script_name: str) -> None:
    """Run a required script as a blocking sovereign pipeline step."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        raise BuildError(f"Cannot run missing script: {script_path.relative_to(ROOT_DIR)}")

    print(f"[BUILD] Running {script_name} ...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        check=False,
        text=True,
    )

    if result.returncode != 0:
        raise BuildError(f"Pipeline step failed: {script_name}")


def run_sovereign_build() -> None:
    """Run the full sovereign build pipeline through the quality gate."""
    ensure_build_prerequisites()

    print("=" * 72)
    print("FUNNELPLUGS — SOVEREIGN BUILD SYSTEM")
    print("=" * 72)
    print(f"[BUILD] Timestamp      : {utc_now_iso()}")
    print(f"[BUILD] Environment    : {CONFIG.build.environment}")
    print(f"[BUILD] Branch         : {CONFIG.build.github_branch}")
    print(f"[BUILD] Root Mode      : live root on main")
    print(f"[BUILD] Canonical Root : {CONFIG.site.canonical_url}")
    print(f"[BUILD] Source of Truth: GitHub")
    print("=" * 72)

    # The quality gate is the authoritative guardian of the build.
    # It internally runs generation, sitemap, and content validation.
    run_script("quality_gate.py")

    print("=" * 72)
    print("[BUILD] Sovereign build completed successfully.")
    print("[BUILD] Output is authorized for controlled deployment.")
    print("=" * 72)


def parse_args() -> argparse.Namespace:
    """Parse sovereign build arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Run the Funnelplugs sovereign build pipeline. "
            "This is the single approved entry point for controlled builds."
        )
    )
    parser.add_argument(
        "--mode",
        default="production",
        choices=("production",),
        help="Build mode. Only 'production' is permitted in the sovereign pipeline.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the sovereign build system."""
    args = parse_args()

    if args.mode != "production":
        raise SystemExit("[BUILD_ERROR] Only production mode is permitted.")

    try:
        run_sovereign_build()
    except BuildError as exc:
        raise SystemExit(f"[BUILD_ERROR] {exc}") from exc


if __name__ == "__main__":
    main()
