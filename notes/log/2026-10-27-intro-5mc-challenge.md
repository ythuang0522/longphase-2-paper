# Introduction: 5mC challenge reframed as accuracy (version B of 3)

Author request (2026-10-27): the paragraph was too long, and "integrating 5mC is a
challenge" is not defensible, because MethPhaser, HapBridge and LongHap already use
methylation. The challenge should point to accuracy, which the Results test
(Fig. 3d–f). Author chose version B of three drafts, then asked for a more precise word
than "sparse" and a stronger last sentence.

- First challenge is now "methylation-aware phasing gains contiguity at a possible cost
  in accuracy". Evidence from the MethPhaser abstract: N50 +78–151% "at a phasing accuracy
  of 83.4–98.7%" (fu2024methphaser). No switch-error numbers were found for HapBridge
  (bioRxiv introduction only) or LongHap (PyPI description only).
- NanoMethPhase removed as a tool (it assigns methylation after phasing and joins no
  blocks); still cited for the biology.
- "Sparse" replaced by the specific properties: haplotype-specific methylation is confined
  to a small fraction of CpGs, the state of a CpG can differ between molecules of the same
  haplotype, varies between cells and tissues, and is called as a per-molecule probability.
- Last sentence: a join resting on a few such CpGs can reverse the phase of every variant
  beyond it, so methylation needs to be weighed against the sequence alleles on the same
  reads, not added after the phase is fixed (echoes the Results heading "methylation
  post-processing").
- Open: confirm how MethPhaser defines "phasing accuracy" in its Results before submission.
