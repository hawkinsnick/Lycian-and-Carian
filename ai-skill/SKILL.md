---
name: lycian-and-carian-research
description: Evidence-first AI research skill for the Lycian and Carian corpus.
version: 0.3.1
---

# Lycian and Carian Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization, computational derivation, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, or rights.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Corpus-specific caution
Treat Lycian and Carian as distinct corpora/languages even when co-housed; preserve language-specific provenance and do not merge correspondences or analyses without explicit justification.

## Default research response
Give the direct answer, followed as relevant by Evidence; Evidentiary status; Uncertainty/limitations; Reproducibility; Rights/attribution.

## Synchronization
Read `ai-skill/generated/source-state.json` before substantive work. It records the corpus commit from which the AI-facing package was synchronized. Generated files are rebuildable views; canonical corpus files govern if a discrepancy is found.

## Academic-scrutiny gates
- Lycian, Carian and Milyan remain separate analytical partitions
- Digital catalogue entries are not verified physical monument counts
- Source annotation columns and duplicated clitic columns are not independent occurrences
- Frequency counts source strings, not phonemes, native signs or reconstructed words
- Upstream lemmata, translations, POS and morphology remain attributed source assertions


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. It searches only files explicitly admitted by `research/browser-sources.json`. Browser admission requires rights/provenance review; never recursively ingest restricted or raw upstream material. Display does not establish decipherment, source independence, or expert validation.


## Linear A method-parity gate
This corpus has reached the machine-resolvable method-parity baseline for its current lawful eDiAna evidence layer. Source lineage, partition boundaries, disagreements, component rights, browser/API/exports, validation and review boundaries are explicit. Read `docs/RIGHTS-ONLY-READINESS.md` and `research/residual-blocker-ledger.json`. Do not treat 453 catalogue entries as 453 physical monuments, merge Milyan into Lycian, or count dependent editions as independent confirmation. Further systematic critical collation is rights/access bound.
