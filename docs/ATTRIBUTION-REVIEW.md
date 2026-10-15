# Attribution review

All five controls retain partitions and source uncertainty. Global editorial-choice statements do not supply record-specific aligned variants.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| `research/disagreement-register.json/items` | 5 |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'LC-DIS-001'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| LC-DIS-001 | READING_COMPARISON | Direction uncertainty is an inherited source qualification, not an encoded competing direction pair. | Select exact Carian records and cite their direction marks and underlying edition loci. |
| LC-DIS-002 | COVERAGE_GAP | TITUS states editorial selection from Friedrich/critical apparatus; no complete entry-specific two-reading apparatus is encoded by this control. | Locate main-text and apparatus readings at the same locus before claiming a pair. |
| LC-DIS-003 | COUNT_OR_IDENTITY | The 453 digital entries are not a physical-monument census. | Inventory/fragment/face concordances remain required. |
| LC-DIS-004 | CLASSIFICATION | Lycian, Milyan and Carian are distinct native partitions. | Comparison designs must specify language and source units; no merged linguistic inference follows from membership. |
| LC-DIS-005 | COVERAGE_GAP | The later-publication frontier is not a list of fully attributed alternatives. | Acquire publication-specific locators, rights and identity joins for proposed additions. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
