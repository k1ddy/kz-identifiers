import random

from kz_identifiers import (
    generate_card,
    is_mobile,
    is_test_card_number,
    luhn_ok,
    normalize_phone,
    validate_kz_passport,
    validate_kz_travel_passport,
    validate_phone,
    validate_rf_passport,
)


def test_luhn_known_vectors():
    assert luhn_ok("4111111111111111")
    assert not luhn_ok("4111111111111112")
    assert not luhn_ok("41111111111111")  # 14 цифр
    assert not luhn_ok("4111-1111-1111-111")  # 15 цифр


def test_generated_cards_valid():
    rng = random.Random(4)
    for _ in range(100):
        c = generate_card("440000", rng=rng)
        assert len(c) == 16 and luhn_ok(c)


def test_test_card_detection():
    assert is_test_card_number(generate_card("411111"))


def test_phone_normalization():
    assert normalize_phone("+7 701 555 12 34") == "+77015551234"
    assert normalize_phone("8(701)555-12-34") == "+77015551234"
    assert normalize_phone("870155512345") is None  # 12 цифр
    assert validate_phone("+77015551234")
    assert is_mobile("+7 701 555 12 34")


def test_passports_structural():
    assert validate_kz_passport("012345678")  # 9 цифр
    assert validate_kz_passport("01234567")  # 8 цифр (старый образец)
    assert not validate_kz_passport("0123456")  # 7 цифр — не паспорт РК
    assert not validate_kz_passport("01234567890")
    assert validate_kz_travel_passport("N1234567")  # буква + 7 цифр
    assert validate_kz_travel_passport("A12 123456")  # серия + номер с разделителем
    assert validate_kz_travel_passport("A12123456")
    assert not validate_kz_travel_passport("1234567")
    assert not validate_kz_travel_passport("1234567")
    assert validate_rf_passport("45 10 123456")
    assert not validate_rf_passport("4510123456")  # без разделителя — это не RF-формат шлюза
