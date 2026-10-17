# Further phasers (2026-10-17)

Sheet `Other_phasers` of `supplementary.xlsx` (Supplementary Data 1), written by `build_sheet.py`
from the `longphase compare` reports of the runs below. Not in the manuscript text or figures;
whether and how to use them is left to the authors.

All runs: HG002, replicate 1; nanopore 10-60x, HiFi 10-50x (`hg002.hifi.50x.1.bam` is the full 48x
set); the paper's inputs (per-coverage PEPPER calls, the same BAMs, the same Sniffles 2.8 SVs);
default parameters or the workflow the tool documents, no tuning. Scored like every other row:
`longphase compare --ignore-sample-name` against v5.0q chr1-22, no BED (release v2.1; the HiFi
HiPhase runs with the v2.1.1 static binary, same comparison code). Switch errors are SNV switch
errors; SVs themselves are not scored. Run scripts in `scripts/`.

## Tools and how they were run

| Tool | Version | Platform | Command / notes | Script |
|---|---|---|---|---|
| LongHap | 0.2.0 (pip) | ONT | `--ont --min_base_quality 10` (its README for ONT), `--snvs_only`, with `-m` 5mC bedMethyl (modkit 0.6.4 `pileup --combine-strands --cpg --modified-bases 5mC`, as its README) or without; per chromosome | `run_longhap.sh` |
| LongHap, all variants | 0.2.0 | ONT | as above without `--snvs_only`, with 5mC; one VCF = PEPPER SNVs/indels + Sniffles SVs made sequence-resolved by `merge_sv.py` (LongHap reads one VCF and needs allele sequences: `<DEL>` filled from the reference, INS with REF N given the reference base; INV/DUP/BND, 296-373 per coverage, left out) | `run_longhap_allvar.sh`, `merge_sv.py`, `prep_inputs.sh` |
| HapBridge | Humonex/HapBridge ec48f02 | ONT | `bridge.py <vcf> <bam> <out> -t 16` (default bridge2) on the MethPhaser input: LongPhase 2 SNV phasing without GNN and its haplotagged BAM (primary alignments, MM/ML kept). `local_counter.patch`: two debug counters were never defined, so every call raised UnboundLocalError; phasing logic unchanged | `run_hapbridge.sh` |
| TinkerHap | 1.0.0 (pip) | ONT, HiFi | defaults, one run per chromosome (`-r chr<i>`, no thread option); phases indels by default | `run_others_ont.sh`, `run_extra.sh` |
| HiPhase | 1.7.0 | HiFi | defaults (global realignment on), `--threads 16 --ignore-read-groups` (required: BAM read groups do not name the VCF sample); phases indels by default | `run_hiphase_hifi.sh` |
| LongPhase | 2.1.1 static | HiFi | the paper's HiFi command with `--indels` | `run_hifi_indels.sh` |
| WhatsHap | 2.8 | HiFi | the paper's HiFi command without `--only-snvs` | `run_hifi_indels.sh` |
| HapCUT2 | 1.3.4 | ONT, HiFi | the paper's commands with `extractHAIRS --indels 1`; ONT input = full PEPPER calls (`pepper_calling/`; the paper's SNV runs read the SNV-only `pepper_calling3/`); records whose GT is not two alleles from {0,1,2} dropped | `run_hapcut2_indels.sh`, `run_hapcut2_indels_hifi.sh` |

Dropped: HiPhase on nanopore (a PacBio tool; 10-40x were run, `/ssd/longphase_process/others_ont/`,
not in the sheet); LongHap on HiFi (5mC on HiFi not used in the paper); HiPhase all-variant
co-phasing on nanopore. A chr22 30x screen of HiPhase and TinkerHap is in `run_quicktest.sh`.

## Results (SNV switch error % / Hamming % / block N50)

LongPhase rows not in `Other_phasers` come from `SNV_Detail` and `co-phase_Detail` (replicate 1).

**ONT, SNV + 5mC** (N50 Mb)

