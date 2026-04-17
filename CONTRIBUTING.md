# Contributing

## Contribution Standard

This repository is a governed strategic asset system.
Every contribution must preserve doctrine, structure, and trust posture.

Read before contributing:

- `docs/PROJECT_DOCTRINE.md`
- `docs/QUALITY_GATE.md`
- `docs/SECURITY_POLICY.md`
- `docs/ARCHITECTURE.md`

## Required Workflow

1. Create a branch from `main`.
2. Keep each change focused and traceable.
3. Run local checks before opening a PR:
   - `python scripts/quality_gate.py`
   - `python scripts/governance_guard.py`
   - `python scripts/check_markdown_links.py`
   - `python scripts/sovereign_standards_guard.py`
4. Open a PR using the provided PR template.

## Governance Rules

- Do not weaken the GitHub-first deployment chain.
- Do not introduce undocumented publishing paths.
- Do not add secrets, tokens, credentials, or private keys.
- Do not bypass quality gates.
- If you change governance-critical files, include a clear decision rationale.

## Governance-Critical Change Rule

If you modify any of the files below, update `docs/DECISION_LOG.md` in the same PR:

- `.github/workflows/deploy.yml`
- `docs/PROJECT_DOCTRINE.md`
- `docs/FOUNDATION_DOCTRINE.md`
- `docs/SECURITY_POLICY.md`
- `scripts/quality_gate.py`

## Commit Style

Use specific commits with operating meaning.

Examples:

- `docs: refine doctrine boundaries for first release`
- `ci: add governance guard checks`
- `security: strengthen repository disclosure policy`

Avoid:

- `update`
- `misc changes`
- `fix stuff`
