# Methods condensation and prior-art wording, 2026-10-06 (author request)

**Methods condensation and prior-art wording, 2026-10-06 (author request).**
The abstract and Introduction now acknowledge quality-weighted and probabilistic phasing,
including WhatsHap's weighted objective and HapCUT2's quality-aware likelihood and confidence
pruning. The contribution is framed around joint evidence integration, genomic context and
learned phase-error detection; the uniform-weighting and categorical confidence claims were removed.
Methods now follows the scientific workflow rather than command boundaries. Its prose was
reduced from 6,239 to 2,592 words (TeXcount, excluding source comments, TODO text and headings),
a 58% reduction. Core equations, decision thresholds, train/validation/test chromosomes,
replicate design and metric definitions remain in the main text.
Supplementary Methods retain the detailed input eligibility, 5mC/5hmC interpretation, graph
features, architecture, training configuration and phase-set update. The software's integration
of GNN correction into phasing does not change this conceptual description.
The historical weight-20 source-release reminder remains tracked in this README rather than
in the manuscript. No result tables, measurements or figure artwork were changed. Both PDFs
were rebuilt successfully with TeX Live; the changed Abstract/Introduction, Methods and
supplementary pages were rendered and checked. There are no undefined references/citations,
missing characters or new overfull-box warnings. The main PDF is now 22 pages; Supplementary
Information is 36 pages. The existing title/affiliation overfull box and Supplementary Table 4
float-size warning are unchanged.
