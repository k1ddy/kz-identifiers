import datetime as dt
import random

from kz_identifiers import bin_check_digit, generate_bin, parse_bin, validate_bin


def test_bin_check_digit_same_rule_as_iin():
    assert bin_check_digit("00122530123") == \
        sum(int(d) * (i + 1) for i, d in enumerate("00122530123")) % 11


def test_generated_bin_roundtrip():
    rng = random.Random(42)
    for _ in range(100):
        b = generate_bin(rng=rng)
        assert validate_bin(b)
        assert validate_bin(b, strict_facets=True)


def test_bin_facets():
    info = parse_bin(generate_bin(registered_on=dt.date(2018, 3, 15), entity_type=4,
                                  subdivision=1, serial="12345"))
    assert info.valid
    assert info.registration_date == (2018, 3)
    assert info.entity_type == 4
    assert info.subdivision == 1
    assert info.serial == "12345"


def test_iin_type_digit_rejected_in_strict_mode():
    # a5 = 1 в БИН невозможен (исключён правилами): фасеты валидны, checksum валидна — strict отвергает
    first11 = "1804" + "1" + "0" + "00001"
    cd = bin_check_digit(first11)
    candidate = first11 + str(cd)
    assert bin_check_digit(first11) is not None
    assert not validate_bin(candidate, strict_facets=True)


def test_typo_invalid():
    b = generate_bin(rng=random.Random(5))
    broken = b[:-1] + str((int(b[-1]) + 3) % 10)
    assert not validate_bin(broken)
