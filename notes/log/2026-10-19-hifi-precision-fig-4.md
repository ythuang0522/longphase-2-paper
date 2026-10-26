# HiFi precision in Fig. 4, 2026-10-19 (issue #9; author approved the figure first)

**HiFi precision in Fig. 4, 2026-10-19 (issue #9; author approved the figure first).** JHL counted
the phased heterozygous SNV calls on chr1–22 of the HiFi SNV-only runs (4393308,
`notes/unphased/phased_calls_hifi_chr1_22.tsv`). Fig. 4 is now a 4 × 2 grid without row titles:
a nanopore completeness, b nanopore precision, c HiFi completeness, d HiFi precision (LongPhase 2,
WhatsHap, HiPhase), e genotype errors phased, f–h SNVs unphased by GNN (former e–g). Every
`fig:unphased` panel reference in Results and Methods remapped (Methods had cited c for the
genotype errors; now e), legend rewritten, Supplementary Data 1 rows updated (Fig. 4b,d and 4e).
Results: one sentence after the nanopore F1 sentence (HiFi precision 92.2–95.0% LongPhase 2,
90.3–94.6% WhatsHap, 91.1–93.9% HiPhase; lead over WhatsHap 1.8 → 0.3 points, over HiPhase
1.1–1.5), values in its provenance comment. Supplementary Table 11 has a Precision column
(LongPhase 2, WhatsHap, HiPhase; -- for the others). Sheet `Phased_calls` now has a `platform` column
and the 15 HiFi rows (143 rows), from the new `notes/unphased/phased_calls_sheet.tsv`, which
`notes/v2.1.1/update_xlsx.py` now reads. Rebuilt: 28 and 42 pages, clean logs.
