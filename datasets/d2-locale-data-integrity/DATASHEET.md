# D2 - Locale-data Integrity (datasheet)

**Version** 1.1 | **Schema** 0.2

Numbers and dates can be written differently across languages and regions. For example, the English decimal number 12.5 is written as 12,5 in French. This dataset checks whether a translation uses an accepted format for the requested language and region.

Each example adds one number, date, currency amount or measurement in square brackets to a sentence from software translation catalogs. Expected formats come from Unicode CLDR, a collection of language and regional conventions. The check covers the bracketed value only. Amounts and units stay the same; currency and measurement conversions are outside the task.

## How to use this dataset

1. Download and unpack the dataset. Start with `data/dev.jsonl`, which includes reference translations for trying out the checks.
2. Test whether translation tools format numbers, dates, currencies and units for the requested language and region. The tool must keep the bracketed value in its output.
3. Run the scoring function described below on the translated output. Test inputs do not include all the reference information needed for official scoring.

## Task and scoring

Translate the sentence and render the final `[...]` slot in the target locale. Call
`score_item(record, hypothesis)` in `validators.py` with a reference-bearing benchmark
record. The `locale_form_conformant` gate compares that slot with accepted renderings of
the record's semantic value. Surrounding prose is not scored. A failed form can match
one of five corruption classes; otherwise the diagnostic is `locale_form_mismatch`.
`missing_entity` means no slot was found. Every current item uses the format track:
amounts and units retain their values, with no exchange-rate conversion or metrication.
Date records do not cover time-of-day translation. A source form identical to an
accepted target form passes.

A pass means that the implemented checks were satisfied. Report the pass rate with its denominator and scorer version; it is not an overall translation-quality score.

## MDC technical summary

- Domain: software localization and machine-translation quality evaluation for
  locale-specific rendering of numbers, dates, currencies, and units.
- Size: 6,120 records; the open archive contains the dev split (with
  references), the test inputs, the contrastive pairs, README, this datasheet,
  third-party notices, manifest, and Croissant metadata.
- Structure: JSONL records with source and target text, source and target
  locales, entity metadata (kind, semantic value, expected rendering, accepted
  variants), expected invariants, error-category tags, split, and provenance.
- License: CC-BY-4.0 open layer; upstream attributions in
  `THIRD_PARTY_NOTICES.md`.
- Dataset on MDC (download the open layer): https://mozilladatacollective.com/datasets/cmr0mnoo201bwmk07nh4yc04u

## Independent evaluation

Test references and the hidden split are withheld from the open archive. This reduces direct exposure of evaluation answers; it does not guarantee unseen inputs or absence of training overlap, particularly where upstream data is public. Disclose training and tuning on benchmark or upstream material. For evaluation on retained records, contact Prompsit at info@prompsit.com.

## Contents and splits

| Split | File | Records | What it contains |
|---|---|---|---|
| Open dev | `data/dev.jsonl` | 630 | inputs plus the reference translation and labels |
| Test inputs | `data/test.input.jsonl` | 4,266 | inputs only; references withheld |
| Test references | `data/test.ref.jsonl` | 4,266 | withheld, retained by Prompsit |
| Hidden | - | 1,224 | never distributed |
| Contrastive | `data/contrastive.dev.jsonl` | 821 | (correct, damaged) minimal pairs from the dev split, each pair separated by the scoring script |

680 sources x 9 locales = **6,120 records**. Split ~10% dev / 70% test / 20%
hidden (sources: 70 / 474 / 136), stratified by error category and partitioned
by `item_id`, so a source and its nine translations never cross splits.

No training set is shipped. The dev split is a small labelled set for optional
few-shot prompting or sanity checks; it is not required to run the benchmark.

## Languages

`en-US` into `ca-ES, es-ES, fr-FR, it-IT, pt-PT, de-DE, nl-NL, pl-PL, ru-RU` -
the same nine-language matrix as the D1 dataset. The dataset is keyed by full
locale rather than language alone, because a language code underspecifies
separators, date patterns, and currency format. Every source is present in all
nine locales with the same embedded value, so per-locale scores are directly
comparable.

## Error categories

