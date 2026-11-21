# Fig. 5: one 2 × 4 grid, panel h as vertical bars (option C)

2026-11-21, author decision after three draft PNGs (`notes/drafts/2026-11-21-fig5-alignment/`).

- Problem: the two rows of Fig. 5 were two subfigures, so each row set its own column widths; the long y tick labels of panel h narrowed and shifted the panels of row 2 (e–h not aligned with a–d).
- Change (`fig5()` in `figures-source/make_results_figs.py`): one 2 × 4 grid under constrained layout, so the columns of both rows align; panel h drawn as two vertical stacked bars (aligned 1:1 / not aligned 1:1), y axis "SNVs at 60× (%)", labels "Phased (random sample)" and "Unphased at high phasing uncertainty" under the bars, as in panel a.
- Options not chosen: A (one grid, h unchanged; column 4 narrower), B (horizontal bars with labels above them).
- No data, panel order, key or legend text changed; the Fig. 5 legend (h) is still correct. Only `figures/fig5_phased_unphased.pdf` changed in the regenerated output.
