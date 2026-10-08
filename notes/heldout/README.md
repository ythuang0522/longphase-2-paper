# Held-out chromosomes chr17, chr21, chr22 (issue #2)

The GNN was trained on windows from chr1–14 and chr18–20, validated on
chr15–16 and tested on chr17, chr21 and chr22. These tables rescore the
existing phased VCFs (the same files as the 2026-09-24 tables, `data/vcf/`)
on the three held-out chromosomes only. No new phasing was run.

## Command

Release v2.1 `compare`, the same options as the 2026-09-24 tables, plus
`--regions`:

```
longphase compare --ignore-sample-name --regions=chr17,chr21,chr22 TRUTH QUERY.vcf -o OUT
```

TRUTH is `HG002_GRCh38_v5.0q_smvar.chr1_22.vcf` or
`HG002_GRCh38_1_22_v4.2.1_benchmark_hifiasm_v11_phasetransfer.noDirty.vcf`, with
no BED. `run_heldout.sh` runs every group and writes the tables.

Check: without `--regions`, the command reproduces the 2026-09-24 tables exactly
(e.g. `longphase_gnn_10x_1`: 1,510 SNV switch errors against v5.0q). Eight
groups were checked at 10x_1: LongPhase 2 GNN, co-phasing (SV, indel+SV),
WhatsHap with and without indels and HapCUT2, against v5.0q and v4.2.1.

## Files

| File | Runs | Truth |
|---|---|---|
| `heldout_v50q.txt` | SNV-only: `longphase_gnn`, `longphase` (no GNN), `whatshap_v28_onlySNVs`, `hapcut2_v134` (64 runs each), `margin_v231`, `ralphi` (60 runs each, 10–20x) | v5.0q |
| `heldout_cophase_v50q.txt` | the 12 co-phasing groups (with and without GNN), `longphase_gnn`, `longphase`, `whatshap_v28` (with indels), `whatshap_v28_onlySNVs` (64 runs each) | v5.0q |
| `heldout_GIAB421.txt` | the same SNV-only groups as `heldout_v50q.txt` | v4.2.1 |
| `heldout_summary.tsv` | per coverage: mean SNV switch error rate of each SNV-only tool, WhatsHap/LP2 and HapCUT2/LP2 ratios, GNN reduction of switch errors, and GNN cost (phased SNVs withheld per switch error removed; the B = 0.30 criterion of Supplementary Method 4 is cost ≤ 10). Pooled over the 60 runs at 10–20× (v5.0q): 21.2% removed at cost 10.5, against 33.1% at 8.3 genome-wide | both |

The table format is that of the 2026-09-24 tables: one `###` summary line per
run (phased SNVs, SNV switch errors and rate, Hamming distance, blocks, N50).

## Summary (SNV-only, SNV switch error rate, means over replicates at 10–20x)

| | held-out chr17/21/22 | genome-wide (2026-09-24 tables, `supplementary.xlsx`) |
|---|---|---|
| WhatsHap / LongPhase 2, v5.0q | 2.8–3.9 (10–20x), 2.7–4.6 (30–60x) | 2.9–3.7 |
| HapCUT2 / LongPhase 2, v5.0q | 3.3–4.9 (10–20x), 2.8–4.9 (30–60x) | 3.3–4.8 |
| GNN reduction of switch errors, v5.0q | 20–23% (10–20x), 14–20% (30–60x) | 31–33% |
| GNN reduction of switch errors, v4.2.1 | 4–16% (10–20x), 0–3% (30–60x) | |

- All tools have higher switch error rates on the held-out chromosomes than
  genome-wide (LongPhase 2 GNN at 10x: 0.127% against 0.082%).
- The advantage over WhatsHap and HapCUT2 is about the same on the held-out
  chromosomes as genome-wide.
- GNN correction removes fewer switch errors on the held-out chromosomes
  (14–23%) than genome-wide (31–33%). The genome-wide reduction is 31–33% also
  at 30–60x, coverages never used for training, so the difference goes with the
  chromosome rather than the coverage: the training chromosomes contain the same
  loci at every coverage. The held-out value is the better estimate for unseen
  sequence.
- Margin (10–20x only) has a lower held-out switch error rate than LongPhase 2
  at 10–12x against v5.0q (0.099% against 0.127% at 10x) and at all of 10–20x
  against v4.2.1, with shorter blocks (10x_1 N50 0.20 against 0.68 Mb).

## Were chr17, chr21 and chr22 held out from the graph-constant sweep?

No: those constants were tuned on the whole genome, so the three chromosomes are held out from
GNN training only. The constants of Supplementary Method 3 date from LongPhase development in
2023–2024 and have not changed since:

- β = 0.7 (`edgeThreshold`) is in release v1.6 (2024-01); v1.5 already had 0.7 as
  `snpConfidenceThreshold`.
- The base-quality threshold 12 came in PR #42 (2023-12) and PR #50/#52 (2024-02/03), and is in
  v1.7.
- α = 0.1, w = 20 and the single-read guard (N = 3, μ = 0.2) came in PR #82 (2024-07, first
  released in v2.0). The PR gives before/after numbers for SNP-only phasing on HG002 at 10–60×
  (switch errors 1,087–1,196 after the change, N50 up to 2.84 Mb at 60×). Those are
  whole-genome values; chr17/21/22 alone would give about 50 switch errors.

The alignments evaluated in the paper were made in 2026-03, after these sweeps, and the
chromosome split was defined only for GNN training. The B = 0.30 deployment threshold was also
chosen on whole-genome results of the 60 runs at 10–20× (Supplementary Method 4).
