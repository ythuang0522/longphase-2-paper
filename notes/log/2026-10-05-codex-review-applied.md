# Codex review applied, 2026-10-05 (two passes)

**Codex review applied, 2026-10-05 (two passes).** Verified against source before editing:
`compare` computes Hamming over all common variants incl. indels (`CompareProcess.cpp`:579) while
switch errors are SNV-only; the region filter also applies to the query (`:353`, though N50 is
identical under both truth sets, so the BED was probably not passed);
`run_t2t_validation.sh` samples its background from all pre-correction phased SNVs (:75), tests
the assembly VCF by start coordinate only (:104) and includes chrX/chrY; the indel-cost reduction
is 41-67% (not "at least half"); four-class Hamming falls 34-54% (not "halved").

*Pass 1, corrections:* six overstatements fixed in Results/Discussion ("at least halves", "exactly
as accurate", "halved", indel cost "in the evidence itself", Margin "by fragmenting", "no threshold
on a variant's own votes"); co-phasing Hamming values flagged as SNV+indel (`\todo`); assembly
analysis narrowed to "no assembly VCF record at the same coordinate", chr19 475-fold headline
dropped, rebuild requirements as `\todo`; WhatsHap comparison restated as regional co-location;
benchmark paragraph replaced by the unresolved-contributions sentence; "error probability" ->
"phase-error score" (Methods, Supplementary); Fig. 1 stage label "Evidence calibration" ->
"Evidence weighting"; stale HiFi statements fixed (methods :36, :126); Supplementary "share one
denominator" corrected; N50/BED and paired-difference `\todo`s added; held-out chr17/21/22,
matched-retention comparison promoted to `\todo`. Figures: Fig. 2e
relabelled "switch-error-rate ratio", legend moved off the panel; Fig. 3 colours now match Fig. 2
(hatching for indel/SV runs), panel f from zero; Fig. 4 s.d. on both endpoints; Supp. Fig. 12
capped bin marked censored; legends updated.

*Pass 2, length:* Results 2,575 -> 1,377 words, seven subsections with one finding, one
representative comparison and its cost each (coverage-by-coverage values left to Supp. Tables
7-12); Discussion 1,673 -> 620 words in four paragraphs (contribution; weighting and withholding;
limits; one downstream test). Word counts exclude `\todo`s and comments; Introduction (1,017)
untouched. The cut is reviewable on its own: `notes/length_cut_2026-10-05_{results,discussion}.diff`.
