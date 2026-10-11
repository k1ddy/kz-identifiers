# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-10-11

First public release.

### Added

- `iin`: validation, parsing (birth date, century, sex), generation; two-cycle
  check digit per Правила формирования ИИН (adilet V2300032918)
- `bin`: validation with 5-facet parsing, generation; same check-digit algorithm
  per Правила формирования БИН (adilet V2300032918)
- `iban`: KZ IBAN (`KZ2!n3!n13!c`, 20 chars) with MOD-97-10 (ISO 7064),
  generation, parsing; accepts print format with spaces
- `cards`: Luhn validation and test-card generation
- `phones`: E.164 normalization and validation
- `passports`: structural validators (KZ internal, KZ travel, RF)
- cross-reference tests: two independent IIN/BIN implementations, real BINs
  (Kaspi Bank, Kazakhtelecom head + branch), SWIFT registry IBAN vector,
  `python-stdnum` cross-checks for IBAN/Luhn
- CI: pytest + ruff on Python 3.9–3.13
- docs: README with API reference, CONTRIBUTING, SECURITY, Makefile

### Fixed

- internal: MOD-97 conversion of IBAN letters (A=10…Z=35) — first draft added
  two-digit letter values as single digits, causing false rejections

### Known limitations

- passport structures follow production regex; final adilet/MVD verification
  planned for 0.2
