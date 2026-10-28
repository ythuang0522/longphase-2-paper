# Results: indel-pair sentence compares tools; line styles removed from text, 2026-10-28 (author decision, option B)

In the first comparison paragraph of `sections/results.tex`, "consecutive variant pairs
containing an indel: rates decreased from 0.100% to 0.029% for LongPhase 2 …" described a
change across coverage within one tool. It now gives the between-tool comparison first
(8–32-fold lower indel-pair switch error rates than WhatsHap; 0.029–0.100% versus
0.75–0.91%) and then why the fold difference increases with coverage. "Indel pairs" is
defined at first use, matching the later "indel-pair switch error rates" and Supplementary
Table 13. "(solid lines)" and "(dotted lines)" were removed; the Fig. 2 legend defines them.
Values checked against `notes/benchmark_strata/item3_indel.tsv` (all ten coverages; fold
8.4 at 10× to 31.8 at 60×, per-replicate means).
