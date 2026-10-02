# Researcher workflow

1. Download and unzip the release, or clone this repository. Python 3.10 or
   newer runs the tools without installing extra packages. Open a terminal in
   the folder containing `VERSION` and `corpuskit`.
2. Run `python -m corpuskit validate` and
   `python -m corpuskit verify-export exports`. Both should report `valid: true`.
3. Read `exports/audit.json` and `NOTICE` before selecting records. The release
   number describes a tested source snapshot and toolkit; it is not a claim of
   exhaustive coverage, a settled reading, or decipherment.
4. Use `exports/corpus.json` for nested records, `corpus.jsonl` for streaming,
   or `lines.csv` for line-level work. Keep record IDs, language partitions,
   categories, source URLs, source locators and analytical eligibility.
5. Examine the exact raw response or scanned page before proposing a new
   reading. Record your alternatives as additional attributed versions of the
   same object; do not overwrite the source or create a new witness.
6. Cite the release and original edition. Publish transformations and derived
   datasets under CC BY-SA 4.0 with source attribution and a description of
   changes. Public-domain originals retain their original status; code is MIT.

For an assistant-assisted analysis, supply the selected records together with
`audit.json` and `ATTRIBUTION.md`. A useful prompt is:

> Work only from these records. Retain record IDs and exact source locators.
> Separate language partitions and reading versions. Do not treat excluded or
> uncertain records as established readings. Report missing data as missing.
> Label proposed translations and sign correspondences as hypotheses. For
> every finding, identify the source lines and the reproducible operation.

Verify any generated analysis against the saved source and deterministic
exports. Model-generated readings are not additional epigraphic evidence.
