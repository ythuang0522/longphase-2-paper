# Introduction: phaser overview rewritten (version 1 of 3)

Author request (2026-10-27): "These methods centre on SNVs…" disagreed with the Results
(WhatsHap and HiPhase phase SVs; HapCUT2 phases indels), and the paragraph's opening did
not give an overview of the existing phasers. Author chose version 1 of three drafts.

- The first two sentences of the second Introduction paragraph are now a tool-by-tool
  overview: model and variant types of WhatsHap, HapCUT2, Margin, HiPhase (new in the
  Introduction; it is compared in the Results) and LongPhase, ending with the gap
  "each phaser handles a different subset of variant types, and none phases sequence
  variants and allele-specific methylation in one model". "In one model" keeps the gap
  true for HiPhase and LongHap.
- The later part of the paragraph (pipelines, error propagation) had been rewritten on
  disk before this change and was kept. Two edits for the merge: "which we developed
  previously\cite{lin2022longphase}" removed (LongPhase is now introduced in the overview)
  and "structural variants (SVs)" → "SVs" (now defined in the HiPhase clause). SNVs are
  defined in the WhatsHap sentence.
- Open: check that edge2017hapcut2 describes indel phasing ([citation] comment).
