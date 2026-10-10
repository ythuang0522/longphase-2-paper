# MethPhaser 0.0.4 on LongPhase 2 SNV phasing (issue #5; Fig. 2i–l, Supplementary Fig. 11)

HG002 nanopore, replicate 1, 10, 20, 30, 40, 50 and 60×. Scored with `longphase compare`
(release v2.1) against `HG002_GRCh38_v5.0q_smvar.chr1_22.vcf`, no BED, as for the other tables.

## Why the old values equalled the input

The first run (MethPhaser 0.0.3, bioconda) wrote output VCFs equal to their input. Every
`methphasing` call crashed on secondary alignments, which have no SEQ but keep the MM tag
("MM tag refers to bases beyond sequence length", then `AttributeError` on `mm.keys()`), and
`meth_phaser_parallel` ignores the exit status of its workers. This is cause 1/2 of the issue,
not cause 3. MethPhaser was rerun with 0.0.4 (git tag `0.0.4`, `/disk/software/methphaser`) on
primary alignments only (`-F 0x900`), as the WhatsHap-input pipeline
(`/disk/research/methphaser/run_methphaser.sh`) already did.

## Run checks

All six runs finished: `Exit status: 0` from `/usr/bin/time -v` for both `meth_phaser_parallel`
and `meth_phaser_post_processing`, no `Traceback` in either log, and every record of the
repaired VCF has 10 columns.

| Cov. | `meth_phaser_parallel` wall | `meth_phaser_post_processing` wall |
|---|---|---|
| 10× | 1:27:10 | 0:21:53 |
| 20× | 2:52:29 | 0:18:32 |
| 30× | 4:18:24 | 2:11:40 |
| 40× | 9:10:16 | 0:34:56 |
| 50× | 11:43:45 | 0:36:57 |
| 60× | 14:06:50 | 0:41:40 |

## Commands

Input: `longphase/longphase_{c}x_1.vcf` (LongPhase 2 SNV phasing without GNN; the same file as
`supplementary.xlsx` `SNV_Detail`, `longphase_v2.0.1`, replicate 1), its BAM haplotagged by
LongPhase (from the BAM header: `longphase haplotag -r GRCh38.fa -s longphase_{c}x_1.vcf.gz -b
hg002.sup.{c}x.1.bam -o hg002.sup.{c}x.1.tagged -t 24`, v2.0.2), and a phase-block GTF of that
VCF (one record per PS block, `whatshap stats --gtf` format; its blocks equal the PS blocks).
`scripts/run_mp.sh` runs, per coverage (T = 16):

```sh
samtools view -b -F 0x900 -o tagged.primary.bam hg002.sup.{c}x.1.tagged.bam
meth_phaser_parallel -t 16 -b tagged.primary.bam -r GRCh38.fa -g longphase_{c}x_1.gtf \
    -vc longphase_{c}x_1.vcf.gz -o work/
meth_phaser_post_processing -t 16 -ib tagged.primary.bam -if work/ \
    -ov methphaser_{c}x_1.vcf -ob output -vc longphase_{c}x_1.vcf.gz
python fix_methphaser_vcf.py methphaser_{c}x_1.vcf methphaser_{c}x_1.fixed.vcf
```

`meth_phaser_post_processing` writes some records without a newline; `scripts/fix_methphaser_vcf.py`
splits them and sorts the records. `meth_phaser_post_processing` has one local patch: the new PS value
is wrapped in `str()` before it replaces the old one (0.0.4 passes an int to `str.replace` and
crashes); nothing else in 0.0.4 was changed. Outputs:
`/disk/research/methphaser/rerun_0.0.4/{c}x/methphaser_{c}x_1.fixed.vcf`.

## Output against input (`vcf_diff.tsv`, `scripts/vcf_diff.py`)

Records matched by CHROM, POS, REF and ALT. Blocks = distinct (CHROM, PS).

| Cov. | GT changed | PS changed | Blocks before | Blocks after | Records not in output |
|---|---|---|---|---|---|
| 10× | 27,157 | 61,465 | 7,035 | 6,888 | 2,885 |
| 20× | 343,588 | 700,376 | 4,573 | 3,634 | 3,097 |
| 30× | 441,037 | 1,003,763 | 3,595 | 2,588 | 3,280 |
| 40× | 457,429 | 1,007,789 | 2,932 | 1,956 | 4,136 |
| 50× | 524,665 | 1,133,369 | 2,590 | 1,664 | 3,833 |
| 60× | 554,753 | 1,154,000 | 2,386 | 1,493 | 3,997 |

GT changes are flips (`0|1` ↔ `1|0`) of joined blocks. The records missing from the output are
dropped by `meth_phaser_post_processing` itself (they are already absent from the unrepaired
VCF); at 10×, 2,641 of the 2,885 are homozygous or RefCall records and 244 heterozygous. The
phased SNV count assessed by `compare` is identical before and after at every coverage.

