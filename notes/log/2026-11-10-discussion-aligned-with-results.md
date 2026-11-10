# Discussion aligned with the updated Results

2026-11-10. Author-approved old | new draft after two reviews (Claude, Codex). Paragraph order
unchanged; no HiFi Hamming sentence (author). No new measurements. File: `sections/discussion.tex`.

## Paragraph 1
- MethPhaser: "for MethPhaser, most of this difference came from GNN correction" (share 0.66–0.95, in
  source comments only) replaced by "This comparison also includes the effect of GNN correction, which
  was not applied to the MethPhaser input." Added: MethPhaser blocks are longer but contain more SNVs
  on the wrong haplotype (Supplementary Fig. 1e).
- SVs: HiPhase sentence balanced (similar overall; LongPhase 2 lower at >= 1 kb, HiPhase for shorter SVs).
- Variant classes: block-join explanation from the Results (added phased sites do not predict joins;
  5mC about twice the sites of indels but fewer joins; indels most joins and most added switch errors;
  nearly additive; SVs barely change block length).

## Paragraph 3
- Citations added: Supplementary Note 1 (before GNN correction), Supplementary Table 5 (SVs, "on both
  platforms": right +0.7 to +6.3%, wrong x1.45–2.27 over nanopore and HiFi, SNV + SV input).
- New lead: 29–48% fewer genotype errors phased against 0.7–1.0 (nanopore) and 0.2–0.5 (HiFi) points of
  completeness; 9.8–13.0% of unphased against 89.9–93.3% of phased calls match the benchmark; 3.3–7.6%
  confirmed genotype errors; benchmark absence kept apart from confirmed error.
- Removed: "Most additional SNV calls phased by WhatsHap…" and the 13–26 times sentence (Supplementary
  Table 9 only).
- "unphased by the GNN" became "a subset left unphased at high phasing uncertainty" (as Fig. 5h).

## Paragraph 4
- Fold values at 30–60x removed (number-free sentence).
- "most disappeared" and "agreed with v5.0q at most of these sites" narrowed to switch-error counts:
  `item4_overlap.tsv` compares tools within one truth set; no analysis follows the same variant pairs
  across the two benchmarks.

## Paragraph 5
- "with the largest separation in newly covered regions" became "including in newly covered regions".
  HapCUT2 / LongPhase 2 rate ratio at 60x: shared 8.46, new 7.07 (`item4_strata.tsv`, truth v5); at
  30–50x and for WhatsHap at every coverage the new regions are larger.
- `[claim]` comment: Supplementary Table 12 -> 8.
