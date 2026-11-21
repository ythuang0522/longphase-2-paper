# 2026-11-12 Supplementary Note 1 shortened to the GNN ablation

Author decision (option A): Supplementary Note 1 keeps three paragraphs — the effect of GNN
correction genome-wide, on the chromosomes excluded from training (chr17, chr21, chr22) and on
PacBio HiFi data. The two paragraphs on variant-class combinations (indels, excess switch error
rate, indel-pair switch errors) were deleted: they are a different topic, and the values stay in
Supplementary Figs. 5 and 9 and Supplementary Tables 2 and 6. No legend was changed and no
supplementary item lost its citation (Supplementary Figs. 5 and 9 and Tables 2 and 6 are cited in
the Results). The main Methods already cite the note (`sections/methods.tex`, Training paragraph),
so no citation was added.

Removed text and its source comments (verbatim):

```tex
Indels were associated with the largest increases in both contiguity and SNV switch error rates across seven combinations of variant classes (Supplementary Figs.~5 and~9 and Supplementary Table~6). Relative to SNV-only phasing at the same coverage before GNN correction, adding SVs changed block N50 by at most 0.2\% and adding 5mC increased it by 2--14\%, with SNV switch error rates changing by at most 3\%. Indels increased N50 by 29--51\% (31--74\% with SVs and 5mC), but increased switch error rates by 22--33\%.

GNN correction reduced SNV switch error rates by 31--37\% in configurations without indels and 37--43\% in those with indels. It reduced the excess SNV switch error rate relative to SNV-only phasing by 40--71\%, calculated as $1-E_{\mathrm{after}}/E_{\mathrm{before}}$, where $E$ is the rate difference from SNV-only phasing at the same coverage and GNN setting. It also reduced indel-pair switch error rates by 21--39\% (Supplementary Table~2). Block N50 decreased by 12--21\% with indels and 0.3--9\% without them as unphasing disconnected blocks.
%  [limitation] Former \todo (demoted 2026-10-09, author: no new experiments): for
%  indel-containing configurations, compare computes the Hamming distance over SNVs and indels
%  (CompareProcess.cpp:579), whereas switch errors are SNV-only. No Hamming value of such a
%  configuration is quoted in this section; Methods, the legends of Supplementary Figs. 14 and
%  15 and the captions of Supplementary Tables 8 and 9 state that it includes indels, and
%  configurations are compared by SNV switch error rate. Indel accuracy: Supplementary Table 13.
%  [provenance] 2026-10-09 recomputation over all ten coverages (Supplementary Data 1,
%  co-phase_Detail): the former "41--67%" was the four-class configuration only; across
%  the four indel-containing configurations the v2.1.1 range is 38--71%. The indel-pair
%  switch-error reduction is 22--40% across all four configurations and ten coverages
%  (notes/v2.1.1/claims.py, P25.indel_pair_removed); 24--39% applies to indels alone.
%  v2.1.2 (2026-10-26, notes/v2.1.2/claims.py): 21--39% over the four configurations, additional error
%  removed 40--71%; four-class vs indel-only indel-pair change 6.8% (v2.1.1: 3.8%).
```
