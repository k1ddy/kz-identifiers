"""ИИН — индивидуальный идентификационный номер (12 цифр, контрольный разряд).

Структура ИИН (Правила формирования ИИН, adilet V2300032918):
    разряды 1-6  — дата рождения YYMMDD;
    разряд 7     — век и пол: 1/2 — XIX век, 3/4 — XX, 5/6 — XXI
                   (нечётные — мужской, чётные — женский);
    разряды 8-11 — порядковый номер;
    разряд 12    — контрольный.

Контрольный разряд (два цикла, per Правила РК):
    a12 = (a1*1 + a2*2 + ... + a11*11) mod 11
    если 10 — пересчёт с весами 3,4,5,6,7,8,9,10,11,1,2;
    если снова 10 — такой номер не используется (невалиден).
"""

from __future__ import annotations

import calendar
import datetime as _dt
import random
from dataclasses import dataclass

_FIRST_WEIGHTS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
_FALLBACK_WEIGHTS = (3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2)

#: разряд 7 → (полный год столетия, пол)
_CENTURY = {
    1: (1800, "male"),
    2: (1800, "female"),
    3: (1900, "male"),
    4: (1900, "female"),
    5: (2000, "male"),
    6: (2000, "female"),
}


@dataclass(frozen=True)
class IinInfo:
    iin: str
    valid: bool
    birth_date: _dt.date | None = None
    sex: str | None = None
    serial: str | None = None
    check_digit: int | None = None


def _digits(value: str) -> list[int] | None:
    s = value.strip()
    if len(s) != 12 or not s.isdigit():
        return None
    return [int(c) for c in s]


def iin_check_digit(first_11: str) -> int | None:
    """Контрольный разряд для первых 11 цифр; None — номер невозможен (оба цикла дали 10)."""
    if len(first_11) != 11 or not first_11.isdigit():
        raise ValueError("expected 11 digits")
    d = [int(c) for c in first_11]
    t = sum(x * w for x, w in zip(d, _FIRST_WEIGHTS)) % 11
    if t == 10:
        t = sum(x * w for x, w in zip(d, _FALLBACK_WEIGHTS)) % 11
        if t == 10:
            return None
    return t


def is_valid_iin_checksum(value: str) -> bool:
    """Только контрольная сумма (как в детекторах), без валидации даты."""
    d = _digits(value)
    if d is None:
        return False
    expected = iin_check_digit("".join(map(str, d[:11])))
    return expected is not None and expected == d[11]


def parse_iin(value: str, *, check_date: bool = True) -> IinInfo:
    d = _digits(value)
    if d is None:
        return IinInfo(iin=str(value), valid=False)
    s = "".join(map(str, d))
    checksum_ok = is_valid_iin_checksum(s)
    century = d[6]
    if century not in _CENTURY:
        return IinInfo(iin=s, valid=False)
    base, sex = _CENTURY[century]
    year = base + d[0] * 10 + d[1]
    month, day = d[2] * 10 + d[3], d[4] * 10 + d[5]
    date_valid = 1 <= month <= 12 and 1 <= day <= calendar.monthrange(year, month)[1]
    if check_date and not date_valid:
        return IinInfo(iin=s, valid=False, sex=sex, serial=s[7:11])
    birth = _dt.date(year, month, day) if date_valid else None
    valid = checksum_ok and (date_valid or not check_date)
    return IinInfo(iin=s, valid=valid, birth_date=birth, sex=sex, serial=s[7:11], check_digit=d[11])


def validate_iin(value: str, *, check_date: bool = True) -> bool:
    return parse_iin(value, check_date=check_date).valid


def generate_iin(*, birth_date=None, sex=None, serial=None, rng=None) -> str:
    """Сгенерировать валидный ИИН.

    birth_date — date (по умолчанию случайная 1930..2010);
    sex       — 'male'/'female' (по умолчанию случайный);
    serial    — 4 символа (по умолчанию случайный).
    """
    rng = rng or random.Random()
    if birth_date is None:
        start = _dt.date(1930, 1, 1).toordinal()
        end = _dt.date(2010, 12, 31).toordinal()
        birth_date = _dt.date.fromordinal(rng.randint(start, end))
    if sex is None:
        sex = rng.choice(("male", "female"))
    century_digit = {1800: (1, 2), 1900: (3, 4), 2000: (5, 6)}[(birth_date.year // 100) * 100]
    c = century_digit[0] if sex == "male" else century_digit[1]
    for _ in range(1000):
        ser = serial or f"{rng.randint(0, 9999):04d}"
        first11 = f"{birth_date.year % 100:02d}{birth_date.month:02d}{birth_date.day:02d}{c}{ser}"
        cd = iin_check_digit(first11)
        if cd is not None:
            return first11 + str(cd)
    raise ValueError("no valid serial found for this date/century; pass explicit serial")
