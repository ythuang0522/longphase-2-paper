# Runtime and memory (issue #3)

SNV-only phasing of HG002 ONT R10.4.1, replicate 1 at 10× and the 60× run, on the
workstation of Methods (inputs and outputs on the hard-disk drive `/disk/research`).
`runtime.tsv`: wall-clock time, CPU time (user + sys) and peak resident memory (KiB, as
`/usr/bin/time` reports it; GiB in the table below);
`build_runtime.py` rebuilds it on the lab server.

| Tool | Threads | 10× wall | 10× CPU | 10× peak RSS | 60× wall | 60× CPU | 60× peak RSS |
|---|---|---|---|---|---|---|---|
| LongPhase 2 | 24 | 2.9 min | 4.5 min | 1.4 GiB | 14.8 min | 22.8 min | 3.5 GiB |
| LongPhase 2 | 1 | 3.2 min | 2.8 min | 1.2 GiB | 12.8 min | 11.9 min | 1.2 GiB |
| WhatsHap 2.8 `--only-snvs` | 1 | 25.2 min | 25.1 min | 1.5 GiB | 113.8 min | 113.6 min | 4.0 GiB |
| HapCUT2 1.3.4 | 1 | 24.1 min | 24.1 min | 6.6 GiB | 96.4 min | 95.9 min | 19.4 GiB |

## Sources

- **LongPhase 2 v2.1.2 (2026-10-26), the values in the tables above:** release binary, all runs repeated on
  the same workstation and disk (`/ssd/longphase_process/v2.1.2/run_a.sh`): nanopore 24 threads at every
  coverage (64 runs), one thread at 10× and 60×, HiFi 24 threads at 10–50×; one run at a time on an idle
  machine, page cache cleared before each run, output identical to v2.1.1. Logs:
  `/disk/research/v2.1.2/{longphase_gnn,longphase_gnn_t1,pacbio/longphase_hifi}/*.log`. Compared with
  v2.1.1 (10–20×, 60 runs, medians): wall 4.8 → 4.3 min, CPU 13.8 → 6.3 min, peak memory 22.9 → 1.7 GiB.
  The v2.1.1 rows below are in git history.

- **LongPhase 2 (v2.1.1, 2026-10-16):** 24 threads from the logs of the v2.1.1 rerun,
  `/disk/research/v2.1.1/longphase_gnn/longphase_gnn_{c}x_1.log` (one `phase` command, GNN
  included); 1 thread re-timed on 2026-10-16 with the release binary
  (`/ssd/longphase_process/runtime/run_t1_v2.1.1.sh`, `time/longphase_v2.1.1_gnn-t1_{c}.time`),
  after waiting for no other phasing job and a load average below 2, BAM read once before the
  run. The v2.1 values (24 threads 4.6 and 16.3 min, 36.0 and 63.0 GiB; 1 thread 8.1 and
  18.0 min) are in git history.
- **WhatsHap, HapCUT2 (and LongPhase 2 v2.1, superseded):** the runs that produced the phased VCFs of
  the paper. Their logs end with the output of `/usr/bin/time`; these are the values behind
  the current Results sentence (about 4 and 16 min, 25 and 95 min, 25 and 112 min).
  - LongPhase 2: `/disk/research/longphase/longphase_{c}x_1.log` (`phase`) plus
    `/disk/research/longphase_gnn/longphase_gnn_{c}x_1.log` (`gnn`); times summed, peak RSS
    the larger of the two.
  - WhatsHap: `/disk/research/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.log`
  - HapCUT2: `/disk/research/hapcut2_v1.3.4/hapcut2_v134_{c}x_1.log` (one timing covering
    `extractHAIRS` and `HAPCUT2`). The 30× and 40× logs were overwritten on 2026-07-18 by a rerun
    that was stopped after 3–5 s (`Command terminated by signal 2`), so these two runs were
    re-timed on 2026-10-16 with the same binaries, commands and inputs, one at a time on an idle
    machine (`/ssd/longphase_process/runtime/run_hapcut2_30_40.sh`, logs in
    `/ssd/longphase_process/runtime/hapcut2_rerun/hapcut2_v134_{30,40}x_1.log`). Their phased
    genotypes are identical to the paper's `hapcut2_v134_{30,40}x_1.vcf.gz` (chrom, pos and
    sample column of every record), so only the timing is new.
