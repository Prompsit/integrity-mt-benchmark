# D5 - Linguistic-resource Adherence (datasheet)

**Version** 1.1 | **Schema** 0.2

Translation workflows may receive a glossary of required terms or a translation memory: previously translated sentences provided for reuse. This dataset checks whether the output uses the prescribed term, repeats it when required, and avoids terms explicitly listed as disallowed.

The examples combine software translation sentences with added term fields and constructed glossary or translation-memory examples. Some cases include an outdated suggested term or conflicting instructions. Glossary and translation-memory results are reported separately. The checks assess term use, not reuse of an entire sentence or overall translation quality.

## How to use this dataset

1. Download and unpack the dataset. Start with `data/dev.jsonl`, which includes reference translations for trying out the checks.
2. Test translation workflows that can receive a glossary or translation memory. Report the two types of result separately, and identify any resource type the workflow does not support.
3. Run the scoring function described below on the translated output. Test inputs do not include all the reference information needed for official scoring.

## Task and scoring

Translate the source and provide the resources carried by the record to the system or
wrapper. Call `score_item(record, hypothesis)` in `lingres.py` using the benchmark
record containing `ref_term`. Only the final bracketed term slot and the absence of
disallowed terms in the whole output are scored. The gates are `term_present`,
`term_count`, `term_consistent`, `term_correct` and `forbidden_absent`. Repeated records
require exactly two prescribed terms separated by a vertical bar; other records require
exactly one. Matching uses exact surface forms after trimming slot whitespace. Passing
does not establish the quality of the surrounding sentence or reuse of an entire TM
translation.

Report the `glossary` and `tm` tracks separately. Report `conflict` and `quality` as
additional diagnostic tracks, without combining them into a single headline score. Mark
each unsupported resource track `not_applicable` and state how resources were delivered.
Glossary precedence in conflict items is an explicit benchmark policy. Fuzzy records
carry an assigned `match_pct` of 85; this is synthetic metadata, not a computed source-
similarity score.

A pass means that the implemented checks were satisfied. Report the pass rate with its denominator and scorer version; it is not an overall translation-quality score.

## MDC technical summary

- Domain: machine-translation quality evaluation for adherence to supplied
  linguistic resources - glossary terminology and translation-memory matches.
- Size: 4,590 records; the open archive contains the dev split (with
  references), the test inputs, the contrastive pairs, README, this datasheet,
  third-party notices, manifest, and Croissant metadata.
- Structure: JSONL records with source and target text, target language,
  resource profile, glossary and TM payloads, the prescribed term (`ref_term`),
  forbidden terms, expected invariants, error-category tags, split, and
  provenance.
- License: CC-BY-4.0 open layer; upstream attributions in
  `THIRD_PARTY_NOTICES.md`.
- Dataset on MDC (download the open layer): https://mozilladatacollective.com/datasets/cmr0motgu01awns07eeeyiv6m

## Independent evaluation

Test references and the hidden split are withheld from the open archive. This reduces direct exposure of evaluation answers; it does not guarantee unseen inputs or absence of training overlap, particularly where upstream data is public. Disclose training and tuning on benchmark or upstream material. For evaluation on retained records, contact Prompsit at info@prompsit.com.

## Contents and splits

| Split | File | Records | What it contains |
|---|---|---|---|
| Open dev | `data/dev.jsonl` | 459 | inputs plus the reference translation and labels |
| Test inputs | `data/test.input.jsonl` | 3,213 | inputs only; references withheld |
| Test references | `data/test.ref.jsonl` | 3,213 | withheld, retained by Prompsit |
| Hidden | - | 918 | never distributed |
| Contrastive | `data/contrastive.dev.jsonl` | 864 | reference and damaged output pairs from dev, with rejection checked by the scorer |

510 sources x 9 languages = **4,590 records**. Split ~10% dev / 70% test / 20%
hidden, stratified by resource profile and partitioned by `item_id`, so a
source and its nine translations never cross splits.

