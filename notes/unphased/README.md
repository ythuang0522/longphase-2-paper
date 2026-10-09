# Heterozygous SNVs left unphased by LongPhase 2 and WhatsHap (Fig. 3c–f)

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

## Issue #6: benchmark composition, the other tool's accuracy, depth histograms, intervals

`issue6.py` (2026-10-09), same runs and sets as above. Truth: v5.0q chr1–22
(`HG002_GRCh38_v5.0q_smvar.chr1_22.vcf`, the file of the manuscript tables), no BED.

### Universe (item 1)

Heterozygous SNV calls: single-base REF and ALT, GT 0/1 (`0|1` and `1|0` count), as in
`run_coverage.sh`. No FILTER condition is applied; all such calls are PASS. The two VCFs
contain exactly the same calls (same POS and ALT): 2,334,730 at 10×, 2,579,823 at 60×.
`1/2` calls and calls with two ALT alleles are outside the universe (at 60×: 3,012 `1/2`
and 4,457 `0/1` with two ALTs). chrX and chrY calls are in it (column `chrXY`).

### Composition (item 2, `issue6_composition.tsv`)

| Class | Definition |
|---|---|
| `het_match` (a) | the truth has the call's POS, REF and ALT with GT 0/1, the match `compare` uses |
| `het_other_allele` (b) | another heterozygous truth record at that POS: other alleles, or a `1/2` record that includes the call's ALT |
| `hom` (c) | a homozygous truth record at that POS |
| `absent` (d) | no truth record at that POS |
| `chrXY` | on chrX or chrY, outside the chr1–22 truth |

`issue6_reconcile.tsv`: the two sources of the Fig. 3c numbers now agree. `het_match` of
`lp_only` minus `het_match` of `wh_only` equals WhatsHap `Phased_SNV` minus LongPhase 2
`Phased_SNV` (22,201, 18,443, 23,757 at 10×, 30×, 60×); calls with two ALTs contribute
nothing to that difference. The rest of the Venn difference (88,696, 61,843, 44,613) is
in classes (b)–(d) and chrX/Y.

### The other tool at these sites (item 3)

For the `het_match` calls of each tool-only set, the other tool's output is scored as
`compare` does (`CompareProcess.cpp`: common variants by POS/REF/first ALT, blocks by truth
PS × query PS over variants phased in both, block-wise Hamming = min(m, n − m), switch
pairs on consecutive variants of a block). `issue6_checks.tsv`: this reproduces
`compare`'s Phased_SNV, SNV switch errors and Hamming % for both tools at all three
coverages exactly.

- `other_assessed`: in a block of the other tool with ≥ 2 assessed variants
- `other_hamming_err`: phase disagrees with the truth relative to the block's majority
  orientation (the orientation that gives min(m, n − m); ties count as the same orientation)
- `other_switch_endpoint`: first or second SNV of one of the other tool's switch-error pairs

| | WhatsHap at `lp_only` (a) sites: Hamming error / switch endpoint | WhatsHap genome-wide Hamming | LongPhase 2 at `wh_only` (a) sites: Hamming error / switch endpoint | LongPhase 2 genome-wide Hamming |
|---|---|---|---|---|
| 10× | 5,427 / 3,516 of 23,690 (22.9% / 14.8%) | 7.71% | 215 / 139 of 1,549 (13.9% / 9.0%) | 5.28% |
| 30× | 3,187 / 2,302 of 19,996 (15.9% / 11.5%) | 2.56% | 261 / 170 of 1,565 (16.7% / 10.9%) | 1.82% |
| 60× | 2,463 / 1,607 of 24,719 (10.0% / 6.5%) | 2.75% | 150 / 113 of 991 (15.1% / 11.4%) | 1.53% |

### Depth histograms (item 4, `issue6_depth_hist.tsv`)

FORMAT/DP of the LongPhase 2 VCF, 2× bins, last bin DP ≥ 124, per coverage and set
(`lp_only`, `lp_only_phase`, `lp_only_gnn`, `wh_only`, `both`). The `lp_only`, `wh_only`
and `both` rows are identical to the histograms of `figure_data_*.js` / `UnphaseVenn3.jsx`.

### Switch-error intervals (item 6, `issue6_intervals.tsv`)

- A switch-error pair is two consecutive SNVs phased in the same block of the truth and
  of the tool (blocks as above) whose switch encodings differ. `compare --sw-bed` writes
  it as start = POS₁ − 1, end = POS₂ − 1.
- `run_coverage.sh` counts a site as inside when start < POS ≤ end, so an interval runs
  from the first SNV of the pair to the base before the second SNV: the first SNV is
  included, the second is not.
- Expected share: the same count over all heterozygous SNV calls the tool phased (not
  only the calls assessed against the truth).
- The Fig. 3e intervals were made against the full v5.0q file (with chrX/Y), not the
  chr1–22 file.
- Including the second SNV changes the enrichment by at most 0.7 (largest for
  `lp_only_gnn`: 4.47 → 5.15 at 10×); `lp_only` 4.26 / 8.11 / 9.62 becomes
  4.45 / 8.19 / 9.65 and `wh_only` 1.95 / 4.21 / 9.49 becomes 1.95 / 4.25 / 9.44.
