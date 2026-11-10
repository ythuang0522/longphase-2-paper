# Unphased SNV Results rewritten around genotype errors and phase reliability

Rewrote the author-requested subsection, from its title through the read-depth analysis. The new narrative leads with fewer benchmark-defined genotype errors incorporated into haplotypes, then explains the small benchmark-SNV completeness difference, higher benchmark agreement, phase errors among comparator-only calls, and the within-benchmark high-depth false-positive subset.

The title is “LongPhase 2 leaves error-prone SNV calls unphased”. Used 60x examples to reduce numerical load. Preserved a short comparison of indel/SV completeness and the observation that LongPhase 2 also uniquely phases some error-prone calls. Distinguished benchmark absence genome-wide from absence within benchmark regions. Did not attribute the overall unphased set to GNN correction; the following GNN-only subsection is unchanged.

Evidence: current generated Supplementary Tables 1, 3 and 9; notes/unphased/issue6_composition.tsv; Fig. 5 and its definitions. The 29–48% reduction is calculated from phased homozygous-reference calls (LongPhase 2: 14154, 9578, 8339; WhatsHap: 27135, 13706, 11815). The high-depth subset (3669; 92.8%) is retained from the existing source/provenance, since its site-level table is not available locally. An independent read-only review checked the principal numbers and interpretation boundaries.

Preserved original source comments. Detailed numbers removed from the narrative remain in tables and in the original text below. Figures, Methods, and the following subsection were not changed.

Validation: main.pdf rebuilt successfully; revised pages 8–9 rendered and inspected. No overfull boxes, undefined references, or missing characters; git diff --check passed. Visible source text reduced from 807 to 461 words. Independent final review found no material factual correction; incorporated its clarifications that wrong-phase fractions apply only to assessable benchmark-matching SNVs and that the high-depth false positives are classified by this benchmark.

## Original subsection

