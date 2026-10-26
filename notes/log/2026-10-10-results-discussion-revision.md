# Results and Discussion revision, 2026-10-10 (Codex; final author-approved structure)

**Results and Discussion revision, 2026-10-10 (Codex; final author-approved structure).**
Results has six declarative, unnumbered subsection headings and no run-in headings:
overview, phaser comparisons, benchmark context, completeness and genotype errors,
GNN-unphased SNVs, and internal modules. The final section's opening transition
preserves the comparison-then-modules order. Paragraph openings state the findings;
CLAUDE.md and the Results structure comment record this convention. Discussion has
seven focused paragraphs without subheadings: contribution, uncertainty measures,
retention trade-offs, truth-set disagreement, benchmark extent, generalization, and
remaining scope/downstream tests. Results figure pages are flushed before Discussion.

The comparison heading covers evidence types and sequencing platforms without claiming
similar contiguity for every comparison or universal superiority over Margin. The
Ralphi paragraph reports its higher switch error rates; the accuracy/contiguity
trade-off applies to Margin only. Ralphi's block N50 is not comparable (Supplementary
Table 8 and Supplementary Fig. 9c). The MethPhaser paragraph explicitly attributes the
lower Hamming distance to LongPhase 2. The genotype-error heading names WhatsHap;
the assembly heading specifies 60×; and the one-third reduction refers to genome-wide
SNV switch error rates. Repeated heading claims were removed from the assembly and
internal-module paragraph openings.

The revision separates accuracy from contiguity, completeness from call composition,
and assembly findings from their limitations. It clarifies identical SNV inputs,
modcall, GNN prediction versus subsequent unphasing/block splitting, and the separate
sources of training reads and labels. The accepted Hamming-denominator correction is
991–1,565 assessable benchmark-matching SNVs. Numerical anchors retained include the
uncorrected accuracy/contiguity comparison (1.9–2.5-fold lower rates, N50 3% shorter to
7% longer), CPU-time growth (2.5/4.5/4.0-fold), 8–31-fold lower indel-pair rates, and
2.1–10-fold lower rates inside v5.0q benchmark regions. The previously checked
13–25-fold ratio uses assessed benchmark-matching calls (23,690/19,996/24,719 versus
1,549/1,565/991); CPU-time growth uses 816→2,067 s, 1,504→6,817 s and 1,443→5,754 s.
Within-BED comparisons use rates per assessed pair with both variants inside the BED.

Benchmark-absence cautions, uncertain-region limits, unverified truth-set disagreements,
the explicit 60×/90× depth definition, citation keys, figure references and the SV/5mC
data-deposit TODO remain. The 15–41 errors remain neutral count context. No data,
figure artwork, Methods or Supplementary content changed in this editorial revision.

Validation: main.pdf rebuilt with TeX Live (26 pages); revised Results pages rendered
and inspected. Exactly six subsection headings and no paragraph headings. No undefined
references/citations or missing characters. Existing title/affiliation overfull and
caption underfull warnings remain. git diff --check passes.
