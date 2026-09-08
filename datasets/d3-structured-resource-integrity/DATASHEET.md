# D3 - Structured-resource Integrity (datasheet)

**Version** 1.1 | **Schema** 0.2

Software stores text in resource files: files that pair an identifier with text shown to users. For example, save_button identifies a button, while Save is its label. When translating the label into Spanish as Guardar, the identifier must remain unchanged. This dataset checks these kinds of requirements.

The examples use Android software translations arranged into small XML, JSON, properties and ARB files. Checks cover file syntax, identifiers, whether values remain text and protected fields. They also flag unchanged source text where the reference translation uses different wording. Passing does not establish translation accuracy or guarantee that a complete application can load the file.

## How to use this dataset

1. Download and unpack the dataset. Start with `data/dev.jsonl`, which includes reference translations for trying out the checks.
2. Test translation workflows that accept and return software resource files. The workflow should translate the permitted text while preserving the required file structure.
3. Run the scoring function described below on the translated output. Test inputs do not include all the reference information needed for official scoring.

## Task and scoring

Translate the values and return the complete resource fragment. Call `score_item(record,
hypothesis)` in `resources.py`. The gates are `parser_valid`, `key_path_match`,
`schema_match`, `value_translated`, `nonvalue_literal_preserved` and
`nonvalue_marked_preserved`. Duplicate keys are rejected, values must remain strings and
XML elements must follow the flat string-resource profile. XML do-not-translate markers
must be preserved. ARB metadata is restricted to `@@locale`, which must change to the
target locale. `value_translated` is a reference-aware non-identity heuristic: it flags
source copying only where the reference changed the value. It does not assess whether a
changed value is a correct translation. Use a reference-bearing benchmark record for
this gate.

A pass means that the implemented checks were satisfied. Report the pass rate with its denominator and scorer version; it is not an overall translation-quality score.

## MDC technical summary

- Domain: software localization and machine-translation quality evaluation for
  structured resource files (XML, JSON, .properties, ARB).
- Size: 3,780 records; the open archive contains the dev split (with
  references), the test inputs, the contrastive pairs, README, this datasheet,
  third-party notices, manifest, and Croissant metadata.
- Structure: JSONL records with the source resource file and its reference
  translation, format, key/value metadata, non-translatable fields, expected
  invariants, error-category tags, split, and provenance.
- License: CC-BY-4.0 open layer; upstream attributions in
  `THIRD_PARTY_NOTICES.md`.
- Dataset on MDC (download the open layer): https://mozilladatacollective.com/datasets/cmr0mny2b01asns073985z0va

## Independent evaluation

Test references and the hidden split are withheld from the open archive. This reduces direct exposure of evaluation answers; it does not guarantee unseen inputs or absence of training overlap, particularly where upstream data is public. Disclose training and tuning on benchmark or upstream material. For evaluation on retained records, contact Prompsit at info@prompsit.com.

## Contents and splits

| Split | File | Records | What it contains |
|---|---|---|---|
| Open dev | `data/dev.jsonl` | 378 | inputs plus the reference translation and labels |
| Test inputs | `data/test.input.jsonl` | 2,646 | inputs only; references withheld |
| Test references | `data/test.ref.jsonl` | 2,646 | withheld, retained by Prompsit |
| Hidden | - | 756 | never distributed |
| Contrastive | `data/contrastive.dev.jsonl` | 2,070 | reference and damaged output pairs from dev, with rejection checked by the scorer |

420 sources x 9 languages = **3,780 records**. Split ~10% dev / 70% test / 20%
hidden (sources: 42 / 294 / 84), stratified by format and error-category
profile and partitioned by `item_id`, so a source and its nine translations
never cross splits.

No training set is shipped. The dev split is a small labelled set for optional
few-shot prompting or sanity checks; it is not required to run the benchmark.

## Languages

`en` into `ca, es, fr, it, pt-PT, de, nl, pl, ru`. Every source is present in
all nine languages in the same format, so per-language scores are directly
comparable.

## Error categories

Every record is tagged with the error categories it can expose; the scoring
script evaluates overlapping constraints and returns diagnostic categories. Severity is
reported alongside a failure for error analysis; it does not change the
pass/fail rule.

