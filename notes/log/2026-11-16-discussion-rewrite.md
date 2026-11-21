# 2026-11-16 Discussion rewritten to interpret the results

Author: the Discussion must discuss the results, not restate them (criticism of the MethPhaser passage,
which repeated the Results comparison and added a disclosure sentence about GNN-based unphasing).

- `sections/discussion.tex` rewritten in seven paragraphs: summary; joint versus post hoc methylation
  (MethPhaser; Hamming distance with switch error rates for block-joining methods); roles of the evidence
  classes (5mC, indels, SVs); withholding phase (switch error rates read with recall, precision and
  contiguity); benchmarks; limitations; outlook and closing sentence. 1,160 words (was 1,184).
- Removed: the disclosure sentence on GNN-based unphasing in the MethPhaser comparison and the
  sentence that GNN-based unphasing reduced the indel error. Kept: one GNN sentence in the limitations
  (held-out chromosomes and HG008, Supplementary Note 7).
- Every number comes from the current Results. Draft: `notes/drafts/discussion_2026-11-16.tex`.
- `DISCUSSION_WRITING_GUIDELINES.md` (shared): rule on restating Results comparisons added; the rule that
  asked for a disclosure of combined effects replaced by a rule against component attribution and
  disclosure sentences.
