# Pull Request

## What changed

- [ ] Describe the change clearly.
- [ ] Keep scope limited and traceable.

## Why this change is correct

- [ ] Doctrine alignment confirmed (`docs/PROJECT_DOCTRINE.md`)
- [ ] Quality-gate alignment confirmed (`docs/QUALITY_GATE.md`)
- [ ] Security posture preserved (`docs/SECURITY_POLICY.md`)

## Governance checks

- [ ] `python scripts/quality_gate.py`
- [ ] `python scripts/governance_guard.py`
- [ ] `python scripts/check_markdown_links.py`
- [ ] `python scripts/sovereign_standards_guard.py`

## Governance-critical change declaration

- [ ] I did not modify governance-critical files
- [ ] I modified governance-critical files and updated `docs/DECISION_LOG.md`

## Risk review

- [ ] No new secrets or credentials introduced
- [ ] No undocumented publishing path introduced
- [ ] No quality gate bypass introduced

## Solo self-review gate (when no second reviewer exists)

- [ ] CI required check passed.
- [ ] Branch is up to date with `main`.
- [ ] I posted a self-review comment confirming:
  - [ ] scope clarity and traceability
  - [ ] governance checks completed
  - [ ] no hidden changes or output noise
  - [ ] no secrets and no policy bypass
