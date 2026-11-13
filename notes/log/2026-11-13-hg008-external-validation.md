# HG008 external validation of the frozen GNN (issue #11)

2026-11-13, `notes/hg008_validation/`. Frozen v2.1.2 on HG008-N-P nanopore (10× and 20× seeds 1–3, 30× seed 1;
28 runs) against assembly-derived phase from HG008-N v6.3.

- **GNN effect:** it removes 15–20% of switch errors in every run.
- **Comparison with other tools:** LongPhase 2 keeps 1.8–3.6-fold lower switch error rates than WhatsHap and 2.4–5.4-fold lower than HapCUT2.
- **Completeness:** about 0.6 percentage point lower than both.
- **Caveat:** the evaluation reads very likely contributed to the assembly.

Results were posted to the issue on the same day. Not yet in the manuscript. To decide (author): main-text panel or Supplementary, and the Results/Discussion wording.
