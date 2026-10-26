# Threshold sweep and HiFi check, 2026-10-09

**Threshold sweep and HiFi check, 2026-10-09.**
- Author: there is one released GNN (e6), and the full 0.05–0.95 sweep was done on it. The
  "later models were swept over 0.30–0.40" sentence and its `[check]` comment are deleted from
  Supplementary Method 4.
- Issue #4 (HiFi) checked: every value in JHL's comment reproduces from `supplementary.xlsx`
  (switch errors, 2.2–2.6-fold rate ratio, Hamming lower at 10–40× only, N50 within 3.1%, 0.4–0.5
  points more phased SNVs for WhatsHap, GNN removes 19–25%, N50 ratio 4.3). Two stale sentences
  that 9fb0cc4 left were fixed: the old HiFi description and its "being regenerated" `\todo` in
  Methods (duplicating the new HiFi data sentence), and "HiFi call-set handling remains to be
  confirmed" in the Discussion. JHL's view that more HiFi replicates are unnecessary is unchanged
  in Methods ("could be drawn … but were not").
- Same day, Discussion after issues #2 and #4: the limitations paragraph reports the held-out
  result (advantage unchanged; GNN removes 14–23% vs 31–33% at cost 10.5 vs 8.3; chr17/21/22 held out
  from network training only, not from the 2023–2024 constant tuning) instead of asking for it; the
  Margin sentence adds 10–12× on the held-out chromosomes. Supplementary Fig. 13e gains a held-out
  line (nanopore, chr17/21/22), legend moved above the data. No main-figure change.
