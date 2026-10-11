"""Kazakhstan identifiers: validation, parsing and generation.

Modules
-------
iin      — Individual Identification Number (ИИН), 12 digits, check digit (two-cycle per Правила РК)
bin      — Business Identification Number (БИН), 12 digits, 5 facets, check digit
iban     — IBAN for Kazakhstan (KZ2!n3!n13!c, 20 chars, MOD-97-10 / ISO 7064)
cards    — payment cards (16 digits, Luhn / ISO/IEC 7812)
phones   — Kazakhstan phone numbers (+7 7xx xxx xx xx / 8 7xx ...)
passports— passport numbers (KZ internal, KZ travel, RF) — structural only

Sources
-------
IIN check digit: Правила формирования идентификационного номера (Правительство РК,
постановление от 01.09.2023, редакция от 18.10.2017 № 649), см. adilet V2300032918.
BIN structure:   Правила формирования бизнес-идентификационного номера, adilet V2300032918.
IBAN structure:  SWIFT IBAN Registry (National Bank of RK): KZ|20|KZ2!n3!n13!c.

Standard library only. No network, no dependencies.
"""

from .bin import (
    BinInfo,
    bin_check_digit,
    generate_bin,
    parse_bin,
    validate_bin,
)
from .cards import generate_card, is_test_card_number, luhn_ok
from .iban import (
    IbanInfo,
    generate_iban,
    iban_check_digits,
    parse_iban,
    random_iban,
    validate_iban,
)
from .iin import (
    IinInfo,
    generate_iin,
    iin_check_digit,
    is_valid_iin_checksum,
    parse_iin,
    validate_iin,
)
from .passports import (
    validate_kz_passport,
    validate_kz_travel_passport,
    validate_rf_passport,
)
from .phones import PHONE_PATTERN, is_mobile, normalize_phone, validate_phone

__version__ = "0.1.0"

__all__ = [
    "PHONE_PATTERN",
    "BinInfo",
    "IbanInfo",
    "IinInfo",
    "bin_check_digit",
    "generate_bin",
    "generate_card",
    "generate_iban",
    "generate_iin",
    "iban_check_digits",
    "iin_check_digit",
    "is_mobile",
    "is_test_card_number",
    "is_valid_iin_checksum",
    "luhn_ok",
    "normalize_phone",
    "parse_bin",
    "parse_iban",
    "parse_iin",
    "random_iban",
    "validate_bin",
    "validate_iban",
    "validate_iin",
    "validate_kz_passport",
    "validate_kz_travel_passport",
    "validate_phone",
    "validate_rf_passport",
]
