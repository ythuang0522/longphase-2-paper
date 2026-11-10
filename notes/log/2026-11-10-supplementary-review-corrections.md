# Supplementary review: remaining corrections

2026-11-10 (author: apply all review items). No new measurements.

- S1 Supplementary Table 3 legend: "(Fig. 5d)" → "(Supplementary Fig. 6b)" (HiFi precision; Fig. 5d is now
  the WhatsHap phase-error panel). Generator and `supp_tables/hifi.tex`.
- S3 Supplementary Data 1 text: 15 sheets (the `Runtime` sheet added to the inventory; Supplementary
  Fig. 8 and Table 11 use its SSD rows); labels `longphase_v2.1.2` (were `v2.1.1`) in `co-phase_Detail`
  and `SV_5mC_phasing`; the list of figures and tables now has Supplementary Figs. 2 and 8 and
  Supplementary Table 11. Checked against the sheet names and labels of `supplementary.xlsx`.
- S4 Results, variant-class paragraph: "(Supplementary Fig. 5 and Supplementary Table 6)". Supplementary
  Fig. 5 had no main-text citation; the numbering by first citation is now complete for Figs. 1–18.
- S6 Supplementary Table 10 title: "SNVs left unphased at high phasing uncertainty (unphased by GNN
  correction), …". Generator and `supp_tables/t2t.tex`.
- S8 Supplementary Fig. 10e legend: the last neighbour-link filter is not shown.
- S10 Supplementary Table 19: the HiFi reads row moved after the nanopore reads row.
- S11 Supplementary Table 16 legend: "released model (trained for v2.1.1 and unchanged in v2.1.2)".
- S12 Source comments with old numbers marked as "before the 2026-11-03 renumbering".
- S7 Supplementary Table 4 title (author, option B, after the TinkerHap rows were removed): "Phasing compared
  with further phasers." → "Additional phasing comparisons on replicate 1."; "replicate 1" removed from the
  first legend sentence.
- Not changed: S9 (present tense in
  Supplementary Methods 5 and 6 is kept for software behaviour and metric definitions).

Generated legends were edited in `figures-source/make_results_figs.py` and, with the same text, in the
generated `.tex` files (no figure regeneration).