Every record is tagged with the error categories it can expose; the scoring
script evaluates overlapping constraints and returns diagnostic categories. Severity is
reported alongside a failure for error analysis; it does not change the
pass/fail rule.

| Error category | What it means | Severity | Records |
|---|---|---|---|
| `wrong_decimal_separator` | the decimal separator is not the target-locale one (comma vs point) | Major | 2,223 |
| `wrong_grouping` | digit grouping is missing or uses the wrong separator for the target locale | Minor | 1,449 |
| `mis_converted_datetime` | the date is not rendered in the target-locale pattern (for example left in the source form) | Major | 1,152 |
| `broken_currency_format` | the currency symbol, code, or its position does not follow the target-locale pattern | Major | 1,152 |
| `wrong_unit_format` | the unit symbol is not the localized form the target locale uses | Minor | 425 |
| `locale_form_mismatch` | failed conformance not matched to a known corruption pattern | Major | diagnostic only |
| `missing_entity` | the output drops the value entirely | Critical | all |

At least 400 records per error category (a construction quota, not a guarantee of statistical reliability). Record counts are over the scored set (the dev and test
splits). Four entity kinds are covered: number (160 sources), currency (160),
date (160), and unit (200). `missing_entity` can occur on any record, since
every record carries exactly one value. `wrong_unit_format` is scoreable in the
four locales where CLDR prescribes a unit symbol different from the English
form (fr-FR, pl-PL, pt-PT, ru-RU); elsewhere the unchanged symbol is the
correct rendering.

## Sample records

Real records from the open dev split, truncated for width. Angle brackets in
markup are shown as ⟨ ⟩ because this platform strips raw HTML-like tags; the
data files contain the ordinary characters.

| item_id | target | source text | target text | entity (input -> expected) | error categories |
|---|---|---|---|---|---|
| d2-000023 | ca | ⟨ahelp hid="..."⟩Sorts the selection from the lowest value to the highest value. You can define the sort rules...⟨/ahelp⟩ ... [£19,999.90] | ⟨ahelp hid="..."⟩Ordena la selecció del valor més petit al més gran. Podeu definir les regles d'ordenació...⟨/ahelp⟩ ... [19.999,90 £] | currency: `£19,999.90 -> 19.999,90 £` | wrong_decimal_separator, wrong_grouping, broken_currency_format |
| d2-000163 | ca | ⟨item type="input"⟩=OFFSET(A1;2;2)⟨/item⟩ returns the value in cell C3 (A1 moved by two rows and two columns down)... [Jul 1, 2024] | ⟨item type="input"⟩=DESPLAÇAMENT(A1;2;2)⟨/item⟩ retorna el valor de la cel·la C3 (A1 desplaçada dues files i dues columnes cap avall)... [1 de jul. 2024] | date: `Jul 1, 2024 -> 1 de jul. 2024` | mis_converted_datetime |
| d2-000321 | ca | ⟨emph⟩Server⟨/emph⟩ is the name of a server application. ⟨item type="productname"⟩%PRODUCTNAME⟨/item⟩ applications have the server name... [1,200,000] | ⟨emph⟩Servidor⟨/emph⟩ és el nom d'una aplicació de servidor. En el cas de les aplicacions de l'⟨item type="productname"⟩%PRODUCTNAME⟨/item⟩... [1.200.000] | number: `1,200,000 -> 1.200.000` | wrong_decimal_separator, wrong_grouping |
| d2-000489 | ca | ⟨ahelp hid=""⟩Enter or edit general information for an ⟨link ...⟩XML filter⟨/link⟩.⟨/ahelp⟩ [350 lb] | ⟨ahelp hid=""⟩Introduïu o editeu la informació general per a un ⟨link ...⟩filtre XML⟨/link⟩.⟨/ahelp⟩ [350 lb] | unit: `350 lb -> 350 lb` (ca-ES keeps `lb`; `350 lliures` also accepted) | missing_entity only (the ca-ES unit symbol is unchanged) |

## Source data and licenses

The sentences that host the values are human translations shared with the D1
inline-asset dataset, drawn from key-aligned localization catalogs; each
record's `provenance` field names its corpus, license, URL, revision, and the
originating D1 item. The expected target-locale forms come from Unicode CLDR
locale data as bundled with Babel 2.18.0.

