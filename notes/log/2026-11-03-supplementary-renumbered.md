# Supplementary Figures and Tables renumbered by first citation in the main text, 2026-11-03 (author request)

The author asked that the Supplementary Figures and Tables be numbered in the order of their first
citation in the main text (Results, figure legends, Discussion, Methods, in document order).

## Citations added first (author decision)

Ten items were not cited in the main text. The author agreed to cite all of them except the
Margin/Ralphi figure (old Supplementary Fig. 9), whose Results sentence is `[author-hidden]` since
2026-10-13. Old numbers:

- Methods, methylation calling: Supplementary Fig. 7 (`modcall`).
- Methods, read-level observations: Supplementary Fig. 1.
- Methods, multi-neighbour voting: Supplementary Fig. 2.
- Methods, read-based correction: Supplementary Fig. 3.
- Methods, GNN: Supplementary Fig. 4 (overview), Supplementary Fig. 5 (window); the sentence on the
  released model now also cites Supplementary Note 1 and Supplementary Fig. 13e.
- Methods, benchmark data: Supplementary Table 6 (input call sets).
- Discussion, indel error reduced by GNN correction: Supplementary Note 1 and Supplementary Fig. 14.
- Error fixed: Methods cited Supplementary Table 17 (further phasers) for the held-out classification
  scores of the ten trained models; the correct table is old Supplementary Table 18.

## Mapping (old → new)

| Figures | | Tables | |
|---|---|---|---|
| 16 → 1 | Hamming distance, Figs. 2–3 | 7 → 1 | SNV-only, nanopore |
| 17 → 2 | SVs with indels | 13 → 2 | indel phase accuracy |
| 11 → 3 | MethPhaser | 10 → 3 | HiFi SNV-only |
| 15 → 4 | all co-phasing configurations | 17 → 4 | further phasers |
| 12 → 5 | read depth, unphased calls | 19 → 5 | SV phasing |
| 10 → 6 | runtime | 9 → 6 | co-phasing configurations |
| 14 → 7 | co-phasing with/without GNN | 8 → 7 | two benchmarks |
| 7 → 8 | `modcall` | 12 → 8 | switch-error location |
| 1 → 9 | read-level observations | 16 → 9 | calls phased by one tool |
| 2 → 10 | voting and entropy | 11 → 10 | T2T classification |
| 3 → 11 | read-based correction | 15 → 11 | runtime |
| 4 → 12 | GNN overview | 1 → 12 | node features |
| 5 → 13 | GNN window | 2 → 13 | edge features |
| 6 → 14 | GNN architecture | 3 → 14 | GNN hyperparameters |
| 13 → 15 | effect of GNN correction | 4 → 15 | GNN training |
| 8 → 16 | evaluation metrics | 18 → 16 | ten GNN models |
| 9 → 17 | Margin and Ralphi (not cited in main text) | 14 → 17 | held-out chromosomes |
| | | 6 → 18 | input call sets |
| | | 5 → 19 | software |

## Implementation

- `Supplementary.tex`: floats reordered; `placeins` loaded and `\FloatBarrier` after every table.
- `make_results_figs.py` writes one file per generated table to `figures-source/supp_tables/<label>.tex`
  (replaces `figures-source/supp_tables.tex`, deleted), so that generated and hand-written tables
  interleave; Makefile dependency updated.
- Every live reference renumbered in `main.tex`, `sections/*.tex`, `Supplementary.tex` and the captions
  written by `make_results_figs.py`; `make_supp_figs.py` panel text "Supplementary Fig. 4" → 12.
- File names and function names keep the old numbers. `%` comments, script comments and dated notes
  keep the old numbers; read them with this mapping.
- CLAUDE.md and README updated.