| Error category | What it means | Severity | Records |
|---|---|---|---|
| `parser_break` | the output no longer parses | Critical | 3,024 |
| `key_path_translated` | a key or path was translated | Major | 3,024 |
| `schema_changed` | the structure or nesting changed | Major | 3,024 |
| `value_untranslated` | a translatable value was left in English | Major | 3,024 |
| `nonvalue_modified_literal` | a non-translatable token - symbols, numbers, ratios, degrees, placeholders, the ARB `@@locale` field - was altered; checked in every format | Major | 2,592 |
| `nonvalue_modified_marked` | an alphabetic token explicitly marked `translatable="false"` was altered; XML only | Major | 432 |

At least 400 records per error category (a construction quota, not a guarantee of statistical reliability); counts are over the scored dev and test records. Four
format profiles are covered: `xml` (native Android), `json`, `properties`, and
`arb` (which carries the non-translatable `@@locale` metadata field).

Non-translatable fields are protected in two tiers. Tier 1 covers tokens with
no letters - symbols, numbers, ratios, degrees, placeholders, and the ARB
`@@locale` field. These can never be legitimately translated, so they are
checked in every format, no marker needed. Tier 2 covers alphabetic tokens
(acronyms, brands, proper nouns), which sometimes are legitimately
translatable; these are checked only in XML, where the source explicitly marks
them with `translatable="false"`. An unmarked alphabetic token that passes
through unchanged in JSON, .properties or ARB is not penalised; no inline
do-not-translate list is shipped, which keeps this dataset separate from the
D5 dataset.

## Sample records

Real records from the open dev split, truncated for width. Angle brackets in
markup are shown as ⟨ ⟩ because this platform strips raw HTML-like tags; the
data files contain the ordinary characters.

| item_id | target | source text | target text | format | error categories |
|---|---|---|---|---|---|
| d3-000001 | ca | ⟨?xml version="1.0" encoding="utf-8"?⟩ ⟨resources⟩ ⟨string name="accessibility_action_label_panel_slice"⟩enter settings⟨/string⟩ ... ⟨string name="external_display_rotation_180" translatable="false"⟩180°⟨/string⟩ ⟨/resources⟩ | ⟨?xml version="1.0" encoding="utf-8"?⟩ ⟨resources⟩ ⟨string name="accessibility_action_label_panel_slice"⟩obre la configuració⟨/string⟩ ... ⟨string name="external_display_rotation_180" translatable="false"⟩180°⟨/string⟩ ⟨/resources⟩ | xml | parser_break, key_path_translated, schema_changed, value_untranslated, nonvalue_modified_literal |
| d3-000124 | ca | { "apn_user": "Username", "app_and_notification_dashboard_summary": "Recent apps, default apps", ... "external_display_rotation_270": "270°" } | { "apn_user": "Nom d'usuari", "app_and_notification_dashboard_summary": "Aplicacions recents, aplicacions predeterminades", ... "external_display_rotation_270": "270°" } | json | parser_break, key_path_translated, schema_changed, value_untranslated, nonvalue_modified_literal |
| d3-000223 | ca | battery_app_usage=App usage since last full charge battery_app_usage_for=App usage for %s ... | battery_app_usage=Ús de l'aplicació des de la darrera càrrega completa battery_app_usage_for=Ús d'aplicacions entre %s ... | properties | parser_break, key_path_translated, schema_changed, value_untranslated, nonvalue_modified_literal |
| d3-000322 | ca | { "@@locale": "en", "bounce_keys_dialog_title": "Bounce key threshold", ... "print_job_summary": "%1$s %2$s" } | { "@@locale": "ca", "bounce_keys_dialog_title": "Llindar de la tecla de rebot", ... "print_job_summary": "%1$s %2$s" } | arb | parser_break, key_path_translated, schema_changed, value_untranslated, nonvalue_modified_literal |

The first four categories apply throughout this construction. Non-value
categories depend on the literal/marked tiers: XML records with alphabetic
protected tokens exercise `nonvalue_modified_marked`; not every record
exercises both non-value categories.

## Source data and licenses

| Corpus | License | What |
|---|---|---|
| AOSP Settings string resources (`aosp-mirror/platform_packages_apps_Settings@7c598253ff60`) | Apache-2.0 | EN plus 9-language `strings.xml`, identical keys, human translations |

