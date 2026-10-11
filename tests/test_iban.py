import re

from kz_identifiers import (
    generate_iban,
    parse_iban,
    random_iban,
    validate_iban,
)


def test_registry_example_valid():
    # пример из SWIFT IBAN Registry (National Bank of Kazakhstan)
    assert validate_iban("KZ86125KZT5004100100")


def test_generate_reproduces_registry_example():
    assert generate_iban("125", "KZT5004100100") == "KZ86125KZT5004100100"


def test_spaces_and_case_normalized():
    assert validate_iban("kz86 125 kzt50 0410 0100")


def test_broken_check_digits_invalid():
    assert not validate_iban("KZ87125KZT5004100100")


def test_broken_account_invalid():
    assert not validate_iban("KZ86125KZT5004100199")


def test_gateway_regex_misses_real_iban():
    """Регрессия: в pii-шлюзе regex KZ\\d{2}[A-Z]{4}\\d{13} (21 символ, 4 буквы банка)
    не матчит реальные KZ IBAN — детектор УТЕЧИВАЕТ. Фиксируем баг тестом."""
    gw = re.compile(r"\bKZ\d{2}[A-Z]{4}\d{13}\b")
    assert not gw.search("перевод на KZ86125KZT5004100100")


def test_random_iban_roundtrip():
    import random

    rng = random.Random(11)
    for _ in range(50):
        ib = random_iban(rng=rng)
        info = parse_iban(ib)
        assert info.valid
        assert len(info.iban) == 20
