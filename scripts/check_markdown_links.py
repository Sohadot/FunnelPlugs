from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_FILES = sorted(ROOT.rglob("*.md"))
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


def is_relative_link(target: str) -> bool:
    cleaned = target.strip()
    if not cleaned:
        return False
    if cleaned.startswith(SKIP_PREFIXES):
        return False
    return True


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if "<" in target and ">" in target:
        target = target.strip("<>")
    target = target.split("#", 1)[0]
    return target


def main() -> int:
    issues: list[str] = []

    for md_file in MARKDOWN_FILES:
        try:
            text = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for match in LINK_PATTERN.finditer(text):
            raw_target = match.group(1)
            if not is_relative_link(raw_target):
                continue

            target = normalize_target(raw_target)
            if not target:
                continue

            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                issues.append(
                    f"{md_file.relative_to(ROOT).as_posix()} -> missing link target: {raw_target}"
                )

    if issues:
        print("[MARKDOWN_LINK_CHECK_BLOCKED] Broken relative markdown links found:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("[MARKDOWN_LINK_CHECK_PASSED] No broken relative markdown links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
