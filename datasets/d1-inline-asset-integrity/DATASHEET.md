# D1 - Inline Asset Integrity (datasheet)

**Version** 1.1 | **Schema** 0.1

Software text often contains more than words. It may include tags that mark bold text, placeholders such as {name}, or a web address that must stay unchanged. This dataset checks whether a translation preserves the supported elements and their syntax.

The examples come from software translation catalogs, with some markup added to cover more cases. The checks can detect missing or damaged elements. They do not determine whether every tag surrounds the right words or whether the translation itself is accurate.

## How to use this dataset

1. Download and unpack the dataset. Start with `data/dev.jsonl`, which includes reference translations for trying out the checks.
2. Test translation tools used for software and other text containing tags or placeholders. Use the results alongside a separate assessment of translation quality.
3. Run the scoring function described below on the translated output. Test inputs do not include all the reference information needed for official scoring.

## Task and scoring

Translate the source string while preserving the supported inline constraints. Call
`score_item(source, hypothesis)` in `validators.py`. The seven gates are `inventory`,
`placeholder_syntax`, `nesting`, `icu_syntax`, `order`, `attributes` and `verbatim`. The
inventory is normalized: some human-readable attribute values and XLIFF correspondence
labels may change; plural categories may adapt across languages. ICU select keys,
explicit numeric branches, offsets and the required other branch must be retained. The
parser covers the benchmark's unquoted ICU subset, not the complete ICU grammar.

A pass means that the implemented checks were satisfied. Report the pass rate with its denominator and scorer version; it is not an overall translation-quality score.

## MDC technical summary

- Domain: software localization and machine-translation quality evaluation for
  UI and resource strings with inline assets.
- Size: 5,391 records; the open archive contains the dev split (with
  references), the test inputs, the contrastive pairs, README, this datasheet,
  third-party notices, manifest, and Croissant metadata.
- Structure: JSONL records with source and target text, target language, asset
  inventory, asset positions (`ref_tag_positions`, located by verbatim search),
  expected invariants, error-category tags, split, and provenance.
- License: CC-BY-4.0 open layer; upstream attributions in
  `THIRD_PARTY_NOTICES.md`.
- Dataset on MDC (download the open layer): https://mozilladatacollective.com/datasets/cmr0mng9z01bsmk07cuqltz81

## Independent evaluation

Test references and the hidden split are withheld from the open archive. This reduces direct exposure of evaluation answers; it does not guarantee unseen inputs or absence of training overlap, particularly where upstream data is public. Disclose training and tuning on benchmark or upstream material. For evaluation on retained records, contact Prompsit at info@prompsit.com.

## Contents and splits

| Split | File | Records | What it contains |
|---|---|---|---|
| Open dev | `data/dev.jsonl` | 639 | inputs plus the reference translation and labels |
| Test inputs | `data/test.input.jsonl` | 3,717 | inputs only; references withheld |
| Test references | `data/test.ref.jsonl` | 3,717 | withheld, retained by Prompsit |
| Hidden | - | 1,035 | never distributed |
| Contrastive | `data/contrastive.dev.jsonl` | 1,279 | (correct, damaged) minimal pairs from the dev split, each pair separated by the scoring script |

599 sources x 9 languages = **5,391 records**. Split ~10% dev / 70% test / 20%
hidden (sources: 71 / 413 / 115), stratified by asset-class profile and
partitioned by `item_id`, so a source and its nine translations never cross
splits.

No training set is shipped. The dev split is a small labelled set for optional
few-shot prompting or sanity checks; it is not required to run the benchmark.

## Languages

`en` into `ca, es, fr, it, pt-PT, de, nl, pl, ru`. Every source is present in
all nine languages with the same asset-class profile, so per-language scores are
directly comparable.

## Error categories

Every record is tagged with the error categories it can expose; the scoring
script evaluates overlapping constraints and returns diagnostic categories. The scorer returns gates rather than a complete error-category annotation. It does not assign severity; any failed gate rejects the record.

