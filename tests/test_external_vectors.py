"""Внешние векторы: номера из открытых источников, не сгенерированные нами.

Политика repo: настоящие ИИН не публикуются. Сервисы проверки контрагентов
Казахстана следуют тому же правилу — adilet.kz: «ИИН физических лиц не
отображается никогда». Поэтому векторы берутся ТОЛЬКО из случаев, где номер
уже опубликован самим автором как пример в открытом коде или реестре, и каждый
вектор несёт provenance. Все эти номера прошли через реализацию автора примера,
а не через нашу.

БИН — не персональные данные (идентификатор юрлица), их объём берётся из
открытых реестров напрямую.
"""
from __future__ import annotations

from kz_identifiers import parse_bin, parse_iin, validate_bin, validate_iin

# --- ИИН: внешние векторы из чужих репозиториев ------------------------------
# (источник, номер, что проверяем)
IIN_VECTORS = [
    # ZhymabekRoman/kz-iin-validator — пример из README (Python)
    ("ZhymabekRoman/kz-iin-validator README", "061211600012"),
    # ZhymabekRoman/kz-iin-validator — примеры извлечения из текста
    ("ZhymabekRoman/kz-iin-validator README (extract demo)", "251112401047"),
    ("ZhymabekRoman/kz-iin-validator README (extract demo)", "700911204362"),
    # toleubekov/check-iin-kaz — пример из README (Go)
    ("toleubekov/check-iin-kaz README", "031231500126"),
    # agatai20agatai-tech/kz-utils — пример из README (TypeScript)
    ("agatai20agatai-tech/kz-utils README.ru.md", "850101123458"),
]


def test_external_iin_vectors_validate():
    for source, iin in IIN_VECTORS:
        assert validate_iin(iin), f"{source}: {iin} не прошёл checksum"


def test_external_iin_vectors_match_source_semantics():
    """Проверяем не только checksum, но и смысл, заявленный автором примера."""
    # 031231500126 — пример из Go-библиотеки с извлечением демографии
    info = parse_iin("031231500126")
    assert info.valid and info.birth_date is not None
    # 850101123458 — пример из kz-utils
    info2 = parse_iin("850101123458")
    assert info2.valid


# --- БИН: векторы из открытых реестров --------------------------------------
BIN_VECTORS = [
    # org-id.guide (KZ-BIN list) — примеры схемы идентификаторов
    ("org-id.guide/list/KZ-BIN", "950440001673"),
    ("org-id.guide/list/KZ-BIN", "990940003030"),
    ("org-id.guide/list/KZ-BIN", "000640002067"),
    # ifin.kz / myqaz.kz / ba.prg.kz — публичные реквизиты Kaspi Bank
    ("ifin.kz (Kaspi Bank)", "971240001315"),
    # b2b.telecom.kz — публичные реквизиты Казахтелекома
    ("b2b.telecom.kz (Казахтелеком, голова)", "941240000193"),
    ("b2b.telecom.kz (Казахтелеком, филиал)", "250141018288"),
]


def test_external_bin_vectors_validate():
    for source, b in BIN_VECTORS:
        assert validate_bin(b), f"{source}: {b} не прошёл checksum"


def test_external_bin_facets_decode():
    for source, b in BIN_VECTORS:
        info = parse_bin(b)
        assert info.valid
        assert info.entity_type in (4, 5, 6), f"{source}: неожиданный тип {info.entity_type}"


def test_bin_coverage_note():
    """Покрытие фасетов публичными векторами: тип 4 и подразделения 0/1.

    Типы 5 (нерезидент) и 6 (ИП) публичными примерами не покрыты — фиксируем
    честно, расширение возможно при появлении sourced-номеров.
    """
    types = {parse_bin(b).entity_type for _, b in BIN_VECTORS}
    assert 4 in types
