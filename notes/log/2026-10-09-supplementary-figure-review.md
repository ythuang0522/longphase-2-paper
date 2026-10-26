# Supplementary figure review, 2026-10-09 (author request)

**Supplementary figure review, 2026-10-09 (author request).**
- All automatic linear tick locators now use steps of 1, 2 or 5 (`_tidy_ticks()` in `save()`), so no
  axis shows labels such as 0.025 or 77.5; applies to main and Supplementary figures. Hamming axes in
  Supplementary Figs. 14d and 15 start at zero.
- Supplementary Fig. 10: plain decimal labels on the log axes (no 10^x), LongPhase 2 first in the
  key, "WhatsHap". Fig. 11: open markers and the Fig. 2 glyphs (MethPhaser triangle). Fig. 12: the
  censored-depth label sits inside the grey band, clear of the lines. Fig. 15: "GNN" no longer
  lower-cased by `str.capitalize()`, open markers with the Fig. 3 glyphs per configuration
  (`CFGM`). Fig. 16: keys above the panels instead of below.
- Supplementary Fig. 2e (schematic): "Suppl. Fig. 4" spelled out. Supplementary Fig. 4a: the initial-phasing box reads "LongPhase 2" (was "LongPhase", which could be read as LongPhase 1).
- Not changed: schematics 1 and 3–8 (consistent and legible at print size); Supplementary Fig. 9 is
  still a placeholder and Fig. 17 still the old raster (both `\todo`s, need source data).
