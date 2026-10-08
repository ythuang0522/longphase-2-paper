# Issue #1: indel phase accuracy and stratified switch errors

Items 3 and 4 of issue #1, computed on 2026-10-08 on the lab server. No `.tex`
file was changed. Nothing here has been written into the manuscript.

## Data

The phased VCFs (449 GB) stay on the lab server and are not in the repository. In the
server checkout of this repository, the gitignored `data/` folder links to them:

| Path | Contents |
|---|---|
| `data/vcf/<group>/` | original phased VCFs, 64 runs per group (10–20× replicates 1–10, 30/40/50/60× replicate 1) |
| `data/truth/` | v5.0q chr1–22 truth VCF, v4.2.1 hifiasm phase-transfer truth VCF, both benchmark BEDs, six GIAB v3.6 stratification BEDs |
| `data/benchmark_strata/` | working directory of this analysis: `out/` (per-run results of `score_phase.py`, `.tsv` counts and `.sw.tsv` switch positions), `run_all.sh` (scores the original VCFs), logs |
| `data/benchmark_strata/release/` | archive copy: one tarball per group of slim VCFs, the truth and region files, `out/`, with md5 lists |

The slim VCFs keep heterozygous (0/1, 1/0) records only, FORMAT reduced to `GT:PS`, INFO
dropped (`slim_vcf.py`); `score_phase.py` gives results identical to the original files on
them. They were packaged for sharing but not published (author decision, 2026-10-08).

| Group | Run name | Paper label |
|---|---|---|
| `longphase_gnn` | `longphase_gnn_{cov}x_{rep}` | LongPhase 2 (v2.1), SNV only |
| `longphase` | `longphase_{cov}x_{rep}` | LongPhase 2 without GNN, SNV only |
| `whatshap_v2.8_onlySNVs` | `whatshap_v28_onlySNVs_{cov}x_{rep}` | WhatsHap 2.8 `--only-snvs` |
| `hapcut2_v1.3.4` | `hapcut2_v134_{cov}x_{rep}` | HapCUT2 1.3.4 |
| `whatshap_v2.8` | `whatshap_v28_{cov}x_{rep}` | WhatsHap 2.8 with indels |
| `longphase_coh_indel[_gnn]` | | SNV + indel |
| `longphase_coh_indel_sv[_gnn]` | | SNV + indel + SV |
| `longphase_coh_indel_methyl[_gnn]` | | SNV + indel + 5mC |
| `longphase_cophasing[_gnn]` | | SNV + indel + SV + 5mC (four-class) |

`_gnn` is LongPhase 2 with GNN correction (the `longphase_v2.1` columns of
`supplementary.xlsx`); the other LongPhase runs are the `longphase_v2.0.1` columns.

## Reproduce

On the lab server (Python 3 with numpy; `aggregate.py` also needs openpyxl):

```bash
# re-aggregate from the stored per-run results
python3 notes/benchmark_strata/aggregate.py data/benchmark_strata/out
# or re-score from the slim archive (~45 min at JOBS=12)
mkdir -p DATA && for t in data/benchmark_strata/release/*.tar; do tar -xf $t -C DATA; done
JOBS=12 notes/benchmark_strata/run_scoring.sh DATA out
```

`aggregate.py` writes the four tables below into the working directory and prints the
summaries; `run_scoring.sh` scores every VCF and then runs it.

## Method

`score_phase.py` re-implements `longphase compare` (release v2.1, commit 46ba470,
`CompareProcess.cpp`) and additionally records every assessed pair:

- record: has an ALT, diploid GT 0/1 or 1/0 (first ALT); phased if the second allele
  carries `|`; a phased record without an integer PS gets PS 1 (whole chromosome)
- truth and query matched by CHROM, POS, REF and first ALT; chr1–22
- intersection blocks: (truth PS, query PS) groups of variants phased in both, by
  position; single-variant blocks dropped
