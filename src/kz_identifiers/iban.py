"""IBAN Казахстана: KZ2!n3!n13!c, 20 символов, контроль MOD-97-10 (ISO 7064).

Структура (SWIFT IBAN Registry, National Bank of Kazakhstan):
    символы 1-2   — код страны KZ;
    символы 3-4   — контрольные цифры IBAN;
    символы 5-7   — идентификатор банка (3 цифры, настоящий БИК);
    символы 8-20  — номер счёта (13 символов, буквенно-цифровой).

Пример из реестра: KZ86125KZT5004100100
(KZ | 86 | 125 | KZT5004100100)

Проверка: переместить первые 4 символа в конец, заменить буквы числами
(A=10 … Z=35), остаток от деления на 97 должен быть равен 1.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass

PATTERN = re.compile(r"^KZ\d{2}\d{3}[A-Z0-9]{13}$")


@dataclass(frozen=True)
class IbanInfo:
    iban: str
    valid: bool
    check_digits: str | None = None
    bank_id: str | None = None
    account: str | None = None


def _to_numeric(s: str) -> str:
    """Буквы → числа (A=10 … Z=35); цифры остаются как есть."""
    return "".join(str(ord(c) - 55) if c.isalpha() else c for c in s)


def _mod97(s: str) -> int:
    """MOD-97 от строки с буквами (ISO 7064): буквы → числа, затем деление на 97."""
    acc = 0
    for ch in _to_numeric(s):
        acc = (acc * 10 + int(ch)) % 97
    return acc


def iban_check_digits(bban: str, country: str = "KZ") -> str:
    """Контрольные цифры IBAN для данного BBAN (98 − MOD97)."""
    bban = bban.replace(" ", "").upper()
    if not re.fullmatch(r"\d{3}[A-Z0-9]{13}", bban):
        raise ValueError("KZ BBAN must be 3 digits (bank) + 13 alphanumerics (account)")
    check = 98 - _mod97(f"{bban}{country}00")
    return f"{check:02d}"


def validate_iban(value: str) -> bool:
    return parse_iban(value).valid


def parse_iban(value: str) -> IbanInfo:
    s = re.sub(r"\s+", "", str(value)).upper()
    if not PATTERN.match(s):
        return IbanInfo(iban=s, valid=False)
    if _mod97(s[4:] + s[:4]) != 1:
        return IbanInfo(iban=s, valid=False)
    return IbanInfo(iban=s, valid=True, check_digits=s[2:4], bank_id=s[4:7], account=s[7:])


def generate_iban(bank_id: str, account: str) -> str:
    """Собрать валидный IBAN из идентификатора банка (3 цифры) и номера счёта (13 символов)."""
    bank_id = str(bank_id).strip()
    account = str(account).strip().upper()
    if not re.fullmatch(r"\d{3}", bank_id):
        raise ValueError("KZ bank identifier is exactly 3 digits")
    if not re.fullmatch(r"[A-Z0-9]{13}", account):
        raise ValueError("KZ account is exactly 13 alphanumerics")
    return f"KZ{iban_check_digits(bank_id + account)}{bank_id}{account}"


def random_iban(*, rng: random.Random | None = None) -> str:
    rng = rng or random.Random()
    bank_id = f"{rng.randint(100, 999)}"
    account = rng.choice(["KZT", "USD", "EUR"]) + f"{rng.randint(0, 10**10 - 1):010d}"
    return generate_iban(bank_id, account)
