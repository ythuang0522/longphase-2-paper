# Second-tier phasers removed from the manuscript, 2026-11-10

TinkerHap, Margin, Ralphi and GCphase (author decision). Removed source passages, verbatim, for restoration.
Generated table rows and legends come back when the keys `th`, `margin`, `ralphi` (and `gc`) are removed
from `HIDE` in `figures-source/make_results_figs.py`.

## sections/methods.tex, Comparison with other methods, fourth paragraph

```latex
TinkerHap\cite{hartmann2025tinkerhap} was run on replicate~1, at 10--60$\times$ in steps of 10$\times$ on nanopore data and at 10--50$\times$ on HiFi data, with default parameters (Supplementary Tables~4 and~19).  It phases indels by default and has no SNV-only mode; on HiFi data, it was run on the full call sets and on the call sets restricted to SNVs, and on nanopore data on the full call sets only.  Margin v2.3.1\cite{shafin2021margin} and Ralphi\cite{battistella2025ralphi} were evaluated at 10--20$\times$, with ten down-sampling replicates per coverage, and not at 30--60$\times$ (Supplementary Table~19).  GCphase\cite{luo2024gcphase} was excluded because, given the full input VCF, it phased filtered homozygous-reference calls as heterozygous variants; it was not evaluated with input restricted to heterozygous SNVs.  All runs were scored in the same way.
```

## sections/methods.tex, Statistics and reproducibility (phrase)

```latex
comparisons with TinkerHap and HiPhase, 
```

## Supplementary.tex, Supplementary Table 19 row

```latex
Margin & 2.3.1 & SNV-only comparison, 10--20$\times$; phasing parameters \code{allParams.phase\_vcf.ont.json}; input restricted to SNVs \\
```

## Supplementary.tex, Supplementary Table 19 row

```latex
Ralphi & v0.0.1 (commit \code{d7d17b1}) & SNV-only comparison, 10--20$\times$; model \code{ralphi.v1.long.pt}, ONT configuration with \code{max\_coverage 15}, \code{mapq 20}, read selection and bad-read filtering \\
```

## Supplementary.tex, Supplementary Table 19 row

```latex
TinkerHap\cite{hartmann2025tinkerhap} & 1.0.0 & nanopore 10--60$\times$ and HiFi 10--50$\times$, replicate~1 (Supplementary Table~4); default parameters, run per chromosome; phases indels by default and has no SNV-only mode, so SNV-only phasing, on HiFi data, used the call sets restricted to SNVs \\
```

## Supplementary.tex, Supplementary Fig. 19 (file figures/supp/suppfig10_more_tools.pdf kept)

```latex
\begin{figure}[h]
\centering\includegraphics[width=\textwidth]{figures/supp/suppfig10_more_tools.pdf}
\caption{\textbf{SNV-only phasing compared with Margin and Ralphi.} HG002 nanopore R10.4.1 data at 10--20$\times$, means of ten replicates with s.d., scored against v5.0q; \toolname with GNN correction.
\textbf{a}, Switch error rate. \textbf{b}, Hamming distance. \textbf{c}, Block N50; Ralphi is omitted because its blocks sum to more than the autosome length. \textbf{d}, Number of phase blocks. Values in Supplementary Table~1.}
\label{fig:supp_tools}
\end{figure}
```

## Supplementary.tex, replaced text

```latex
Supplementary Figs.~1, 2, 4--9, 17 and~19 and Supplementary Tables
```

## Supplementary.tex, replaced text

```latex
Replicate~1 of further phasers, run with default parameters or the documented workflow, scored as in \code{SNV\_Detail}: TinkerHap on nanopore data; HiPhase and TinkerHap on HiFi data, with indels and on an SNV-only input VCF (neither has an SNV-only option); and \toolname, \whatshap and HapCUT2 with indels (Supplementary Table~4).
```
