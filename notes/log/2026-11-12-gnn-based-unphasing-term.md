# 2026-11-12 "GNN correction" renamed to "GNN-based unphasing"

Author decision: "correction" suggests that the network repairs the phase (a flip). The network
only leaves variants unphased, so the step is now named "GNN-based unphasing" in every visible text.

| Old | New |
| --- | --- |
| GNN correction | GNN-based unphasing |
| unphased by GNN correction | unphased by the GNN |
| correction (bare, for the GNN step) | GNN-based unphasing, unphasing, or "it" |
| Supplementary Note 7. Effect of GNN correction | Supplementary Note 7. Effect of GNN-based unphasing |
| Supplementary Fig. 15e,f panel titles "Before/After correction" | "Before unphasing: one phase set", "After unphasing: phase set split" |

Changed: `main.tex` (Fig. 1 legend), `sections/methods.tex`, `sections/discussion.tex`,
`Supplementary.tex`, `figures-source/make_results_figs.py` (keys of Supplementary Figs. 5 and 17, table
captions) and the regenerated `figures-source/supp_tables/*.tex`, `figures/supp/make_supp_figs.py`
(Supplementary Figs. 14 and 15), `CLAUDE.md`. "Read-based correction" is unchanged. Source comments
and `notes/` keep the old term.
