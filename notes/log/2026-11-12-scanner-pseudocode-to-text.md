# 2026-11-12 Supplementary Method 1: scanner pseudocode replaced by text and a constants table

Author decision (option A of three: text + table; text + table + state-diagram figure; formal Algorithm box).
The code listing of the copy-number-aware scanner was at code level and hard to read.

- Removed: the two displayed piecewise formulas for r, p and f, the sentence that listed the constants,
  the 30-line `verbatim` listing and the paragraph after it.
- Added: paragraphs "Scanner states", "Opening an interval", "Step intervals", "Ramp intervals",
  "Discarding a candidate", and one unnumbered table (Π, A, E, Λ, Σ, r, p, f) in the text of the
  Supplementary Method. No Supplementary table number changed.
- Unchanged: "Clipping counts", "Site removal", "Choice of constants".
- Checked against `../longphase/PhasingGraph.cpp:1113-1198` and `PhasingGraph.h:19-23` (v2.1.1, f9962dd).
  The full transition rules stay in the source code.
