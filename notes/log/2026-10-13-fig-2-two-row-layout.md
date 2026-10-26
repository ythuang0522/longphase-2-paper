# Fig. 2 two-row layout, 2026-10-13 (author decision)

**Fig. 2 two-row layout, 2026-10-13 (author decision).** The four-row figure (11 panels, four row keys,
a five-entry legend for c) carried too much. Now two rows, seven panels: row 1 a SNV switch error rate
(former a), b SNV + indel switch error rate (former d), c evidence-type accuracy–contiguity (unchanged);
row 2 d,e SNV + 5mC vs MethPhaser (former f,h), f,g HiFi (former i,k). One figure-level key at the top
(tools; line styles of b and c by panel letter) replaces the row keys and the c legend; the dotted
indel lines in b now have hollow markers, so filled markers mean four-class phasing only. The
Hamming-distance column (former b, e, g, j) is new Supplementary Fig. 16 (`sfig16()`), added at the end
so that no Supplementary figure is renumbered; it keeps the HiFi 50× value at which LongPhase 2 has the
higher Hamming distance visible. Legend, Results panel letters and Hamming citations (Supplementary
Fig. 16a–d; MethPhaser also Supplementary Fig. 11c), Supplementary Data 1 description (Fig. 2d,e;
Supplementary Figs. 9 and 11–16) updated. Height 198 → 122 mm.
- Superseded the same day by **proposal A** (author: a five-panel draft with the key in an empty slot
  was rejected as ugly; six panels preferred). Fig. 2 is a 3 × 2 grid, one type of plot per row: row 1
  switch error rate against coverage — a SNV (WhatsHap, HapCUT2), b SNV + indel, c PacBio HiFi; row 2
  switch error rate against N50 — d by evidence type (former c), e SNV + 5mC vs MethPhaser, f HiFi
  (own x-axis 0.025–0.2%). Title on the panel-letter line (`letter(..., title=)`, placed by `save()`),
  tool key at the top, line-style keys inside b and d, lines 0.75 pt and markers at 0.8 size
  (`_light()`). HapCUT2 is now solid in every figure (`STY`), so dashed means "+ indels" only.
  Supplementary Fig. 16 (`suppfig16_fig2_coverage.pdf`) is a 5mC switch error rate against coverage
  (former Fig. 2d) and b–e the Hamming distances. Results letters: evidence panel c → d, HiFi
  i/f → c, HiFi N50 → f, 5mC switch error rate → Supplementary Fig. 16a, Hamming 16a–d → 16b–e.
  Height 104 mm.
- Same day: Fig. 2 d and e swapped (d SNV + 5mC vs MethPhaser, e evidence-type summary), so that each
  evidence class is met before the panel that combines them and e sits below b (same WhatsHap runs).
  The first Results section was condensed from ten paragraphs (about 1,050 words) to five (about 620),
  cited in panel order a–f: SNV (a; held-out chromosomes, Margin/Ralphi and runtime as one sentence
  each), indels (b), HiFi accuracy (c), 5mC vs MethPhaser (d), contiguity by evidence type and on HiFi
  (e, f). Removed detail is listed in the `[provenance]` comment at the end of the section.