| Cov | LongPhase 2.1.1 Mod | MethPhaser | HapBridge | LongHap 5mC | LongHap seq |
|---|---|---|---|---|---|
| 10x | 0.083 / 5.38 / 0.88 | 0.124 / 7.19 / 0.96 | 0.122 / 6.93 / 0.94 | 0.180 / 4.35 / 0.41 | 0.175 / 4.09 / 0.40 |
| 30x | 0.030 / 2.05 / 2.08 | 0.052 / 5.96 / 3.35 | 0.046 / 2.58 / 1.98 | 0.158 / 19.99 / 4.35 | 0.136 / 8.81 / 1.79 |
| 60x | 0.022 / 1.60 / 3.09 | 0.035 / 3.95 / 5.49 | 0.033 / 2.50 / 4.18 | 0.110 / 18.44 / 5.40 | 0.096 / 10.06 / 2.55 |

LongHap phases 59.9% of benchmark SNVs at 10x and 87-90.5% above (LongPhase 77.9-91.5%): its ONT
mode leaves alleles with no read on one strand unphased. HapBridge left the 10x and 20x input
unchanged and corrected no switch at any coverage (`detect_switch` empty); it joined blocks at
30-60x.

**ONT, SNV + indel** (N50 Mb; LongPhase = co-phase_Detail Indel, WhatsHap = co-phase_Detail)

| Cov | LongPhase | WhatsHap | HapCUT2 | TinkerHap |
|---|---|---|---|---|
| 10x | 0.091 / 7.02 / 0.98 | 0.270 / 12.47 / 1.28 | 0.315 / 12.79 / 1.37 | 0.332 / 8.14 / 0.80 |
| 30x | 0.037 / 4.96 / 2.48 | 0.137 / 9.71 / 2.98 | 0.177 / 11.65 / 3.45 | 0.197 / 9.72 / 1.96 |
| 60x | 0.027 / 3.56 / 3.74 | 0.097 / 9.29 / 4.20 | 0.126 / 13.48 / 5.01 | 0.151 / 13.16 / 3.13 |

**ONT, SNV + indel + SV + 5mC** (N50 Mb, phased indels %)

| Cov | LongPhase Indel+Mod+SV | LongHap all variants |
|---|---|---|
| 10x | 0.092 / 6.92 / 1.02 / 30.5 | 0.219 / 6.43 / 0.47 / 27.1 |
| 30x | 0.038 / 5.49 / 2.65 / 43.4 | 0.166 / 21.91 / 4.52 / 47.7 |
| 60x | 0.026 / 3.34 / 4.14 / 45.4 | 0.114 / 20.97 / 6.83 / 50.7 |

**HiFi, SNV + indel** (N50 kb; LongPhase SNV-only from SNV_Detail for reference)

| Cov | LongPhase SNV | LongPhase indels | WhatsHap | HapCUT2 | HiPhase | TinkerHap |
|---|---|---|---|---|---|---|
| 10x | 0.049 / 0.73 / 341 | 0.094 / 2.54 / 402 | 0.252 / 4.89 / 435 | 0.272 / 5.44 / 449 | 0.164 / 4.15 / 445 | 0.283 / 5.36 / 439 |
| 30x | 0.038 / 0.81 / 540 | 0.054 / 1.84 / 626 | 0.144 / 3.24 / 650 | 0.177 / 4.27 / 704 | 0.091 / 2.60 / 713 | 0.181 / 3.94 / 688 |
| 50x | 0.033 / 0.82 / 584 | 0.041 / 1.49 / 681 | 0.096 / 2.05 / 686 | 0.131 / 3.39 / 746 | 0.070 / 2.11 / 778 | 0.133 / 3.44 / 747 |

HiPhase wall/CPU/RSS on HiFi (16 threads, alone on the machine): 10x 3.4 min / 57 min / 4.1 GiB,
50x 12.2 min / 187 min / 4.1 GiB (LongPhase 50x: 2.4 / 14.3 min). Other runs shared the machine
and are not timed.

On chr22 alone (30x screen) HiPhase had fewer switches than LongPhase (ONT 38 vs 42, HiFi 45 vs 49);
genome-wide LongPhase has about half (HiFi 10-50x). chr22 is not representative.
