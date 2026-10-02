# Reusable eDiAna adapter specification

This directory documents the reusable parts of the eDiAna ingestion path used by this corpus.

The adapter pattern is intentionally language-parameterized. It separates:
- public catalogue membership,
- acquisition batches,
- raw source bytes and checksums,
- source row parsing,
- corpus-language partitioning,
- conservative token eligibility,
- provenance/export validation.

## Safe reuse

A new eDiAna-backed corpus must supply its own:
1. language identifiers and catalogue scope,
2. source-index reconciliation,
3. source rights/redistribution record,
4. transliteration conventions,
5. script/language screening rules,
6. tests for known edge cases.

Do **not** copy Lycian-specific Greek-parallel screening or token conventions blindly into Lydian, Sidetic, Pisidian, Luwian, or Palaic.

The implementation in `corpuskit/core.py` is the reference behavior for the current Lycian/Carian/Milyan snapshot. The Corpus Factory should reuse the acquisition/replay architecture while injecting language-specific policy.
