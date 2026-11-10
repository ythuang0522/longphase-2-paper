# Methods review, group C: text for analyses that are not reported

2026-11-10. Author-approved old | new draft. No new measurements.

- C1 LongPhase 1.0: no result of it is in the Results, a Supplementary table or Supplementary Data 1.
  Removed from Methods ("LongPhase 1.0 and LongPhase 2 were run with the nanopore setting…", "LongPhase
  1.0 was re-run on every down-sampling replicate") and its row of Supplementary Table 19 (v1.0, `--ont`,
  commit fe8c1fdff11ba2a082d363a7ffcb5c923cacc316). The citation in the Methods overview stays.
- C2 "and 1-Mb bins" removed (only the by-chromosome result remains, Supplementary Fig. 6d).
- C3 GCphase exclusion shortened to one sentence (the Results sentence is hidden). Removed detail: it
  ignored the FILTER field; about 1.2 million such calls in the 10x replicate-1 output.
- C4 Evaluation metrics: four result sentences removed (SNV-only 30–60x: 2–5% longer blocks and
  1.4–1.8-fold lower Hamming than WhatsHap; SNV + indel: WhatsHap blocks 12–33% longer, indel Hamming
  1.8–2.7-fold higher; MethPhaser Hamming 1.8–2.8-fold over its input at 20–60x). The sentence on block
  length and Hamming distance stays. Provenance comment below the paragraph kept.
- C5 GNN settings in "Comparison with other methods" replaced by "the GNN settings given above".
