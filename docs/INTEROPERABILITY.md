# Interoperability contract

This repository participates in the **hawkinsnick epigraphic corpus interoperability
contract 1.0.0**. The contract is intentionally narrower than a universal epigraphic
ontology: it defines the semantics that sibling corpora may safely rely on without
erasing project-specific source models.

Machine-readable form: `schemas/interoperability-contract.json`.

## Stable semantics

- Every analytical text remains source-attributed and tied to reproducible evidence.
- Checksums establish source-byte integrity, not correctness of a reading.
- Uncertainty is preserved rather than silently normalized away.
- Unknown physical-object or witness counts remain unknown; catalogue rows and
  alternate editions are never promoted to independent witnesses by counting them.
- Language/script partitions remain explicit. Cross-project links, geographic
  proximity, or visual resemblance do not establish language identity, sign
  equivalence, decipherment, or additional witnesses.
- Cross-language pooling is opt-in and must be justified by the downstream study.
- `analysis_eligible` is a documented admission decision, not a claim that a
  reading is linguistically correct.

## Compatibility boundary

Sibling projects may use different `record_unit` values because their sources expose
different evidence units. Consumers must inspect `project.json.record_unit` and must
not equate a digital catalogue entry with an attributed reading version or physical
inscription.

This contract governs interoperability only. Project-specific METHOD, COVERAGE,
source locks, and evidence remain authoritative for corpus-specific interpretation.
