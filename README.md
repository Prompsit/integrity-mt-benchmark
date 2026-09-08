# Prompsit MT Integrity Benchmark

> AI agents: see [AGENTS.md](AGENTS.md) for how to run the validators and score an MT output, or the [`evaluate-mt-integrity`](.agents/skills/evaluate-mt-integrity/SKILL.md) skill for a step-by-step download-and-score walkthrough.

This benchmark evaluates selected localization constraints in machine translation:
inline markup and placeholders, locale-specific formatting, resource-file
structure, document structure and prescribed terminology. "MT integrity" is the
project's umbrella term for these checks. They complement separate evaluation of
translation accuracy and fluency; passing does not certify production readiness.
English into nine languages (ca, es, fr, it, pt-PT, de, nl, pl, ru).

General MT metrics do not guarantee that each localization constraint holds.
Targeted challenge sets can reveal errors that an aggregate quality score misses[^1][^2].
The terminology is related to MQM's markup, locale-convention and terminology
categories, but these deterministic checks are not a complete MQM evaluation[^3].

This repository contains the scoring code and technical documentation. The datasets
are distributed through Mozilla Data Collective. Test references and hidden
assessment data are excluded from the downloads.

## The five dimensions

| ID | Dimension | What it checks |
|----|-----------|----------------|
| D1 | Inline Asset Integrity | inline tags, placeholders, ICU, Markdown and do-not-translate spans survive |
| D2 | Locale-data Integrity | numbers, dates, currency and units render in the target locale |
| D3 | Structured-resource Integrity | XML/JSON/.properties/ARB keep their keys and schema; only values are translated |
| D4 | Document-structure Integrity | HTML element hierarchy, table rows, link bindings and text positions |
| D5 | Linguistic-resource Adherence | prescribed term forms/counts under glossary and TM input scenarios |

The canonical catalog (versions, sizes, classes, sourcing and check status) is the
single source of truth:

[Dataset catalog](docs/MDC_Dataset_Registry.md). Each dataset has a DATASHEET
with its scoring contract, examples, sources and limitations.

## Datasets on Mozilla Data Collective

- [Prompsit D1 - Inline Asset Integrity](https://mozilladatacollective.com/datasets/cmr0mng9z01bsmk07cuqltz81)
- [Prompsit D2 - Locale-data Integrity](https://mozilladatacollective.com/datasets/cmr0mnoo201bwmk07nh4yc04u)
- [Prompsit D3 - Structured-resource Integrity](https://mozilladatacollective.com/datasets/cmr0mny2b01asns073985z0va)
- [Prompsit D4 - Document-structure Integrity](https://mozilladatacollective.com/datasets/cmr0moi2k01c0mk07eocv137z)
- [Prompsit D5 - Linguistic-resource Adherence](https://mozilladatacollective.com/datasets/cmr0motgu01awns07eeeyiv6m)

The dataset **content** (open layer: dev reference + test inputs + a contrastive
pack) is downloaded from MDC. This repository ships the **code** (validators and
build pipeline) and the metadata and docs only. To run the validators, fetch the
open layer from MDC into each dataset's `data/`.

## Independent evaluation

The open dev split supports self-evaluation. Withholding test references and a
hidden split reduces direct answer exposure, but does not guarantee unseen data
or freedom from training overlap. Public upstream sources may be recoverable.
For evaluation on retained records, contact info@prompsit.com.

## How scoring works

Each dataset ships a deterministic scoring script under `datasets/<id>/build/`,
next to the dataset-quality checks (`k1_discrimination.py`,
`k2_false_positives.py`) and an integrity check (`validate.py`). For each output,
the scorer reports boolean checks and, where available, a failure diagnostic.
Pass rate measures satisfaction of these checks, not overall translation quality.
Report scorer version, language, sample count and resource track (D5).

- **K1:** sensitivity to the packaged synthetic corruption baselines; not a live
  comparison of MT engines.
- **K2:** false rejections among tested legal variants. Zero observed failures
  is not proof that every acceptable translation will pass.
- **Reference self-check:** every retained reference must pass its scorer;
  this checks consistency, not independent linguistic correctness.

The build is deterministic and seeded, and each v1.1 archive ships
`checksums.sha256` for download verification. A full rebuild starts from the
reference translations, so the open layer alone does not regenerate the
withheld splits - each DATASHEET states what is reproducible for that dataset.
To sanity-check your setup, score the dev references: they must pass 100%.

```
pip install "Babel==2.18.0"   # needed for D2/D5 only; D1/D3/D4 use the stdlib
# then score data/dev.jsonl references with score_item - see AGENTS.md
```

## License

- **Code** (scoring scripts, build pipeline, tooling): [MPL-2.0](LICENSE).
- **Dataset content** (the open layer): distributed on Mozilla Data Collective
  under **CC-BY-4.0**; not hosted in this repository.
- **Upstream sources**: each dataset's `THIRD_PARTY_NOTICES.md` records per-corpus
  attribution (Apache-2.0 / BSD-3-Clause / MIT) and the Unicode CLDR terms.

## References

[^1]: Mathur et al., *Tangled Up in BLEU: Reevaluating the Evaluation of Automatic Machine Translation Evaluation Metrics*, ACL 2020. https://aclanthology.org/2020.acl-main.448/
[^2]: Challenge sets showing metric failures on targeted error phenomena: ACES (Amrhein et al., WMT 2022, https://aclanthology.org/2022.wmt-1.44/) and DEMETR (Karpinska et al., EMNLP 2022, https://aclanthology.org/2022.emnlp-main.649/).
[^3]: MQM error typology. https://themqm.org/
