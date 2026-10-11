"""Банковские карты: 16 цифр, проверка по алгоритму Луна (ISO/IEC 7812)."""

from __future__ import annotations

import random
import re

RE_CARD = re.compile(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)")


def luhn_ok(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    if len(digits) != 16:
        return False
    total = 0
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            total += d - 9 if d > 9 else d
        else:
            total += d
    return total % 10 == 0


def generate_card(prefix: str = "400000", *, rng: random.Random | None = None) -> str:
    """Сгенерировать номер карты с валидной checksum Луна (для тестов/бенчей)."""
    rng = rng or random.Random()
    prefix = re.sub(r"\D", "", prefix)
    if not 6 <= len(prefix) < 16:
        raise ValueError("prefix must be 6..15 digits")
    body = prefix + "".join(str(rng.randint(0, 9)) for _ in range(16 - len(prefix) - 1))
    total = 0
    for i, ch in enumerate(body):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            total += d - 9 if d > 9 else d
        else:
            total += d
    return body + str((10 - total % 10) % 10)


#: хорошо известные тестовые префиксы (Visa/Mastercard/МИР-разработка)
TEST_PREFIXES = ("411111", "555555", "510510", "400000", "220138")


def is_test_card_number(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    return luhn_ok(value) and any(digits.startswith(p) for p in TEST_PREFIXES)
