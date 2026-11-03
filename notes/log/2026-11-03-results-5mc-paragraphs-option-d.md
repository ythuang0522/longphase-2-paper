# Results: 5mC paragraphs redesigned by input set (MethPhaser and LongHap), 2026-11-03 (author decision, option D)

Paragraph 1 (Fig. 3d,e, SNVs with 5mC) now gives the MethPhaser mechanism first, the switch error rates of
MethPhaser and LongHap in one sentence, then block length with its cost in Hamming distance (share of SNVs on
the wrong haplotype; MethPhaser input 1.8-6.9%). Paragraph 2 (Fig. 3f) keeps the four-class WhatsHap
sentences and gives LongHap on all classes. Ranges are over 10-60x; LongHap 10x is stated apart because the
direction reverses there (shorter blocks, lower Hamming, 60% of SNVs phased). LongPhase 2 Hamming at 10x
corrected to 5.3% (v2.1.2: 5.28; the old text had 5.4). Values: v2.1.2 rep 1 (notes/v2.1.2/claims.py),
sheet Other_phasers, notes/methphaser/methphaser_vs_longphase.tsv.

Previous text:

We then asked whether phasing 5mC together with sequence variants is more accurate than adding methylation after phasing. On nanopore data, joint SNV and 5mC phasing by \toolname had the lowest switch error rate of the three phasers that use 5mC at every coverage (Fig.~\ref{fig:methylation}d and Supplementary Table~17). It had 1.5--1.8-fold lower switch error rates and 1.4--3.1-fold lower Hamming distances than MethPhaser\cite{fu2024methphaser} (Fig.~\ref{fig:methylation}d and Supplementary Fig.~16e). MethPhaser produced longer blocks, with N50 1.1-fold that of \toolname at 10$\times$ and 1.3--1.8-fold at 20--60$\times$ (0.96--5.49 versus 0.87--3.12~Mb; Fig.~\ref{fig:methylation}e), whereas phased fractions differed by approximately 0.2 percentage points or less (Supplementary Table~17). The block joins of MethPhaser increased switch errors in its input by 2--15\% (Supplementary Fig.~11).

LongHap\cite{pfennig2026longhap} had 2.2--5.4-fold higher switch error rates than \toolname (Fig.~\ref{fig:methylation}d). At 20--60$\times$, its blocks were 1.4--2.1-fold longer than those of \toolname (Fig.~\ref{fig:methylation}e), but its Hamming distances were 18--20\%, compared with 1.7--3.4\% for \toolname, consistent with long segments of reversed phase within its blocks (Supplementary Fig.~16e). At 10$\times$, its block N50 was 0.41 versus 0.87~Mb, and it phased 60\% of benchmark heterozygous SNVs, compared with 78\% for \toolname (Supplementary Table~17); its Hamming distance there was lower than that of \toolname (4.4 versus 5.4\%). With SNVs, indels, SVs and 5mC, \toolname had 2.5--3.2-fold lower SNV switch error rates than \whatshap in SNV-only mode and 3.0--3.8-fold lower rates than \whatshap with indels (Fig.~\ref{fig:methylation}f). Its blocks were 6--52\% longer than those of \whatshap in SNV-only mode and 6--21\% shorter than those of \whatshap with indels at 10--40$\times$ (within 1.4\% at 50--60$\times$; Supplementary Table~9). With SNVs, indels, SVs and 5mC, LongHap had 2.4--4.5-fold higher switch error rates than \toolname and blocks 1.3--1.8-fold longer at 20--60$\times$, with 19.5--21.9\% Hamming distances (Fig.~\ref{fig:methylation}f and Supplementary Table~17).

Correction, same day (author): the Hamming sentence came before the block-length sentence, so the text
announced Hamming distance and then gave N50. New order: block length of MethPhaser and LongHap (LongHap
10x apart), then why Hamming distance measures the cost of longer blocks, then the Hamming values, then the
conclusion. The process wording "we also compared" was removed.

Second correction, same day (author): LongHap is now given over 10-60x like MethPhaser, in both paragraphs.
SNVs with 5mC: N50 0.47-2.1-fold (0.41-5.40 Mb), shorter only at 10x; 0.9-18 points fewer benchmark SNVs
phased (most at 10x, 60 vs 78%); Hamming 4.4-20%. All classes with 5mC: N50 0.46-1.8-fold (0.47-6.83 vs
1.02-4.14 Mb), shorter only at 10x; Hamming 6.4-21.9% vs 3.6-7.1%.

Third correction, same day (author: one message per sentence): the LongHap phased-fraction clause ("phased
0.9-18 percentage points fewer benchmark heterozygous SNVs, most at 10x (60 versus 78%)") was removed; the
values stay in Supplementary Table 17.

Fourth correction, same day (author, option A): the Hamming sentence ("A longer block is useful only if its
segments are on the correct haplotypes: one wrong link ...") became three sentences that name the methylation
joins: "MethPhaser and LongHap lengthen blocks by joining them with methylation evidence. One wrong join places
a whole block on the opposite haplotype. Hamming distance measures this error as the share of SNVs in a block
that are on the wrong haplotype (Supplementary Fig. 16e)." Support: with 5mC, LongHap N50 1.03-2.4-fold and
Hamming 4.1-10.5% -> 4.4-20% over LongHap without 5mC (sheet Other_phasers).

Fifth correction, same day (author's own wording, edited): "MethPhaser and LongHap lengthen blocks by joining
them with methylation evidence. Because one wrong join places a whole block on the opposite haplotype, Hamming
distance measures this error better than the switch error rate, which counts it as a single switch
(Supplementary Fig. 16e)."
