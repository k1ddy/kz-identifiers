"""Паспортные номера — только структурная проверка (контрольных разрядов нет).

    РК, внутренний (удостоверение личности):  8-9 цифр;
    РК, загранпаспорт:                        буква + 7 цифр (напр. N1234567), возможно с разделителем;
    РФ, паспорт:                              4 цифры серии + 6 цифр номера с разделителем (напр. 45 10 123456).

Структуры соответствуют regex, принятым в продуктиве pii-шлюза;
финальную сверку с adilet вынести в релиз-ноты (см. README «Статус верификации»).
"""

import re

RE_KZ_ID = re.compile(r"^\d{8,9}$")
#: загран: буква + 7 цифр (N1234567) либо буква + 2 цифры + (пробел) + 6 цифр
RE_KZ_TRAVEL = re.compile(r"^(?:[A-Z]\d{7}|[A-Z]\d{2}\s?\d{6})$")
RE_RF = re.compile(r"^\d{2}\s\d{2}\s\d{6}$")


def validate_kz_passport(value: str) -> bool:
    return bool(RE_KZ_ID.match(value.strip()))


def validate_kz_travel_passport(value: str) -> bool:
    return bool(RE_KZ_TRAVEL.match(value.strip().upper()))


def validate_rf_passport(value: str) -> bool:
    return bool(RE_RF.match(value.strip()))
