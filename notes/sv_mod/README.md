# Phased SVs and 5mC sites in co-phasing (Results, four-class paragraph; Supplementary Data 1)

LongPhase 2 co-phasing runs on HG002 nanopore, every configuration with SVs or 5mC, all 64 runs
(10–20× replicates 1–10, 30–60× replicate 1), without and with GNN correction.

Source VCFs: `/disk/research/longphase_<config>[_gnn]/longphase_<config>[_gnn]_<c>x_<r>_SV.vcf`
and `..._mod.vcf`, the SV and 5mC outputs of `longphase phase --sv-file ... --mod-file ...`
(SVs: Sniffles2 2.8; 5mC: `longphase modcall`).

| Configuration (`co-phase_Detail`) | Directory |
|---|---|
| Mod+Indel | `longphase_coh_indel_methyl` |
| Mod | `longphase_coh_methyl` |
| SV | `longphase_coh_sv` |
| Indel+SV | `longphase_coh_indel_sv` |
| Indel+Mod+SV (four-class) | `longphase_cophasing` |

## Definitions (`count_sv_mod.py`)

- Heterozygous: GT `0|1`, `1|0` or `0/1`. Phased: GT `0|1` or `1|0`.
- Counted on chr1–22 and on all contigs (`sv_mod.tsv` has both). `SV_5mC_phasing` in
  `supplementary.xlsx` and the Results ranges use all contigs, as `Variant_Calling` does: the
  heterozygous 5mC counts equal `Hetero. methyl` there; the heterozygous SV counts are 0–7 higher
  than `Hetero. SV` (Sniffles2 input) per run.
- GNN correction changes no genotype other than unphasing: the heterozygous counts are identical
  with and without GNN, and no run has more phased records after it.
- Unphased by GNN = (phased without GNN − phased with GNN) / phased without GNN.

## Four-class, replicate 1, all contigs (Results)

| Cov. | Het. SV | Phased | % | Het. 5mC | Phased | % | SV unphased by GNN (%) | 5mC unphased by GNN (%) |
|---|---|---|---|---|---|---|---|---|
| 10× | 14,910 | 10,433 | 69.97 | 284,230 | 281,593 | 99.07 | 3.46 | 4.57 |
| 12× | 16,102 | 11,190 | 69.49 | 364,526 | 361,203 | 99.09 | 3.53 | 4.05 |
| 14× | 16,753 | 11,645 | 69.51 | 407,794 | 404,480 | 99.19 | 3.35 | 3.57 |
| 16× | 17,011 | 11,759 | 69.13 | 429,972 | 427,085 | 99.33 | 3.10 | 3.04 |
| 18× | 17,348 | 11,948 | 68.87 | 441,632 | 438,448 | 99.28 | 2.87 | 2.72 |
| 20× | 17,462 | 11,890 | 68.09 | 450,624 | 447,570 | 99.32 | 3.17 | 2.40 |
| 30× | 17,806 | 12,187 | 68.44 | 474,512 | 471,632 | 99.39 | 2.89 | 1.84 |
| 40× | 17,768 | 12,101 | 68.11 | 485,070 | 482,333 | 99.44 | 2.43 | 1.64 |
| 50× | 17,607 | 12,012 | 68.22 | 493,774 | 490,699 | 99.38 | 2.61 | 1.42 |
| 60× | 17,481 | 11,918 | 68.18 | 499,496 | 496,254 | 99.35 | 2.93 | 1.37 |

Ranges: SV phased 68.1–70.0%, 5mC phased 99.1–99.4%; GNN unphases 2.4–3.5% of the phased SVs
and 1.4–4.6% of the phased 5mC sites. Over all 64 four-class runs: 68.0–70.6%, 98.9–99.4%,
2.4–4.1% and 1.4–4.6%.

The earlier Results values (5mC 99.0–99.4%, SV 68.1–70.1%, SV unphased 2.4–3.8%) came from an
audit table (`q10_sv_mod.tsv`) that is not in the repository; they are replaced by these counts
from the current VCFs.

## Rebuild

```sh
for cfg in coh_sv coh_indel_sv coh_methyl coh_indel_methyl cophasing; do
  for r in $(ls /disk/research/longphase_$cfg | grep -oE '[0-9]+x_[0-9]+\.vcf$' | grep -oE '[0-9]+x_[0-9]+' | sort -u); do
    echo "$cfg $r"; done; done | xargs -P 16 -L1 python3 count_sv_mod.py > counts.tsv
# sv_mod.tsv = counts.tsv with a header and the configuration labels; then:
python3 build_sheet.py   # writes the SV_5mC_phasing sheet
```
