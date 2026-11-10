# Retain Fig. 5h with a concise subset comparison

Following the author's revised decision, retained Fig. 5h and all figure files. Removed the repeated subset count (61,389–64,201) and benchmark-absence fraction (84.0–93.6%) from Results. The corresponding data remain in Supplementary Fig. 6c. Replaced the long assembly paragraph with the outside-alignment comparison (88.6% versus 7.4%), retaining Fig. 5h and Supplementary Table 10. Removed the odds ratio and chromosome/satellite detail from the main narrative; these remain in the supplementary material.

The Results comparison avoids the module name but explicitly says “a subset of unphased SNVs”. Methods and the Fig. 5h legend retain the scope definition. The introductory sentence now says “some calls” rather than generalizing the assembly result to all unphased calls. The background is described as initially phased SNVs. No claim that most unphased calls arise from GNN correction was introduced. No panels were moved or renumbered.

Validation: rebuilt main.pdf, checked the revised text and retained Fig. 5h, and scanned compile warnings.

## Removed main-text passage

```tex
A subset of the unphased calls, 61,389--64,201 SNVs per genome at 10--60$\times$, was left unphased because the phase assignment was highly uncertain; 84.0--93.6\% of these SNVs were absent by position from the v5.0q benchmark (Supplementary Fig.~6c). In an exploratory comparison with the T2T-HG002 assembly at 60$\times$, 11.4\% of this subset lay in regions where both haplotypes aligned one-to-one to GRCh38, compared with 92.6\% of a random sample of phased SNVs (odds ratio for lying outside these regions, 98; Fig.~\ref{fig:unphased}h); this enrichment outside one-to-one alignments was present on every autosome, with clusters in pericentromeric satellites (Supplementary Fig.~6d and Supplementary Table~10). The comparison identifies genomic context but does not independently validate phase or allele identity, because v5.0q derives from the same assembly. 
```
