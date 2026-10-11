"""БИН — бизнес-идентификационный номер (12 цифр, 5 фасетов).

Структура (Правила формирования БИН, adilet V2300032918):
    a1-a4  — год (две последние цифры) и месяц регистрации (YYMM);
    a5     — тип: 4 резидент, 5 нерезидент, 6 ИП(С); резерв 7,8,9
             (цифры 0,1,2,3 исключены — чтобы БИН не совпал с ИИН);
    a6     — признак подразделения: 0 головной, 1 филиал, 2 представительство,
             3/4 крестьянское (фермерское) хозяйство (зависит от редакции);
    a7-a11 — порядковый номер регистрации (5 цифр);
    a12    — контрольный разряд (алгоритм тот же, что у ИИН).
"""

from __future__ import annotations

import datetime as _dt
import random
from dataclasses import dataclass

from .iin import iin_check_digit

ENTITY_TYPES = {4: "resident", 5: "non-resident", 6: "joint-individual-entrepreneur"}
SUBDIVISIONS = {
    0: "head",
    1: "branch",
    2: "representative-office",
    3: "farm-holding",
    4: "farm-holding",
}


@dataclass(frozen=True)
class BinInfo:
    bin: str
    valid: bool
    registration_date: tuple | None = None  # (year, month)
    entity_type: int | None = None
    subdivision: int | None = None
    serial: str | None = None
    check_digit: int | None = None


def bin_check_digit(first_11: str) -> int | None:
    """Контрольный разряд БИН (алгоритм идентичен ИИН)."""
    return iin_check_digit(first_11)


def parse_bin(value: str, *, strict_facets: bool = False) -> BinInfo:
    s = value.strip()
    if len(s) != 12 or not s.isdigit():
        return BinInfo(bin=s, valid=False)
    d = [int(c) for c in s]
    cd = bin_check_digit(s[:11])
    checksum_ok = cd is not None and cd == d[11]
    year, month = d[0] * 10 + d[1], d[2] * 10 + d[3]
    etype, subdiv = d[4], d[5]
    facets_ok = (
        etype in ENTITY_TYPES  # 4..6 (7..9 — резерв, допускаются)
        and 1 <= month <= 12
        and (subdiv in SUBDIVISIONS or not strict_facets)
    )
    if strict_facets and not facets_ok:
        return BinInfo(bin=s, valid=False)
    return BinInfo(
        bin=s,
        valid=checksum_ok and facets_ok,
        registration_date=(2000 + year if year < 40 else 1900 + year, month),
        entity_type=etype,
        subdivision=subdiv,
        serial=s[6:11],
        check_digit=d[11],
    )


def validate_bin(value: str, *, strict_facets: bool = False) -> bool:
    return parse_bin(value, strict_facets=strict_facets).valid


def generate_bin(*, registered_on=None, entity_type=4, subdivision=0, serial=None, rng=None) -> str:
    """Сгенерировать валидный БИН. registered_on — date (по умолчанию случайная 2000..2026)."""
    rng = rng or random.Random()
    if registered_on is None:
        start = _dt.date(2000, 1, 1).toordinal()
        end = _dt.date(2026, 12, 31).toordinal()
        registered_on = _dt.date.fromordinal(rng.randint(start, end))
    if entity_type not in ENTITY_TYPES:
        raise ValueError("entity_type must be 4 (resident), 5 (non-resident) or 6 (joint IE)")
    ser = serial or f"{rng.randint(0, 99999):05d}"
    for _ in range(1000):
        first11 = f"{registered_on.year % 100:02d}{registered_on.month:02d}{entity_type}{subdivision}{ser}"
        cd = bin_check_digit(first11)
        if cd is not None:
            return first11 + str(cd)
        ser = f"{rng.randint(0, 99999):05d}"
    raise ValueError("no valid serial found for this date/type; pass explicit serial")
