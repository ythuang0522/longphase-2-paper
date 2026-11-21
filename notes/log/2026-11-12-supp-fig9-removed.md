# 2026-11-12 Supplementary Fig. 9 removed; Supplementary Figs. 10–18 became 9–17

Author decision after a review of all supplementary items: the former Supplementary Fig. 9
(co-phasing configurations with and without GNN-based unphasing, `figures/supp/suppfig14_cophase_gnn.pdf`)
repeats Supplementary Fig. 5 and Supplementary Table 6. It is removed from `Supplementary.tex`; the PDF
and `sfig12()` in `make_results_figs.py` stay as an archive. The Discussion sentence that cited it now
cites Supplementary Note 7 and Supplementary Fig. 5.

| Old | New |
| --- | --- |
| Supplementary Fig. 9 | removed |
| Supplementary Figs. 10–18 | Supplementary Figs. 9–17 |
| Supplementary Data 1: "Supplementary Figs. 1, 2, 4–9 and 17" | "Supplementary Figs. 1, 2, 4–8 and 16" |

Renumbered in `sections/methods.tex` and `Supplementary.tex` (visible text only; source comments keep
older numbers). Table numbers did not change. Other candidates of the review that the author kept:
Supplementary Figs. 7, 14 and 18 (old numbers) and Supplementary Tables 15 and 16.

Removed block (verbatim):

```tex
\begin{figure}[h]
\centering\includegraphics[width=\textwidth]{figures/supp/suppfig14_cophase_gnn.pdf}
\caption{\textbf{Co-phasing configurations with and without GNN-based unphasing.} HG002 nanopore R10.4.1 data; seven combinations of variant classes, each phased separately; SNV metrics against v5.0q.
\textbf{a},\textbf{b}, SNV switch error rate against block N50 at 10$\times$ (\textbf{a}; means of ten replicates with s.d.) and 60$\times$ (\textbf{b}); arrows run from the result without (open) to the result with (filled) GNN-based unphasing.
\textbf{c},\textbf{d}, SNV switch error rate (\textbf{c}) and Hamming distance (\textbf{d}; computed over SNVs and indels for four-class phasing) for SNV-only and four-class phasing.}
\label{fig:supp_cophase_gnn}
\end{figure}
```
