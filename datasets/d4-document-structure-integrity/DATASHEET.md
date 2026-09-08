# D4 - Document-structure Integrity (datasheet)

**Version** 1.1 | **Schema** 0.2

Translating a document should preserve its structure as well as its text. This dataset checks the arrangement of elements such as headings, paragraphs and lists, the structure of tables, and the destinations of links and images in translated HTML.

The documents are built from software translation examples placed in a small set of templates. Automated checks compare the original and translated structures and check that the document follows the required syntax. They do not assess visual appearance or translation accuracy. Moving translated text into the wrong paragraph or table cell can still pass if the structure stays the same.

## How to use this dataset

1. Download and unpack the dataset. Start with `data/dev.jsonl`, which includes reference translations for trying out the checks.
2. Test document translation workflows that accept and return HTML. Use the structural results alongside checks of translation quality and visual appearance.
3. Run the scoring function described below on the translated output. Test inputs do not include all the reference information needed for official scoring.

## Task and scoring

Translate document text and return XML-well-formed HTML. Call `score_item(record,
hypothesis)` in `documents.py`. `tree_match` compares element paths and tag
names, including parentage and sibling order. `block_order` compares selected block
tags. `table_cells` checks every row, cell type and row/column span. `links_images`
binds each href/src to its element path and preserves multiplicity. `segment_map`
compares positions of non-whitespace text nodes. The gate `roundtrip_valid`
means XML parse success; it does not execute an extraction-and-reconstruction workflow.
Tag case and formatting whitespace may vary. Source signatures use version 2 (record
schema 0.2).

A pass means that the implemented checks were satisfied. Report the pass rate with its denominator and scorer version; it is not an overall translation-quality score.

## MDC technical summary

- Domain: machine-translation quality evaluation for document-structure
  preservation.
- Size: 1,440 records; the open archive contains the dev split (with
  references), the test inputs, the contrastive pairs, README, this datasheet,
  third-party notices, manifest, and Croissant metadata.
- Structure: JSONL records with source and target HTML, a structural
  signature of element paths, tag names and text-node positions, link and image
  targets, expected invariants, error-category tags, split, and provenance.
- License: CC-BY-4.0 open layer; upstream attributions in
  `THIRD_PARTY_NOTICES.md`.
- Dataset on MDC (download the open layer): https://mozilladatacollective.com/datasets/cmr0moi2k01c0mk07eocv137z

## Independent evaluation

Test references and the hidden split are withheld from the open archive. This reduces direct exposure of evaluation answers; it does not guarantee unseen inputs or absence of training overlap, particularly where upstream data is public. Disclose training and tuning on benchmark or upstream material. For evaluation on retained records, contact Prompsit at info@prompsit.com.

## Contents and splits

| Split | File | Records | What it contains |
|---|---|---|---|
| Open dev | `data/dev.jsonl` | 144 | inputs plus the reference translation and labels |
| Test inputs | `data/test.input.jsonl` | 1,008 | inputs only; references withheld |
| Test references | `data/test.ref.jsonl` | 1,008 | withheld, retained by Prompsit |
| Hidden | - | 288 | never distributed |
| Contrastive | `data/contrastive.dev.jsonl` | 864 | reference and damaged output pairs from dev, with rejection checked by the scorer |

160 sources x 9 languages = **1,440 records**. Split ~10% dev / 70% test / 20%
hidden (sources: 16 / 112 / 32), partitioned by `item_id`, so a source and its
nine translations never cross splits.

No training set is shipped. The dev split is a small labelled set for optional
few-shot prompting or sanity checks; it is not required to run the benchmark.

## Languages

`en` into `ca, es, fr, it, pt-PT, de, nl, pl, ru`. Every source document is
present in all nine languages with the same intended document tree. Report each language separately with its sample size.

## Error categories

