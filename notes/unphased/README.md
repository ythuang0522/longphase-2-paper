# Heterozygous SNVs left unphased by LongPhase 2 and WhatsHap (Fig. unphased, Supp. Fig. 12)

Source data for the paragraph of Results that compares the SNVs each tool leaves
unphased (`results.tex`, "At 60×, LongPhase 2 left 210,683 heterozygous SNV calls
unphased …") and for `UnphaseVenn3.jsx`. HG002 ONT R10.4.1 replicate 1 at 10×, 30× and
60×; LongPhase 2 with GNN correction (`longphase_gnn`) against WhatsHap 2.8
`--only-snvs`.

The analysis was first run on 2026-09-26/27 with the scripts in `scripts/`; the numbers
were then copied into `UnphaseVenn3.jsx` and the commit message of 0025929, and no table
was committed. On 2026-10-09 the same scripts, unchanged, were rerun on the same VCFs
(`run_all.sh`), and `summarize_sets.py` collected the results in one table.

## Files

| File | Contents |
|---|---|
| `unphased_sets.tsv` | one row per coverage × set: number of sites, read depth (quartiles, share at the depth cap), PE, enrichment in the other tool's switch-error intervals |
| `figure_data_{10,30,60}x.js` | output of `scripts/run_coverage.sh`: Venn counts, enrichment and depth histograms, the `DATA` block of `UnphaseVenn3.jsx` |
| `giveup_detail_{10,30,60}x.txt` | output of `scripts/giveup_detail.sh`: depth and PE per set (its background row is a random 100,000-site sample) |
| `scripts/` | the original scripts: `run_coverage.sh`, `run_unphase_venn.sh` (site lists), `giveup_detail.sh` |
| `run_all.sh` | runs the three scripts on 10×, 30× and 60× (lab-server paths) |
| `summarize_sets.py` | builds `unphased_sets.tsv` |

## Sets and columns (`unphased_sets.tsv`)

Sites: heterozygous SNVs (single-base REF and ALT, GT 0/1) of the two VCFs.

| Set | Definition |
|---|---|
| `lp_only` | unphased by LongPhase 2, phased by WhatsHap |
| `lp_only_gnn` | the part of `lp_only` phased before GNN correction (`longphase/longphase_{c}x_1.vcf`) and unphased after it |
| `lp_only_phase` | the rest of `lp_only`, left unphased by `phase` itself |
| `wh_only` | unphased by WhatsHap, phased by LongPhase 2 |
| `both` | unphased by both tools |
| `background` | heterozygous SNVs of the LongPhase 2 VCF in none of the sets above (all of them; `giveup_detail.sh` samples 100,000) |

- `dp_*`: FORMAT/DP of the LongPhase 2 VCF (the PEPPER call); quartiles as in
  `giveup_detail.sh`. `dp_at_cap_pct`: DP ≥ 124, the last 2× bin of the histograms; the
  caller's depth is capped near 125×.
- `pe_*`: INFO/PE (phasing entropy) of the LongPhase 2 VCF, over the sites that carry it
  (`pe_sites`). LongPhase writes PE only for sites it phased in `phase`, so
  `lp_only_phase` has none.
- `in_other_sw_pct`: share of the set inside the other tool's switch-error intervals
  (`longphase compare --sw-bed` against v5.0q, start < pos ≤ end);
  `other_tool_background_pct`: the same share for all heterozygous SNVs that tool phased;
  `enrichment`: their ratio.

## Values in the manuscript and where they are

| Manuscript (60× unless stated) | `unphased_sets.tsv` |
|---|---|
| LongPhase 2 left 210,683 unphased, WhatsHap 142,313; 88,692 in both, 121,991 LongPhase 2 alone, 53,621 WhatsHap alone | `n` of `lp_only` + `both`, `wh_only` + `both`, `both`, `lp_only`, `wh_only` |
| enrichment 4.3-fold (10×) to 9.6-fold (60×) for SNVs unphased by LongPhase 2 alone | `enrichment` of `lp_only`: 4.3, 8.1, 9.6 |
| 2.0-fold to 9.5-fold for those unphased by WhatsHap alone | `enrichment` of `wh_only`: 1.9 (3.38% / 1.73%; 2.0 from the rounded percentages), 4.2, 9.5 |
| WhatsHap-only median depth 18× | `dp_median` of `wh_only` |
| 57.6% of WhatsHap-only sites with zero phasing entropy | `pe_zero_pct` of `wh_only` |
| 15.6% of LongPhase-only sites at the depth cap | `dp_at_cap_pct` of `lp_only` |

## Reproduction check (2026-10-09)

- `figure_data_10x.js` and `figure_data_30x.js` are identical to the 2026-09-27 files in
  `/disk/research` and to `UnphaseVenn3.jsx` (200 numbers each).
- `figure_data_60x.js` is identical to `UnphaseVenn3.jsx` except one histogram value
  (LongPhase-only, last bin: 0.15608 against 0.15607 in the JSX).
- At 60×, the three site lists, the Venn summary and the `giveup_detail` rows (except the
  sampled background) are identical to the 2026-09-26/27 files in `/disk/research`.
- `summarize_sets.py` reproduces the enrichment percentages of `run_coverage.sh` and the
  depth and PE values of `giveup_detail.sh` for every set those scripts report.

## Commands

```
# per coverage c = 10, 30, 60 (run_all.sh)
bash scripts/run_coverage.sh ${c}x longphase/longphase_${c}x_1.vcf longphase_gnn/longphase_gnn_${c}x_1.vcf \
     whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf HG002_GRCh38_v5.0q_smvar.vcf.gz longphase OUT
bash scripts/run_unphase_venn.sh longphase_gnn/longphase_gnn_${c}x_1.vcf \
     whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf T2T_DIPCALL_DIR OUT
bash scripts/giveup_detail.sh OUT OUT/gnn_removed.txt longphase_gnn/longphase_gnn_${c}x_1.vcf OUT
python3 summarize_sets.py OUT > unphased_sets.tsv
```

`longphase` is release v2.1 (`compare --sw-bed`); `T2T_DIPCALL_DIR` holds the
T2T-HG002 v1.1 dipcall BED and VCF (used only for the assembly classification in
`run_unphase_venn.sh`, not for these numbers).