No training set is shipped. The dev split is a small labelled set for optional
few-shot prompting or sanity checks; it is not required to run the benchmark.

## Languages

`en` into `ca, es, fr, it, pt-PT, de, nl, pl, ru`. Every source is present in
all nine languages with the same resource profile, so per-language scores are
directly comparable.

## Error categories

Every record is tagged with the error categories it can expose; the scoring
script evaluates overlapping constraints and returns diagnostic categories. Severity is
reported alongside a failure for error analysis; it does not change the
pass/fail rule.

Categories are grouped by resource type: glossary, TM, and a conflict case
where the glossary takes precedence over the TM. Categories are reported
separately and never collapsed into one number; each record names its group in
a `track` field. `fuzzy_discernment` is the one category that rewards not
reusing a match: copying the stale term from a synthetic fuzzy-TM input labelled 85% is the error.

| Error category | What it means | Severity | Records |
|---|---|---|---|
| `required_term_missing` | the prescribed term is absent from the output | Major | 1,080 |
| `forbidden_term_used` | a disallowed target term appears anywhere in the output | Major | 1,080 |
| `inconsistent_term` | the term is rendered two different ways in one output | Major | 1,080 |
| `approved_tm_ignored` | the term prescribed by an exact-TM input was not used | Major | 864 |
| `conflict_mishandled` | when the glossary and the TM disagree, the glossary must win | Major | 864 |
| `fuzzy_discernment` | a stale term was copied from a synthetic fuzzy-TM input instead of using the prescribed current term | Major | 864 |

At least 400 records per error category (a construction quota, not a guarantee of statistical reliability). The source profile of each category - the record kind
that exercises it - is: `required_term_missing`, `forbidden_term_used` and
`inconsistent_term` come from glossary records; `approved_tm_ignored` from
exact-TM records; `fuzzy_discernment` from fuzzy-TM records;
`conflict_mishandled` from conflict records. The dev split contains every
profile.

## Sample records

Real records from the open dev split, truncated for width. Angle brackets in
markup are shown as ⟨ ⟩ because this platform strips raw HTML-like tags; the
data files contain the ordinary characters.

| item_id | target | source text | target text | resource kind + prescribed term | error categories |
|---|---|---|---|---|---|
| d5-000000 | ca | Y: %1 M: %2 D: %3 H: %4 M: %5 S: %6 [world \| world] | A: %1 M: %2 D: %3 H: %4 M: %5 S: %6 [Món \| Món] | glossary: Món (forbidden: Amèrica del Nord) | required_term_missing, forbidden_term_used, inconsistent_term |
| d5-000154 | ca | at ⟨xliff:g id="time" example="2:33 am"⟩**%s**⟨/xliff:g⟩ [Bosnian] | a les ⟨xliff:g id="TIME"⟩**%s**⟨/xliff:g⟩ [bosnià] | tm_exact: bosnià (100% match) | approved_tm_ignored |
| d5-000270 | ca | ⟨xliff:g id="count"⟩`%d`⟨/xliff:g⟩d [Manchu] | ⟨xliff:g id="COUNT"⟩`%d`⟨/xliff:g⟩ d [manxú] | tm_fuzzy: manxú (the 85% match holds stale "malai") | fuzzy_discernment |
| d5-000395 | ca | Revoke access to Modes for ⟨xliff:g id="app" example="Tasker"⟩%1`$s`⟨/xliff:g⟩? [Argentine Peso] | Vols revocar l'accés als modes per a ⟨xliff:g id="APP"⟩%1`$s`⟨/xliff:g⟩? [peso argentí] | conflict: peso argentí (the TM offers "dòlar australià") | conflict_mishandled |

## Source data and licenses

| Resource | Source | License |
|---|---|---|
| Glossary terminology | CLDR display names (territories / languages / currencies) via Babel | Unicode-3.0 |
| TM carriers | catalog-derived translations and additions inherited from D1 | per-segment (Apache-2.0 / BSD-3-Clause / MIT, inherited) |

