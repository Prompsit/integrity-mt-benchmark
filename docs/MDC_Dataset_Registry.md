# Dataset catalog

Updated 2026-09-08. The descriptions and open archives below are published on
Mozilla Data Collective. Counts and versions come from each dataset's manifest.

| ID | Dataset | Ver | Scoring rule | Sources | Records | Splits (sources: test / dev / hidden) | Classes | K1 | K2 |
|----|---------|-----|-------------------|--------:|--------:|---------------------------------------|--------:|----|----|
| **D1** | inline-asset-integrity | 1.1 | A — normalized inline inventory and syntax | 599 | 5 391 | 413 / 71 / 115 | 7 | PASS | PASS |
| **D2** | locale-data-integrity | 1.1 | B — adapt values to target locale | 680 | 6 120 | 474 / 70 / 136 | 5 | PASS | PASS |
| **D3** | structured-resource-integrity | 1.1 | C — preserve skeleton, translate content | 420 | 3 780 | 294 / 42 / 84 | 6 | PASS | PASS |
| **D4** | document-structure-integrity | 1.1 | C — preserve document tree, translate text | 160 | 1 440 | 112 / 16 / 32 | 5 | PASS | PASS |
| **D5** | linguistic-resource-adherence | 1.1 | D — prescribed term forms and counts | 510 | 4 590 | 357 / 51 / 102 | 6 (4 tracks) | PASS | PASS |

**On Mozilla Data Collective:** [D1](https://mozilladatacollective.com/datasets/cmr0mng9z01bsmk07cuqltz81) · [D2](https://mozilladatacollective.com/datasets/cmr0mnoo201bwmk07nh4yc04u) · [D3](https://mozilladatacollective.com/datasets/cmr0mny2b01asns073985z0va) · [D4](https://mozilladatacollective.com/datasets/cmr0moi2k01c0mk07eocv137z) · [D5](https://mozilladatacollective.com/datasets/cmr0motgu01awns07eeeyiv6m)

English source; target languages: ca, es, fr, it, pt-PT, de, nl, pl and ru.
Record totals include the withheld splits. Public downloads contain dev records
with references, test inputs, and contrastive examples. Dataset content is
obtained from MDC; this repository contains the code and documentation.

K1 checks sensitivity to synthetic corruptions. K2 found no false rejections
among the tested legal variants. These checks do not establish overall
translation quality or independent human validation.

## Scoring contracts and limitations

- [D1: inline markup and placeholders](../datasets/d1-inline-asset-integrity/DATASHEET.md)
- [D2: locale-specific formatting](../datasets/d2-locale-data-integrity/DATASHEET.md)
- [D3: localization resource files](../datasets/d3-structured-resource-integrity/DATASHEET.md)
- [D4: HTML document structure](../datasets/d4-document-structure-integrity/DATASHEET.md)
- [D5: glossary and translation-memory constraints](../datasets/d5-linguistic-resource-adherence/DATASHEET.md)

Per-class construction checks are recorded in each dataset's `k1_report.json`
and `k2_report.json`. Report the scorer version alongside evaluation results.