- **1 thread (LongPhase 2 v2.1, superseded):** timed on 2026-10-09 with `/usr/bin/time -v`, same machine and
  disk, with every other job on the server stopped.

## PacBio HiFi (`runtime_hifi.tsv`, 2026-10-17)

Replicate 1 at 10–50×, same columns, written by `build_runtime.py`:

- LongPhase 2 v2.1.1 (`--pb -t 24`) at 10–50× and WhatsHap at 10× and 20×: re-timed
  (`/ssd/longphase_process/runtime/run_hifi_retime.sh`, `hifi_retime/*.time`), because the
  original runs had shared the machine (LongPhase 20× 25% CPU, WhatsHap 10–20× 73–82%). One run
  at a time on an idle machine, BAM read once before each run (page cache), output identical to
  the original VCFs. The 10× LongPhase run overlapped a 20-s figure rendering and was repeated
  (53.1 s against 54.4 s); the overlapped files are in `hifi_retime/overlapped/`.
- WhatsHap 30–50×: original logs (`/disk/research/pacbio/whatshap_v28_hifi_onlySNVs_{c}x_1.log`,
  95–99% CPU).
- HapCUT2 (`extractHAIRS --pacbio 1` + `HAPCUT2`): the 2026-10-16 runs that produced its output
  (`/disk/research/pacbio/hapcut2_v1.3.4/hapcut2_v134_hifi_{c}x_1.log`), idle machine.

| Tool | 10× wall | 10× CPU | 10× RSS | 50× wall | 50× CPU | 50× RSS |
|---|---|---|---|---|---|---|
| LongPhase 2, 24 threads | 1.6 min | 2.5 min | 1.4 GiB | 5.9 min | 10.0 min | 1.6 GiB |
| WhatsHap 2.8 | 23.9 min | 23.8 min | 1.5 GiB | 98.4 min | 98.2 min | 3.7 GiB |
| HapCUT2 1.3.4 | 19.5 min | 19.4 min | 7.1 GiB | 59.5 min | 59.1 min | 19.6 GiB |

v2.1.2: LongPhase 2 timed with the page cache cleared (as on nanopore data); CPU time 9.7–14.2-fold less
than WhatsHap and 5.9–10.1-fold less than HapCUT2. Before (v2.1.1, BAM read first):
The LongPhase wall time profits from the page cache (the nanopore 24-thread runs did not read the
BAM first), so CPU time is the comparison to use: 4.0–7.8-fold less than WhatsHap, 3.2–5.1-fold less
than HapCUT2.

### Original HiFi runs against the re-timed runs

Original: `/disk/research/v2.1.1/pacbio/longphase_hifi_{c}x_1.log` (time -v) and
`/disk/research/pacbio/whatshap_v28_hifi_onlySNVs_{c}x_1.log` (GNU time); re-timed:
`/ssd/longphase_process/runtime/hifi_retime/*.time`. Same commands, binaries and inputs; the
phased genotypes of every re-timed run equal the original VCF (chrom, pos and sample column of
every record), so only the times differ.

LongPhase 2 v2.1.1, `--pb -t 24`:

| Coverage | Wall (min), original → re-timed | CPU (min) | CPU use | Peak RSS (GiB) |
|---|---|---|---|---|
| 10× | 2.1 → 0.9 | 5.9 → 6.0 | 279% → 676% | 16.1 → 16.7 |
| 20× | 32.7 → 1.0 | 8.4 → 8.7 | 25% → 837% | 18.5 → 19.5 |
| 30× | 8.7 → 1.2 | 11.0 → 11.2 | 126% → 961% | 19.5 → 20.9 |
| 40× | 10.5 → 1.7 | 12.5 → 13.0 | 119% → 775% | 20.8 → 21.8 |
| 50× | 16.2 → 2.4 | 14.7 → 14.3 | 90% → 607% | 21.9 → 22.6 |

WhatsHap 2.8 `--only-snvs` (30–50× not re-timed; 95–99% CPU in the original runs):

