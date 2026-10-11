"""Ошибочные пути: API должен падать с внятной ошибкой, не молча."""

import pytest

from kz_identifiers import (
    bin_check_digit,
    generate_bin,
    generate_card,
    generate_iban,
    iban_check_digits,
    iin_check_digit,
)


def test_check_digit_rejects_wrong_length():
    with pytest.raises(ValueError):
        iin_check_digit("123")
    with pytest.raises(ValueError):
        bin_check_digit("1234567890123")


def test_iban_check_digits_rejects_bad_bban():
    with pytest.raises(ValueError):  # банк не 3 цифры
        iban_check_digits("12KZT5004100100")
    with pytest.raises(ValueError):  # счёт не 13 символов
        iban_check_digits("125KZT50041001")


def test_generate_iban_rejects_bad_parts():
    with pytest.raises(ValueError):  # банк не 3 цифры
        generate_iban("12", "KZT5004100100")
    with pytest.raises(ValueError):  # счёт не 13 символов
        generate_iban("125", "KZT50041001")


def test_generate_bin_never_returns_invalid_even_after_dead_serial():
    # мёртвый серийный префикс → генератор перебирает серию, а не возвращает мусор
    dead = None
    for n in range(100_000_000, 200_000_000):
        s = f"{n:011d}"
        if bin_check_digit(s) is None:
            dead = s
            break
    assert dead is not None
    import random as _random

    from kz_identifiers import validate_bin

    for _ in range(50):
        b = generate_bin(registered_on=None, serial=dead[6:11], rng=_random.Random())
        assert validate_bin(b)


def test_generate_card_rejects_bad_prefix():
    with pytest.raises(ValueError):
        generate_card("123")  # < 6 цифр
    with pytest.raises(ValueError):
        generate_card("1" * 16)  # >= 16 цифр


def test_generate_bin_rejects_wrong_entity_type():
    with pytest.raises(ValueError):
        generate_bin(entity_type=1)  # 0-3 запрещены правилами
