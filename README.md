# LongPhase 2 — manuscript

Germline haplotype phasing from long reads. Co-phases SNVs, small indels, SVs and
5mC in a single weighted phasing graph, and scores the reliability of every phased
variant with a GNN that unphases (never flips) variants predicted to be misphased.

## Layout

```
main.tex                  # skeleton, macros (\toolname, \todo), Fig. 1
sections/introduction.tex
sections/results.tex
sections/methods.tex
sections/discussion.tex
references.bib
Supplementary.tex         # Supplementary Methods, Notes, Tables 1-6, Figs. 1-9 (separate PDF)
figures/                  # fig1_overview.svg/.pdf (generated), fig2-6_*.png, supp/
figures-source/           # make_fig1.py (Fig. 1 vector source); concept drafts
Makefile                  # `make`, `make wordcount`, `make clean`; rebuilds Fig. 1 from its source
```

Build: `make` (latexmk + `naturemag.bst`, both in TeX Live 2025; `rsvg-convert` for the SVG figures).

Figure 1 is generated entirely by `figures-source/make_fig1.py` (all four panels, house
style of the original vector master), redrawn on 2026-09-18 to the new design: single-row
legend and six panel-filling reads (a); original graph with long-range read arcs,
calibration insets, reweighted graph with low-confidence and faded edges (b);
feature-labelled window → local message passing (GATv2 star) + global self-attention
(Transformer token row) → feature fusion with input skip → feed-forward network with skip,
framed as repeated layers → phase-confidence refinement; layer norm and classifier head
left to the caption and Supplementary Fig. 6 (c); haplotypes with SV, indel and
CpG alleles plus haplotagged reads (d). Edit the script, not the SVG.

## Before submission

Red `\todo{}` marks flag everything still unverified — 74 as of the 2026-09-20
proofreading pass (main text 20, Methods 35, Supplementary 19). The critical ones:

1. **Training description is absent.** No training code exists in the LongPhase
   repository on any branch; `prepare_gnn_data.py` and `embed_weights.py` are
   referenced only in code comments. The Methods scaffold lists every field needed.
2. **`gnn` and `compare` exist only on branch JH** (tip `cc17fb1`, 2026-08-25, the
   latest source; re-checked after `git fetch` on 2026-09-18). Tag v2.0.2 on `main`
   cannot reproduce any result in this paper. Merge and tag before submission.
3. **Everything is HG002, one chemistry**, and the GNN was trained on it. No second
   individual, no PacBio HiFi, no downstream demonstration (the ClairS purity-sweep
   experiment in the algorithm slides is the natural candidate; see the Results todo).
4. **Text↔code discrepancies** are flagged inline in `methods.tex` with file:line.
   The six Supplementary matching errors were fixed on 2026-09-18 (Table 1 log bases and
   feature order, Table 3 node cap, Table 4 `--svWindow`/`--svThreshold` and `--ont`,
   Table 5 caption, Fig. S1b/S6c legends). One earlier flag was itself wrong and has been
   removed: the homopolymer SNV filter *is* gated on `--ont` (`PhasingProcess.cpp:122`).
5. **Speed claim** is now stated consistently as six- to eightfold at 60× (5–8× across
   30–60×) in abstract, introduction and results; still to be confirmed from the TSVs.
6. **Novelty claim on phase confidence** was corrected: HapCUT2 already emits per-variant
   Phred-scaled switch/mismatch confidences and prunes below a threshold by default. The
   manuscript now positions the GNN against that precedent (Introduction, Discussion) and
   asks for a matched comparison against HapCUT2 pruning (Results todo). State in Methods
   whether HapCUT2's default pruning was enabled in the benchmark runs.
7. **Supplementary figures consolidated on 2026-09-19** (12 → 9): S1 now holds all pre-graph
   filters including the copy-number filter (e–f, rule table replaced by a state diagram);
   S2 is the six-panel voting figure (pair support, vote rule, votes, single-read guard,
   entropy, blocks); S5 holds window construction, DOT export and the phase-set update (e–f).
   Node glyphs and haplotype colours now match Fig. 1 throughout. Order: 1 filters, 2 voting,
   3 read-based correction, 4 GNN overview, 5 window+update, 6 architecture, 7 modcall,
   8 metrics, 9 calibration (placeholder). All cross-references updated.
8. **Source fix to file** (`PhasingGraph.cpp:253–266` at cc17fb1): the `else if` that
   assigns vote weight 20 chains off `if(debug)` instead of the edge-threshold test.
   Harmless in release (`debug` is hard-coded false at the only call site, :404) but a
   latent behaviour change; re-attach it. `findBestEdgePair` also takes an unused `isONT`.
   Two text errors traced to the same file were corrected on 2026-09-19: `--distance` is a
   gap test that skips a variant (:350), not a 300 kb cap on edges or votes, and the
   weight-20 upgrade also fires irrespective of s when one pairing has < 1 unit of support.
9. **Main Figs. 2–6 are raster exports** (PNG from the pptx) with in-figure titles,
   uppercase panel letters and, in Fig. 6, a caption paragraph inside the artwork.
   Regenerate them as vector figures from the `longphase compare` TSVs: lowercase bold
   panel letters, no titles or "(↑ better)" annotations, s.d. bands for 10–20×.

Figure numbers currently come from `LongPhaseGNN_0902_2-1.pptx` (slides 7–11) and are
approximate to plot resolution; replace with exact values from the `longphase compare`
TSVs.

## References

Citation sources: Europe PMC (80 citing articles) and OpenAlex (96 citing works) for
`10.1093/bioinformatics/btac058`, queried 2026-09-18. Ten references added in the
2026-09-18 revision (all resolved through Crossref): the T2T-HG002/Q100 benchmark paper
(Hansen et al., *Cell* 2026), GIAB stratifications (Dwarshuis 2024), benchmarking in the
complete-genome era (Olson 2023), T2T-CHM13 variant analysis (Aganezov 2022), CMRG
benchmark (Wagner 2022), SHAPEIT5 (Hofmeister 2023), methylation-based parent-of-origin
haplotyping (Akbari 2023), long-read 5mC caller comparison (Sigurpalsdottir 2024), and two
clinical long-read references (Eisfeldt 2025; Negi 2025). Three entries with raw HTML in
their titles (`<scp>`, `<i>`) and two malformed author lists were repaired; they printed
verbatim in the compiled bibliography.
