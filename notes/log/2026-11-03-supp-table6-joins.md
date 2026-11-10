# Supplementary Table 6: blocks joined, sites added and switch errors per join; HiFi rows; landscape, 2026-11-03 (author request)

Author: "it's ok to add supplementary table 6 with new columns", for a rewrite of the four-class
paragraph that explains block length and its cost (draft discussed in chat, not yet in results.tex).

- New columns (`tables()` in `figures-source/make_results_figs.py`): Blocks; Blocks joined (blocks of
  SNV-only phasing minus blocks of the configuration); Sites added (phased indels + SVs + 5mC sites,
  thousands); Joins per 10^3 sites; Switch errors per join (SNV switch errors added to SNV-only
  phasing / blocks joined; "--" for +SV, which joins almost no blocks). Each is paired with SNV-only
  phasing of the same down-sampling replicate at the same GNN setting; mean (s.d.) at 10-20x.
- Phased SV and 5mC counts: sheet `SV_5mC_phasing` (notes/sv_mod/), now attached to the co-phasing
  runs by `results_data.load()` as `psv`, `pmod`.
- New PacBio HiFi section: SNV, +SV and +indel+SV, without and with GNN, 10-50x, replicate 1, from
  `notes/sv_phasing/snv.tsv` (issue #10 runs, v2.1.2). Phased indels are not scored for these runs, so
  the site columns are "--". HiFi has no 5mC runs.
- The table is set on landscape pages (`pdflscape`, `\begin{landscape}` around its `\input` in
  `Supplementary.tex`); in portrait it was 86 pt too wide.
- Existing columns and values unchanged. No other table changed when `tables()` was rerun.
