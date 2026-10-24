# Combine the shared Milyan cache without double-counting

The Milyan source cache in this repository is byte-identical to the other project's frozen eDiAna Milyan cache. Its114 nonempty source-text rows are two views of the same digital evidence, not 228 ancient attestations or independent confirmation.

The master now supplies `scripts/prepare_milyan_union.py` and a frozen input manifest. It assembles 114 source-row groups from 228 view rows, retaining both exact file/commit/pointer paths per group. Empty header rows are excluded under a declared source-string rule. Changed caches, hash mismatches and incompatible units are rejected rather than matched semantically.

From a master checkout:

```sh
python scripts/prepare_milyan_union.py --checkouts /path/to/corpora --output /tmp/milyan-union.json
```

Use the [master remediation guide](https://github.com/hawkinsnick/Master-Corpus-AI-Skill/blob/main/references/academic-remediation-2026-10-24.md). The unit is a nonempty digital source-text row, not a physical line, sign, inscription, object or independent witness. Source readings, segmentation and edition collation remain unadjudicated. Preserve CC BY-SA 4.0 and the native eDiAna attribution, edition references and change notices; this output grants no blanket rights to printed editions.