| Error category | What it means | Records |
|---|---|---|
| `missing_asset` | an inline asset from the source is absent from the output | 4,356 |
| `extra_asset` | the output contains an asset the source does not have | 4,356 |
| `corrupted_syntax` | an asset survives but its markup or placeholder syntax is damaged | 4,356 |
| `invalid_nesting` | paired tags overlap or close in the wrong order | 2,772 |
| `moved_paired_tag` | opportunity annotation only: semantic tag placement is not scored | 2,772 |
| `wrong_order` | opportunity annotation; the order gate checks non-positional printf placeholders | 2,565 |
| `lost_attribute` | a tag survives but loses an attribute it had in the source (href, id, ...) | 2,304 |
| `broken_icu` | an ICU MessageFormat structure is damaged (missing branch, broken braces) | 1,467 |
| `dnt_violation` | a do-not-translate span was translated or altered | 1,260 |

At least 400 records per error category (a construction quota, not a guarantee of statistical reliability). Seven asset classes are covered, each with at least 400
records in the scored set: `xliff` (1,548), `software_placeholder` (1,503),
`icu_messageformat` (1,467), `markdown_inline` (1,431), `template_variable`
(1,350), `html_tag` (1,323), `do_not_translate` (1,260). The dev split contains
every class.

## Sample records

Real records from the open dev split, truncated for width. Angle brackets in
markup are shown as ⟨ ⟩ because this platform strips raw HTML-like tags; the
data files contain the ordinary characters.

