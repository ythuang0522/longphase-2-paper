# Fig. 1a,b,d: shared eight columns, stage labels removed, inset titles renamed, 2026-10-27 (author decisions)

The author found the stage-label column of panel b ("Original graph -> Evidence weighting -> Reweighted graph") ugly and space-inefficient, and panels a and b disconnected. After several rounds of drafts (rejected: reads and graph on one shared axis, read threads, arc graph, inset cards), the author chose to keep the panel b design, remove the stage column, widen panel a and give both panels the same eight variants. Panel d was left for later and still shows the seven columns of the earlier panel a.

| Old | New |
|---|---|
| a|b separator at x 498; stage labels and block arrows in b | Separator at x 632; no stage labels |
| a: seven columns (SNV, SNV, SV, CpG, SNV, indel, SNV), 48 px pitch | a and b: eight columns SNV A/G, SNV T/C, indel A/CA, CpG, SNV G/A, SNV A/T, SV, SNV C/T; a at 62 px pitch |
| b first column A/G; no SV in b | b keeps A/G; SV at column 7 (author: SV and CpG swapped) |
| No node for the SV reference allele | Non-SV allele = SV box with a dash (option 1 of 4), in the reads of a and both graphs of b |
| CNV region in b over three SNVs (T/C, G/A, A/T) | Over two SNVs (G/A filtered, A/T kept) |
| a: no CNV evidence | a: reads 7 and 8 (grey) span the two CNV SNVs, clipped at both ends (orange zigzags), alternate allele at both; the CNV is not named in a (author) |
| Inset titles: Uncertain base call / Sequence-context reliability / Miscalled SNVs in CNV | Base-quality weighting / Tandem-repeat weighting / Copy-number filtering (set A, terms of the Results) |
| CNV inset: generic reads T-(x)-A | Reads 1, 2 and 7 of a at G/A and A/T, with a "Call" row: G/A filtered, A/T kept (option 1); no MR value, because with two SNVs the formula would also remove A/T |
| a legend items packed left | Legend items spread over the panel width |
| Inset cards | Not used: they weaken the yellow highlights and cover the long-range read arcs |

Caption, panel a: added "a dash marks the reference allele of the SV, and grey reads are clipped at both ends (orange)". Panel b: "Weighted phasing graph before (top) and after (bottom) evidence weighting. Read-supported edges link allele nodes; observations at low-quality bases and indels in tandem repeats are down-weighted, and a variant whose alternate allele comes from clipped reads in a copy-number-altered region is filtered (insets)." (was: "...weighted by base quality and sequence context; the inset shows an indel down-weighted inside a tandem repeat.").

Panel d, same day (author request): eight columns of a and b; haplotypes carry the dashed non-SV node, the G/A SNV as a cross (faded cross in the reads) and the C/T SNV faded (unphased in c). To fit eight columns (56 px pitch), the haplotype labels moved above their tracks; read labels stay on the left.

| Old | New |
|---|---|
| d: seven columns (SNV, SNV, SV, CpG, unphased SNV, indel, SNV); labels left of tracks | Eight columns as in a and b; haplotype labels above tracks |
| Caption d: "...with the selected variant left unphased (faded), and haplotagged reads." | "...with the filtered variant crossed and the selected variant left unphased (faded), and haplotagged reads." |

Panel d, same day (author decision): the filtered G/A cross on the haplotypes is faded like the unphased C/T SNV, because the copy-number filter removes the variant's observations from all reads before graph construction (`applyCnvFilter` -> `filterHighMismatchVariants`, PhasingGraph.cpp), so the variant is unphased in the output; the cross shape is kept to show why. Not traced: whether the VCF writer outputs it as an unphased heterozygous call.

| Old | New |
|---|---|
| d haplotypes: dark cross at G/A | Faded cross (as in the reads) |
| Caption d: "...with the filtered variant crossed and the selected variant left unphased (faded)..." | "...with the filtered variant (cross) and the selected variant left unphased (faded)..." |
