# Lycian, Carian and Milyan source corpus


## AI research skill

This corpus project includes a vendor-neutral, evidence-first AI research skill in [`ai-skill/`](ai-skill/). The corpus remains the scholarly source of truth; the skill is an interface, not a second corpus or independent authority.

Researchers can give a capable AI this repository or its AI-ready bundle together with [`ai-skill/SKILL.md`](ai-skill/SKILL.md). The skill preserves provenance, uncertainty, exclusions, source dependence, rights and this project's scientific gates. Check [`ai-skill/generated/source-state.json`](ai-skill/generated/source-state.json) and the generated research-bundle index before substantive use.

For questions spanning corpus projects, use the **Combined Corpus Research AI** in [`combined-ai-skill/`](https://github.com/hawkinsnick/Linear-A/tree/ai-skill-v0.1/combined-ai-skill). It orchestrates registered individual skills without merging their evidence. Membership does not imply linguistic relationship, sign equivalence, chronology, decipherment or independent replication.

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
