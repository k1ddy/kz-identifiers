from __future__ import annotations

import random
import sys

from kz_identifiers import (
    generate_card,
    generate_iin,
    is_valid_iin_checksum,
    luhn_ok,
    normalize_phone,
    parse_iban,
    parse_iin,
    validate_iban,
    validate_iin,
)


def main() -> int:
    rng = random.Random(1)

    iin = generate_iin(rng=rng)
    print(f"IIN: {iin}  valid={validate_iin(iin)}")
    info = parse_iin(iin)
    print(f"     birth={info.birth_date} sex={info.sex} check={info.check_digit}")

    # checksum не зависит от «валидности даты»
    checksum_only = "000000300005"
    print(f"checksum-only: {checksum_only} -> {is_valid_iin_checksum(checksum_only)}, "
          f"validate_iin -> {validate_iin(checksum_only)}")

    iban = "KZ86125KZT5004100100"
    print(f"IBAN: {iban} valid={validate_iban(iban)} {parse_iban(iban)}")

    card = generate_card(rng=rng)
    print(f"CARD: {card} luhn={luhn_ok(card)}")

    print(f"PHONE: '+7 701 555-12-34' -> {normalize_phone('+7 701 555-12-34')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
