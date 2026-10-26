# Further phasers in the manuscript, 2026-10-19 (author request)

**Further phasers in the manuscript, 2026-10-19 (author request).** Used the `Other_phasers`
sheet (JHL, 2026-10-17/18) in the text; no new runs. New Supplementary Table 18 (`other_phasers_table()`
in `make_results_figs.py`): five comparison blocks (nanopore SNV + 5mC, SNV + indel, all classes +
5mC; HiFi SNV-only, SNV + indel), LongPhase 2 first in each block, with the switch error rate relative
to LongPhase 2; the GNN-model table is now Supplementary Table 19 (two references renumbered).
Results: one paragraph after the MethPhaser paragraph (HiPhase 1.7–1.9-fold, TinkerHap, HapBridge 1.5-fold,
LongHap 2.2–5.3-fold, with its 18–22% Hamming distances), ratios in its provenance comment; "three tools"
made explicit where the paragraph made it ambiguous; the runtime sentence now covers both platforms.
Methods: one passage on the four phasers in "Comparison with other methods"; the HiFi runtime
sentence rewritten to state that wall-clock times of the re-timed HiFi runs had the alignment file
in the page cache and that CPU time is the cross-platform measure (Table 16 caption to match, and it
now says LongPhase 2 was re-timed at every coverage). Discussion: one sentence after the LongHap
contrast (1.5–1.7-fold vs MethPhaser and HapBridge, 2.2–5.3-fold vs LongHap; most of the MethPhaser
gap from GNN correction). Supplementary Table 5: rows for HapBridge, LongHap, TinkerHap and HiPhase,
HapCUT2 indel runs. New reference `hartmann2025tinkerhap` (GigaScience 2025). Supplementary Data 1
paragraph: tables 7–11, 13, 14, 17 and 18. Rebuilt: main.pdf 28 pages, Supplementary.pdf 42 pages,
no undefined references, overfull boxes or missing characters.