- `snv` pairs: consecutive SNVs of a block (compare's SNV_SW); `all` pairs: consecutive
  variants of a block; `indel` pairs: `all` pairs with at least one indel
- switch: the pair's switch encodings differ; Hamming per block =
  min(mismatches, size − mismatches); indel Hamming counts indel mismatches under the
  block orientation chosen on all variants

A pair belongs to a region set when both of its variants lie inside it, so the region
rows do not add up to `all` (pairs that straddle a boundary are in neither).
Regions: `v5bed`, `v4bed`, `shared` (both), `v5only`, `v4only`, `neither`; strata (GIAB
v3.6): `segdup`, `tandem_repeat`, `homopolymer`, `satellite`, `lowmap_segdup`,
`not_difficult`; every region × stratum combination is in `item4_strata.tsv`.

Validation: on `longphase_gnn_10x_1` and `whatshap_v28_10x_1` every total equals
`longphase compare` (phased SNVs and indels, SNV switch errors and pairs, all-variant
switch errors and pairs, Hamming).

## Step 0: reproduction

All 1,024 runs that have a manuscript table value reproduce it exactly (phased SNVs and
SNV switch errors; `step0_check.tsv`). The remaining 64 runs (LongPhase 2 without GNN
against v4.2.1) are not in any table.

The tables were scored **without** a benchmark BED, as Methods states. Restricting
to the v5.0q BED does not reproduce them (`longphase_gnn_10x_1`: 1,510 switch errors
without the BED, 965 with it). The issue text asked for the BED-restricted run; that was
an error in the issue. The GIAB URLs in the issue (`/ReferenceSamples/giab/release/...`)
return 404; the files are under `https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/`.

## Item 4: where the switch errors are (SNV only)

SNV switch errors per genome (mean of ten replicates at 10×, one run at 60×):

| Truth | Region | LongPhase 2 | WhatsHap | HapCUT2 |
|---|---|---|---|---|
| v5.0q | all (table values) | 1,518 / 496 | 4,383 / 1,785 | 5,018 / 2,309 |
| v5.0q | shared | 805 / 33 | 1,483 / 63 | 1,686 / 273 |
| v5.0q | v5only | 41 / 15 | 266 / 88 | 322 / 148 |
| v5.0q | neither | 438 / 348 | 2,030 / 1,337 | 2,175 / 1,430 |
| v4.2.1 | all (table values) | 1,820 / 1,676 | 2,773 / 1,801 | 3,050 / 2,088 |
| v4.2.1 | shared | 1,445 / 1,178 | 2,235 / 1,245 | 2,432 / 1,435 |

What the numbers show:

1. Under v5.0q, the largest part of the separation lies outside both benchmark BEDs
   (`neither`): heterozygous records of the v5.0q VCF outside its own benchmark regions.
   WhatsHap and HapCUT2 have switch error rates of 2.6–4.9% there against 0.8–1.2% for
   LongPhase 2; at 60× 75% of the WhatsHap and 62% of the HapCUT2 switch errors are
   there. The v5only regions contribute little.
2. Under v4.2.1 most switch errors at high coverage are at the same SNV pairs in all
   three tools: at 60×, 1,556 of the 1,676 LongPhase 2 errors (93%) are also WhatsHap and
   HapCUT2 errors at the identical pair, against 183 of 496 under v5.0q
   (`item4_overlap.tsv`). Inside the shared regions each tool has 1,127–1,492 errors at
   30–60× under v4.2.1 and 32–393 under v5.0q. The convergence under v4.2.1 therefore
   comes from switch positions common to all tools, which points to the v4.2.1
   phase-transfer truth rather than to new sequence; v5.0q truth separates the tools
   within the same regions (shared: 2.1–3.1-fold at 10–20× and 6–10-fold at 30–60×,
   the latter driven by HapCUT2).
3. Inside the v5.0q BED the low-coverage separation is concentrated in segmental
   duplications and low-mappability regions (10×: 51 / 264 / 292 errors in `segdup`); in
   `not_difficult` the three tools are close at 30–60× (60×: 20 / 38 / 40). HapCUT2's
   excess at high coverage is in homopolymers and tandem repeats.

What they do not show: whether the shared-position errors under v4.2.1 are truth errors
was not checked against reads or the T2T assembly; `neither` sites are not covered by
either benchmark's region definition, so their truth phase is the least certain.

## Item 3: indel phase accuracy (v5.0q, no BED)

Per genome, 10× (mean of ten replicates) / 60×:

| | LP2 SNV+indel | LP2 SNV+indel, no GNN | LP2 four-class | WhatsHap with indels |
|---|---|---|---|---|
| phased indels | 157,148 / 234,254 | 159,017 / 234,940 | 157,408 / 234,414 | 169,742 / 257,426 |
| switch errors in pairs with an indel | 300 / 130 | 495 / 183 | 311 / 138 | 2,685 / 4,377 |
| rate, pairs with an indel | 0.101% / 0.030% | 0.165% / 0.042% | 0.105% / 0.031% | 0.840% / 0.912% |
| rate, all SNV+indel pairs | 0.090% / 0.027% | 0.151% / 0.042% | 0.091% / 0.027% | 0.350% / 0.253% |
| indel Hamming | 6.8% / 3.5% | 10.8% / 6.4% | 7.0% / 3.5% | 12.5% / 9.8% |
| SNV switch errors (Fig. 4) | 1,704 / 591 | 2,913 / 953 | 1,726 / 585 | 5,174 / 2,139 |

- LongPhase 2's indel switch error rate is 8–31-fold below WhatsHap's; WhatsHap's
  indel errors rise with coverage while its SNV errors fall.
- GNN correction removes 29–39% of the indel switch errors; adding SVs or 5mC does not
  change indel accuracy.
- WhatsHap phases 8–10% more indels.
- Restricted to the v5.0q BED (`region = v5bed` rows) the picture is the same: LongPhase
  2 four-class 0.084% / 0.015%, WhatsHap 0.73% / 0.86% at 10× / 60×.

## Files

| File | Contents |
|---|---|
| `score_phase.py` | scorer (see Method) |
| `slim_vcf.py` | builds the slim archive VCFs |
| `run_scoring.sh` | scores every VCF of an unpacked slim archive, then runs `aggregate.py` |
| `aggregate.py` | builds the tables below; reads the manuscript tables for step 0 |
| `step0_check.tsv` | every run's totals next to the table values |
| `item4_strata.tsv` | SNV pairs and switch errors per tool, run, truth, region, stratum |
| `item4_overlap.tsv` | switch errors at identical SNV pairs across tools, replicate 1 |
| `item3_indel.tsv` | indel and SNV switch errors, pairs and Hamming per configuration, run, region |
| `summary.txt` | printed output of `aggregate.py` |

Tools: `longphase compare` from release v2.1 (validation only), Python 3.12, numpy 2.4.4.
