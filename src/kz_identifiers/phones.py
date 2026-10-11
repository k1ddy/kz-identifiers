"""Телефоны Казахстана: +7 7xx xxx xx xx (и запись через 8).

Нормализация к E.164 (+7XXXXXXXXXX). Структурная проверка:
11 цифр, первая 7. Мобильные коды операторов меняются — проверка кода
оператора намеренно отключена по умолчанию.
"""

from __future__ import annotations

import re

#: допускает разделители пробел/тире/скобки, ведущий +7 или 8
PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+7|8)[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{2}[\s\-()]?\d{2}(?!\d)"
)


def normalize_phone(value: str) -> str | None:
    """Привести к E.164 (+7XXXXXXXXXX); None если не телефон."""
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    if len(digits) != 11 or not digits.startswith("7"):
        return None
    return "+" + digits


def validate_phone(value: str) -> bool:
    return normalize_phone(value) is not None


def is_mobile(value: str) -> bool:
    """Мобильный (вторая цифра 7 у казахстанских номеров +7 7xx ...)."""
    n = normalize_phone(value)
    return n is not None and len(n) == 12 and n[2] == "7"
