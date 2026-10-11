# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅ |

## Scope

`kz-identifiers` **validates and generates** identifiers. It is a library, it does
not transmit or store anything. Relevant risks:

- **Generated identifiers are not real.** `generate_iin`, `generate_bin`,
  `generate_iban`, `generate_card` produce numbers that pass checksum checks but
  may belong to real people or entities. Use them only in tests, benchmarks and
  synthetic data. Using them against production systems may violate the Law of
  the Republic of Kazakhstan on Personal Data (ст. 12: storage in the RK) and
  banking regulations.
- **Validation ≠ identity.** A valid checksum does not mean the IIN/BIN/IBAN is
  assigned or belongs to the claimant. Identity checks require state registries.
- **Structural weaknesses.** Passport validators are structural only (no check
  digit exists in the spec) — treat their output as "possible", not "valid".

## Reporting a vulnerability

Please **do not** open a public issue for:

- a way to construct a valid identifier for a **specific real** person/entity
  (that is by design of any checksum library — not a vulnerability),
- anything requiring access to state registries.

Do open an issue/PR for: incorrect algorithm, missed input format, false
positives in detection, or license/attribution problems.

Contact: open a GitHub issue with the `security` label.
