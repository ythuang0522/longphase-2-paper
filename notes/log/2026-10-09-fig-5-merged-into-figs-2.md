# Fig. 5 (HiFi) merged into Figs. 2 and 4, 2026-10-09 (author decision, option C of a design discussion)

**Fig. 5 (HiFi) merged into Figs. 2 and 4, 2026-10-09 (author decision, option C of a design
discussion).** Main figures go from five to four, one message each: Fig. 2 accuracy and contiguity,
Fig. 3 benchmarks, Fig. 4 completeness.
- **Fig. 2** gains a fourth row, "SNV phasing, PacBio HiFi" (j switch error rate, k Hamming distance,
  l switch error rate against N50; LongPhase 2 vs WhatsHap, one replicate per coverage, 10–50×).
  j and k use the same axes as the nanopore rows; l has its own N50 axis (0–0.7 Mb), stated in the
  legend. The HiFi N50-by-coverage panel (old Fig. 5c) is replaced by the path in l. Height
  150 → 198 mm; `main.tex` limits it to 0.64\textheight in the draft so that the legend fits.
- **Fig. 4** gains b, HiFi completeness (old Fig. 5d); precision and genotype errors move to c and d
  and are titled "nanopore" because no HiFi precision or genotype-error counts exist.
- Rejected: option A (Fig. 4 as two rows, nanopore completeness and all HiFi metrics; two messages
  in one figure) and C' (HiFi row in Fig. 2 only; Fig. 4 stays thin).
- Results: the HiFi paragraph moved to directly after the MethPhaser paragraph (Fig. 2j–l); its
  phased-fraction clause moved to the completeness paragraph with the HiFi trend (87% at 10× to
  92% at 20–50×, Fig. 4b, Supplementary Table 11). `fig5()` and `figures/fig5_hifi.pdf` removed.
  Literal references updated: Methods (Figs. 2–4, Fig. 4c,d), Supplementary block-N50 paragraph
  (Figs. 2c,f,i,l) and Supplementary Data 1 paragraph (Figs. 2–4, Fig. 4c,d).
