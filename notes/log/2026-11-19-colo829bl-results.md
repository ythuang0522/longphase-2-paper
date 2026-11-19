# COLO829BL phasing benchmark: chr1-22 results

Completes `2026-11-16-colo829bl-chr20-setup.md`. COLO829BL nanopore (ONT open data `PAU59807`), Clair3 v1.2.0 calls,
seed 1 at 10, 20 and 30×. Truth: SMaHT COLO829BL DSA v3.0.0 assembly, scored under the HG008 rules. Full write-up in
`notes/colo829_validation/README.md`. No manuscript text or figure changed.

## SNV switch error rate, chr1-22

| coverage | LongPhase 2 (GNN) | `--disableGNN` | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|--:|--:|--:|--:|
| 10× | 0.065% | 0.081% | 0.144% | 0.206% |
| 20× | 0.023% | 0.029% | 0.054% | 0.114% |
| 30× | 0.018% | 0.022% | 0.044% | 0.089% |

## What the results show

- **GNN effect:** the GNN cuts switch errors by 18.7–19.6%. It costs 0.05–0.17 percentage point of completeness.
- **Against the comparators:** LongPhase 2 is 2.2–2.4-fold lower than WhatsHap and 3.2–4.9-fold lower than HapCUT2, and
  it has the fewest errors on every chromosome in every run.
- **Completeness:** 0.6–1.0 point below WhatsHap.

## Results against the method

- **Hamming distance at 30×:** WhatsHap is lower (0.46% against 0.51%).
- **Switch errors from 20× to 30×:** they rise on chr7, chr16 and chr21.

## Scoring correction found by the summary check

The chr17 20×/30× scores predated the re-phasing that followed the duplicate-record fix. They were rescored; only WhatsHap
changed, by one phased SNV and one pair.