The pinned upstream files can be re-downloaded with the open build pipeline. Values are human translations from AOSP; the JSON, .properties and
ARB profiles re-serialize the same key-value pairs. The upstream license is
permissive and compatible with a CC-BY-4.0 open layer; the attribution notice
accompanies the release in `THIRD_PARTY_NOTICES.md`.

## Construction method

1. **Harvest**: download the pinned AOSP Settings string resources - English
   plus the nine target languages with identical keys; keep only keys present
   in all ten files.
2. **Classification**: mark each key as translatable (the English value
   differs from the translations) or non-translatable (identical in every
   language); assign non-translatable tokens to Tier 1 (letterless) or Tier 2
   (alphabetic, marked `translatable="false"` in XML).
3. **Fragmenting and serialization**: group keys into small resource fragments
   (three translatable keys plus one non-translatable) and serialize each
   fragment into one of the four format profiles - Android XML, JSON, Java
   .properties, or Flutter ARB (which adds the `@@locale` metadata field).
4. **Pairing**: the source is the English serialization; the reference is the
   target-language serialization of the same fragment with the human values;
   each record is tagged with the error categories it can expose.
5. **Splits**: ~10/70/20, stratified by format and error-category profile,
   partitioned by `item_id`.

## Dataset-quality checks

K1 measures separation between controlled corruption baselines under the implemented scorer. It supports sensitivity to those perturbations, not a general claim about MT systems. K2 measures false rejections among tested legal variants. Zero observed flips is not proof that every correct human translation will pass. Reference self-consistency is a separate check and is not independent human validation. The existing paired-bootstrap results resample records; shared sources and reused carriers limit their interpretation.

| Check | Result |
|---|---|
| Discrimination (K1) | **PASS** on the packaged synthetic corruption baselines; see `k1_report.json` in the code repository for per-class results. These are not live MT system scores. |
| False positives (K2) | **PASS** - 0 flips over 10,260 tested legal variants (0.0%) |
| Reference self-check | 3,780/3,780 - every retained reference (dev, test and hidden) passes the scoring script |
| Croissant 1.0 | `croissant.json`, mlcroissant-validated |

## Reproducibility

The build is deterministic and seeded; rebuilding produces a bit-identical
package, and `checksums.sha256` (included in the archive) verifies a download.
D3 is built from a pinned public upstream (the AOSP revision in the Source
data table), so the open build pipeline can regenerate the dataset in full;
official, comparable scores on the withheld splits are still issued only by
Prompsit (see Independent evaluation).

The scoring script and the full build pipeline are open-source at
https://github.com/Prompsit/integrity-mt-benchmark - the dataset content itself is
distributed here on MDC.

## Scope boundaries

- Flat resource profiles only; arbitrary nested JSON, full Android/ARB schemas and general Java properties syntax are outside scope.
- A successful parse is not proof that a target application can import the output. No target-tool import is performed.
- The non-identity heuristic is not a translation-quality metric. Without reference values it cannot identify source copying reliably.
- Alphabetic protected values are enforced where XML carries the explicit marker; letterless literals are checked across all profiles.
- All profiles share one upstream corpus. The pinned public source and build code can reconstruct even the withheld splits.

## Related work

This datasheet follows the structure proposed in Datasheets for Datasets
(Gebru et al., https://arxiv.org/abs/1803.09010). The error categories map to
the locale, terminology and markup branches of the MQM error typology
(https://themqm.org/), turned from human
annotation tags into automated checks.

FormatRL (https://arxiv.org/abs/2512.05100) trains and evaluates
format-preserving translation for XML/HTML markup only, and Hashimoto et al.
(https://arxiv.org/abs/2006.13425) measured XML tag accuracy for one format.
This dataset scores key, schema and non-translatable-field preservation
across four resource formats (XML, JSON, .properties, ARB) with a
parse-or-fail check.

## Record metadata

Reference-bearing records contain reference translations and expected values or structural metadata needed by the scorer. Test inputs omit withheld answer fields. `failure_opportunity_tags` identify intended test opportunities; they are not human error annotations. `oracle_validated` records automated self-consistency, not independent linguistic review. Total dataset counts include withheld records and therefore exceed the number of open reference-bearing records.