Glossary terms come from CLDR; the carrier sentences are inherited from D1 catalogs and generated additions. The term sits in a neutral `[...]` slot of a
catalog-derived carrier sentence. Complete records include synthetic term slots and resource payloads. All upstream
licenses are permissive and compatible with a CC-BY-4.0 open layer; upstream
attribution notices accompany the release in `THIRD_PARTY_NOTICES.md`.

## Construction method

1. Select CLDR territory, language and currency display-name pairs using Babel 2.18.0.
2. Append a bracketed term slot to D1-derived carrier pairs. Glossary items repeat the term twice; other profiles use one occurrence.
3. Build glossary and TM payloads. Exact-TM inputs carry an exact source match; fuzzy inputs contain a changed source term and a stale target term. The fuzzy percentage is assigned as 85, without a similarity calculation. Conflict items prescribe glossary-over-TM precedence.
4. Generate disallowed terms from other CLDR display names. These are negative test terms, not a synonym inventory.
5. Partition by item_id into dev/test/hidden and score each reference with the deterministic checks.

## Dataset-quality checks

K1 measures separation between controlled corruption baselines under the implemented scorer. It supports sensitivity to those perturbations, not a general claim about MT systems. K2 measures false rejections among tested legal variants. Zero observed flips is not proof that every correct human translation will pass. Reference self-consistency is a separate check and is not independent human validation. The existing paired-bootstrap results resample records; shared sources and reused carriers limit their interpretation.

| Check | Result |
|---|---|
| Discrimination (K1) | **PASS** on the packaged synthetic corruption baselines; see `k1_report.json` in the code repository for per-class results. These are not live MT system scores. |
| False positives (K2) | **PASS** - 0 flips over 13,770 tested legal variants (0.0%) |
| Reference self-check | 4,590/4,590 - every retained reference (dev, test and hidden) passes the scoring script |
| Croissant 1.0 | `croissant.json`, mlcroissant-validated |

## Reproducibility

The build is deterministic and seeded; rebuilding produces a bit-identical
package, and `checksums.sha256` (included in the archive) verifies a download.
The glossary terms come from public CLDR, but the TM sentences are shared
with D1 and largely withheld, so the open layer alone does not regenerate
the test and hidden splits.

The scoring script and the full build pipeline are open-source at
https://github.com/Prompsit/integrity-mt-benchmark - the dataset content itself is
distributed here on MDC.

## Scope boundaries

- Synthetic terminology slots and generated TM scenarios around catalog-derived carriers; the complete items are not independent human translations.
- Disallowed terms are other CLDR display names, often unrelated concepts. They should not be described as synonyms.
- Exact-TM scoring checks the prescribed term only. Full-sentence TM reuse, retrieval quality and a real fuzzy-match algorithm are not evaluated.
- The fuzzy match percentage is assigned, not measured. The conflict precedence rule is benchmark-specific.
- Exact term matching does not cover contextual inflection, paraphrase or general terminology quality. Surrounding prose is unscored.

## Related work

This datasheet follows the structure proposed in Datasheets for Datasets
(Gebru et al., https://arxiv.org/abs/1803.09010). The error categories map to
the locale, terminology and markup branches of the MQM error typology
(https://themqm.org/), turned from human
annotation tags into automated checks.

IFMTBench (https://arxiv.org/abs/2605.28218) scores joint
constraint-following with a single multiplicative index; this dataset
isolates glossary and TM adherence as per-category pass rates. Bulte &
Tezcan (ACL 2019, https://aclanthology.org/P19-1175/) reuse fuzzy TM matches
to improve MT output; here, avoiding the stale term in a constructed fuzzy-TM scenario is evaluated.

## Record metadata

Reference-bearing records contain reference translations and expected values or structural metadata needed by the scorer. Test inputs omit withheld answer fields. `failure_opportunity_tags` identify intended test opportunities; they are not human error annotations. `oracle_validated` records automated self-consistency, not independent linguistic review. Total dataset counts include withheld records and therefore exceed the number of open reference-bearing records.
