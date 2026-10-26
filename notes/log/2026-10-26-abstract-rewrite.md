# Abstract rewritten as a whole, 2026-10-26 (author decision)

The author asked to rewrite the whole abstract so that reviewers see LongPhase 2 as better than its
competitors without listing every tool. Four drafts (A–D) were shown. Author: "Start with C motivation and
use A. But don't mention nine as only few major players are compared"; keep the Fig. 4 contrast between the
T2T-derived benchmark and the earlier GIAB benchmark; end with one closing sentence.

- Motivation (draft C): the four classes on the same molecules, phased separately by other tools.
- Body (draft A, without the count of nine phasers and without "all comparisons but one"): SNVs 1.7–5.0-fold
  lower than widely used read-based phasers, 5mC 1.5–5.4-fold lower than methylation-aware phasers, at every
  coverage; SVs 1.3–2.3-fold lower than WhatsHap; four-class blocks 18–46% longer at ≥ 2.5-fold lower
  switch error rates than WhatsHap.
- Benchmark sentence (Fig. 4): 1.2–1.3-fold under GIAB v4.2.1 at 30–60× with shared errors, 4.3–5.0-fold
  under v5.0q.
- Closing sentence: speed (8.9-fold on one thread, v2.1.2) and the drop-in replacement.
- Both abstract `\todo` marks (SV range, speed) resolved. Sources in the `[provenance]` comment under the
  abstract. Length: 186 words (the earlier abstract had 178).

**Benchmark sentence, same day (author: version H2 of several rounds).** The author found the coverage-specific
fold ranges ("1.2- to 1.3-fold at 30–60×") too complex for readers and wanted the sentence to convey why the
T2T-derived benchmark is the better measure (Fig. 4). New sentence: "Switch errors shared by all phasers
under the earlier GIAB benchmark largely disappeared under the T2T-derived benchmark, which distinguished the
phasers more clearly, particularly in segmental duplications and other difficult regions." Sources in the
abstract provenance comment.
