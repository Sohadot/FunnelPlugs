from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GOVERNANCE_CRITICAL = {
    ".github/workflows/deploy.yml",
    "docs/PROJECT_DOCTRINE.md",
    "docs/FOUNDATION_DOCTRINE.md",
    "docs/SECURITY_POLICY.md",
    "scripts/quality_gate.py",
}

MANDATORY_WITH_GOVERNANCE_CHANGE = "docs/DECISION_LOG.md"


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def resolve_base_ref(explicit_base: str | None) -> str:
    if explicit_base:
        return explicit_base
    return "origin/main"


def list_changed_files(base_ref: str) -> set[str]:
    # Use symmetric diff so PR and branch workflows both behave correctly.
    diff_range = f"{base_ref}...HEAD"
    committed_output = run_git("diff", "--name-only", diff_range)
    working_output = run_git("diff", "--name-only")
    staged_output = run_git("diff", "--name-only", "--cached")

    paths: set[str] = set()
    for output in (committed_output, working_output, staged_output):
        paths.update(
            line.strip().replace("\\", "/")
            for line in output.splitlines()
            if line.strip()
        )

    porcelain = run_git("status", "--porcelain")
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        candidate = line[3:].strip()
        if not candidate:
            continue
        if " -> " in candidate:
            candidate = candidate.split(" -> ", 1)[1].strip()
        paths.add(candidate.replace("\\", "/"))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce repository governance checks.")
    parser.add_argument(
        "--base-ref",
        default=None,
        help="Base git ref for diff range (default: origin/main).",
    )
    args = parser.parse_args()

    base_ref = resolve_base_ref(args.base_ref)
    issues: list[str] = []

    try:
        changed = list_changed_files(base_ref)
    except RuntimeError as exc:
        print(f"[GOVERNANCE_GUARD_ERROR] {exc}")
        return 1

    if not changed:
        print("[GOVERNANCE_GUARD] No changed files detected.")
        return 0

    changed_governance_files = sorted(path for path in changed if path in GOVERNANCE_CRITICAL)
    decision_log_changed = MANDATORY_WITH_GOVERNANCE_CHANGE in changed

    if changed_governance_files and not decision_log_changed:
        issues.append(
            "Governance-critical files changed without updating docs/DECISION_LOG.md: "
            + ", ".join(changed_governance_files)
        )

    if issues:
        print("[GOVERNANCE_GUARD_BLOCKED] Governance checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[GOVERNANCE_GUARD_PASSED] Governance checks passed.")
    if changed_governance_files:
        print(
            "[GOVERNANCE_GUARD] Governance-critical changes detected and decision log updated."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