```tex
\subsection*{\toolname phases slightly fewer benchmark SNVs and places fewer genotype errors on haplotypes than \whatshap}
\toolname phased slightly fewer benchmark heterozygous SNVs than \whatshap and \hapcut despite identical input calls. We measured completeness as the fraction of benchmark heterozygous SNVs phased. \whatshap and \hapcut phased 0.7--1.0 percentage points more than \toolname at every nanopore coverage. For all three tools, the phased fraction rose steeply up to 16$\times$ and plateaued at 91--92\% from 20$\times$ (Fig.~\ref{fig:unphased}a and Supplementary Table~1). On HiFi data, \whatshap and \hapcut phased 0.4--0.5 percentage points more and HiPhase 0.2--0.3 percentage points more, and all four tools increased from 87\% at 10$\times$ to 92\% at 20--50$\times$ (Fig.~\ref{fig:unphased}c). On nanopore data with indels, \whatshap phased 2.5--4.5 percentage points more benchmark heterozygous indels, with a larger difference at higher coverage (Supplementary Table~7). On HiFi data with indels, \whatshap, \hapcut and HiPhase phased 2--3, 6--9 and 5--8 percentage points more benchmark heterozygous indels than \toolname (Supplementary Table~4). With SNVs and SVs as input, \whatshap and HiPhase also phased more SVs than \toolname: 89.5--91.2\% versus 70.3--75.6\% of heterozygous deletions and insertions on nanopore data, and 87.0--89.8\% and 84.7--85.6\% versus 76.9--78.0\% on HiFi data (Supplementary Table~5).

A larger share of the calls phased by \toolname matched benchmark heterozygous SNVs. Among heterozygous SNV calls phased on chr1--22, the share matching a benchmark heterozygous SNV increased from 89.6\% to 93.3\% for \toolname and from 86.2\% to 91.5\% for \whatshap (Fig.~\ref{fig:unphased}b). The share was higher for \toolname in every replicate, although the difference narrowed from 3.4 percentage points at 10$\times$ to 1.8 at 50--60$\times$. F1, the harmonic mean of this share and completeness, was also higher in every replicate. The difference decreased from 0.9--1.1 percentage points at 10--18$\times$ to 0.4 at 50--60$\times$ (83.3--92.3\% for \toolname and 82.3--91.9\% for \whatshap; Supplementary Table~1). On HiFi data, the share was also highest for \toolname at every coverage, increasing from 92.2\% to 95.0\%, compared with 90.3\% to 94.6\% for \whatshap and 91.1\% to 93.9\% for HiPhase (Fig.~\ref{fig:unphased}d and Supplementary Table~3). The difference from \whatshap narrowed from 1.8 percentage points at 10--20$\times$ to 0.3 at 50$\times$, whereas the difference from HiPhase remained at 1.1--1.5 points.
%  [provenance] 2026-10-19, issue #9 (JHL, 4393308): notes/unphased/phased_calls_hifi_chr1_22.tsv; precision =
%  Phased_SNV (SNV_Detail; Other_phasers for HiPhase) / phased het. SNV calls on chr1-22. 10-50x: LongPhase 2
%  92.16 93.08 93.70 94.43 94.96, WhatsHap 90.31 91.26 92.43 93.74 94.61, HiPhase 91.05 91.60 92.28 93.26 93.89.
%  Above the call-set precision (89.4-92.6%) because the unphased calls are mostly false (9-22% match the
%  benchmark; notes/unphased/phased_unphased_hifi_chr1_22.tsv).
%  [provenance] Issue #6 (JHL, notes/unphased/, 2026-10-09; Supplementary Data 1 sheets
%  Unphased_composition, Unphased_intervals, Unphased_depth). Phased calls on chr1-22 =
%  phased by both + phased by that tool only, minus chrX/Y; matched = compare's Phased_SNV
%  (asserted in make_results_figs.py). issue6.py reproduces compare's Phased_SNV, switch
%  errors and Hamming distance for both tools at 10/30/60x (issue6_checks.tsv).
%  Precision (issue #7, notes/unphased/phased_calls_chr1_22.tsv, every run): LP2 mean 89.39 (10x)
%  ... 93.05 (60x), WH 86.22 ... 91.52; mean difference 3.17, 2.98, 2.70, 2.45, 2.45, 2.21 (10-20x),
%  2.12, 1.93, 1.54, 1.53 (30-60x); paired per replicate 1.96-3.47 at 10-20x.
%  Phased-fraction gaps over all ten coverages: WH-LP2 0.74-0.99, HC-LP2 0.76-1.00;
%  WH-LP2 without GNN 0.61-0.90; GNN 0.09-0.26 percentage points. Fig. 3 follows option A
%  of the 2026-10-09 discussion with the author (one message). Later the same day, after reading
%  GIAB v5.0q (olson2026giabv5), the author chose panel c = genotype errors phased (calls at
%  positions with a homozygous v5.0q record; phased by a tool = background + that tool only,
%  phased_class() in make_results_figs.py): LP2 14,444 / 9,828 / 8,497, WH 27,135 / 13,706 /
%  11,815 (ratio 1.88 / 1.39 / 1.39); other allele LP2 2,473 / 2,656 / 2,375, WH 3,514 / 3,455 /
%  3,068 (1.42 / 1.30 / 1.29); absent LP2 198,031 / 182,411 / 152,798, WH 269,608 / 236,374 /
%  190,344 (1.36 / 1.30 / 1.25). Read depth in Supplementary Fig. 12. F1 (precision_runs()):
%  difference per coverage 0.91 0.97 0.92 0.84 0.86 0.75 (10-20x, mean of ten; min 0.62) 0.69
%  0.57 0.32 0.26 (30-60x); LP2 higher in all 64 paired runs. Indel
%  completeness was in the main figure as panel c for part of that day and was removed again
%  (author: the SNV panels carry the argument); phased indels per tool, Supplementary Table 8
%  (WH-LP2 2.53 at 10x rising to 4.52 at 60x).
%  v2.1.1 (2026-10-16, notes/v2.1.1/claims.py): precision LP2 89.6 (10x) ... 93.3 (60x); difference
%  3.41 3.20 2.91 2.65 2.65 2.41 (10-20x) 2.36 2.12 1.76 1.75 (30-60x); F1 difference 1.01 1.08 1.02 0.94
%  0.96 0.85 0.81 0.66 0.42 0.37; LP2 higher in all 64 paired runs (precision and F1).

\toolname also phased fewer genotype errors than \whatshap. These errors place an incorrect allele on a haplotype when a homozygous site is called and phased as heterozygous\cite{olson2026giabv5}. At positions with a homozygous v5.0q genotype on chr1--22, \whatshap phased 27,135, 13,706 and 11,815 heterozygous calls at 10, 30 and 60$\times$, compared with 14,154, 9,578 and 8,339 for \toolname (1.4--1.9 times as many; Fig.~\ref{fig:unphased}e). \whatshap also phased 1.3--1.4 times as many calls with a different allele in v5.0q or no v5.0q record. The latter category included 190,344 calls for \whatshap and 147,307 for \toolname at 60$\times$; benchmark absence alone does not establish a genotype error.

Calls phased by only one tool explained these differences (Supplementary Table~9). \whatshap phased 124,000--151,000 calls that \toolname left unphased; 15--20\% matched benchmark heterozygous SNVs. Among benchmark-matching calls in blocks with at least two assessed variants, 22.8\%, 16.2\% and 9.9\% were phased incorrectly at 10, 30 and 60$\times$, three to six times its overall rate. Conversely, \toolname phased 34,000--50,000 calls that \whatshap left unphased. About 90\% were absent from the benchmark, and 92--93\% lay in segmental duplications or outside one-to-one assembly alignments. Among the 958--1,489 benchmark-matching SNVs assessed in such blocks, 12.7--14.9\% were phased incorrectly. Calls phased by either tool alone also overlapped that tool's switch-error intervals 2.4--9.9 times more often than its phased calls overall.

At higher sequencing coverage, calls left unphased by \toolname alone included more high-depth sites than those left unphased by \whatshap alone (Supplementary Fig.~6). At 10$\times$, 62--71\% of calls in each set had depth below 20$\times$. At 30 and 60$\times$, this remained true for 51--59\% of calls left unphased by \whatshap alone, compared with 12--17\% of those left unphased by \toolname alone. The latter set had a depth peak near the sequencing coverage and included more high-depth calls. At 60$\times$, 28\% had depth of at least 90$\times$, and 15.5\% reached the variant caller's depth cap. Only 3\% of calls left unphased by \whatshap alone reached 90$\times$.

The excess depth persisted when measured relative to sequencing coverage. At 30 and 60$\times$, 28\% and 17\% of calls left unphased by \toolname alone had at least twice the sequencing coverage, compared with 8\% and 2\% for \whatshap alone. Such depth can arise when reads from two paralogous copies map to one locus, a known source of false variant calls\cite{olson2026giabv5}. At 60$\times$, 3,669 calls left unphased by \toolname alone had depth of at least 90$\times$ within v5.0q benchmark regions; 92.8\% were absent from the benchmark VCF and thus classified as false positives by this benchmark. However, calls left unphased by \toolname alone overlapped segmental duplications or regions outside one-to-one assembly alignments less often than those left unphased by \whatshap alone (54--75\% versus 92--93\%). The source of the excess depth remains unresolved.
%  [provenance] Issue #6 (notes/unphased/issue6_composition.tsv, issue6_intervals.tsv,
%  issue6_depth_hist.tsv). JHL's set names: lp_only = left unphased by LongPhase 2 only
%  (phased by WhatsHap only); wh_only = left unphased by WhatsHap only; both = by both.
%  lp_only: het_match 16.0/15.1/20.3%, not matched 84.0/84.9/79.7%; wh_only: het_match
%  4.2/3.0/1.9%, absent 89.9/90.2/89.5%. Wrong phase (block-wise Hamming, scored as compare):
%  WhatsHap 5,427/23,690, 3,187/19,996, 2,463/24,719 vs 7.71/2.56/2.75% overall
%  (3.0/6.2/3.6x); LongPhase 2 215/1,549, 261/1,565, 150/991 vs 5.28/1.82/1.53%
%  (2.6/9.2/9.9x). Fig. 3c "correct" = net het_match - net wrong, so it includes the matched calls in
%  blocks too small to assess (lp_only 86/26/40, wh_only 26/14/11). Own switch-error intervals: lp_only in WhatsHap's
%  4.26/8.11/9.62, wh_only in LongPhase 2's 1.95/4.21/9.49; expected = all heterozygous calls
%  that tool phased. Depth, 2x-bin histograms: below 20x at 10x 0.695 (lp_only) / 0.639
%  (wh_only) / 0.707 (both), 30x 0.162/0.600, 60x 0.117/0.531; 60x >=90x 28.7% (lp_only, cap
%  bin 15.6%), 3.2% (wh_only). The inside-BED >=90x figure (3,684 sites, 92.0% absent; 5 and 7
%  sites in the other sets) and the segdup-or-outside-1:1 shares (lp_only 53.7/75.0/73.0%,
%  wh_only 92.0-92.9%, both 88.4-93.5%) come from the site-level table on the lab server
%  (data/unphased/issue6_sites.tsv.gz, notes/unphased/issue6_sites.py; JHL's issue #6 comment
%  of 2026-10-09) and could not be recomputed on the writing machine.
%  v2.1.1 (2026-10-16; notes/v2.1.1/claims.py and the site table, same definitions): lp_only
%  het_match 14.8-19.9%; WhatsHap wrong 5,386/23,616, 3,231/19,946, 2,432/24,629 (22.8/16.2/9.9%); LongPhase 2 wrong 188, 222, 142 =
%  12.7/14.9/14.8% of 1,478/1,489/958; enrichment lp_only 4.3/8.1/9.5, wh_only 2.4/4.1/9.9; depth <20x
%  at 10x 0.694/0.620/0.712, 30x 0.167/0.590, 60x 0.124/0.512; 60x >=90x 28.4% (cap 15.5%), 3.4%;
%  >=2x coverage 28.0/16.8% vs 7.7/1.6%; inside-BED >=90x 3,669 sites, 92.8% absent; segdup-or-
%  outside-1:1 lp_only 54.3/75.2/73.3%, wh_only 91.5-93.0%, both 88.5-93.6%.

```
