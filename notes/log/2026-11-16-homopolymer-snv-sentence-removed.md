# 2026-11-16 Methods, allele extraction: nanopore homopolymer SNV sentence removed

Author: "Under the nanopore setting, when two SNVs lie close together in homopolymers, the downstream
SNV is removed." is too detailed (implementation).

- `sections/methods.tex`, Allele extraction paragraph: sentence removed.
- The full rule stays in Supplementary Note 1 (Allele extraction) and in the Supplementary figure
  legend of the homopolymer SNV filter (`--ont`); no content lost.
- `../../METHODS_WRITING_GUIDELINES.md`: section 6 now says that a filter active only on one platform
  or one option is a Supplementary detail, even without numbers; example row added.
