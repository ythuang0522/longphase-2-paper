# Results: SV rate sentence leads with the fold; "SV phasing error rate" used throughout, 2026-10-28 (author decision, option A)

- The nanopore SV sentence now leads with the fold, like the indel-pair sentence: "On nanopore
  data, LongPhase 2 had 1.6–2.1-fold lower SV phasing error rates than WhatsHap at every
  coverage (5.8–11.3% versus 11.2–18.7% at 10–60×; Fig. 3a and Supplementary Table 19)." Fold
  checked against Supplementary Table 19 (1.58 at 18× to 2.08 at 40×).
- The definition moved from an apposition in that sentence to the end of the preceding one:
  "…, and the SV phasing error rate was the share of phased SVs that were wrongly phased
  (Methods)."
- Term (author): "SV error rate" → "SV phasing error rate" in the two other Results sentences
  and in Methods, matching the Fig. 3 axis labels and legend.

Follow-up (author, option B): the HiFi SV sentence now leads with the fold against WhatsHap
(1.4–1.5-fold; 1.37 at 40× to 1.53), and HiPhase has its own sentence with the direction:
"HiPhase had similar rates (5.4–6.4%), lower than those of LongPhase 2 at four of five
coverages, and phased 7–9% more SVs correctly." HiPhase is lower at 10, 20, 40 and 50×
(by 0.1–0.8 points) and higher at 30× (Supplementary Table 19).

Follow-up (author, D1 with E1): the nanopore count sentence ("WhatsHap phased slightly more
SVs correctly … but about twice as many incorrectly …, and 2.7–3.3 times as many SVs that are
homozygous in the assembly") now names the two error types first: "WhatsHap made both types of
SV error more often than LongPhase 2. It placed 1.8–2.3 times as many heterozygous SVs on the
wrong haplotype and phased 2.7–3.3 times as many SVs that are homozygous in the assembly,
which are genotype errors of the variant caller. WhatsHap placed slightly more SVs on the
correct haplotype (0.7–6.3% more), so its higher error rate came from its additional errors."
The author's draft "the major source of incorrectly phased SVs are homozygous" was not used:
homozygous SVs are a separate column of Supplementary Table 19, not part of "Wrong", and are
21–30% of WhatsHap's errors (wrong + homozygous) at 10–60×.

Follow-up (author): the clause ", and the SV phasing error rate was the share of phased SVs
that were wrongly phased" was removed from the definition sentence; Methods define the rate.

Follow-up (author): "WhatsHap made both types of SV error more often than LongPhase 2." →
"We found that WhatsHap made two types of SV error more often than LongPhase 2."

Follow-up (author): "WhatsHap placed slightly more SVs on the correct haplotype (0.7–6.3%
more), so its higher error rate came from its additional errors." removed; correct counts
are in Supplementary Table 19.

Follow-up (author): the HiPhase sentence is now "HiPhase had SV phasing error rates similar to
those of LongPhase 2 (5.4–6.4% versus 5.8–6.6%)." The direction at four of five coverages and
the 7–9% more correctly phased SVs were removed (one accuracy measure per sentence; counts in
Supplementary Table 19).

Follow-up (author, option B, moved): the two SV sentences with indels ("With indels co-phased,
LongPhase 2 had SV phasing error rates of 7.2–12.1% and 7.1–7.8% … and phased 1–9% more SVs
correctly …. HiPhase had higher error rates … at 10–30× and lower at 40 and 50× …, and phased
16–19% more SVs correctly") were replaced by one sentence with the error rate only: "With
indels co-phased, LongPhase 2 had 1.7–2.3-fold lower SV phasing error rates than WhatsHap on
nanopore data and 1.3–1.7-fold lower rates on HiFi data, and rates similar to those of HiPhase
(Supplementary Fig. 17)." It moved from the end of the SV-size paragraph to the end of the
first SV paragraph. Folds from Supplementary Table 19 (nanopore 1.69–2.28, HiFi 1.27–1.69;
HiPhase within 1.2 points).

Follow-up (author, option A): the SV-size paragraph no longer opens with "The difference
depended on SV size (Fig. 3c)." (no clear antecedent; size changes the result only against
HiPhase on HiFi data). It now opens with its result: "For SVs of at least 1 kb, LongPhase 2
had the lowest SV phasing error rates at every coverage on both platforms (Fig. 3c): …". Both
"error rate(s)" in the paragraph now read "SV phasing error rate(s)".
