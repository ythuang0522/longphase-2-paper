# Figs. 2 and 3 split by message (option B), 2026-10-20 (author decision)

**Figs. 2 and 3 split by message (option B), 2026-10-20 (author decision).** The 3 × 2 Fig. 2 carried
three messages (platforms, evidence types, methylation tools) and showed HiFi with SNVs only. Options A
(by platform), B (by message) and C (add dashed HiFi indel lines) were discussed; the author chose B
after draft PNGs. No new runs; HiFi indel-pair switch error rates (would need rescoring on the lab
server) and TinkerHap stay out.

- Fig. 2 (`fig2()`, 2 × 4): columns nanopore SNVs, nanopore SNVs + indels (WhatsHap and HapCUT2
  `--indels 1`, replicate 1; dotted indel pairs for LongPhase 2 and WhatsHap), HiFi SNVs, HiFi SNVs +
  indels (`Other_phasers`); row 1 switch error rate against coverage, row 2 against block N50. The
  author asked whether row 2 should use Hamming distance; a draft showed the HiFi paths tangled and
  Hamming growing with block length, so row 2 stays switch error rate.
- Fig. 3 (`fig3_methylation()`, new file `fig3_methylation.pdf`, 2 × 2): a SNVs + 5mC switch error
  rate against N50 (MethPhaser, HapBridge, LongHap), b by evidence type (former Fig. 2e) with LongHap on
  all classes (former separate panel merged on request), c Hamming distance (former Supplementary
  Fig. 16d), d phased benchmark SNVs, markers side by side (lines overlapped; author). The author removed
  an "effect of adding 5mC" arrow panel (its MethPhaser/HapBridge arrows start from LongPhase 2 without
  GNN) and asked that the first panel show error rates, not phased SNVs.
- Former Figs. 3 and 4 are Figs. 4 and 5 (`fig4()`, `fig5()`; files renamed `fig4_two_benchmarks.pdf`,
  `fig5_phased_unphased.pdf`). Supplementary Fig. 16 is Hamming only: a–c as before (former b, c, e),
  d new (HiFi with indels; LongPhase 2 1.3–2.4-fold lower at every coverage).
- Results: new seventh subsection "Joint 5mC phasing gives lower error rates than methylation
  post-processing" (author's wording; the author will refactor it) holds the former 5mC paragraph, split
  into MethPhaser/HapBridge and LongHap paragraphs with Fig. 3 citations; HapCUT2 with indels added to
  the nanopore paragraph (3.5–4.8-fold); HiFi with indels added to the HiFi paragraph (HiPhase 1.6–1.9-,
  WhatsHap 2.3–2.9-, HapCUT2 3.1–3.5-fold) and to the contiguity paragraph (LongPhase 2 blocks 14–18%
  longer with indels, others a further 1–17%; HiPhase and HapCUT2 phase 5–9 points more indels); the
  further-phasers paragraph keeps TinkerHap only. Values in the provenance comments.
- Legends of Figs. 2 and 3 rewritten; Discussion, Supplementary Fig. 16 legend, Supplementary Data 1
  table, Supplementary Method N50 sentence and Table 11 caption updated for the new numbering.
- Rebuilt: main.pdf 30 pages, Supplementary.pdf 43 pages; 0 undefined references, 0 overfull boxes.
- Fig. 3 panel order changed the same day (author: the evidence-type panel "should be the last one to
  conclude"): a SNVs + 5mC against N50, b Hamming distance, c phased SNVs, d by evidence type. Results,
  legend, Supplementary Fig. 16 legend and the N50 method sentence remapped (3b→3d, 3c→3b, 3d→3c).
