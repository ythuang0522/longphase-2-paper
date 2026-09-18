# LongPhase 2 — manuscript (Nature Methods)

Germline haplotype phasing from long reads. Co-phases SNVs, small indels, SVs and
5mC in a single weighted phasing graph, and attaches a per-variant phasing entropy
plus an optional GNN that unphases (never flips) variants predicted to be misphased.

Companion manuscripts, both unpublished and both built on the **LongPhase v1.0**
graph (not on LongPhase 2):

| | scope | status |
|---|---|---|
| LongPhase-S  | paired tumour–normal somatic haplotyping, purity estimation | bioRxiv preprint, under review |
| LongPhase-TO | tumour-only somatic haplotype reconstruction | manuscript in review |

## Layout

```
main.tex                  # skeleton, macros (\toolname, \todo), Fig. 1
sections/introduction.tex
sections/results.tex
sections/methods.tex
sections/discussion.tex
references.bib
Supplementary.tex         # Supplementary Notes, Tables 1-8, Figs. 1-10 (separate PDF)
figures/                  # fig1_overview.pdf, fig2-6_*.png, supp/
figures-source/           # Fig. 1 masters (longphase_overview_nature.*) + concept drafts
Makefile                  # `make`, `make wordcount`, `make clean`
```

Build: `make` (latexmk + `naturemag.bst`, both in TeX Live 2025).

## Before submission

Red `\todo{}` marks flag everything still unverified — 74 of them as of the
2026-09-18 section review. The critical ones:

1. **Training description is absent.** No training code exists in the LongPhase
   repository on any branch; `prepare_gnn_data.py` and `embed_weights.py` are
   referenced only in code comments. The Methods scaffold lists every field needed.
2. **`gnn` and `compare` exist only on branch JH.** Tag v2.0.2 on `main` cannot
   reproduce any result in this paper.
3. **Everything is HG002, one chemistry**, and the GNN was trained on it. No second
   individual, no PacBio HiFi, no downstream demonstration.
4. **Nine text↔code discrepancies** are flagged inline in `methods.tex` with
   file:line; six matching errors remain to be fixed in `Supplementary.tex`.
5. **Speed claim differs** across abstract (6–8×), introduction (5–10×) and
   results (6–8×); reconcile against the runtime panel.

Figure numbers currently come from `LongPhaseGNN_0902_2-1.pptx` (slides 7–11) and are
approximate to plot resolution; replace with exact values from the `longphase compare`
TSVs.

Citation sources: Europe PMC (80 citing articles) and OpenAlex (96 citing works) for
`10.1093/bioinformatics/btac058`, queried 2026-09-18.
