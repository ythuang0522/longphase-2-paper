# Results: component names removed; GNN subsection moved to Supplementary Note 1, 2026-10-28 (author decision, options 4A, 5a-A, 5b-A)

Author rule: the Results present LongPhase 2 as one tool.

- **4A, overview.** "The `modcall` module calls allele-specific 5mC sites …" → "LongPhase 2
  calls allele-specific 5mC sites …"; "5mC sites called by `modcall`" → "5mC sites that it
  called". The overview still describes the uncertainty step and the GNN as part of the method.
- **5a-A, unphased-SNV subsection.** Title "At 60×, SNVs unphased by GNN correction lie mostly
  outside one-to-one assembly alignments" → "At 60×, SNVs withheld at high phasing uncertainty
  lie mostly outside one-to-one assembly alignments". "SNVs unphased by GNN correction" →
  "SNVs that LongPhase 2 withheld at high phasing uncertainty"; the sentence "This step
  accounted for 17–20% of the calls left unphased by LongPhase 2 alone …; the rest were
  withheld before correction" was removed; "random sample phased before correction" →
  "random background sample of phased SNVs"; "sites later unphased by correction" →
  "withheld sites". Fig. 5 row 2 labels and legend still say "unphased by GNN" (draft titles
  shown to the author; not yet changed).
- **5b-A, GNN subsection.** The subsection "GNN correction reduces genome-wide SNV switch error
  rates by one-third and limits indel-associated errors" was removed from the Results. Its
  three with/without-GNN paragraphs (genome-wide effect; held-out chromosomes and HiFi;
  evidence classes before and after correction), with their source comments, are now
  Supplementary Note 1, "Effect of GNN correction", a new section of `Supplementary.tex`
  before the Supplementary Tables. The evidence-class contiguity paragraph and the
  phased-fraction-by-class paragraph moved to the end of the 5mC subsection (they describe
  Fig. 3f); "After correction," was removed, and the sentence "All configurations retained at
  least 2.5-fold lower SNV switch error rates than WhatsHap with or without indels" was
  removed because the moved four-class sentence states it.

Open: Supplementary Figs. 13 and 14 are now cited only from Supplementary Note 1, not from the
main text. The Results now have seven subsections.
