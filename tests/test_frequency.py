"""Эмпирические замеры, на которые ссылается документация.

Каждый тест здесь — это измерение с фиксированным seed, а не оценка на глаз.
Если число в документации расходится с этими тестами — документация неверна.
"""
import random

from kz_identifiers import iin_check_digit, is_valid_iin_checksum, validate_iin


def test_twelve_zeros_pass_checksum_but_not_date():
    assert is_valid_iin_checksum("000000000000") is True
    assert validate_iin("000000000000") is False


def test_random_12digit_checksum_pass_rate():
    """Замер: случайное 12-значное число проходит checksum ~10% (не 1/11=9.09%)."""
    rng = random.Random(20261011)
    n = 200_000
    hits = sum(
        is_valid_iin_checksum("".join(str(rng.randint(0, 9)) for _ in range(12)))
        for _ in range(n)
    )
    rate = hits / n
    assert 0.085 < rate < 0.115, f"rate {rate:.4f} вне допуска — проверь алгоритм"


def test_dead_prefix_found_early_and_always_invalid():
    """Мёртвый префикс (оба цикла = 10) встречается среди первых кандидатов."""
    dead = None
    for n_candidate in range(100_000_000, 200_000_000):
        s = f"{n_candidate:011d}"
        if iin_check_digit(s) is None:
            dead = s
            break
    assert dead is not None
    for last in "0123456789":
        assert not is_valid_iin_checksum(dead + last)


def test_worked_example_from_docs():
    """Ручной расчёт из документации: 90051730114 → контрольный 6."""
    assert iin_check_digit("90051730114") == 6
    assert validate_iin("900517301146")
