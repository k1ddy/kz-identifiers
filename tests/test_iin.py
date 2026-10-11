from kz_identifiers import (
    generate_iin,
    iin_check_digit,
    is_valid_iin_checksum,
    parse_iin,
    validate_iin,
)


def _find_dead_prefix():
    """первые 11 цифр, для которых оба цикла дают 10 → номер невозможен"""
    for n in range(100_000_000, 200_000_000):
        s = f"{n:011d}"
        if iin_check_digit(s) is None:
            return s
    raise AssertionError("no dead prefix found")


def test_iin_check_digit_hand_computed():
    # ручной расчёт: 001225301234? берём префикс 00122530123
    # сумма произведений на веса 1..11 по модулю 11, далее финальный разряд
    prefix = "00122530123"
    cd = iin_check_digit(prefix)
    weighted = sum(int(d) * (i + 1) for i, d in enumerate(prefix)) % 11
    assert cd == weighted


def test_generated_iin_roundtrip():
    rng = __import__("random").Random(42)
    for _ in range(200):
        iin = generate_iin(rng=rng)
        assert len(iin) == 12 and iin.isdigit()
        assert validate_iin(iin)
        assert is_valid_iin_checksum(iin)


def test_parse_iin_date_and_sex():
    info = parse_iin(
        generate_iin(birth_date=__import__("datetime").date(1990, 5, 17), sex="female")
    )
    assert info.valid
    assert info.birth_date is not None and info.birth_date.year == 1990
    assert info.sex == "female"
    assert info.check_digit is not None


def test_single_digit_typo_invalid():
    iin = generate_iin(rng=__import__("random").Random(1))
    broken = iin[:-1] + str((int(iin[-1]) + 1) % 10)
    assert not validate_iin(broken)


def test_dead_prefix_invalid():
    prefix = _find_dead_prefix()
    # любой 12-й разряд провалит checksum, т.к. контрольный не определён
    for last in "0123456789":
        assert not is_valid_iin_checksum(prefix + last)


def test_bad_century_digit_invalid():
    iin = generate_iin(rng=__import__("random").Random(7))
    for c in "0789":
        broken = iin[:6] + c + iin[7:]
        assert not validate_iin(broken)


def test_impossible_date_invalid():
    iin = generate_iin(rng=__import__("random").Random(9))  # e.g. YYMMDD
    broken = iin[:2] + "13" + iin[4:]  # месяц 13
    # checksum может случайно совпасть после подмены — тогда валидна только датой не станет
    assert not validate_iin(broken)


def test_short_and_spaces_rejected():
    assert not validate_iin("123")
    assert not validate_iin("1234567890AB")


def test_checksum_only_mode_ignores_date():
    # валидная checksum, но дата 000000: parse_iin → invalid; checksum-only → True
    first11 = "000000" + "3" + "0000"
    cd = iin_check_digit(first11)
    fake = first11 + str(cd)
    assert is_valid_iin_checksum(fake)
    assert not validate_iin(fake)
    assert validate_iin(fake, check_date=False)
