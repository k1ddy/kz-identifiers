# kz-identifiers

[![CI](https://github.com/k1ddy/kz-identifiers/actions/workflows/ci.yml/badge.svg)](https://github.com/k1ddy/kz-identifiers/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue)](https://pypi.org/project/kz-identifiers/)
[![Python versions](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.13-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-39%20passed-brightgreen)](#development)

**Validation, parsing and generation of Kazakhstan identifiers.** Zero dependencies,
Python standard library only, fully tested against independent implementations and
real-world identifiers.

`kz-identifiers` exists because Kazakhstan's identifiers (ИИН, БИН, IBAN) are
routinely validated with the wrong algorithms — sending PII to LLM gateways,
filters and ETL pipelines unmasked. The library gives you deterministic,
spec-traceable checks with references to the primary sources.

## Features

| Module | What | Algorithm / spec |
|---|---|---|
| [`kz_identifiers.iin`](#iin--индивидуальный-идентификационный-номер) | IIN (ИИН): validate, parse, generate | two-cycle check digit (per Правила РК) |
| [`kz_identifiers.bin`](#bin--бизнес-идентификационный-номер) | BIN (БИН): validate, parse, generate | 5 facets + check digit |
| [`kz_identifiers.iban`](#iban-казахстана) | IBAN for Kazakhstan | `KZ2!n3!n13!c`, 20 chars, MOD-97-10 (ISO 7064) |
| [`kz_identifiers.cards`](#payment-cards) | payment cards | 16 digits, Luhn (ISO/IEC 7812) |
| [`kz_identifiers.phones`](#phones) | phones | `+7 7xx xxx xx xx` / `8 7xx …`, E.164 normalization |
| [`kz_identifiers.passports`](#passports) | passports (KZ internal, KZ travel, RF) | structural only |

- **Zero dependencies** — standard library only, works offline.
- **Python 3.9 – 3.13.**
- **Checked against independent implementations**: two third-party IIN/BIN
  implementations and `python-stdnum` (IBAN/Luhn), plus real BINs of Kaspi Bank
  and Kazakhtelecom.
- **Negative examples** — generate structurally valid *and* deliberately invalid
  identifiers for PII benchmarks.

## Installation

```bash
pip install kz-identifiers
# from TestPyPI (pre-release):
pip install -i https://test.pypi.org/simple/ kz-identifiers
```

## Quick start

```python
import datetime as dt
from kz_identifiers import (
    validate_iin,
    parse_iin,
    generate_iin,
    validate_bin,
    parse_bin,
    generate_bin,
    validate_iban,
    generate_iban,
    parse_iban,
    luhn_ok,
    generate_card,
    normalize_phone,
)

# --- IIN: validate + parse + generate -------------------------------------
iin = generate_iin(birth_date=dt.date(1990, 5, 17), sex="female")
validate_iin(iin)  # True
info = parse_iin(iin)
info.birth_date  # datetime.date(1990, 5, 17)
info.sex  # 'female'

# checksum only (like PII detectors do), without date validation:
from kz_identifiers import is_valid_iin_checksum

is_valid_iin_checksum("000000300005")  # True — валидная checksum, дата 000000

# --- BIN ------------------------------------------------------------------
bin_info = parse_bin("971240001315")  # Kaspi Bank
bin_info.valid  # True
bin_info.registration_date  # (1997, 12)
bin_info.entity_type  # 4 (resident)
bin_info.subdivision  # 0 (head office)
generate_bin(registered_on=dt.date(2018, 3, 15), entity_type=4)

# --- IBAN -----------------------------------------------------------------
validate_iban("KZ86125KZT5004100100")  # True — пример из реестра SWIFT
iban = generate_iban("125", "KZT5004100100")
iban  # 'KZ86125KZT5004100100'
parse_iban("KZ86 125K ZT50 0410 0100")  # печатный форт с пробелами — тоже валиден

# --- cards, phones ---------------------------------------------------------
generate_card("440000")  # валидный номер для тестов
luhn_ok("4111111111111111")  # True
normalize_phone("+7 701 555-12-34")  # '+77015551234'
```

## Common mistakes this library prevents

1. **KZ IBAN is 20 characters, bank code is 3 digits.** Structure per the SWIFT
   IBAN registry (National Bank of Kazakhstan): `KZ2!n3!n13!c`, e.g.
   `KZ86125KZT5004100100`. A pattern like "letter + 4 letters + 13 digits"
   matches **no real Kazakh IBAN** — a whole class of maskers and validators
   silently misses them. Always verify MOD-97.
2. **IIN is exactly 12 digits with a check digit.** Ten-digit loan and contract
   numbers are not IINs. Use `is_valid_iin_checksum` (checksum only) or
   `validate_iin` (checksum + birth-date plausibility).
3. **BIN ≠ IIN.** In a BIN the 5th digit is never 0–3 (excluded by the rules so a
   BIN can never collide with an IIN). `validate_bin(strict_facets=True)` enforces it.
4. **Phones.** `8 7xx…` and `+7 7xx…` are the same number — normalize before
   comparing.

## API reference

### IIN — индивидуальный идентификационный номер

```python
iin_check_digit(first_11: str) -> int | None   # None = номер невозможен
is_valid_iin_checksum(value: str) -> bool      # только checksum
parse_iin(value: str, *, check_date: bool = True) -> IinInfo
validate_iin(value: str, *, check_date: bool = True) -> bool
generate_iin(*, birth_date=None, sex=None, serial=None, rng=None) -> str
```

Digits 1–6 birth date `YYMMDD`, digit 7 century+sex (1/2 XIX, 3/4 XX, 5/6 XXI;
odd = male, even = female), 8–11 serial, 12 check digit. Source: Правила
формирования ИИН, adilet [V2300032918](https://adilet.zan.kz/rus/docs/V2300032918).

### BIN — бизнес-идентификационный номер

```python
bin_check_digit(first_11: str) -> int | None
parse_bin(value: str, *, strict_facets: bool = False) -> BinInfo
validate_bin(value: str, *, strict_facets: bool = False) -> bool
generate_bin(*, registered_on=None, entity_type=4, subdivision=0, serial=None, rng=None) -> str
```

Facets: `YYMM` registration date, entity type (4 resident / 5 non-resident /
6 joint IE; 0–3 forbidden), subdivision (0 head / 1 branch / 2 representative
office / 4 farm), 5-digit serial, check digit. Source: Правила формирования БИН,
adilet [V2300032918](https://adilet.zan.kz/rus/docs/V2300032918).

### IBAN Казахстана

```python
iban_check_digits(bban: str, country: str = "KZ") -> str
validate_iban(value: str) -> bool
parse_iban(value: str) -> IbanInfo
generate_iban(bank_id: str, account: str) -> str
random_iban(*, rng=None) -> str
```

`KZ2!n3!n13!c`, 20 characters; MOD-97-10 per ISO 7064. Spaces (print format,
groups of 4) are accepted. Source: [SWIFT IBAN Registry](https://www.swift.com/resource/iban-registry-pdf), entry KZ (National Bank of the Republic of Kazakhstan).

### Payment cards

```python
luhn_ok(value: str) -> bool
generate_card(prefix: str = "400000", *, rng=None) -> str
is_test_card_number(value: str) -> bool
```

### Phones

```python
normalize_phone(value: str) -> str | None
validate_phone(value: str) -> bool
is_mobile(value: str) -> bool
```

### Passports

```python
validate_kz_passport(value: str) -> bool            # внутренний: 8–9 цифр
validate_kz_travel_passport(value: str) -> bool     # загран: буква + 7 цифр
validate_rf_passport(value: str) -> bool            # РФ: 4 + 6 цифр с разделителем
```

Structural checks only — passports carry no check digit. KZ passport structures
follow the regex used in production DLP service; vs adilet/MVD — see
[verification status](#verification-status).

## Verification status

All items below are reproducible via `pytest` — see
[`tests/test_cross_reference.py`](tests/test_cross_reference.py):

- [x] IIN/BIN check digit — matches the rules on adilet, the production detector
      implementation, **and two independent implementations** (adilkhash gist;
      ZhymabekRoman/kz-iin-validator). 300 generated IINs validate in all three.
- [x] **External vectors**: IIN `061211600012` (README of the independent library);
      real BINs `971240001315` (Kaspi Bank), `941240000193` and `250141018288`
      (Kazakhtelecom, head + branch — facets decode correctly).
- [x] IBAN/Luhn — cross-checked with `python-stdnum` (2000 valid + 300 mutations).
- [x] Dead-prefix IIN (both cycles give 10) — rejected by all implementations.
- [x] Эмпирические замеры (не оценки): случайное 12-значное проходит checksum в
      **9.95 %** случаев при n=200 000; «мёртвый» префикс находится среди первых
      кандидатов перебора. Формулировки «1/11» и «100 млн вариантов» из ранних
      версий исправлены по этим замерам.
- [ ] Passport structures — production regex; final adilet/MVD check planned for 0.2.

Install the cross-check extras and run:

```bash
pip install -e ".[dev,crosscheck]"
pytest -m crosscheck -q
```

## Development

```bash
make install   # pip install -e ".[dev,crosscheck]"
make test      # pytest + coverage
make lint      # ruff check + ruff format --check
make build     # sdist + wheel
make publish-test  # twine upload --repository testpypi
```

Requirements: Python ≥ 3.9, no runtime dependencies. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Do not use generated identifiers against real systems — they are for tests and
benchmarks only. See [SECURITY.md](SECURITY.md).

## License

Apache-2.0 — see [LICENSE](LICENSE). Commercial use is permitted, including
banking and legal-industry deployments (the Apache patent grant is one reason
this license was chosen).