| item_id | target | source text | target text | asset classes | error categories |
|---|---|---|---|---|---|
| d1-001527 | ca | {HOURS, plural, =1 {This device will be saved for 1 hour and you can connect without a code next time...}} | {HOURS,plural, =1{Aquest dispositiu es desarà durant 1 hora i et podràs connectar sense un codi la propera vegada...}} | icu_messageformat | broken_icu |
| d1-000934 | ca | ⟨xliff:g id="app_name" example="Gmail"⟩%1$s⟨/xliff:g⟩ isn't available right now. This is managed by... | ⟨xliff:g id="APP_NAME_0"⟩%1$s⟨/xliff:g⟩ no està disponible en aquests moments. Aquesta opció es gestiona a... | xliff, software_placeholder | missing_asset, corrupted_syntax |
| d1-000048 | ca | FileName: Name of the file, including the path, that you want to test attributes of. If you do not enter a path, ⟨emph⟩SetAttr⟨/emph⟩... | FileName: Nom del fitxer, inclòs el camí, del qual voleu provar els atributs. Si no introduïu un camí, ⟨emph⟩SetAttr⟨/emph⟩... | html_tag, do_not_translate | dnt_violation, invalid_nesting |
| d1-000418 | ca | This ⟨emph⟩Fontwork⟨/emph⟩ dialog is only available for Fontwork in old Writer text documents that were created prior to %PRODUCTNAME... | Aquest diàleg ⟨emph⟩Fontwork⟨/emph⟩ només està disponible per al Fontwork de documents de text del Writer creats amb una versió anterior a %PRODUCTNAME... | html_tag, template_variable | missing_asset, moved_paired_tag |
| d1-000161 | ca | ⟨emph⟩Reference⟨/emph⟩ (list of options) is the position of the cell to be examined... | ⟨emph⟩Referència⟨/emph⟩ (llista d'opcions) és la posició de la cel·la que s'ha d'examinar... | html_tag, markdown_inline | wrong_order, extra_asset |

## Source data and licenses

Key-aligned localization catalogs (msgid / resource name / JSON key); values are
human translations.

| Corpus | License |
|---|---|
| Apache OpenOffice (openoffice-translation) | Apache-2.0 |
| Chromium (generated_resources + ui_strings) | BSD-3-Clause |
| AOSP Settings / frameworks/base | Apache-2.0 |
| DSpace dspace-angular | BSD-3-Clause |
| Flutter Gallery | BSD-3-Clause |
| Godot editor-l10n | MIT |

All upstream licenses are permissive and compatible with a CC-BY-4.0 open layer;
upstream attribution notices accompany the release in `THIRD_PARTY_NOTICES.md`.
Injected HTML/Markdown assets (added to meet the per-class minimum) are flagged
in provenance.

## Construction method

1. **Harvest** key-aligned catalogs; keep only strings translated in EN plus all
   nine targets; deduplicate; drop fuzzy, obsolete and stale entries.
2. **Asset extraction** with deterministic parsers and regular expressions:
   XLIFF placeholders (`xliff:g`), HTML, printf / positional / named
   placeholders, `{{template}}` variables, inline ICU, Markdown, and
   do-not-translate spans (URLs, emails, brand terms verbatim in all
   references).
3. **Plural conversion**: Android `plurals` resources and gettext plurals
   re-serialized as inline ICU `{count, plural, ...}` with the original human
   translations.
4. **Injection** for classes the UI catalogs lack (HTML, Markdown): one tag pair
   around a verbatim anchor identical across the source and all human
   translations.
5. **Splits**: ~10/70/20, stratified by asset-class profile, partitioned by
   `item_id`.

## Dataset-quality checks

K1 measures separation between controlled corruption baselines under the implemented scorer. It supports sensitivity to those perturbations, not a general claim about MT systems. K2 measures false rejections among tested legal variants. Zero observed flips is not proof that every correct human translation will pass. Reference self-consistency is a separate check and is not independent human validation. The existing paired-bootstrap results resample records; shared sources and reused carriers limit their interpretation.

| Check | Result |
|---|---|
| Discrimination (K1) | **PASS** on the packaged synthetic corruption baselines; see `k1_report.json` in the code repository for per-class results. These are not live MT system scores. |
| False positives (K2) | **PASS** - 0 flips over 830 tested legal variants (0.0%) |
| Reference self-check | 5,391/5,391 - every retained reference (dev, test and hidden) passes the scoring script |
| Croissant 1.0 | `croissant.json`, mlcroissant-validated |

## Reproducibility

The build is deterministic and seeded; rebuilding produces a bit-identical
package, and `checksums.sha256` (included in the archive) verifies a download.
Rebuilding the inputs starts from the reference translations, so the open
layer alone regenerates and verifies the dev split but not the withheld test
and hidden material.

The scoring script and the full build pipeline are open-source at
https://github.com/Prompsit/integrity-mt-benchmark - the dataset content itself is
distributed here on MDC.

## Scope boundaries

- Passing establishes only the implemented syntactic and inventory constraints; it does not establish translation accuracy or fluency.
- `failure_opportunity_tags` describe possible error opportunities, not nine independently detected error labels. The seven scoring gates overlap.
- Semantic placement of paired tags is not scored. Moving a valid tag pair to the wrong words can pass.
- ICU apostrophe escaping, comprehensive branch-body semantics and arbitrary markup grammars are outside this profile. Select-key regression tests are included; the existing corpus primarily exercises plural messages.
- Upstream catalogs and generated additions can be publicly recoverable; withholding a reference file does not prove that a model has never seen it.

## Related work

This datasheet follows the structure proposed in Datasheets for Datasets
(Gebru et al., https://arxiv.org/abs/1803.09010). The error categories map to
the locale, terminology and markup branches of the MQM error typology
(https://themqm.org/), turned from human
annotation tags into automated checks.

Tag handling in MT has been studied before: Hashimoto et al.
(https://arxiv.org/abs/2006.13425) measured XML tag translation accuracy for
a single format. This dataset packages the problem as an auto-scored
benchmark across seven asset classes (XLIFF, HTML, placeholders, template
variables, ICU, Markdown, do-not-translate spans) with per-category error
reporting.

## Record metadata

Reference-bearing records contain reference translations and expected values or structural metadata needed by the scorer. Test inputs omit withheld answer fields. `failure_opportunity_tags` identify intended test opportunities; they are not human error annotations. `oracle_validated` records automated self-consistency, not independent linguistic review. Total dataset counts include withheld records and therefore exceed the number of open reference-bearing records.
