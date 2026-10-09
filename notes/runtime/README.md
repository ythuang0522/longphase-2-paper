# Runtime and memory (issue #3)

SNV-only phasing of HG002 ONT R10.4.1, replicate 1 at 10× and the 60× run, on the
workstation of Methods (inputs and outputs on the hard-disk drive `/disk/research`).
`runtime.tsv`: wall-clock time, CPU time (user + sys) and peak resident memory;
`build_runtime.py` rebuilds it on the lab server.

| Tool | Threads | 10× wall | 10× CPU | 10× peak RSS | 60× wall | 60× CPU | 60× peak RSS |
|---|---|---|---|---|---|---|---|
| LongPhase 2 | 24 | 4.6 min | 13.6 min | 37.7 GB | 16.3 min | 34.5 min | 66.1 GB |
| LongPhase 2 | 1 | 8.1 min | 8.3 min | 6.5 GB | 18.0 min | 18.8 min | 7.7 GB |
| WhatsHap 2.8 `--only-snvs` | 1 | 25.2 min | 25.1 min | 1.6 GB | 113.8 min | 113.6 min | 4.1 GB |
| HapCUT2 1.3.4 | 1 | 24.1 min | 24.1 min | 6.9 GB | 96.4 min | 95.9 min | 20.4 GB |

## Sources

- **24 threads (LongPhase 2), WhatsHap, HapCUT2:** the runs that produced the phased VCFs of
  the paper. Their logs end with the output of `/usr/bin/time`; these are the values behind
  the current Results sentence (about 4 and 16 min, 25 and 95 min, 25 and 112 min).
  - LongPhase 2: `/disk/research/longphase/longphase_{c}x_1.log` (`phase`) plus
    `/disk/research/longphase_gnn/longphase_gnn_{c}x_1.log` (`gnn`); times summed, peak RSS
    the larger of the two.
  - WhatsHap: `/disk/research/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.log`
  - HapCUT2: `/disk/research/hapcut2_v1.3.4/hapcut2_v134_{c}x_1.log` (one timing covering
    `extractHAIRS` and `HAPCUT2`)
- **1 thread (LongPhase 2):** timed on 2026-10-09 with `/usr/bin/time -v`, same machine and
  disk, with every other job on the server stopped.

## Commands

```
# LongPhase 2, 24 threads (paper runs)
longphase phase --ont -t 24 --dot -s pepper_${c}x_1.vcf.gz -b hg002.sup.${c}x.1.bam -r REF -o longphase_${c}x_1
longphase gnn -t 24 -B 0.30 -s longphase_${c}x_1.vcf -r REF -o longphase_gnn_${c}x_1

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
