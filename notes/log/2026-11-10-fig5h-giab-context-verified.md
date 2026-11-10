# Fig. 5h interpretation checked against the GIAB preprint

Reread the relevant full-text Results, Discussion, and Methods of Olson et al., “The Genome In A Bottle HG002 assembly-based variant benchmark set enables comprehensive benchmarking of small and structural variants”, bioRxiv 10.64898/2026.09.23.752440v1 (posted 2026-10-01), on 2026-11-10. Direct page retrieval returned HTTP 403; the web search tool returned indexed full-text passages, including the relevant Methods and Discussion sections.

Source: https://www.biorxiv.org/content/10.64898/2026.09.23.752440v1.full

Relevant evidence, paraphrased:
- Methods, V5.0q Benchmark Set Generation: initial diploid regions require a one-to-one alignment of each assembled haplotype to the reference. Additional exclusions cover gaps, large repeats with alignment breaks, structural variants, and other assembly/variant-calling issues.
- Discussion: large structural or copy-number differences between HG002 haplotypes and the reference impede variant benchmarking; direct genome comparisons can extend evaluation into excluded regions but remain challenging.
- Results, Benchmark content and genome coverage: the chromosome 8 inversion illustrates an HG002–GRCh38 structural difference affecting assessed regions. Gene-family examples also illustrate mapping complexity. These examples were not added to our Results because our loci have not been individually validated.

Revised the main-text Fig. 5h interpretation to briefly connect the observed alignment distribution with these assessment limitations. Kept “a subset”, “exploratory”, and an explicit statement that alignment status alone does not establish call or phasing errors. The preprint supplies context; the 88.6%/7.4% comparison is our data, not a result attributed to Olson et al. Did not claim that all non-one-to-one regions are structural variants, or that most unphased calls originate from any particular module. Fig. 5h remains in the main article, and the repetitive subset count/absence sentence remains removed.

Validation: rebuilt main.pdf and inspected the revised paragraph; no figures or numerical data changed.
