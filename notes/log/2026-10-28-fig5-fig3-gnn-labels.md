# Fig. 5 row 2 labels and legend, Fig. 3 legend: GNN wording removed, 2026-10-28 (author decision)

Follows the Results change of the same day (LongPhase 2 presented as one tool).

- `make_results_figs.py`, `fig5()`: f y-axis "SNVs unphased by GNN (%)" → "Withheld SNVs
  (%)"; g bar label "Unphased by GNN" → "Withheld"; row-2 key "unphased by GNN" → "withheld".
  `make results-figs` rewrote only `figures/fig5_phased_unphased.pdf` (other outputs
  unchanged); Arial embedded.
- Fig. 5 legend (`main.tex`): title "… and SNVs unphased by GNN correction" → "… and SNVs
  withheld at high phasing uncertainty"; f "SNVs phased before and unphased after GNN
  correction" → "SNVs that LongPhase 2 withheld at high phasing uncertainty"; g "a random
  sample of SNVs phased before correction" → "a random sample of phased SNVs".
- Fig. 3 legend: "MethPhaser and HapBridge were given the SNV-only output of LongPhase 2
  without GNN correction;" removed (stated in Methods).
