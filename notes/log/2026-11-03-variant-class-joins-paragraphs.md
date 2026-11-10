# Results: variant-class paragraph replaced by two paragraphs on block joins and their cost, 2026-11-03 (author decision)

The author found the option-B paragraph descriptive and asked for analyses that explain the four-class
result. New analyses from supplementary.xlsx (blocks joined, sites added, joins per 1,000 sites,
switch errors per join; Supplementary Table 6, see 2026-11-03-supp-table6-joins.md) and the HiFi issue
#10 runs give two messages: indels, not 5mC, join most blocks (5mC adds 1.9-2.3x as many phased sites
but 4.4-9.5-fold fewer joins per site; the two classes add up, 93-99%); 5mC joins add almost no
switch errors, indel joins add 0.18-0.31 per join on nanopore and 0.18-0.60 on HiFi. The SV
statement was reduced to one sentence for both platforms (N50 within 1%), after the author noted
that "SVs joined no blocks" contradicted the HiFi clause. Not in the text: the HiFi switch error
rate increase with indels (26-90%), the replicate-level correlations (no stable sign), and the
position-level analyses (gap anatomy, location of the added switch errors), which need the lab
server VCFs.

Second paragraph, first sentence (author, same day: 5mC still adds a few errors; join with "while"):
"5mC lengthened blocks without adding errors; indels lengthened them at a cost." became
"5mC lengthened blocks with few added switch errors, while indels lengthened them at a higher cost in accuracy."

Last sentence (author, same day): "of the heterozygous SVs called by Sniffles2" became "of the called heterozygous SVs" (parallel with "the called heterozygous 5mC sites"; Sniffles2 is named in Methods).

Last sentence (author, same day: unclear which tool): "Four-class phasing placed" became "In four-class phasing, \toolname placed". The values are LongPhase 2 only (notes/sv_mod/, co-phase_Detail).

Phased fractions moved (author, same day: compare completeness where Fig. 5 shows it). Removed from the
variant-class paragraph: In four-class phasing, \toolname placed 97.4--99.2\% of the called heterozygous 5mC sites, 66.1--68.5\% of the called heterozygous SVs and 30.5--45.4\% of benchmark heterozygous indels in phase blocks (replicate~1; Supplementary Data~1).
The indel part repeated the completeness section (WhatsHap 2.5-4.5 points more); the 5mC fraction has no
comparator (Supplementary Data 1 keeps it). Added to the completeness paragraph of the Fig. 5 section, after the
HiFi indel sentence: SV phased fractions, SNV+SV input (as Fig. 3a,b), from notes/sv_phasing/sv_phasing.tsv,
with GNN, sv_phased/sv_input summed over sizes and types: nanopore LongPhase 2 70.3-75.6, WhatsHap 89.5-91.2;
HiFi LongPhase 2 76.9-78.0, WhatsHap 87.0-89.8, HiPhase 84.7-85.6 (Supplementary Table 5).

Previous paragraph (option B, same day):

  Phasing all four classes together gave longer blocks at a small cost in accuracy, and indels caused most of both changes (Fig.~\ref{fig:methylation}f, Supplementary Fig.~4e--h and Supplementary Table~6). Compared with SNV-only phasing, four-class phasing gave blocks 18--46\% longer at 10--60$\times$ (4.14 versus 2.87~Mb at 60$\times$), with 14--27\% higher SNV switch error rates. Indels alone lengthened blocks by 16--33\% and raised switch error rates by 14--24\%. 5mC lengthened blocks by 2--16\% with switch error rates within 3\% of SNV-only phasing, and SVs changed N50 by at most 1.7\%, because an SV does not join two blocks on its own. Adding SVs and 5mC to indels changed indel-pair switch error rates by at most 7\% (Supplementary Table~2). Four-class phasing placed 97.4--99.2\% of the called heterozygous 5mC sites, 66.1--68.5\% of the heterozygous SVs called by Sniffles2 and 30.5--45.4\% of benchmark heterozygous indels in phase blocks (replicate~1; Supplementary Data~1).

## Closing sentence added (author chose option B, without LongHap)
Added at the end of the second variant-class paragraph (end of the subsection "Joint phasing extends lower error rates to SVs and 5mC"):
> Joint phasing thus extended the lower error rates of \toolname to SVs and 5mC, and phasing all four classes together lengthened blocks while keeping switch error rates below those of \whatshap (Fig.~\ref{fig:methylation}f).

LongHap is not named: the author considers it a minor comparator next to HiPhase and MethPhaser. Four-class \toolname is 2.5--3.2-fold below \whatshap at every coverage (results.tex four-class paragraph).
