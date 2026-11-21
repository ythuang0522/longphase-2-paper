# 2026-11-16 GNN schematics reduced from three to two Supplementary figures (option A)

Author decision, option A of three (A two figures, B one figure, C keep three), after a
review of the overlap between Supplementary Figs. 13–15.

- **Supplementary Fig. 15 removed** (`suppfig6_gnn_architecture.pdf`, GNN architecture).
  Every layer, dimension and the 687,358 stored values are in Supplementary Table 15 and the
  Supplementary Note 4 "Architecture" paragraph; Supplementary Fig. 13c gives the visual summary.
  `fig_s6()` in `figures/supp/make_supp_figs.py` still writes the file; the build does not use it.
- **Supplementary Fig. 14 reduced to panels a–c** (window, bridge-vertex feature, centre-zone
  mask). Panels d (DOT format), e and f (phase set before and after unphasing) are removed:
  Supplementary Fig. 13d shows the same step, and Supplementary Table 14 defines the DOT edge
  label. The rule for the new phase sets (largest component keeps the PS; every other component
  receives the position of its first variant) moved from the Fig. 14f legend to the Fig. 13d legend.
  This also removes the stale "Before/After correction" legend terms and the "PS removed" /
  "PS dropped" mismatch.
- **Renumbering:** Supplementary Figs. 16–18 became 15–17 (GNN effect, metrics, HG008).
  References changed in `Supplementary.tex` (Notes 4, 6, 7 and the Fig. 13 legend) and
  `sections/methods.tex` (lines 88, 90, 127, 153). The Methods and Note 4 architecture sentences
  now cite Supplementary Table 15 only.
