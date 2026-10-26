# 2026-09-24, author decisions and read provenance

**2026-09-24, author decisions and read provenance.** The authors confirmed minimap2
2.30, samtools 1.23.1 and Clair3 v2.0.1 with `r1041_e82_400bps_sup_v500` (inferred
marks removed), 60 training runs, and that the v4.2.1 benchmark BED was applied
(chr1-22); the Zenodo data deposition is dropped at their request, and the code
availability todos no longer ask for Zenodo DOIs.

The previous LongPhase papers do not describe these reads: LongPhase 1.0 (2022) used
the 2019 UCSC ultra-long PromethION HG002 data (R9.4.1), and LongPhase-S and
LongPhase-TO use cancer cell lines only. The provenance was recovered instead from
the reads of `demo/demo.bam` in the source repository, whose basecaller tags name
flow cells PAG65784 and PAG68757, 4 kHz sampling, November 2022 start times and 5mC/5hmC
calls. Those are the two HG002 flow cells of ONT's open-data release
`giab_lsk114_2022.12` (FLO-PRO114M, SQK-LSK114, 400 bps). ONT's workflow report for its
`hg002_sup_v4` output basecalls with Dorado `dna_r10.4.1_e8.2_400bps_sup@v4.0.0` +
`5mCG_5hmCG@v2`, and 12 of 12 demo read IDs match that output with identical read
lengths. Read N50 29.2/29.4 kb (MinKNOW run reports); mean autosomal depth 70.4x (ONT's
released mosdepth distribution); licence CC BY-NC 4.0. All of it is now in Methods,
Data availability and Supplementary Table 5.

**New flag:** the confirmed Clair3 model `r1041_e82_400bps_sup_v500` is trained on
5 kHz Dorado v5.0.0 SUP data, but these reads are a 4 kHz `sup@v4.0.0` basecall. The
matched model is `r1041_e82_400bps_sup_v400` (Rerio), or `sup_v410` among those bundled
with Clair3. The earlier `sup_v500` inference rested on the wrong (2025.01) read-source
hypothesis. Flagged inline in Methods.

The reasoning behind the window: nothing in `GNN source/`, this repo or
`../longphase` records the minimap2, samtools or Clair3 version. The dating
argument, kept as a `%  [note on versions]` comment above
Methods' "Benchmark data" paragraph: Sniffles 2.8.0 (from the demo SV VCF header)
was released 2026-05-07 and branch JH was last committed 2026-08-25, so the calling
runs fall in that window. That **excludes Clair3 v2.0.3** (released 2026-09-09);
the in-window candidates are v2.0.1 and v2.0.2. minimap2 2.30/2.31 and samtools
1.23.1/1.24 bracket similarly but only if alignment happened in the same window,
which is not established. Unconfirmed read-source candidate: the ONT GIAB 2025.01
open-data release (PromethION, SQK-LSK114, Dorado v0.8.2, model
`dna_r10.4.1_e8.2_400bps@v5.0.0`), which would imply the Clair3 model
`r1041_e82_400bps_sup_v500`.
