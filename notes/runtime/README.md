# Runtime and memory (issue #3)

SNV-only phasing of HG002 ONT R10.4.1, replicate 1 at 10× and the 60× run, on the
workstation of Methods (inputs and outputs on the hard-disk drive `/disk/research`).
`runtime.tsv`: wall-clock time, CPU time (user + sys) and peak resident memory (KiB, as
`/usr/bin/time` reports it; GiB in the table below);
`build_runtime.py` rebuilds it on the lab server.

| Tool | Threads | 10× wall | 10× CPU | 10× peak RSS | 60× wall | 60× CPU | 60× peak RSS |
|---|---|---|---|---|---|---|---|
| LongPhase 2 | 24 | 3.5 min | 12.3 min | 19.3 GiB | 15.5 min | 30.7 min | 30.1 GiB |
| LongPhase 2 | 1 | 8.3 min | 8.4 min | 6.3 GiB | 19.1 min | 18.8 min | 7.4 GiB |
| WhatsHap 2.8 `--only-snvs` | 1 | 25.2 min | 25.1 min | 1.5 GiB | 113.8 min | 113.6 min | 4.0 GiB |
| HapCUT2 1.3.4 | 1 | 24.1 min | 24.1 min | 6.6 GiB | 96.4 min | 95.9 min | 19.4 GiB |

## Sources

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
    `extractHAIRS` and `HAPCUT2`). No time at 30× and 40×: these two logs were overwritten on
    2026-07-18 by a rerun that was stopped after 3–5 s (`Command terminated by signal 2`), and no
    other copy of the original logs was found; `build_runtime.py` skips them.
- **1 thread (LongPhase 2 v2.1, superseded):** timed on 2026-10-09 with `/usr/bin/time -v`, same machine and
  disk, with every other job on the server stopped.

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