Every record is tagged with the error categories it can expose; the scoring
script evaluates overlapping constraints and returns diagnostic categories. Severity is
reported alongside a failure for error analysis; it does not change the
pass/fail rule.

| Error category | What it means | Severity | Records |
|---|---|---|---|
| `lost_or_duplicated_node` | a node from the source tree is missing or duplicated | Major | 1,152 |
| `block_order_change` | block elements appear in a different order | Major | 1,152 |
| `table_cell_corruption` | a table's rows-by-columns shape changed | Major | 1,152 |
| `broken_link_image` | an href or src no longer matches the source verbatim | Major | 1,152 |
| `roundtrip_failure` | the output is no longer well-formed XML | Critical | 1,152 |

At least 400 records per error category (a construction quota, not a guarantee of statistical reliability). Each error category is exercised in all 1,152 dev+test
records; the 288 hidden records are additional.

## Sample records

Real records from the open dev split, truncated for width. Angle brackets in
markup are shown as ⟨ ⟩ because this platform strips raw HTML-like tags; the
data files contain the ordinary characters.

| item_id | target | source text | target text | structure profile | error categories |
|---|---|---|---|---|---|
| d4-000023 | ca | ⟨html⟩⟨body⟩ ⟨h1⟩{COUNT, plural, =1 {an address} other {# addresses}}⟨/h1⟩ ⟨p⟩{MINUTES, plural, =1 {1m} other {#m}}⟨/p⟩... | ⟨html⟩⟨body⟩ ⟨h1⟩{COUNT,plural, =1{1 adreça}other{# adreces}}⟨/h1⟩ ⟨p⟩{MINUTES,plural, =1{1 m}other{# m}}⟨/p⟩... | h1 p h2 p ul(3) p+a table(2x2) img | lost_or_duplicated_node, roundtrip_failure |
| d4-000025 | ca | ⟨html⟩⟨body⟩ ⟨h1⟩⟨xliff:g id="numprocess"⟩%1$d⟨/xliff:g⟩ process and ⟨xliff:g id="numservices"⟩**%2$d**⟨/xliff:g⟩ service⟨/h1⟩ ⟨h2⟩{COUNT, plural, =1 {Item} other {# items}}⟨/h2⟩... | ⟨html⟩⟨body⟩ ⟨h1⟩⟨xliff:g id="NUMPROCESS"⟩%1$d⟨/xliff:g⟩ procés i ⟨xliff:g id="NUMSERVICES"⟩**%2$d**⟨/xliff:g⟩ servei⟨/h1⟩ ⟨h2⟩{COUNT,plural, =1{Element}other{# elements}}⟨/h2⟩... | h1 h2 p p ul(3) table(2x2) p+a img | block_order_change, table_cell_corruption |
| d4-000066 | ca | ⟨html⟩⟨body⟩ ⟨h1⟩MIDI Input on Channel=%s Message=%s⟨/h1⟩ ⟨p⟩at ⟨xliff:g id="time" example="2:33 am"⟩**%s**⟨/xliff:g⟩⟨/p⟩ ⟨h2⟩⟨xliff:g id="extension" example="PDF"⟩`%1$s`⟨/xliff:g⟩ file⟨/h2⟩... | ⟨html⟩⟨body⟩ ⟨h1⟩Entrada de MIDI al Canal=%s Missatge=%s⟨/h1⟩ ⟨p⟩a les ⟨xliff:g id="TIME"⟩**%s**⟨/xliff:g⟩⟨/p⟩ ⟨h2⟩Fitxer ⟨xliff:g id="EXTENSION"⟩`%1$s`⟨/xliff:g⟩⟨/h2⟩... | h1 p h2 p table(2x2) ul(3) p+a img | broken_link_image, block_order_change |

The structure profile column lists the block sequence of the document: the
three documents above share the same building blocks (headings, paragraphs, a
three-item list, a 2x2 table, a link, an image) but arrange them in different
orders, which is exactly what the `block_order` check must track.

## Source data and licenses

| Content | License | Structure |
|---|---|---|
| Human translations (shared with the D1 inline-asset dataset) | per-segment (Apache-2.0 / BSD-3-Clause / MIT, inherited) | templated HTML (headings, paragraphs, list, table, link, image) |

The text is human parallel translation; the structural scaffolding is
templated, and the structure is exactly what this dataset scores. Upstream
attribution notices accompany the release in `THIRD_PARTY_NOTICES.md`.

## Construction method

1. **Segment pool**: human translation segments shared with the D1
   inline-asset dataset; each segment exists in English plus all nine target
   languages.
2. **Composition**: `build_dataset.py` assembles each document from those
   segments on a fixed template - headings, paragraphs, a three-item list, a
   2x2 table, a link, and an image - with the block order varied between
   documents.
3. **Reference labels**: a structural signature of element paths, tag names and text-node positions, the block sequence, per-table shapes, and the link and
   image targets are extracted deterministically from the source; the checks
   compare the output against this fingerprint.
4. **Splits**: ~10/70/20, partitioned by `item_id`.

## Dataset-quality checks

K1 measures separation between controlled corruption baselines under the implemented scorer. It supports sensitivity to those perturbations, not a general claim about MT systems. K2 measures false rejections among tested legal variants. Zero observed flips is not proof that every correct human translation will pass. Reference self-consistency is a separate check and is not independent human validation. The existing paired-bootstrap results resample records; shared sources and reused carriers limit their interpretation.

| Check | Result |
|---|---|
| Discrimination (K1) | **PASS** on the packaged synthetic corruption baselines; see `k1_report.json` in the code repository for per-class results. These are not live MT system scores. |
| False positives (K2) | **PASS** - 0 flips over 7,200 tested legal variants (0.0%) |
| Reference self-check | 1,440/1,440 - every retained reference (dev, test and hidden) passes the scoring script |
| Croissant 1.0 | `croissant.json`, mlcroissant-validated |

## Reproducibility

The build is deterministic and seeded; rebuilding produces a bit-identical
package, and `checksums.sha256` (included in the archive) verifies a download.
Documents are composed from the D1 translation segments, most of which are
withheld, so the open layer alone does not regenerate the test and hidden
splits.

The scoring script and the full build pipeline are open-source at
https://github.com/Prompsit/integrity-mt-benchmark - the dataset content itself is
distributed here on MDC.

## Scope boundaries

- A small generated template family, not arbitrary browser HTML, DOCX or PDF.
- Structural signatures do not verify which translated meaning belongs in each cell or paragraph. Swapping text between occupied nodes can pass.
- Translation accuracy, fluency, visual layout, CSS, scripts and general attribute preservation are not scored.
- `roundtrip_valid` is a retained API name for XML well-formedness; no browser rendering or document-tool round trip is tested.

## Related work

This datasheet follows the structure proposed in Datasheets for Datasets
(Gebru et al., https://arxiv.org/abs/1803.09010). The error categories map to
the locale, terminology and markup branches of the MQM error typology
(https://themqm.org/), turned from human
annotation tags into automated checks.

CzechDocs (https://arxiv.org/abs/2606.20212) targets format-preserving
document translation (HTML/DOCX/PDF) with parallel data and a planned
shared task, and DocHPLT (WMT 2025, https://aclanthology.org/2025.wmt-1.17/)
provides document-level parallel data. This dataset differs in what it
measures: an automatic pass/fail score for whether the document tree
(nodes, block order, table shape, links and images) survives translation.

## Record metadata

Reference-bearing records contain reference translations and expected values or structural metadata needed by the scorer. Test inputs omit withheld answer fields. `failure_opportunity_tags` identify intended test opportunities; they are not human error annotations. `oracle_validated` records automated self-consistency, not independent linguistic review. Total dataset counts include withheld records and therefore exceed the number of open reference-bearing records.
