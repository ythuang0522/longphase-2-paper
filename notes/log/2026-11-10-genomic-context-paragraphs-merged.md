# Genomic-context paragraphs merged using option 1, 2026-11-10

The author selected option 1 to merge the genomic-stratum and outside-benchmark paragraphs.

The merged paragraph first describes variation in the advantage of LongPhase 2 across genomic regions, then states that regions outside both benchmarks account for 60–77% of the genome-wide switch-error count difference at 60x. It preserves the exploratory interpretation of that component and the 18–41 LongPhase 2 switch errors per coverage in newly covered regions.

The detailed fold ranges, outside-region error rates and changes across coverage were removed from the prose. Their source data and supplementary tables are unchanged. Retained the Dwarshuis and Olson citations, Fig. 4d,e and Supplementary Table 8.

## Previous paragraphs

```tex
The separation between phasers also depended on genomic context. Among GIAB genomic strata\cite{dwarshuis2024stratifications}, the separation was largest in segmental duplications (3.2--5.4-fold at 10 and 60$\times$) and smallest outside difficult regions (1.7--2.2-fold; Fig.~\ref{fig:benchmarks}d,e). The relative advantage of \toolname was greater in regions covered by v5.0q but not v4.2.1\cite{olson2026giabv5}: \whatshap and \hapcut had 4.2--8.3 and 7.1--11 times its switch error rate, compared with 1.7--2.5 and 2.0--9.4 times in regions covered by both benchmarks (Fig.~\ref{fig:benchmarks}d,e). These comparisons involved 18--41 switch errors for \toolname in the newly covered regions per coverage.

Outside the benchmark regions of both truth sets, where the truth phase is least certain, switch errors accounted for an increasing share of each tool's total as coverage rose. This share increased from 28\% to 69\% for \toolname and from 43--46\% to 62--75\% for the other tools between 10 and 60$\times$. Rates in these regions were 0.8--1.1\% for \toolname and 2.6--4.9\% for the other tools. These sites contributed 50--56\% of the genome-wide difference in switch-error counts at 10$\times$ and 60--77\% at 60$\times$. We therefore treat this component of the comparison as exploratory (Supplementary Table~8).
```

## Follow-up: per-tool counts in newly covered regions

Author approved replacing the statement about a greater relative advantage and the isolated 18–41 error range with the 60x comparison: LongPhase 2, 20 switch errors; WhatsHap, 88; HapCUT2, 148. Values are the v5.0q-only region counts in Supplementary Table 8. The new sentence compares tools within the newly covered regions, without claiming that their relative separation exceeds that in shared regions. Retained the Olson citation and added the Supplementary Table 8 reference.
