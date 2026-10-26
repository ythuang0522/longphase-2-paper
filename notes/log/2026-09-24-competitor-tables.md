# Competitor tables, 2026-09-24

**Competitor tables, 2026-09-24.** JHL pushed `20260924_v50q.txt`, `20260924_GIAB421.txt`
and `20260924_cophase_v50q.txt` (`longphase compare` output; WhatsHap 2.8 default and
`--only-snvs`, HapCUT2 1.3.4, and GNN-corrected LongPhase 2 SNV-only, +indel, +SV and
+indel+SV; ten replicates at 10–20×, seed 10 included). The SNV-only corrected LongPhase 2
rows are identical to `GNN source/sw_longphase_v2.0.2_SNVonly_GNN.log` plus the new 10×
seed-10 row; the four-class (with 5mC) configuration is not in the new tables. All WhatsHap
(`--only-snvs`) and HapCUT2 values in Results, Discussion, Introduction and abstract are now
exact, and fold-changes are recomputed from rates: with correction 2.9–3.7× vs WhatsHap and
3.3–4.8× vs HapCUT2 (v5.0q, 10–60×); 1.1–1.7× under v4.2.1 (1.1–1.3× at 30–60×); without
correction 1.9–2.5× and 2.2–3.3×. LongPhase 2 values stay on the n = 9 tables at 10× so
that corrected and uncorrected remain paired; WhatsHap/HapCUT2 are n = 10 (Methods, Fig. 2
legend updated). Still plot-read: LongPhase 1.0, uncorrected LongPhase 2 under v4.2.1,
runtimes. Unused so far: default WhatsHap phases indels (32.9–49.8% of benchmark indels vs
30.5–45.4% for LongPhase 2) at far higher SNV switch error and Hamming distance (9–13%),
which would support an indel co-phasing comparison.
