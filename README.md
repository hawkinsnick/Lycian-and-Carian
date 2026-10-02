# Lycian, Carian and Milyan source corpus

**1.0.0 — a reproducible eDiAna source snapshot and research toolkit.**

A free, attributed dataset for examining inscriptions, preserving source
readings and annotations and preparing reproducible research. The three
languages remain separate. This release captures the selected public eDiAna
catalogue completely; it does not claim to be an exhaustive world corpus or
an independently reviewed critical edition.

| Partition | Digital catalogue entries | Source text rows | Conservative source-string tokens |
|---|---:|---:|---:|
| Lycian (2017 archival source) | 187 | 1,412 | 3,433 |
| Carian (2022 source) | 264 | 448 | 681 |
| Milyan / Lycian B (2021 source) | 2 | 114 | 546 |

The 453 entries include one deleted Carian entry, six entries with source-marked
uncertain readings/directions and one aggregated Lycian coin-legend group.
These eight entries remain inspectable but are excluded from default frequency.
Eighteen Greek-script Lycian rows are also excluded. Catalogue entries are
not a verified count of physical monuments. Counts of independent witnesses
remain unknown.

Download [the 1.0.0 ZIP](https://github.com/hawkinsnick/Lycian-and-Carian/releases/tag/v1.0.0),
unzip it and open a terminal in the extracted folder. Python 3.10+ is sufficient;
no third-party packages or network access are needed for analysis and validation.

```bash
python -m corpuskit validate
python -m corpuskit audit
python -m corpuskit search 'sδi' --language carian
python -m corpuskit search 'prñnawatẽ' --language lycian
python -m corpuskit frequency --language lycian
python -m corpuskit frequency --language carian
python -m corpuskit frequency --language milyan
python -m corpuskit verify-export exports
python scripts/release_check.py
```

Use [corpus JSON](exports/corpus.json), [JSONL](exports/corpus.jsonl),
[line CSV](exports/lines.csv), and [the audit](exports/audit.json).
Each line retains its source locator, exact text, analytical eligibility and
upstream surface/segmentation/lemma/translation/POS/morphology table rows.
Conservative frequency counts unmarked source strings, not native signs,
phonemes or reconstructed words. It excludes damage and supplied readings.

Read [the researcher workflow](docs/RESEARCHER_WORKFLOW.md),
[method](docs/METHOD.md), [coverage and source policy](docs/COVERAGE.md),
[source credits](NOTICE), and [family cross-references](research/family/README.md).
Data and documentation are CC BY-SA 4.0; code is MIT. Academic and commercial
reuse are permitted with the respective licence obligations.

A 1.0 release means this source snapshot, adapters, exclusions and exports
are tested and reproducible. Current readings, object identities, completeness
beyond this catalogue and independent epigraphic review remain separate gates.
