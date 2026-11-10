# Fig. 4d,e regional categories explained in Results, 2026-11-10

The author requested a full rewrite of the regional-comparison paragraph, with the classification explained at its point of use.

- Distinguished reference phase from the v5.0q VCF and genomic intervals from the benchmark BED files.
- Named all six displayed categories: all v5.0q benchmark regions; four subsets (segmental duplications, outside difficult-region annotations, shared with v4.2.1, and v5.0q-only); and outside both benchmark BEDs. The subsets are not presented as mutually exclusive partitions.
- Explained why outside-BED SNV pairs can still be scored: phased reference records exist in the VCF outside those intervals.
- Retained the sequence-context findings and 60x newly covered-region counts (20, 88, 148).
- Expanded 60–77% into the explicit comparisons: 77% for WhatsHap versus LongPhase 2 and 60% for HapCUT2 versus LongPhase 2. From Table 8 at 60x: (1337-328)/(1785-477)=77.14%; (1430-328)/(2309-477)=60.15%.
- Retained the exploratory interpretation outside both benchmark BEDs and the original citations.
- Figures, data, Methods and other Results paragraphs are unchanged.

## Previous paragraph

```tex
The advantage of \toolname over \whatshap and \hapcut varied across genomic regions. Within the v5.0q benchmark regions, the difference in switch error rates was largest in segmental duplications and smallest outside difficult regions\cite{dwarshuis2024stratifications} (Fig.~\ref{fig:benchmarks}d,e). In regions covered by v5.0q but not v4.2.1\cite{olson2026giabv5}, \toolname had 20 switch errors at 60$\times$ coverage, compared with 88 for \whatshap and 148 for \hapcut (Supplementary Table~8). A substantial part of the genome-wide difference nevertheless arose outside both benchmarks: at 60$\times$, these regions accounted for 60--77\% of the difference in switch-error counts between \toolname and the other tools. Because the truth phase is less certain in these regions, we treat this component of the comparison as exploratory (Supplementary Table~8).
```

Independent review clarified the sequence-context comparison: replaced "largest ... smallest" with "larger in segmental duplications than outside difficult regions". This avoids implying that segmental duplications have larger differences than the v5.0q-only subset.
