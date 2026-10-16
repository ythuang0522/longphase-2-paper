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

## Variant calls (`Variant_Calling`, Supplementary Table 7)

| Coverage | Het. SNV | Hom. SNV | Het. indel | Median DP | Het. SNV precision | Het. SNV recall |
|---|---|---|---|---|---|---|
| 10× | 2,367,609 | 2,081,641 | 425,786 | 11 | 0.894 | 0.877 |
| 20× | 2,485,185 | 2,318,132 | 442,122 | 20 | 0.900 | 0.924 |
| 30× | 2,468,170 | 2,428,526 | 432,578 | 29 | 0.908 | 0.926 |
| 40× | 2,438,078 | 2,508,667 | 425,166 | 38 | 0.919 | 0.926 |
| 50× (48×) | 2,410,815 | 2,566,571 | 420,096 | 45 | 0.926 | 0.923 |

Median DP: FORMAT/DP of PASS het. SNV calls on chr20. Precision and recall: PASS
het. SNV calls on chr1–22 matched by position and ALT to the v5.0q heterozygous SNVs.
The earlier rows (one call set for every coverage) had 2,367,609–2,367,619 het. SNVs.

## Results (replicate 1, v5.0q, no BED)

| Coverage | Het. SNV calls | WhatsHap SW | LongPhase 2 no GNN SW | LongPhase 2 GNN SW | WhatsHap / GNN |
|---|---|---|---|---|---|
| 10× | 2,367,609 | 2,655 | 1,328 | 1,070 | 2.48 |
| 20× | 2,485,185 | 2,504 | 1,268 | 945 | 2.65 |
| 30× | 2,468,170 | 2,331 | 1,137 | 885 | 2.63 |
| 40× | 2,438,078 | 1,954 | 1,153 | 869 | 2.25 |
| 50× (48×) | 2,410,815 | 1,687 | 988 | 740 | 2.28 |

SW: SNV switch errors. The full rows (phased SNVs, Hamming distance, blocks,
N50) are in `supplementary.xlsx`. (LongPhase values in this table are from v2.1; the v2.1.1
values are in `supplementary.xlsx` and below.)

## HapCUT2 (added 2026-10-16)

HapCUT2 1.3.4, the same binaries and two steps as the nanopore runs, with `--pacbio 1` in place
of `--ont 1`, on the same per-coverage call sets and BAMs, replicate 1, one run at a time on an
idle machine (`/ssd/longphase_process/runtime/run_hapcut2_hifi.sh`; outputs, logs and compare
reports in `/disk/research/pacbio/hapcut2_v1.3.4/`):

```
extractHAIRS --pacbio 1 --bam hg002.hifi.${c}x.1.bam --ref REF --VCF pepper_hifi_${c}x.vcf --out fragment_${c}x
HAPCUT2 --fragments fragment_${c}x --VCF pepper_hifi_${c}x.vcf --output hapcut2_v134_hifi_${c}x_1
```

HapCUT2 stops on any genotype that is not two alleles from {0,1,2}, so records with such a GT
were dropped when the VCF was unzipped: refCall `./.` (171, 151, 193, 204, 134 at 10–50×) and
one PASS `2/3` indel at 50×; none is a heterozygous SNV, and the nanopore calls have none. Scored
like the other HiFi runs (v5.0q chr1–22, no BED); `notes/hifi/add_hapcut2.py` writes the reports
into the empty `hapcut2_v134` block of the HiFi rows of `SNV_Detail`.

| Coverage | LongPhase 2.1.1 SW (%) | WhatsHap SW (%) | HapCUT2 SW (%) | HapCUT2 / LP | Hamming (%) | Phased SNV (%) | N50 (kb) | CPU (min) | Peak RSS (GiB) |
|---|---|---|---|---|---|---|---|---|---|
| 10× | 1,020 (0.049) | 2,655 (0.128) | 3,174 (0.152) | 3.10 | 1.06 | 87.47 | 340 | 19.4 | 7.1 |
| 20× | 878 (0.040) | 2,504 (0.114) | 3,071 (0.140) | 3.48 | 1.13 | 92.25 | 480 | 44.4 | 11.4 |
| 30× | 829 (0.038) | 2,331 (0.106) | 2,806 (0.127) | 3.36 | 1.00 | 92.45 | 527 | 44.5 | 14.3 |
| 40× | 815 (0.037) | 1,954 (0.089) | 2,345 (0.106) | 2.86 | 0.97 | 92.41 | 562 | 59.5 | 17.2 |
| 50× (48×) | 714 (0.033) | 1,687 (0.077) | 2,116 (0.096) | 2.95 | 0.75 | 92.08 | 577 | 59.1 | 19.6 |

HapCUT2 had 1.20–1.25 times the switch errors of WhatsHap at every coverage, with almost the
same phased fraction and N50. The original LongPhase and WhatsHap HiFi runs shared the machine with other jobs (WhatsHap
73–82% CPU at 10–20×, LongPhase v2.1.1 20× 32.7 min wall at 25% CPU), so LongPhase 10–50× and
WhatsHap 10–20× were re-timed on 2026-10-16/17 (`/ssd/longphase_process/runtime/run_hifi_retime.sh`,
one at a time on an idle machine, BAM read once before each run; phased genotypes identical to
the original VCFs). Runtime table: `notes/runtime/runtime_hifi.tsv` (Supplementary Table 16; Supplementary
Fig. 10 stays nanopore only, it is a figure of the professor's).

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

## LongPhase v2.1.1 (2026-10-16)

The GNN rows (`longphase_v2.1.1` block of `SNV_Detail`) come from the v2.1.1 release binary,
`/disk/research/v2.1.1/run_hifi.sh` (same command as above, output in `/disk/research/v2.1.1/pacbio/`).
The `--disableGNN` and WhatsHap rows are unchanged.
