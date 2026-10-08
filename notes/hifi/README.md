# HiFi: per-coverage variant calls and SNV-only phasing (issue #4)

The earlier HiFi rows phased one call set, made from the 10× alignment, at every
coverage. The rows of `Variant_Calling` and `SNV_Detail` (PB HiFi Revio) now
come from a separate call set for each coverage.

## Data

- Source: GIAB `HG002_PacBio-HiFi-Revio_20231031_48x_GRCh38-GIABv3.bam`
  (Revio, aligned to GRCh38 no-alt). The "50×" rows use this BAM as is.
- 10–40×: one down-sampled replicate each, from the 48× BAM:
  `samtools view --subsample <c/48> --subsample-seed 1` (0.2083, 0.4167, 0.6250, 0.8333).
  More replicates at 10–20× need only another seed (and a PEPPER run each).
- Median depth at chr20 heterozygous SNV calls: 11, 20, 29, 38, 45 (10–50×).

## Commands

Variant calling, PEPPER-Margin-DeepVariant r0.8 (`kishwars/pepper_deepvariant:r0.8-gpu`),
the same as for the nanopore runs except the model preset (`--ont_r10_q20` → `--hifi`):

```
run_pepper_margin_deepvariant call_variant -b hg002.hifi.${c}x.1.bam \
    -f GCA_000001405.15_GRCh38_no_alt_analysis_set.fa -o OUT -p pepper_hifi_${c}x -t 32 --hifi
```

Phasing (SNV-only):

```
longphase phase --pb -t 24 -s pepper_hifi_${c}x.vcf.gz -b hg002.hifi.${c}x.1.bam -r REF -o OUT               # v2.1, GNN
longphase phase --pb -t 24 --disableGNN -s pepper_hifi_${c}x.vcf.gz -b hg002.hifi.${c}x.1.bam -r REF -o OUT  # v2.1, no GNN
whatshap phase --only-snvs --ignore-read-groups --reference=REF -o OUT.vcf pepper_hifi_${c}x.vcf.gz hg002.hifi.${c}x.1.bam   # 2.8
```

LongPhase is the release v2.1 binary (`longphase_linux-x64`). In `SNV_Detail`
the `longphase_v2.0.1` block holds the v2.1 `--disableGNN` run and the
`longphase_v2.1` block the GNN run, as for the nanopore rows.

Scoring, as for the nanopore tables (release v2.1, v5.0q chr1–22, no BED):

```
longphase compare --ignore-sample-name HG002_GRCh38_v5.0q_smvar.chr1_22.vcf OUT.vcf -o sw_OUT
```

## Results (replicate 1, v5.0q, no BED)

| Coverage | Het. SNV calls | WhatsHap SW | LongPhase 2 no GNN SW | LongPhase 2 GNN SW | WhatsHap / GNN |
|---|---|---|---|---|---|
| 10× | 2,367,609 | 2,655 | 1,328 | 1,070 | 2.48 |
| 20× | 2,485,185 | 2,504 | 1,268 | 945 | 2.65 |
| 30× | 2,468,170 | 2,331 | 1,137 | 885 | 2.63 |
| 40× | 2,438,078 | 1,954 | 1,153 | 869 | 2.25 |
| 50× (48×) | 2,410,815 | 1,687 | 988 | 740 | 2.28 |

SW: SNV switch errors. The full rows (phased SNVs, Hamming distance, blocks,
N50) are in `supplementary.xlsx`.

The number of heterozygous SNV calls falls above 20× because PEPPER makes
fewer false heterozygous calls: on chr1–22, against the v5.0q heterozygous
SNVs, precision rises from 0.894 (10×) to 0.926 (50×), and recall is
0.877 at 10× and 0.922–0.926 at 20–50×.

## Variant_Calling columns

Same definitions as the existing rows (checked against nanopore 10x_1 and the
old HiFi 10× row):

- Hetero. SNV: PASS, GT 0/1, single-base REF and ALT.
- Homo. SNV: single-base REF and ALT with PASS GT 1/1 **or refCall GT 0/0**
  (the refCall records are PEPPER candidates genotyped homozygous reference).
- Hetero. INDEL: PASS, GT 0/1, all other records.

The old 10× row and the new 10× row differ by 6 PASS 1/1 calls (a separate
PEPPER run on the same BAM).
