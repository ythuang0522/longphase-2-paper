# Results: modcall sentence in the first subsection rewritten (option A), 2026-10-27 (author decision)

The author asked for a more concise sentence for the `modcall` module in the first Results subsection and chose option A of three.

| Old | New |
|---|---|
| Allele-specific 5mC sites are called from the same reads by the \texttt{modcall} module: a CpG qualifies when its methylated and unmethylated reads are balanced and its methylation state co-segregates with a neighbouring heterozygous marker (Methods). | The \texttt{modcall} module calls allele-specific 5mC sites from the same reads, keeping CpGs whose methylated and unmethylated reads are balanced and whose methylation co-segregates with a neighbouring heterozygous marker (Methods). |

Content unchanged; both criteria match Methods Eqs. (hetmeth) and (linkmeth).

Second change, same day (author: "don't write this 35 in the results ... just overview"): the window size moved out of the Results overview; it stays in Methods (graph construction).

| Old | New |
|---|---|
| ..., and each read links every allele it carries to the next 35 variants it observes. | ..., and each read links the alleles it carries. |

Third change, same day (author's wording): the source of the input calls is named.

| Old | New |
|---|---|
| SNVs, small indels and SVs come from the input calls. | SNVs, small indels and SVs come from upstream variant callers (e.g., Clair3, DeepVariant and Sniffles2), each cited. |

Fourth change, same day (author: "votes are difficult to understand"; option B of three; author also noted that the graph sentence did not cite Fig. 1b).

| Old | New |
|---|---|
| ..., and each read links the alleles it carries. Methylation therefore votes on the same haplotypes as the sequence alleles of the same reads, instead of joining blocks after the sequence phase is fixed. SVs vote within blocks but are never the only link between two blocks. | ..., and each read links the alleles it carries (Fig. 1b). Methylation is therefore phased together with the sequence alleles of the same reads, instead of being used afterwards to join blocks whose sequence phase is already fixed. SVs inform phasing within blocks but never connect two blocks on their own. |

Fifth change, same day (author): "vote" removed before its definition in the next paragraph.

| Old | New |
|---|---|
| ..., and votes cast by indels in tandem repeats are down-weighted tenfold, ... | ..., and observations of indels in tandem repeats are down-weighted tenfold, ... |

Sixth change, same day (author, option H3): the homopolymer-filter sentence removed from the Results overview; the rule stays in Methods (line 31) and Fig. 1b does not show it.

| Old | New |
|---|---|
| On nanopore data, closely spaced SNVs in homopolymers are removed. | (deleted) |

Seventh change, same day (author, option A: "this is an overview not methods. these cutoffs should be never mentioned"): the cutoffs stay in Methods (line 39).

| Old | New |
|---|---|
| Observations at bases of quality below 12 receive one-tenth of the full weight, and observations of indels in tandem repeats are down-weighted tenfold, because a misplaced repeat indel can link the wrong alleles. | Observations at low-quality bases and indels in tandem repeats are down-weighted, because both can link the wrong alleles. |

Eighth change, same day (author: rewrite the GNN paragraph "in a more concise and high level way"; version 1 without the training sentence, last sentence shortened). Window size, chromosome split, node features, block splitting and the training data stay in Methods.

| Old | New |
|---|---|
| \toolname then scores the uncertainty of every phase assignment and examines the least certain ones (Fig.~\ref{fig:overview}c). Phasing entropy, computed from the haplotype votes that a variant receives, ranges from 0 bits for unanimous support to 1 bit for an even split. Around every variant with high entropy, a graph neural network (GNN) examines a window of up to 41 neighbouring variants. Each allele node carries features of phasing evidence, local sequence context and graph structure, and each layer of the network combines attention along the voting edges of the phasing graph with self-attention across the window. The GNN predicts phase-disagreement onsets: isolated variants whose phase disagrees with that of their neighbours, and the first variant of each run of such disagreements. It was trained on HG002 nanopore data with labels from the T2T-HG002-derived benchmark, with chromosomes 17, 21 and 22 excluded from training and model selection (Methods). Predicted variants are unphased, not flipped, and keep their genotypes; if unphasing disconnects a block, its parts become separate phase sets. An incorrect prediction therefore removes a correct phase assignment but does not add a switch error. | \toolname then scores the uncertainty of every phase assignment and re-examines the least certain ones (Fig.~\ref{fig:overview}c). Uncertainty is measured as phasing entropy, from 0 bits when all haplotype support agrees to 1 bit for an even split. Around each high-entropy variant, a graph neural network (GNN) reads the local phasing graph, combining message passing along its edges with self-attention across the window, and predicts where the phase starts to disagree with that of the neighbouring variants. Predicted variants are unphased rather than flipped, so an incorrect prediction cannot add a switch error. |

Ninth change, same day (author): the outputs paragraph of the first Results subsection removed. Its citations (zheng2022clair3, zheng2026clairs, ont2025wfhuman) are still cited elsewhere. Fig. 1d is no longer cited in the text.

| Old | New |
|---|---|
| The outputs are a phased VCF for each variant class, which records the phase set, phasing entropy and haplotype support of each variant, and alignments haplotagged from all four classes (Fig.~\ref{fig:overview}d). \toolname retains the command-line interface and output formats of \longphase, which variant-calling pipelines already run\cite{zheng2022clair3,zheng2026clairs,ont2025wfhuman}. | (deleted) |

Tenth change, same day (author): Fig. 1d cited again, after the outputs paragraph was removed.

| Old | New |
|---|---|
| Predicted variants are unphased rather than flipped, so an incorrect prediction cannot add a switch error. | Predicted variants are unphased rather than flipped (Fig. 1d), so an incorrect prediction cannot add a switch error. |

Eleventh change, same day (author, option P2): the evaluation-setup paragraph shortened to the data, the two truth sets and the reporting default, and moved from the end of the first Results subsection to the start of the second. Replicate design, the use of full truth VCFs, the SV truth set and the Supplementary pointer are in Methods (lines 94-98, 107, 121); every one of Supplementary Tables 6-17 is still cited elsewhere in the main text.

| Old (end of subsection 1) | New (start of subsection 2) |
|---|---|
| We evaluated \toolname on HG002 nanopore R10.4.1 reads at 10--60$\times$ and PacBio HiFi reads from the same individual at 10--50$\times$ (Methods). Nanopore data comprised ten down-sampling replicates per coverage at 10--20$\times$ in 2$\times$ steps, and one each at 30, 40, 50 and 60$\times$; HiFi and unphased-variant analyses used one replicate per coverage. All phasers received the same alignments and variant calls. We scored phase against two HG002 truth sets: GIAB v4.2.1, integrated from mapping-based call sets, and GIAB v5.0q, phased by the diploid telomere-to-telomere (T2T) assembly. Both truth sets were used in full, including variants outside their benchmark regions. SV phase was scored against the variants of the T2T-HG002 assembly, which resolves both alleles of every SV (Methods). Unless stated otherwise, results refer to SNV phasing against v5.0q and include GNN correction. Per-run values and summaries are in Supplementary Data~1 and Supplementary Tables~6--17. | We evaluated \toolname on HG002 nanopore R10.4.1 reads at 10--60x and PacBio HiFi reads at 10--50x, with the same alignments and variant calls for every phaser (Methods). Phase was scored against two HG002 truth sets: GIAB v4.2.1, integrated from mapping-based call sets, and GIAB v5.0q, phased by the diploid telomere-to-telomere (T2T) assembly. Unless stated otherwise, results refer to SNV phasing against v5.0q and include GNN correction. |
