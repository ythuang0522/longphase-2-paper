# Results split into competitors vs internal modules, 2026-10-06 (author request)

**Results split into competitors vs internal modules, 2026-10-06 (author request).**
- Figures were not Nature Methods compliant: tight-cropped to 151–153 mm, so placement at 183 mm
  would push fonts to 7.8 pt; Fig. 2 spent a panel on a legend; Fig. 3 used hatched grouped bars.
  All results figures are now exactly 183 mm wide (constrained layout), 5–7 pt Helvetica, 8 pt bold
  lowercase letters, keys inside the figure, no empty panels, no bars for trends.
- "LongPhase 2 + correction" was undefined in the figures and collided with the read-based
  correction inside `phase`. The step is now "GNN correction" (defined in Fig. 1 legend, Results,
  Methods); in main figures "LongPhase 2" is the complete method, GNN included.
- Results now has two parts. *Comparison with existing phasers* (main Figs. 2–6): SNV phasing vs
  WhatsHap/HapCUT2 with Margin in Fig. 2f; benchmark dependence (Fig. 3, SNV-only tools); indel and
  four-class co-phasing vs WhatsHap (new Fig. 4); HiFi vs WhatsHap (Fig. 5, two tools); unphased sets
  vs WhatsHap (new Fig. 6). *Contribution of the internal modules* (Supplementary only): GNN effect
  (Supp. Fig. 13), co-phasing configurations with/without GNN (14, 15), what the GNN withholds (16, 17).
- Supplementary figures renumbered by citation order: 10 other tools, 11 MethPhaser, 12 depth of
  unphased sets, 13 GNN effect, 14 co-phasing with/without GNN (former Fig. 4), 15 all
  configurations, 16 GNN-removed SNVs (former Fig. 6a–c), 17 old raster. Methods cross-references
  updated. Part headings are plain `\subsection*`, findings are declarative `\paragraph`s.
- Later the same day: panel letters had never been bold (Helvetica.ttc exposes only its regular face
  to matplotlib); all figures now use Arial with Arial-Bold embedded. Fig. 5 redesigned to mirror
  Fig. 2 a–e (phased SNVs on an 80–90% axis instead of a 0.7-point axis that exaggerated the gap,
  switch error *rate* instead of counts, Hamming and N50 from zero, WhatsHap/LongPhase 2 ratio).
- Readability (author, 2026-10-06): main line plots show 10, 20, 30, 40, 50 and 60× only (12–18× stay
  in the tables and Supplementary Data 1), the replicate s.d. is a light band instead of error bars,
  and the ±0.5× offset is gone; HapCUT2 (dashed, open squares) is drawn over WhatsHap where they coincide.
- Replicate design (author, 2026-10-06): the grey "single replicate" shading is removed from every
  figure; it is not standard in benchmarking figures. Legends state the replicate design once.
  The original rationale that overlapping reads make independent random subsampling impossible
  was withdrawn on author review: read overlap does not establish dependence between random draws.
- Markers (author, 2026-10-06): all coverages are plotted again (10–20× in steps of 2, to show
  low-coverage differences). Every tool has an open (unfilled) marker of its own shape and size —
  LongPhase 2 circle, WhatsHap small diamond, HapCUT2 large square, Margin/Ralphi/GCphase triangles
  and cross — so coinciding points nest instead of hiding each other.
