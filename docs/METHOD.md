# Method and admission boundaries

Every reading is attributed to a source, and every source has a reproducible
locator and checksum. Original source snapshots are preserved. Derived records
replay offline; a checksum demonstrates byte integrity, not correctness of an
ancient reading. Unknown physical-object counts remain null.

The JSON line order preserves the source response or printed reading order;
line labels are retained without renumbering physical lines. A source row may
be a comment, header, joined line group, or alphabetic parallel. JSON, JSONL
and CSV exports preserve the same text and source locators. Raw source files
in `data/raw` and page evidence in `data/source-evidence` remain available
in the repository and release archive.

Frequency is explicitly the count of *whole unmarked source strings*, not
phonemes, native glyphs, reconstructed words, or independently verified
readings. Spelling, case and Unicode composition remain unchanged. Source
clitic strings containing `=` count once. Whitespace, `:` and `|` delimit
source strings; this does not assert an ancient word boundary. Damage,
restoration brackets, uncertainty marks, underdots, unexplained glyphs and
editorial numerals block the whole affected string; missing letters are never
silently stripped and fragments are never joined across gaps.

Native family reports retain their own units and acceptance gates. Their
snapshots are pinned by commit and hash. Research and geographic links create
zero independent witnesses and imply neither language identity nor a mapping
between signs. No training/evaluation split or decipherment benchmark is
claimed. A language partition must be selected for frequency; there is no
pooled cross-language frequency command.

## eDiAna adapter

The public catalogue's `docid`/`langid` spans define membership. The public
corpus interface sends POST requests to `includes/api.php`; these requests
were reproduced with explicitly selected catalogue IDs in batches of 15.
No login-only or internal content was requested. Saved request forms, IDs,
responses, hashes and dates are in the acquisition ledger. All 453 returned
IDs must reconcile exactly, once, within their language namespaces.

The source's `sentence` string is the text representation. Empty/null strings
are retained in the original snapshot and do not create text rows. Header
labels and principal-edition references remain source metadata. Six-row HTML
annotation tables are parsed as lists of cells in source order: surface,
segmentation, lemma, translation, POS and morphology. Cells preserve source
content, including empty cells and repeated clitic columns; no new token
alignment is inferred from the annotation columns.

The exact source title flags deleted entries, uncertain readings/directions
and the aggregate Coin Legends entry. These are not silently removed from
catalogue coverage. Lycian rows consisting of Greek letters are screened as
Greek-script parallel candidates, except theta/tau, which also occur in
Lycian transliteration conventions. This conservative screen does not prove
language identity. Mixed Latin/Greek transliteration rows remain attributed
to their source partition; unsupported signs and uncertainty block affected
strings individually. Known Greek strings do not contribute Lycian tokens.

The source index is archival for Lycian. A complete capture of it does not
mean that later discoveries or revisions are complete. Source partitions
are digital data assertions, not a claim that every line is a verified
monolingual text. Character-level sign comparisons require separate,
source-supported inventories and mappings that are not supplied by this release.
