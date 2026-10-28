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
figures/                  # fig1_overview.svg/.pdf, fig2-6_*.pdf (generated), supp/
figures-source/           # make_fig1.py (Fig. 1); make_results_figs.py + results_data.py (Figs. 2-5, Supp. Figs. 9-16, Supp. Tables 7-18)
Makefile                  # `make`, `make wordcount`, `make clean`; rebuilds Fig. 1 from its source
notes/log/                # dated change log, one file per change; index in notes/log/README.md
```

Build: `make` (latexmk + `naturemag.bst`, both in TeX Live 2025; `rsvg-convert` for the SVG figures).

Shared hub (compiled PDFs, page reader, figure gallery, open items):
https://claude.ai/artifact/339iTVSwod8JqKgQASYfZm — rebuilt by `python3 notes/hub/build_hub.py`
and republished to the same URL only on request (see `CLAUDE.md`).

Figure 1 is generated entirely by `figures-source/make_fig1.py` (all four panels, house
style of the original vector master), redrawn on 2026-09-18 to the new design: single-row
legend and six panel-filling reads (a); original graph with long-range read arcs,
calibration insets, reweighted graph with low-confidence and faded edges (b);
feature-labelled window → local message passing (GATv2 star) + global self-attention
(Transformer token row) → feature fusion with input skip → feed-forward network with skip,
framed as repeated layers → phase-confidence refinement; layer norm and classifier head
left to the caption and Supplementary Fig. 6 (c); haplotypes with SV, indel and
CpG alleles plus haplotagged reads (d). Edit the script, not the SVG.
Revised 2026-09-24 for Nature Methods print requirements: no text below 5 pt at 180 mm; SNV
terminology and indel-as-sequence-box glyph throughout; panel d is the phased result of the
panel a reads (same seven columns); phasing-entropy track with threshold added to c and a
the unphased SNV (faded) to d, whose uncertainty strip was later dropped as a repeat of c and its glyphs enlarged (2026-09-25); dashed low-confidence
edges and a down-weighted-allele legend in b; the block split when unphasing disconnects a phase set (`PhasingProcess.cpp:830` in v2.1; `GNNProcess.cpp:540` at `cc17fb1`) is
now stated only in Methods, the Fig. 1 legend having been cut to ~100 words (2026-09-24); panel a has a heading and tighter
reads, no panel carries a heading, the sequence-context inset is coloured by haplotype, and the compacted top half brings the
canvas to 1680×1046. Plain wording in the figure: "phasing uncertainty" for phasing entropy
(the caption names PE once and points to Methods), "haplotype block" / "block membership"
instead of phase set. Wording rule (author, 2026-09-24): headings and captions say "phasing
uncertainty" (entropy is only one measure of it); body text says "haplotype block" for phase set
and keeps "phasing entropy" only where a sentence is about the metric's value (Results, Fig. 6c).
Panel c shows the uncertainty bars with a y-axis label and no threshold line, and node (31) and
edge (6) feature-vector strips segmented by feature group (16/6/5/4 and 3/1/1/1, from
`PhasingProcess.cpp` nf[0..30] and ep[0..5] in v2.1 and the Methods grouping). Open polish: the PDF still embeds five Type 3 fonts (rsvg-convert output).

## Comparison with further phasers (2026-10-17)

Supplementary Data 1, sheet `Other_phasers` (71 runs); commands, inputs and full tables in
`notes/competitors/README.md`, scripts in `notes/competitors/scripts/`. In the manuscript since
2026-10-19 as Supplementary Table 18, one Results paragraph, Methods and one Discussion sentence (log
entries in `notes/log/`). HiPhase (SNV-only) is also in Figs. 2c,g and 5c,d, Supplementary Fig. 16c,
Supplementary Table 11 and the abstract; the HiFi runs with indels and nanopore HapCUT2 with indels are in
Fig. 2b,d,f,h and Supplementary Fig. 16d; HapBridge and LongHap (SNVs with 5mC, and LongHap on all
classes) are in Fig. 3 since 2026-10-20; TinkerHap is not in the figures.

**Tools added and why**

| Tool | Platform | Why it was added |
|---|---|---|
| LongHap 0.2.0 (bioRxiv 2026) | ONT 10–60× | Co-phases SNVs, indels and SVs with 5mC, the same claim as LongPhase 2; its preprint compares itself with LongPhase; cited in the Introduction. Run as SNVs + 5mC (vs LongPhase Mod and MethPhaser) and as all variant types + 5mC (vs LongPhase Indel+Mod+SV). |
| HapBridge | ONT 10–60× | Methylation post-processor of the MethPhaser kind (bridges blocks, corrects switches); MethPhaser is already compared; cited. |
| HiPhase 1.7.0 (PacBio) | HiFi 10–50× | Phaser of PacBio's human WGS pipeline, the default for HiFi users. |
| TinkerHap 1.0.0 (2025) | ONT 10–60×, HiFi 10–50× | Recently published read-based phaser benchmarked against WhatsHap and HapCUT2. |
| LongPhase, WhatsHap, HapCUT2 with indels | HapCUT2: both; LongPhase, WhatsHap: HiFi (ONT rows already existed) | HiPhase and TinkerHap phase indels by default, which lengthens blocks; comparing them with SNV-only runs would favour them. These runs complete the SNV + indel comparison on both platforms. |
| HiPhase, TinkerHap on SNVs only | HiFi 10–50× | Counterpart of the SNV-only rows (WhatsHap `--only-snvs`). Neither tool has an SNV-only option, so both read an SNV-only input VCF (the PEPPER calls restricted to SNVs). |

All replicate 1, the paper's inputs, default parameters or the workflow each tool documents (no
tuning), scored as `SNV_Detail` (`longphase compare`, v5.0q chr1–22, SNV switch error).

**Results** (SNV switch error % / Hamming % / block N50; 10×, 30×, 60× on ONT, 10×, 30×, 50× on HiFi)

| Comparison | LongPhase 2.1.1 | Others |
|---|---|---|
| ONT, SNV + 5mC | 0.083 / 5.4 / 0.88 Mb; 0.030 / 2.1 / 2.08 Mb; 0.022 / 1.6 / 3.09 Mb | MethPhaser 0.124, 0.052, 0.035; HapBridge 0.122, 0.046, 0.033; LongHap 0.180, 0.158, 0.110 (Hamming 18–20% from 20×) |
| ONT, SNV + indel | 0.091, 0.037, 0.027 | WhatsHap 0.270, 0.137, 0.097; HapCUT2 0.315, 0.177, 0.126; TinkerHap 0.332, 0.197, 0.151 |
| ONT, all variants + 5mC | 0.092, 0.038, 0.026 (N50 1.02, 2.65, 4.14 Mb) | LongHap 0.219, 0.166, 0.114 (Hamming 6–22%, N50 0.47, 4.52, 6.83 Mb) |
| HiFi, SNV only | 0.049, 0.038, 0.033 | HiPhase 0.085, 0.068, 0.057; WhatsHap 0.128, 0.106, 0.077; HapCUT2 0.152, 0.127, 0.096; TinkerHap 0.169, 0.130, 0.095 (HiPhase and TinkerHap on an SNV-only input VCF) |
| HiFi, SNV + indel | 0.094, 0.054, 0.041 (SNV only: 0.049, 0.038, 0.033) | HiPhase 0.164, 0.091, 0.070; WhatsHap 0.252, 0.144, 0.096; HapCUT2 0.272, 0.177, 0.131; TinkerHap 0.283, 0.181, 0.133 |

- LongPhase has the lowest SNV switch error in every comparison, platform and coverage, and the
  lowest Hamming distance except LongHap at 10× (which phases only 60% of SNVs there) and HiFi
  SNVs only at 20× (HiPhase, TinkerHap) and 50× (WhatsHap, HapCUT2), by at most 0.14 points.
- HiPhase is second on HiFi, at 1.7–1.9 times LongPhase's switch error with or without indels;
  WhatsHap, HapCUT2 and TinkerHap are at 2.3–3.2 times.
- The others' advantage is block length: MethPhaser, LongHap and HapBridge (60×) on ONT, HiPhase on
  HiFi (N50 11–17% above LongPhase with indels), bought with higher Hamming distance; WhatsHap,
  HapCUT2 and TinkerHap phase 1–9 percentage points more SNVs or indels (HiFi indels: HiPhase 5–8,
  HapCUT2 and TinkerHap 6–9 points more than LongPhase).
- On HiFi SNVs only the block advantage disappears: every tool's N50 is within 3% of LongPhase's
  (HiPhase within 1%). HiPhase and TinkerHap have no SNV-only option; these rows read an SNV-only
  input VCF (the PEPPER calls restricted to SNVs, the set WhatsHap `--only-snvs` phases).
- HapBridge corrected no switch error and left the 10× and 20× input unchanged.
- LongHap's ONT mode leaves alleles seen on one strand only unphased: 60% of SNVs phased at 10×.
- HiPhase on HiFi 50×: 12 min wall, 187 CPU-min with indels, 10 min and 173 CPU-min on SNVs only
  (LongPhase 2.4 and 14.3).
- Adding indels raises the SNV switch error of every tool (LongPhase HiFi 0.033 → 0.041% at 50×)
  and lengthens its blocks.

## Before submission

Red `\todo{}` marks are reserved for what blocks submission: 26 remain after the
2026-09-24 pass (main text 6, Methods 15, Supplementary 5), down from 65 on 2026-09-20.
What is left: the missing WhatsHap/HapCUT2/LongPhase 1.0 and runtime tables (the
largest block), the release and training-code deposition, the Fig. 6 definitions and
plotting script, the constant justifications and the Supplementary Fig. 9 decision, the
ten seed values, the chr1-22 derivation of the v5.0q VCF, source data, and one new flag
on the Clair3 model (`notes/log/2026-09-24-author-decisions-read-provenance.md`).

SV phasing accuracy: issue #10 data arrived 2026-10-26 (`notes/sv_phasing/`, release v2.1.2, 100 runs,
HiPhase on HiFi). Fig. 3a–c is drawn from it (option B, author decision 2026-10-26; the + indels input is Supplementary Fig. 17). Results, Discussion, Methods
and Supplementary Table 20 rewritten from it the same day. The abstract was rewritten as a whole the
same day (179 words).

LongPhase v2.1.2 (JH, 2026-10-26, merged with the local Fig. 3 work the same day; JH's notes in
`notes/log/2026-10-26-longphase-v2-1-2-rerun.md`): still open is the Results memory clause ("at the cost
of higher peak memory" no longer holds), marked `\todo{}`; the abstract speed claim is resolved (8.9-fold).

Runtime on an SSD (2026-10-28, `notes/log/2026-10-28-runtime-ssd.md`, `notes/runtime/runtime_ssd.tsv`, sheet
`Runtime` of `supplementary.xlsx`): all SNV-only runs re-timed with inputs and outputs on an SSD. To decide
(author): HDD or SSD times in Supplementary Fig. 10, Supplementary Table 16, Results, the abstract's 8.9-fold
(9.3–14.2-fold at 60× on the SSD) and the Methods sentence on the hard-disk drive.

Everything else was moved out of the rendered text into `%  [tag]` source comments
next to the paragraph it concerns (grep `^%  \[` in `sections/*.tex` and
`Supplementary.tex`):

- `[optional experiment]` — LongPhase 1.0 co-phasing comparison; accuracy of the
  indel/5mC phase itself; fixed-PE baseline and threshold sweeps; second
  individual, HiFi, runtime table, downstream demonstration.
- `[optional figure]` — MR(v) histogram and scanner interval counts (Supp. Fig. 1g);
  modcall real-data panels (Supp. Fig. 7).
- `[optional, cheap and recommended]` — re-score one coverage on chr17/21/22 with
  `longphase compare --regions`; no new phasing run needed.
- `[note on existing material]` — the ClairS purity-sweep and HG002 slides: usable
  design, numbers from a pre-release build, do not mix into this manuscript.
- `[code housekeeping, not blocking]` — haplotag PS boundary case and PQ documentation.
- `[submission checklist]` — Nature Portfolio Reporting Summary.
- `[editorial, optional]` — quoting LongPhase 1.0 in Fig. 3a,d.

The critical ones:

1. **Training chain is local only.** The complete chain (`prepare_gnn_data_10.py`,
   `train_gnn_29.py`, `export_onnx_2.py`, `embed_weights.py`, driver scripts,
   checkpoint, ONNX file, training log, `requirements.txt`) sits in `GNN source/`
   (gitignored) and nowhere in the LongPhase repository or any archive. Methods now
   describes training in full from those files; the scripts carry absolute paths
   (`/ssd/longphase_process/...`, `/disk/software/...`) and must be parameterized
   and deposited.
2. **(Resolved 2026-10-07.)** The source baseline is the official release v2.1 on `main`
   (`46ba470`), which contains all of branch JH. The results were produced at `cc17fb1`;
   v2.1 folds `gnn` into `phase` with byte-identical outputs (see `notes/log/2026-10-07-source-baseline-moved-release-v2-1.md`).
3. **Everything is HG002, one chemistry**, and the GNN was trained on it. No second
   individual, no PacBio HiFi, no downstream demonstration (the ClairS purity-sweep
   experiment in the algorithm slides is the natural candidate; see the Results todo).
4. **Text↔code discrepancies** are flagged inline in `methods.tex` with file:line.
   The six Supplementary matching errors were fixed on 2026-09-18 (Table 1 log bases and
   feature order, Table 3 node cap, Table 4 `--svWindow`/`--svThreshold` and `--ont`,
   Table 5 caption, Fig. S1b/S6c legends). One earlier flag was itself wrong and has been
   removed: the homopolymer SNV filter *is* gated on `--ont` (`PhasingProcess.cpp:161` in v2.1; `:122` at `cc17fb1`).
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
8. **Source fixes** (status at v2.1, 2026-10-07: (a) is **not** in v2.1; (b) **is** in v2.1):
   (a) `PhasingGraph.cpp:253–266` at cc17fb1, the `else if` that assigns vote
   weight 20 chained off `if(debug)` instead of the edge-threshold test, fixed 2026-09-20;
   **(update 2026-10-07)** this fix did not make it into the v2.1 release (v2.1
   `PhasingGraph.cpp:229` still has `else if`). It was committed on JH as `e5963b0`
   (PR twolinin/longphase#131 → develop) and will ship in LongPhase v2.1.1 or later. Results are
   unaffected: the only caller passes `debug=false`, and the HG002 10× replicate-1 output is
   identical with and without the fix;
   (b) `GNNModel.h` lines 6, 43 and 60 described the edge tensor and encoder as 7-wide
   (`[N, N, 7]`, `[7,128]`) although `kEdgeFeat` is 6, comment corrected 2026-09-20.
   `findBestEdgePair` still takes an unused `isONT`.
   Two text errors traced to the same file were corrected on 2026-09-19: `--distance` is a
   gap test that skips a variant (:350), not a 300 kb cap on edges or votes, and the
   weight-20 upgrade also fires irrespective of s when one pairing has < 1 unit of support.
9. **(Resolved 2026-10-05 — see `notes/log/2026-10-05-results-redesign-jhls-new-data.md`.)** Main Figs. 2–6 were raster exports (PNG from the pptx) with in-figure titles,
   uppercase panel letters and, in Fig. 6, a caption paragraph inside the artwork.
   Regenerate them as vector figures from the `longphase compare` TSVs: lowercase bold
   panel letters, no titles or "(↑ better)" annotations, s.d. bands for 10–20×.

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