| Coverage | Wall (min), original → re-timed | CPU (min) | CPU use | Peak RSS (GiB) |
|---|---|---|---|---|
| 10× | 32.5 → 23.9 (−27%) | 26.9 → 23.8 (−12%) | 82% → 99% | 1.50 → 1.50 |
| 20× | 101.5 → 62.9 (−38%) | 75.1 → 62.9 (−16%) | 73% → 99% | 1.93 → 2.19 |

- LongPhase: the original wall times were dominated by waiting for input (25–279% CPU with 24
  threads); CPU time changed by −3% to +4%, so it was already usable. The re-timed wall times
  had the BAM in the page cache and are therefore the favourable case; the nanopore 24-thread
  times were not measured that way. Peak RSS rose by 0.6–1.4 GiB (not investigated).
- WhatsHap: CPU time also fell, by 12–16%, presumably because the original runs shared caches
  and memory bandwidth with other jobs (not verified).
- Effect on the comparison (CPU time): WhatsHap / LongPhase 4.5–8.9-fold with the original
  times (4.55, 8.95, 7.86, 7.45, 6.69 at 10–50×), 4.0–7.8-fold with the re-timed ones;
  HapCUT2 / LongPhase 3.3–5.3-fold (3.28, 5.30, 4.04, 4.76, 4.03) and 3.2–5.1-fold. The re-timed
  values, used in `runtime_hifi.tsv` and Supplementary Table 16, give the more conservative
  comparison.

## Commands

```
# LongPhase 2 v2.1.1, 24 threads (paper runs; GNN correction runs within phase, threshold 0.35)
longphase phase --ont -t 24 -s pepper_${c}x_1.vcf.gz -b hg002.sup.${c}x.1.bam -r REF -o longphase_gnn_${c}x_1

# LongPhase 2, 1 thread
longphase phase --ont -t 1 -s pepper_${c}x_1.vcf.gz -b hg002.sup.${c}x.1.bam -r REF -o lp_gnn_t1_${c}x

# WhatsHap 2.8
whatshap phase --only-snvs --ignore-read-groups --reference=REF -o OUT.vcf pepper_${c}x_1.vcf.gz hg002.sup.${c}x.1.bam

# HapCUT2 1.3.4
extractHAIRS --ont 1 --bam hg002.sup.${c}x.1.bam --ref REF --VCF pepper_calling3/pepper_${c}x_1.vcf --out fragment_file
HAPCUT2 --fragments fragment_file --VCF pepper_calling3/pepper_${c}x_1.vcf --output hapcut2_v134_${c}x_1
```

REF: `GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`. Check of the timing environment: a
WhatsHap 10× run repeated on 2026-10-09 took 1,490 s against 1,510 s in the paper run.

## All tools, every run (`all_tools_runtime.tsv`, 2026-10-16)

Wall-clock minutes of SNV-only phasing for every nanopore run (10–20× replicates 1–10, 30–60×
replicate 1), all tools, inputs and outputs on `/disk/research`. 10–20× start from the authors'
table (`longphaseGNN-RunTime.tsv`); every value with a log was re-read from it, values without
a log (GCphase, Ralphi) are kept as given, tools without a run at a coverage are empty, and
`LongPhase_GNN` is replaced by `longphase_v2.1.1` (one `phase` command, `-t 24`, from the
2026-10-14/16 rerun). `build_all_tools_runtime.py` rebuilds it on the lab server; its docstring
lists the log of every column.

## SSD (`runtime_ssd.tsv`, 2026-10-28)

The same SNV-only runs (replicate 1, nanopore 10–60×, HiFi 10–50×) re-timed with inputs and outputs on an
SSD (ext4, NVMe), one run at a time on an idle machine, page cache cleared before every run; LongPhase 2
v2.1.2 with 24 threads and one thread at every coverage. `build_runtime_ssd.py` writes the table (its
docstring has the details: binaries, HapCUT2 input, output checks); scripts in `ssd/`. HapCUT2 at nanopore
60× and on HiFi data was not re-timed (column `storage` = HDD). Tables and fold changes are in
`notes/log/2026-10-28-runtime-ssd.md`. `build_runtime_sheet.py` writes the HDD and SSD values into the `Runtime`
sheet of `supplementary.xlsx`.