| Source | License |
|---|---|
| Apache OpenOffice (openoffice-translation) | Apache-2.0 |
| AOSP Settings / frameworks/base | Apache-2.0 |
| Chromium (generated_resources + ui_strings) | BSD-3-Clause |
| DSpace dspace-angular | BSD-3-Clause |
| Unicode CLDR (via Babel 2.18.0) | Unicode-3.0 |

All upstream licenses are permissive and compatible with a CC-BY-4.0 open layer;
upstream attribution notices accompany the release in `THIRD_PARTY_NOTICES.md`.

## Construction method

1. **Sentence selection**: human-translated segments present in EN plus all
   nine target languages, reused from the D1 harvest with their licenses and
   provenance inherited per record.
2. **Value generation**: 680 items - 160 numbers, 160 currency amounts, 160
   dates, 200 unit measures - with values picked deterministically from fixed
   pools, seeded per item.
3. **Rendering**: the source form is produced for en-US and the expected form
   for each target locale from CLDR data via Babel 2.18.0, together with the
   accepted legal variants and, for each applicable error category, a damaged
   form used to build the contrastive pairs.
4. **Injection**: the value is appended to the sentence in a neutral `[...]`
   slot, in the same position in the source and in every reference.
5. **Splits**: ~10/70/20, stratified by error category, partitioned by
   `item_id`.

## Dataset-quality checks

K1 measures separation between controlled corruption baselines under the implemented scorer. It supports sensitivity to those perturbations, not a general claim about MT systems. K2 measures false rejections among tested legal variants. Zero observed flips is not proof that every correct human translation will pass. Reference self-consistency is a separate check and is not independent human validation. The existing paired-bootstrap results resample records; shared sources and reused carriers limit their interpretation.

| Check | Result |
|---|---|
| Discrimination (K1) | **PASS** on the packaged synthetic corruption baselines; see `k1_report.json` in the code repository for per-class results. These are not live MT system scores. |
| False positives (K2) | **PASS** - 0 flips over 20,036 tested legal variants (0.0%) |
| Reference self-check | 6,120/6,120 - every retained reference (dev, test and hidden) passes the scoring script |
| Croissant 1.0 | `croissant.json`, mlcroissant-validated |

## Reproducibility

The build is deterministic and seeded; rebuilding produces a bit-identical
package, and `checksums.sha256` (included in the archive) verifies a download.
The build seed and the locale-data pin (Babel 2.18.0 with
its bundled CLDR) are recorded in `manifest.json`, shipped in the archive.
Rebuilding starts from the reference translations, so the open layer alone
does not regenerate the withheld splits.

The scoring script and the full build pipeline are open-source at
https://github.com/Prompsit/integrity-mt-benchmark - the dataset content itself is
distributed here on MDC.

## Scope boundaries

- Exactly one generated entity, in the final bracketed slot, is scored; surrounding translation quality is not measured.
- CLDR/Babel-derived expected forms are not independent human judgments. Other legitimate locale variants may require extending the accepted set.
- Format conformance covers numbers, dates, currencies and units; no time-of-day or conversion records are included.
- The package includes es-ES and pt-PT, not pt-BR. Entity carriers are reused, so records are correlated.

## Related work

This datasheet follows the structure proposed in Datasheets for Datasets
(Gebru et al., https://arxiv.org/abs/1803.09010). The error categories map to
the locale, terminology and markup branches of the MQM error typology
(https://themqm.org/), turned from human
annotation tags into automated checks.

The closest prior work is Wang et al. (Findings ACL 2021,
https://aclanthology.org/2021.findings-acl.415/), which tests numerical
translation for numerals and separators only. This dataset extends locale
conformance to dates, currency amounts and units, with CLDR as the
reference for the expected target-locale forms.

## Record metadata

Reference-bearing records contain reference translations and expected values or structural metadata needed by the scorer. Test inputs omit withheld answer fields. `failure_opportunity_tags` identify intended test opportunities; they are not human error annotations. `oracle_validated` records automated self-consistency, not independent linguistic review. Total dataset counts include withheld records and therefore exceed the number of open reference-bearing records.
