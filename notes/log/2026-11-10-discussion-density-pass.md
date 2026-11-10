# Discussion density pass

2026-11-10. Second review (Codex) of the Discussion revision of the same day; author decisions:
remove the before-GNN ratio from paragraph 3, keep the SV sentence, change "more SNVs" to "a larger
fraction" in the Results and the Discussion. No new measurements.

`sections/discussion.tex`
- Paragraph 1: "post-processes an SNV phasing" -> "joins existing SNV phase blocks"; "these blocks
  contained more SNVs on the wrong haplotype" -> "a larger fraction of the SNVs in these blocks were on
  the wrong haplotype" (the evidence is Hamming distance); "The gains from indels and 5mC" -> "The
  numbers of blocks joined by indels and 5mC" (93–99% of the sum of joins); indel sentences put together
  after the SV sentence ("Indels joined more blocks but were also associated with more switch errors. A
  similar trade-off in WhatsHap…"); the "8–32-fold" sentence removed (repeats the Results).
- Paragraph 2: "at matched variant retention" -> "when the same number of variants retain phase
  assignments"; "Its onset-prediction score" -> "The GNN prediction score".
- Paragraph 3: before-GNN sentence (1.9–2.5-fold, Supplementary Note 1) removed; "Only 3.3–7.6% … were
  confirmed genotype errors" -> "Among unphased calls, 3.3–7.6% were heterozygous calls at sites
  classified as homozygous in v5.0q" (absent calls inside the benchmark regions are false positives
  too); last sentence -> "In an exploratory analysis of a subset of unphased SNVs, most lay outside…".
- Paragraph 4: first two sentences combined.
- Paragraph 6: "(Supplementary Note 1)" after the held-out sentence. Supplementary Table 17 is not
  cited: a Discussion citation would put it before Supplementary Tables 12–16 (first cited in Methods)
  and force a renumbering.

`sections/results.tex`
- MethPhaser paragraph, last sentence: "contained more SNVs" -> "contained a larger fraction of SNVs".
