# Introduction: "three challenges" frame removed; context and reliability merged

Author decision (2026-10-27): the three challenges were not the same kind of problem. The
methylation paragraph describes the status of a field; the second (context-dependent errors)
and third (unreliable phase assignments) describe one chain, from where phase errors start
to why phasers do not flag them. Author chose order B (methylation, then errors, then
benchmarks, then "Here we present"; the same order as the Results), version 1 of three
merged-paragraph drafts, and option 1 of three rewrites of its confidence sentences.

- "Three challenges remain in read-based phasing. The first is that…" → "Methylation offers
  a further source of phase evidence, but methylation-aware phasers gain contiguity at a
  possible cost in accuracy."
- Challenges 2 and 3 (about 240 words) → one paragraph (about 140 words): errors cluster in
  homopolymers, tandem repeats, segmental duplications and copy-number-altered regions;
  base-quality weights do not detect a misplaced read; WhatsHap and Margin report no
  per-variant confidence, LongPhase only read support, and HapCUT2 posterior confidence can
  stay high when misplaced reads agree; learning-based phasers optimize the objective, not
  detect its errors; the need is context weighting and marks on unreliable assignments.
- Removed: SHAPEIT5 posterior sentence (hofmeister2023shapeit5 stays cited in paragraph 1),
  the definition of the LongPhase tagging quality, the ralphi details (simulated reads,
  SNVs only, the authors' note), and the downstream-consequence sentence (zheng2026clairs
  and keskus2025severus stay cited in paragraph 2).