## Scores (`methphaser_vs_longphase.tsv`, `build_tables.py`)

MethPhaser and its input are scored in `compare/`. LongPhase 2 SNV + 5mC co-phasing is read
from the existing compare TSVs of the paper runs (`/disk/research/longphase_coh_methyl{,_gnn}/`,
the same values as `supplementary.xlsx` `co-phase_Detail`, case `Mod`). Assessed pairs =
`all_assessed_pairs` summed over chromosomes.

| Cov. | Run | Phased SNVs | Switch errors | Assessed pairs | Switch error rate (%) | Hamming (%) | Blocks | N50 (Mb) |
|---|---|---|---|---|---|---|---|---|
| 10× | MethPhaser input | 1,873,883 | 2,277 | 1,868,425 | 0.122 | 6.93 | 6,029 | 0.94 |
| | MethPhaser | 1,873,883 | 2,317 | 1,868,571 | 0.124 | 7.18 | 5,882 | 1.05 |
| | LongPhase 2 SNV + 5mC, no GNN | 1,874,434 | 2,280 | 1,869,105 | 0.122 | 6.95 | 5,896 | 0.96 |
| | LongPhase 2 SNV + 5mC, GNN | 1,868,528 | 1,554 | 1,862,594 | 0.083 | 5.31 | 6,959 | 0.88 |
| 20× | MethPhaser input | 2,185,073 | 1,311 | 2,181,856 | 0.060 | 3.99 | 3,570 | 1.70 |
| | MethPhaser | 2,185,073 | 1,508 | 2,182,789 | 0.069 | 7.09 | 2,633 | 2.51 |
| | LongPhase 2 SNV + 5mC, no GNN | 2,185,194 | 1,288 | 2,182,247 | 0.059 | 4.63 | 3,294 | 1.85 |
| | LongPhase 2 SNV + 5mC, GNN | 2,182,426 | 910 | 2,179,224 | 0.042 | 3.40 | 4,136 | 1.74 |
| 30× | MethPhaser input | 2,197,572 | 1,004 | 2,194,914 | 0.046 | 2.40 | 3,007 | 1.97 |
| | MethPhaser | 2,197,572 | 1,142 | 2,195,916 | 0.052 | 5.89 | 2,004 | 3.78 |
| | LongPhase 2 SNV + 5mC, no GNN | 2,197,510 | 1,015 | 2,195,076 | 0.046 | 2.53 | 2,781 | 2.12 |
| | LongPhase 2 SNV + 5mC, GNN | 2,195,127 | 692 | 2,192,540 | 0.032 | 2.01 | 3,555 | 2.07 |
| 40× | MethPhaser input | 2,198,268 | 878 | 2,195,968 | 0.040 | 2.37 | 2,624 | 2.29 |
| | MethPhaser | 2,198,268 | 944 | 2,196,935 | 0.043 | 4.51 | 1,655 | 4.48 |
| | LongPhase 2 SNV + 5mC, no GNN | 2,198,247 | 881 | 2,196,169 | 0.040 | 2.72 | 2,401 | 2.55 |
| | LongPhase 2 SNV + 5mC, GNN | 2,196,178 | 611 | 2,193,954 | 0.028 | 2.20 | 3,189 | 2.47 |
| 50× | MethPhaser input | 2,196,081 | 883 | 2,194,017 | 0.040 | 1.86 | 2,389 | 2.57 |
| | MethPhaser | 2,196,081 | 938 | 2,194,938 | 0.043 | 5.16 | 1,465 | 5.57 |
| | LongPhase 2 SNV + 5mC, no GNN | 2,196,122 | 890 | 2,194,239 | 0.041 | 2.09 | 2,207 | 2.91 |
| | LongPhase 2 SNV + 5mC, GNN | 2,194,139 | 610 | 2,192,143 | 0.028 | 1.83 | 2,992 | 2.87 |
| 60× | MethPhaser input | 2,193,366 | 743 | 2,191,468 | 0.034 | 1.75 | 2,225 | 2.91 |
| | MethPhaser | 2,193,366 | 777 | 2,192,354 | 0.035 | 3.96 | 1,336 | 6.11 |
| | LongPhase 2 SNV + 5mC, no GNN | 2,193,603 | 736 | 2,191,875 | 0.034 | 1.82 | 2,055 | 3.14 |
| | LongPhase 2 SNV + 5mC, GNN | 2,191,726 | 497 | 2,189,888 | 0.023 | 1.60 | 2,839 | 3.09 |

The MethPhaser rows are also the `MethPhaser` sheet of `supplementary.xlsx` (`SNV_Detail`
columns plus `SNV_assessed_pairs`; `python3 build_tables.py --xlsx ../../supplementary.xlsx`).
`MethPhaserCompare.jsx` (repository root) now holds the MethPhaser output values as well;
`figures-source/make_results_figs.py` (`METH`, `meth_value()`) still holds the input values.
