# Fig. 5 redrawn (option B) and its two subsections merged

2026-11-10, author decisions after two draft PNGs (`notes/drafts/`) and a second review (Codex).

**Why.** The author's point for this part is that LongPhase 2 leaves many calls unphased and that this choice is
correct. The old figure spent four of eight panels on completeness and precision curves, showed only the homozygous
class, and no panel showed which calls are left unphased.

**Fig. 5 (`fig5()` in `figures-source/make_results_figs.py`), 3 + 4 panels, nanopore, chr1-22.**

| Panel | Content | Old place |
|---|---|---|
| a | v5.0q status of calls phased and left unphased by LongPhase 2, 10/30/60x | new |
| b | phased calls at v5.0q homozygous sites, both tools | Fig. 5e |
| c | WhatsHap wrong-phase share at benchmark SNVs unphased by LongPhase 2, against all its phased SNVs | text and Supplementary Table 9 |
| d | precision, nanopore | Fig. 5b |
| e | completeness, nanopore | Fig. 5a |
| f | read depth at 60x | Supplementary Fig. 7c (kept there too) |
| g | T2T-HG002 1:1 alignment, subset left unphased at high phasing uncertainty | Fig. 5g |

Moved to the new Supplementary Fig. 6 (`sfig_unphased_more()`, `figures/supp/suppfig_unphased_more.pdf`): HiFi
completeness and precision (old c, d), v5.0q status of the subset (old f), by chromosome (old h).
Supplementary Figs. 6-18 became 7-19 (first-citation order); literal numbers swept in the .tex files, both figure
scripts, CLAUDE.md and README.md.

**Results.** The subsection "At 60x, SNVs withheld at high phasing uncertainty lie mostly outside one-to-one assembly
alignments" was merged into "LongPhase 2 leaves error-prone SNV calls unphased". New order: which calls (5a), direct
evidence (5b,c), gain and cost (5d,e), read depth (5f), the subset (5g, Supplementary Fig. 6c,d), limits and
conclusion. New first paragraph with the chr1-22 counts (numbers in the provenance comment). "withheld" is now
"left unphased". The copy before the change is not kept in the repository; see git diff.

**Claim level (Codex review, accepted by the author).** Not matching a benchmark heterozygous SNV is not the same as a
calling error: homozygous in v5.0q is direct evidence; absent is not. Depth and T2T alignment are supporting evidence
(v5.0q derives from the same assembly). The 4-6 calls per lost SNV ratio holds only for the calls phased by WhatsHap
only (net 2.1-4.2) and is not in the text. The subset is about 29% of all calls left unphased at 60x, not one sixth.

**Legend.** New title "Heterozygous SNV calls that LongPhase 2 phases and leaves unphased." Methods and Supplementary
Data 1 panel references updated. Subsection title (author, option 1 of 3): "LongPhase 2 leaves error-prone SNV calls unphased" became "LongPhase 2 leaves unphased the SNV calls that rarely match the benchmark".

**Not done.** absent is not split by inside or outside the benchmark regions: the site table is on the lab server.

**Condensed the same day (author: long and fragmented).** Seven paragraphs (811 words) became three (about 470 words):
which calls and direct evidence (Fig. 5a-c), gain and cost (Fig. 5d,e), genomic context and conclusion (Fig. 5f,g).
Removed from the Results: the other-allele share, the 124,000-151,000 calls phased by WhatsHap only and the converse
set, the allele-matched counts of the subset, the autosome-only shares, the odds ratios (98; 131), the three
pericentromeric loci, the 7,072 / 3,843 sentence and three of the four limits of the assembly comparison. The overall odds
ratio (98) was put back into paragraph 3 the same day (author). The autosome-only odds ratio (131) and the three loci
are now in no part of the manuscript; the other values remain in Supplementary Tables 9
and 10. Numbers are listed in the provenance comment in `sections/results.tex`.

**Fig. 5a changed the same day (author).** The first sentence compares LongPhase 2 with WhatsHap, but panel a showed
LongPhase 2 only. Panel a now shows the calls left unphased by each tool as counts (thousands) by v5.0q status at
10/30/60x: 6 bars, chosen from three draft variants (`notes/drafts/draft_fig5a_variants.png`) over 12 or 8 percent
bars. The phased composition is the precision curve in panel d. The author rewrote the first three sentences of
paragraph 1 by hand; only the Fig. 5a citation moved to sentence 1 and the WhatsHap share (2.0-3.3%) was added.

**2 x 4 grid, the same day (author).** The counts panel made the comparison with WhatsHap clear but lost the comparison
of phased with unphased calls, which is the direct evidence for the message. Both panels are kept: a = LongPhase 2
phased and unphased calls in percent (the first option-B panel), b = calls left unphased by both tools as counts.
Panels b-g became c-h; letters updated in the Results, the legend, Methods and the Supplementary Data 1 sheet list
(the stale "precision in Fig. 5b,d" is now "Fig. 5e, Supplementary Fig. 6b"). Paragraph 1 rewritten in panel order
a-d; new value: 66-79% of the additional calls that LongPhase 2 leaves unphased are absent from the benchmark or
homozygous (numbers in the provenance comment). Draft: `notes/drafts/draft_fig5_row1_4panels.png`.

**One sentence reworded (author: "which alone does not establish an error" reads strangely).** "…and 81-86% were absent
from the benchmark VCF, which alone does not establish an error" became "…whereas 81-86% had no record in the benchmark
VCF and could not be classified". The limit stays in the text: it is the only place that says absent is not an error.

**Reason for the absent calls added (author).** The sentence "…had no record in the benchmark VCF and could not be
classified" now gives the two cases from the GIAB v5.0q preprint (Olson 2026, full text read 2026-11-10): inside the
benchmark regions such calls are false positives; outside, they lie in sequence that v5.0q excludes (alignment breaks
in large repeats, large structural or copy-number differences) and cannot be assessed. Open: (1) the inside/outside
split of the 81-86% needs the lab-server site table; (2) citation check: the preprint text does not contain
"homozygous", "paralogous" or "collapsed", so the two other sentences of this subsection that cite it need a check.

**Citation check of Olson 2026 in this subsection (author approved both corrections).** The author had rewritten
paragraph 1 again; checked against the full preprint text. Supported: calls absent from the benchmark are false
positives inside the benchmark regions and unassessed outside. Not supported: (1) "sites incorrectly called
heterozygous, which introduce incorrect alleles when phased" - citation removed; (2) "Excess depth can arise when reads
from paralogous copies map to one locus" - reworded to "Excess depth is expected where HG002 carries more copies of a
sequence than the reference, and v5.0q excludes regions with such copy-number differences". This closes open item (2)
above. A reference for paralogous or collapsed copies (candidate: Aganezov 2022, not read, not in references.bib) was
not added.
