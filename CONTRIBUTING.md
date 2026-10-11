# Contributing to kz-identifiers

Спасибо за интерес к проекту. Этот файл описывает, как вносить изменения.

## Ground rules

1. **Spec first.** Every algorithm must point to a primary source (adilet, SWIFT
   registry, ISO). Comments in code carry the reference; README repeats it.
2. **No runtime dependencies.** Standard library only. Test-only and
   cross-check-only dependencies go to `[project.optional-dependencies]`.
3. **Tests before merge.** New behavior = new test. Bug fix = regression test.
4. **Never weaken a check.** If a test "fails", fix the cause, not the test.

## Setup

```bash
git clone https://github.com/k1ddy/kz-identifiers.git
cd kz-identifiers
make install     # editable install + dev + crosscheck extras
```

## Workflow

```bash
make test        # pytest with coverage
make lint        # ruff check + format check
make format      # auto-fix + format
make check       # lint + test + build (pre-PR gate)
```

## Commit style

[Conventional Commits](https://www.conventionalcommits.org/):

```
feat(iin): add generate_iin(sex=...)
fix(iban): reject 21-char strings with letters in bank position
docs: verification status with external vectors
test: cross-reference against python-stdnum
refactor: extract _mod97 helper
```

Prefixes: `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`.
Breaking changes: `feat(iban)!: …`.

## Adding a new identifier type

1. New module under `src/kz_identifiers/` with a spec reference in the docstring.
2. Re-export from `__init__.py` (keep `__all__` in sync).
3. Tests: valid vectors (real ones if obtainable), invalid mutations,
   negative examples, and — where possible — a cross-reference against an
   independent implementation (see `tests/test_cross_reference.py`).
4. Update README tables (Features, API reference, Verification status).

## Cross-checks

Optional checks against `python-stdnum` run only when the package is installed:

```bash
pytest -m crosscheck -q
```

CI installs the `crosscheck` extra, so these run there too.

## Releases

Maintainer-only: bump version in `pyproject.toml`, update `CHANGELOG.md`,
`make publish-test` → verify install from TestPyPI → upload to PyPI.
