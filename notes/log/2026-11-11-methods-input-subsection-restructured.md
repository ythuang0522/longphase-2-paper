# Methods: input subsection restructured (option A)

Author, 2026-11-11: the subsection "Input variant calls" described the benchmark, not the tool; it
contained a methodology rule (tandem-repeat indels); and it did not say that 5mC is called internally.

Changes in `sections/methods.tex`:

- Heading `Input variant calls` -> `Input alignments and variant calls`. The text now states what
  LongPhase 2 accepts, as in the README of `twolinin/longphase`: SNVs and small indels from
  DeepVariant (`poplin2018deepvariant`; author, same day: the current DeepVariant no longer depends on
  PEPPER and Margin) or Clair3 (`zheng2022clair3` added here), SVs from Sniffles2 or cuteSV (supporting
  read names optional: author, same day; v2.1.2 `ParsingBam.cpp:1336, 1833, 2206` reads `INFO/RNAMES`
  only if present and otherwise uses the CIGAR and split alignments), and 5mC called internally from the modification tags. Present tense for the
  tool's inputs. The callers and versions of the benchmark stay in "Benchmark data", which keeps
  PEPPER-Margin-DeepVariant r0.8 because the benchmark runs used it.
- Heading `Calling allele-specific methylation` -> `Internal calling of allele-specific methylation`.
  Text unchanged.
- The tandem-repeat sentence left the input subsection. The voting subsection now gives the definition
  (dinucleotide immediately downstream in five consecutive copies, from Supplementary Method 2) and the
  reason next to the 0.1 vote weight.

`Supplementary.tex`, Supplementary Method 2: "The supporting read names and length of each retained SV
were recorded." -> "The length of each retained SV was recorded, with its supporting read names when
the caller reported them."

No number or figure changed.

Later the same day (author): the clause about supporting read names was removed from the input
subsection. The sentence now ends at "such as Sniffles2 or cuteSV." The allele-observation subsection
still names the caller's read list as optional SV evidence.

Later the same day (author): the 5mC sentence of the input subsection was rewritten in a direct form:
"Allele-specific 5mC sites are called internally by LongPhase 2 from the modification tags of the
alignments (next subsection)."
