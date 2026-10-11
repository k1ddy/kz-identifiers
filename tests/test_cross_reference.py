"""Кросс-проверка против независимых реализаций и реальных номеров.

Reference implementation (vendored to keep CI offline):
  1. adilkhash gist (github) — ИИН/БИН checksum, веса 1..11 и 3..2

External test vectors:
  IIN   061211600012 — пример из README ZhymabekRoman/kz-iin-validator
  BIN   971240001315 — Kaspi Bank (ifin.kz, myqaz.kz, prg.kz)
  BIN   941240000193 — АО «Казахтелеком», головное (b2b.telecom.kz)
  BIN   250141018288 — филиал «Казахтелеком» (b2b.telecom.kz): a6=1
  IBAN  KZ86125KZT5004100100 — пример SWIFT IBAN Registry (НБ РК)
"""
import random

from kz_identifiers import (
    generate_iban,
    generate_iin,
    iin_check_digit,
    is_valid_iin_checksum,
    parse_bin,
    random_iban,
    validate_iban,
    validate_iin,
)


def _reference_checksum_ok(value: str) -> bool:
    """Независимая реализация контрольного разряда (гист adilkhash)."""
    if len(value) != 12 or not value.isdigit():
        return False
    digits = list(map(int, value))
    for weights in ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), (3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2)):
        total = sum(d * w for d, w in zip(digits, weights)) % 11
        if total != 10:
            return total == digits[-1]
    return False


def test_reference_agrees_on_generated_iin():
    rng = random.Random(777)
    for _ in range(300):
        iin = generate_iin(rng=rng)
        assert is_valid_iin_checksum(iin)
        assert _reference_checksum_ok(iin)


def test_external_iin_vector():
    # пример из README независимой библиотеки
    assert validate_iin("061211600012")
    assert _reference_checksum_ok("061211600012")


def test_external_real_bin_vectors():
    bins = {
        # Kaspi Bank — 3 независимых источника
        "971240001315": {"reg": (1997, 12), "entity_type": 4, "subdivision": 0},
        # АО «Казахтелеком», головное предприятие
        "941240000193": {"reg": (1994, 12), "entity_type": 4, "subdivision": 0},
        # филиал «Казахтелеком»: a6=1
        "250141018288": {"reg": (2025, 1), "entity_type": 4, "subdivision": 1},
    }
    for b, expect in bins.items():
        info = parse_bin(b)
        assert info.valid, b
        assert _reference_checksum_ok(b)
        assert info.registration_date == expect["reg"]
        assert info.entity_type == expect["entity_type"]
        assert info.subdivision == expect["subdivision"], b


def test_bin_mutations_rejected():
    for b in ("971240001315", "941240000193", "250141018288"):
        for pos in (0, 4, 5, 6, 11):
            broken = b[:pos] + str((int(b[pos]) + 1) % 10) + b[pos + 1:]
            assert not validate_iin(broken, check_date=False)
            assert not _reference_checksum_ok(broken)


def test_registry_iban_vector():
    assert validate_iban("KZ86125KZT5004100100")
    iban = generate_iban("125", "KZT5004100100")
    assert iban == "KZ86125KZT5004100100"


def test_reference_agrees_on_generated_iban():
    try:
        from stdnum import iban as _si  # type: ignore
    except ImportError:
        import pytest

        pytest.skip("python-stdnum not installed")
    rng = random.Random(2026)
    for _ in range(200):
        ib = random_iban(rng=rng)
        assert validate_iban(ib)
        assert _si.is_valid(ib), ib


def test_iin_dead_prefix_agreement():
    for n in range(100_000_000, 200_000_000):
        s = f"{n:011d}"
        if iin_check_digit(s) is None:
            for last in "0123456789":
                cand = s + last
                assert not is_valid_iin_checksum(cand)
                assert not _reference_checksum_ok(cand)
            return
    raise AssertionError("dead prefix not found")
