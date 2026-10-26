# SV phasing accuracy requested (issue #10), 2026-10-24 (author decision)

**SV phasing accuracy requested (issue #10), 2026-10-24 (author decision).** After JH's comparison in
twolinin/longphase#136 (LongPhase 2 v2.1.1 against WhatsHap 2.8, HG002 nanopore 10× and 30×, HiFi 30×,
truth from the T2T-HG002 Q100 v1.1 dipcall VCF), the author decided to add SV phasing accuracy to the
main text for every coverage on both platforms, with HiPhase on HiFi. Issue #10 asks JH for the runs
and the scores; the example layout (placeholder values) is on branch `issue-sv-phasing-figures`,
`notes/issue_sv_phasing/`. The layout is not agreed yet.

The text that called SV phasing accuracy untested was changed:
- `sections/discussion.tex`, limitations: "SV and 5mC evaluation measured phased fractions rather than
  phasing accuracy, and neither class had supervised training labels" became "5mC evaluation measured
  phased fractions rather than phasing accuracy, and neither SVs nor 5mC sites had supervised training labels".
- `sections/results.tex`, `[optional experiment]` comment (ii): SVs removed from "phasing accuracy … of the
  indels, SVs and 5mC sites".

Same day (author decision): the SV runs use LongPhase 2 with twolinin/longphase#136 (the SV fix),
head commit `b521eb1` of `sunnyplaycode/longphase` `fix/issue126-split-deletions`, not v2.1.1. The
SNV results of the paper stay on v2.1.1. Issue #10 was edited to match.
