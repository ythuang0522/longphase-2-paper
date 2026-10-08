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
figures-source/           # make_fig1.py (Fig. 1); make_results_figs.py + results_data.py (Figs. 2-6, Supp. Figs. 10-14, Supp. Tables 7-12)
Makefile                  # `make`, `make wordcount`, `make clean`; rebuilds Fig. 1 from its source
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

## Before submission

Red `\todo{}` marks are reserved for what blocks submission: 26 remain after the
2026-09-24 pass (main text 6, Methods 15, Supplementary 5), down from 65 on 2026-09-20.
What is left: the missing WhatsHap/HapCUT2/LongPhase 1.0 and runtime tables (the
largest block), the release and training-code deposition, the Fig. 6 definitions and
plotting script, the constant justifications and the Supplementary Fig. 9 decision, the
ten seed values, the chr1-22 derivation of the v5.0q VCF, source data, and one new flag
on the Clair3 model (below).

Everything else was moved out of the rendered text into `%  [tag]` source comments
next to the paragraph it concerns (grep `^%  \[` in `sections/*.tex` and
`Supplementary.tex`):

- `[optional experiment]` — LongPhase 1.0 co-phasing comparison; accuracy of the
  indel/SV/5mC phase itself; fixed-PE baseline and threshold sweeps; second
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

The 2026-09-20 review resolved every mark that could be settled by tracing the
source (`../longphase` at cc17fb1 plus the working-tree fixes, and the training
chain in `GNN source/`): the copy-number mismatch load, the vote-less `PE = 0` case
(block starts only), the indel phased-fraction denominator and `compare`'s
exact-allele matching rule, the central-zone rule of the GNN, thread-count
independence of `phase` (by construction, not by experiment), the unsupervised
status of SV/5mC corrections, Sniffles2 2.8.0 (from the VCF header of the 10x
replicate-1 SV calls shipped as `demo/demo_sv.vcf.gz`), the reference and v5.0q
file names, and replicate s.d. for the LongPhase 2 values quoted at 10x. Two new
flags came out of it: the repository README times `phase` (v2.0, 24 threads) at
39–180 s, five times faster than Fig. 2e, and `demo/demo_snv.vcf.gz` carries
PEPPER-Margin-DeepVariant headers, not Clair3 headers.

On 2026-09-21 the replicate count was settled: all four `longphase compare` tables
hold nine replicates at 10x (seeds 1-9; 12-20x hold ten, 30-60x one), so the text now
states n = 9 at 10x in Results, in the Methods statistics paragraph and in the Fig. 2
legend that Figs. 3-5 inherit; the `\todo` asking for it is retired. One new flag
replaced it: the training driver skips any replicate whose phased VCF is missing
(`run_edge6_retrain.sh`:96), so if the 10x seed-10 phasing run never existed, the
training set came from 59 runs and not the 60 claimed in Methods and Supplementary
Table 3. The training log records only window counts, so this cannot be settled from
the local files.

Also on 2026-09-21, the file-identity half of the metadata todos was settled from
primary sources (every URL checked, HTTP 200) and written into Methods and Data
availability: the GIAB v4.2.1 benchmark VCF and BED names with their FTP release
directory; the NCBI download path of the GRCh38 no-alt analysis set; and the v5.0q
source distribution. The last was pinned from the repo's own
`demo/demo_bench.vcf.gz`, whose bcftools 1.17+htslib-1.21 header commands are dated
Fri Jan 17 2025 over `GRCh38_HG002-T2TQ100v1.1-dipz2k` — an exact match for the GIAB
release `NIST_HG002_DraftBenchmark_defrabbV0.020-20250117`
(`GRCh38_HG2-T2TQ100-V1.1_smvar.vcf.gz`).

**Versions were then set from that window** (2026-09-21, at the authors'
instruction), each carrying a `\todo{}` that marks it as inferred rather than
recorded: **minimap2 2.30**, **samtools 1.23.1**, **Clair3 v2.0.1** with model
`r1041_e82_400bps_sup_v500`. The rule was to take the release current when the
window opened, because alignment and down-sampling necessarily precede the SV calls
that date the window, and minimap2 2.31 (2026-05-19) and samtools 1.24 (2026-07-09)
both landed after it. Clair3 v2.0.1 against v2.0.2 (2026-06-25) is a genuine coin
flip. Do not substitute current releases: the run predates several of them.

**LongPhase 1.0 is now exact and is not an inference**: `git tag` in `../longphase`
has a single 1.0 tag, `v1.0` (`fe8c1fd`, 2022-03-09), so the old "1.0.x" was simply
wrong. Fixed in Methods and Supplementary Table 5; that closes both marks.

**2026-09-24, author decisions and read provenance.** The authors confirmed minimap2
2.30, samtools 1.23.1 and Clair3 v2.0.1 with `r1041_e82_400bps_sup_v500` (inferred
marks removed), 60 training runs, and that the v4.2.1 benchmark BED was applied
(chr1-22); the Zenodo data deposition is dropped at their request, and the code
availability todos no longer ask for Zenodo DOIs.

The previous LongPhase papers do not describe these reads: LongPhase 1.0 (2022) used
the 2019 UCSC ultra-long PromethION HG002 data (R9.4.1), and LongPhase-S and
LongPhase-TO use cancer cell lines only. The provenance was recovered instead from
the reads of `demo/demo.bam` in the source repository, whose basecaller tags name
flow cells PAG65784 and PAG68757, 4 kHz sampling, November 2022 start times and 5mC/5hmC
calls. Those are the two HG002 flow cells of ONT's open-data release
`giab_lsk114_2022.12` (FLO-PRO114M, SQK-LSK114, 400 bps). ONT's workflow report for its
`hg002_sup_v4` output basecalls with Dorado `dna_r10.4.1_e8.2_400bps_sup@v4.0.0` +
`5mCG_5hmCG@v2`, and 12 of 12 demo read IDs match that output with identical read
lengths. Read N50 29.2/29.4 kb (MinKNOW run reports); mean autosomal depth 70.4x (ONT's
released mosdepth distribution); licence CC BY-NC 4.0. All of it is now in Methods,
Data availability and Supplementary Table 5.

**New flag:** the confirmed Clair3 model `r1041_e82_400bps_sup_v500` is trained on
5 kHz Dorado v5.0.0 SUP data, but these reads are a 4 kHz `sup@v4.0.0` basecall. The
matched model is `r1041_e82_400bps_sup_v400` (Rerio), or `sup_v410` among those bundled
with Clair3. The earlier `sup_v500` inference rested on the wrong (2025.01) read-source
hypothesis. Flagged inline in Methods.

The reasoning behind the window: nothing in `GNN source/`, this repo or
`../longphase` records the minimap2, samtools or Clair3 version. The dating
argument, kept as a `%  [note on versions]` comment above
Methods' "Benchmark data" paragraph: Sniffles 2.8.0 (from the demo SV VCF header)
was released 2026-05-07 and branch JH was last committed 2026-08-25, so the calling
runs fall in that window. That **excludes Clair3 v2.0.3** (released 2026-09-09);
the in-window candidates are v2.0.1 and v2.0.2. minimap2 2.30/2.31 and samtools
1.23.1/1.24 bracket similarly but only if alignment happened in the same window,
which is not established. Unconfirmed read-source candidate: the ONT GIAB 2025.01
open-data release (PromethION, SQK-LSK114, Dorado v0.8.2, model
`dna_r10.4.1_e8.2_400bps@v5.0.0`), which would imply the Clair3 model
`r1041_e82_400bps_sup_v500`.

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
   v2.1 folds `gnn` into `phase` with byte-identical outputs (see the 2026-10-07 entry).
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
9. **(Resolved 2026-10-05 — see the Results redesign entry below.)** Main Figs. 2–6 were raster exports (PNG from the pptx) with in-figure titles,
   uppercase panel letters and, in Fig. 6, a caption paragraph inside the artwork.
   Regenerate them as vector figures from the `longphase compare` TSVs: lowercase bold
   panel letters, no titles or "(↑ better)" annotations, s.d. bands for 10–20×.

**Methods review, 2026-09-24 (text-only fixes).** Fixed SV/indel/5mC observation
qualities stated as numbers (60; 30 for reference-allele SV reads, which still vote at
weight 1 under the default `--baseQuality 12`; `PhasingGraph.cpp:838–862`); modcall
stated to read only the 5mC (`m`) probability, so 5hmC counts as unmethylated
(`ModCallParsingBam.cpp:169`); the flip/unphase/break labels named in Methods;
cross-tool comparisons stated as SNV-only LongPhase 2 (WhatsHap/HapCUT2 *can* phase
indels); HapCUT2 pruning added to the command-line todo; the generalization
limitations moved from Methods ("Hold-out design") to the Discussion; asides cut and
procedural tense made past. Still open from that review, needing decisions or new
analysis (the v5.0q-without-BED item was a text error: per the authors, both truth
sets were scored within their benchmark BEDs; Methods corrected 2026-09-24): the
deployment threshold needed a separate selection rationale (resolved by the author on
2026-10-06: an end-to-end phasing cost trade-off, distinct from checkpoint criterion S); test
accuracy 0.941 is below the all-correct baseline 0.970; no statement that test
chromosomes were unused during architecture search; GNN applied outside its training
configuration (SNV-only, 30–60×); no dispersion at 30–60× (per-chromosome bootstrap
possible); SV/5mC phased-fraction denominator undefined (the truth sets carry no
SV/5mC). Author decisions, 2026-09-24, not to be re-raised: no Zenodo/DOI deposit
(the public repository is the only deposit for code, data and tables), and no
`longphase compare` vs `whatshap compare` validation in the paper.

**Introduction rewrite and Discussion alignment, 2026-09-24 (later pass).** Supersedes
the novelty and HiPhase statements in the entry below. LongHap (Pfennig & Akey, bioRxiv
2026; `pfennig2026longhap`) co-phases SNVs, indels and SVs and adds 5mC in a final
gap-bridging stage, so the four-class novelty sentence was removed from Introduction and
Discussion; both now contrast joint (LongPhase 2) with post-hoc use of methylation
(NanoMethPhase, MethPhaser, HapBridge, LongHap). WhatsHap is stated to co-phase small and
large indels (`martin2016whatshap`), and the HiPhase "HiFi-only joint indel+SV" claim is
gone. First limitation is now 5mC only; the indel-noise sentence was dropped. Third
limitation: LongPhase 1.x per-read `PQ`/`haplotag --log` support described (issues #19,
#28; not cited); GCphase (not learning-based) replaced by NeurHap (`xue2022neurhap`) in
Introduction and Discussion. Benchmark paragraph rewritten from Hansen 2026 and Wagner
2022 (v4.2.1 omits 12% of autosomes; phase on 74% of heterozygous variants, from
trio/WhatsHap agreement; 85→92% coverage exposed 8× more false negatives). Downstream
tools now cite both WhatsHap and LongPhase; the citing-study clause and the only
main-text pointer to Supplementary Table 6 were removed, so Table 6 is now unreferenced
from the main text (open). Final paragraph cut to the four answers to the limitations,
with no numbers and no Fig. 1 reference. Discussion: v4.2.1 exclusions/700 Mb moved to
the Introduction; added 5mC limitations (male LCL autosomes only, tissue dependence,
X inactivation) and the missing comparison with methylation-aware phasers. Word counts:
Introduction ~1,000, Discussion ~1,300.

**Introduction and abstract review, 2026-09-24.** Novelty claim kept as "no
*published* method places all four evidence classes in one model" (author decision,
not to be re-raised): the indel/5mC co-phasing in LongPhase releases 1.5–1.7 is
unpublished development of LongPhase 2 and is not cited separately. HiPhase is cited as
the only published joint indel+SV phaser (HiFi only). Headline numbers now match Results:
2.6–5-fold fewer switch errors (v5.0q,
with correction; 1.1–1.3-fold under v4.2.1), six- to eightfold faster *at 60×*, and
+40% block N50 for *corrected* co-phasing (75% was uncorrected, at a higher switch
error rate). "GNN scores every variant" corrected (entropy scores every variant; the
GNN scores windows around PE ≥ 0.8). HapCUT2 contrast softened to "not designed to";
"calibrates" → "weights". Abstract cut to under 150 words. Aligned in the same pass:
the Results SNV heading now says 2.6- to 5-fold; "calibrated" → "weighted" in Results
and the Fig. 1 caption; the Discussion's first paragraph states that no published method combines all four
classes and recasts the co-phasing contribution as "the extra evidence is not free"
(75% uncorrected, 40% corrected); "most read-based tools" report binary phase (HapCUT2
does not); the HapCUT2-pruning contrast is stated as an expectation, with an
`[optional experiment]` comment for the matched comparison. The co-phasing Results
heading ("up to 75% but raises the SNV switch error rate") was left as is: it
describes uncorrected co-phasing and is accurate.

**Competitor tables, 2026-09-24.** JHL pushed `20260924_v50q.txt`, `20260924_GIAB421.txt`
and `20260924_cophase_v50q.txt` (`longphase compare` output; WhatsHap 2.8 default and
`--only-snvs`, HapCUT2 1.3.4, and GNN-corrected LongPhase 2 SNV-only, +indel, +SV and
+indel+SV; ten replicates at 10–20×, seed 10 included). The SNV-only corrected LongPhase 2
rows are identical to `GNN source/sw_longphase_v2.0.2_SNVonly_GNN.log` plus the new 10×
seed-10 row; the four-class (with 5mC) configuration is not in the new tables. All WhatsHap
(`--only-snvs`) and HapCUT2 values in Results, Discussion, Introduction and abstract are now
exact, and fold-changes are recomputed from rates: with correction 2.9–3.7× vs WhatsHap and
3.3–4.8× vs HapCUT2 (v5.0q, 10–60×); 1.1–1.7× under v4.2.1 (1.1–1.3× at 30–60×); without
correction 1.9–2.5× and 2.2–3.3×. LongPhase 2 values stay on the n = 9 tables at 10× so
that corrected and uncorrected remain paired; WhatsHap/HapCUT2 are n = 10 (Methods, Fig. 2
legend updated). Still plot-read: LongPhase 1.0, uncorrected LongPhase 2 under v4.2.1,
runtimes. Unused so far: default WhatsHap phases indels (32.9–49.8% of benchmark indels vs
30.5–45.4% for LongPhase 2) at far higher SNV switch error and Hamming distance (9–13%),
which would support an indel co-phasing comparison.

**Discussion review for Nature Methods, 2026-09-26.** Every number re-derived from
`20260924_v50q.txt`, `20260924_GIAB421.txt` and `GNN source/sw_*.log`. Four factual errors
fixed: (1) "every tool accumulates more switch errors under the T2T-based benchmark" was
false: corrected LongPhase 2 makes *fewer* under v5.0q (1,820 → 1,518 at 10×; 1,676 → 496 at
60×) and WhatsHap is level at 60× (1,801 vs 1,785); the paragraph now separates the
competitors' rise from a ~1,600-error floor shared by all tools under v4.2.1 that is more
plausibly benchmark discordance (new `[optional experiment]`: intersect those switch
positions); spread restated in rates (1.2–1.3 → 4.3–4.8-fold, matching Results);
(2) corrected four-class co-phasing is more accurate than *uncorrected* SNV-only only
(0.027% vs 0.034%; corrected SNV-only 0.023%); (3) the denominator defence of the GNN was a
non sequitur and is replaced by its price (~2,400 benchmark hets unphased for 247 fewer
switches at 60×); (4) "86–96%" was quoted for 10× alone, and clustered/low-GQ sites are about
half, not "most", of benchmark-absent calls. Uncertainty claims narrowed: `gnn` writes no
error probability (only `phase` writes PE/H1/H2, `ParsingBam.cpp:226–228`) and no link
entropy exists, entropy = 0 for 22–43% of removed genuine hets (Fig. 6c), and calibration is
untested (Supp. Fig. 9 placeholder); the genotype-quality analogy now appears only as a
goal. Limitations added: genome-wide rates include training chromosomes, single replicate at
30–60×, indel/SV/5mC phase accuracy not assessed, unsupervised SV/5mC corrections, polyploidy.
Indel trade-off stated once. Discussion now ~1,400 words (texcount), from ~1,300.
**Still open:** Results heading "A telomere-to-telomere benchmark exposes switch errors hidden
by the GRCh38 truth set" holds for WhatsHap/HapCUT2 only; re-scoring chr17/21/22 is now the
most important cheap analysis, because the Discussion names the train/test overlap as a limitation.

**Results redesign from JHL's new data, 2026-10-05.** Inputs: JHL's seven commits of 26 Sep – 5 Oct
(`supplementary.xlsx`, HiFi/MethPhaser/Venn/composition JSX drafts, `run_t2t_validation.sh`,
`unphase_validation_*`). Changes:

- **Figures regenerated as vectors from exact data** by `figures-source/make_results_figs.py`
  (+ `results_data.py`): Fig. 2 SNV-only vs WhatsHap/HapCUT2 (runtime panel dropped — no exact
  source); Fig. 3 two benchmarks as grouped bars incl. WhatsHap with indels and LongPhase 2
  +indel/+indel+SV (LongPhase 1.0 and uncorrected v4.2.1 dropped — plot-read only); Fig. 4 merges
  old Figs. 4+5 (switch-rate vs N50 trade-off at 10×/60×, SNV vs four-class across coverage);
  **new Fig. 5 HiFi**; Fig. 6 composition (exact), T2T-assembly status, per-chromosome depletion,
  WhatsHap give-up comparison and cross-enrichment. Old PNGs removed; old Fig. 6 kept as Supp. Fig. 13.
- **New Supplementary items**: Figs. 10 (Margin/Ralphi/GCphase), 11 (MethPhaser), 12 (depth of
  give-up sets), 13 (old Fig. 6 raster), 14 (all co-phasing configurations); Tables 7 (call sets),
  8 (SNV-only, 7 tools), 9 (two benchmarks), 10 (co-phasing), 11 (HiFi), 12 (T2T classification);
  Supplementary Data 1 = `supplementary.xlsx`. Supp. Table 5 gained Margin/Ralphi/GCphase/
  MethPhaser/HiFi rows (versions todo).
- **Results rewritten** (7 subsections). All numbers exact; n = 10 at 10× for LongPhase 2 too (the
  xlsx has seed 10), so the abstract's 2.9 became 2.8-fold, correction is 31–33% (not 31–34%),
  N50 loss 2–5% from 30× (40× is 4.9%), WhatsHap phases 0.7–1.0 pp more. New findings: SV/5mC
  co-phasing costs no accuracy after correction (SNV+5mC 0.0227% = SNV-only, +8% N50); correction
  halves the indel cost; LongPhase 2 with indels beats WhatsHap with indels 3.0–3.7× (Hamming 3.5 vs
  9.3%); HiFi transfer without retraining (19–28% of switches removed; 2.5–3.5× fewer than WhatsHap);
  88% of GNN-removed SNVs lie outside the 1:1 T2T alignment (94× depletion), half the assessable rest
  are not variants; LongPhase/WhatsHap give-ups are each enriched up to 10× in the other's errors;
  Margin has fewer switches at 10× only by 3× shorter blocks. Methods gained "Analysis of unphased
  SNVs" and the HiFi/extra-tool runs; statistics paragraph now n = 10 throughout.
- **Discussion revised**: co-phasing paragraph (per-class costs; WhatsHap shows the same indel noise),
  benchmark inversion now WhatsHap(indels)/HapCUT2, network paragraph reinterpreted through the
  assembly analysis and the WhatsHap complementarity, HiFi transfer, Margin caveat; limitations
  updated (HiFi tested on one individual; MethPhaser compared). ~1,700 words (texcount), up from
  ~1,400; the Margin and Ralphi/NeurHap sentences are the cheapest cuts.

**New blocking flags from this data (all `\todo` in the text):**
1. ~~**Variant caller**~~ — resolved the same day (author): PEPPER-Margin-DeepVariant, see below.
2. **MethPhaser output equals its input** to every digit at all six coverages (= uncorrected
   SNV-only LongPhase 2, replicate 1). Probably the input VCF was scored or MethPhaser did not run.
3. **HiFi call sets are coverage-independent** (2,367,609–2,367,619 het SNVs at 10–50×): one call
   set reused, so the 87% phased fraction at 10× is not comparable with ONT; HiFi data source,
   caller and commands missing from Methods.
4. **Unphased-SNV total resolved (author, 2026-10-06): 56,076 at 60×.** The old composition
   total of 60,267 is superseded. Its three benchmark-classification counts still need replacement
   from the confirmed set; 549 sites inside the benchmark BED (413 variants), `compare`'s net loss
   of 2,055 phased benchmark SNVs and the old 2,411 heterozygotes have different eligibility rules.
5. **(Resolved 2026-10-07 — GCphase removed; see the entry below.)** GCphase Hamming 32–40% (near random).
6. Runtimes, SV/5mC phased fractions and Supp. Fig. 13 values still have no exact source; the
   WhatsHap-only median depth (18×) and zero-entropy share (57.6%) come only from a commit message.

Todo count after this pass: Results 10, Methods 20, Supplementary 18 (incl. generated tables).

**Caller, abstract and Results wording, 2026-10-05 (later pass, author request).**
- **Small-variant caller is PEPPER-Margin-DeepVariant** (`shafin2021margin`), not Clair3: changed in
  Methods (input paragraph, Benchmark data, comparison methods), Results, Supp. Table 5 and the
  generated Supp. Table 7 caption. Clair3 v2.0.1 and the `sup_v500` model todo are gone; a new todo
  asks for the PEPPER release, model preset and confirmation that its phased output was discarded.
  The Clair3 version-dating comments in Methods are kept as history, marked superseded. Clair3 is
  still cited where it is a downstream pipeline that embeds LongPhase (abstract, Discussion, Supp. Table 6).
- **Abstract** now reports HiFi (2.5–3.5-fold fewer switch errors than WhatsHap, network not
  retrained); opening sentence tightened to stay at 150 words (texcount).
- **Results wording review**: "correction" defined once and used for the step (the network only
  where the model itself is meant); "genuine heterozygotes" → "benchmark heterozygotes" (the
  composition counts benchmark-VCF records outside the BED), also in the Discussion and Supp. Fig. 13;
  "give-ups" removed; per-chromosome values described as ratios of the outside-alignment share, not
  "depletion"; odds ratio stated as such; GCphase "order of magnitude" → "four to seven times";
  Margin "made the fewest switch errors" → lowest rate; HiFi N50 ratio 4.6 (was "five times");
  WhatsHap indel cost 17–20% (was 18–20%), Hamming ratio 37–56% (was "less than half", true only
  from 16×); co-phasing heading now names methylation only (SVs add 1% N50) and "at least halves";
  interpretive clauses on depth and caller artefacts softened to "consistent with"; three ", so"
  clauses removed (style rule of 2026-09-24).

**Results split into competitors vs internal modules, 2026-10-06 (author request).**
- Figures were not Nature Methods compliant: tight-cropped to 151–153 mm, so placement at 183 mm
  would push fonts to 7.8 pt; Fig. 2 spent a panel on a legend; Fig. 3 used hatched grouped bars.
  All results figures are now exactly 183 mm wide (constrained layout), 5–7 pt Helvetica, 8 pt bold
  lowercase letters, keys inside the figure, no empty panels, no bars for trends.
- "LongPhase 2 + correction" was undefined in the figures and collided with the read-based
  correction inside `phase`. The step is now "GNN correction" (defined in Fig. 1 legend, Results,
  Methods); in main figures "LongPhase 2" is the complete method, GNN included.
- Results now has two parts. *Comparison with existing phasers* (main Figs. 2–6): SNV phasing vs
  WhatsHap/HapCUT2 with Margin in Fig. 2f; benchmark dependence (Fig. 3, SNV-only tools); indel and
  four-class co-phasing vs WhatsHap (new Fig. 4); HiFi vs WhatsHap (Fig. 5, two tools); unphased sets
  vs WhatsHap (new Fig. 6). *Contribution of the internal modules* (Supplementary only): GNN effect
  (Supp. Fig. 13), co-phasing configurations with/without GNN (14, 15), what the GNN withholds (16, 17).
- Supplementary figures renumbered by citation order: 10 other tools, 11 MethPhaser, 12 depth of
  unphased sets, 13 GNN effect, 14 co-phasing with/without GNN (former Fig. 4), 15 all
  configurations, 16 GNN-removed SNVs (former Fig. 6a–c), 17 old raster. Methods cross-references
  updated. Part headings are plain `\subsection*`, findings are declarative `\paragraph`s.
- Later the same day: panel letters had never been bold (Helvetica.ttc exposes only its regular face
  to matplotlib); all figures now use Arial with Arial-Bold embedded. Fig. 5 redesigned to mirror
  Fig. 2 a–e (phased SNVs on an 80–90% axis instead of a 0.7-point axis that exaggerated the gap,
  switch error *rate* instead of counts, Hamming and N50 from zero, WhatsHap/LongPhase 2 ratio).
- Readability (author, 2026-10-06): main line plots show 10, 20, 30, 40, 50 and 60× only (12–18× stay
  in the tables and Supplementary Data 1), the replicate s.d. is a light band instead of error bars,
  and the ±0.5× offset is gone; HapCUT2 (dashed, open squares) is drawn over WhatsHap where they coincide.
- Replicate design (author, 2026-10-06): the grey "single replicate" shading is removed from every
  figure; it is not standard in benchmarking figures. Legends state the replicate design once.
  The original rationale that overlapping reads make independent random subsampling impossible
  was withdrawn on author review: read overlap does not establish dependence between random draws.
- Markers (author, 2026-10-06): all coverages are plotted again (10–20× in steps of 2, to show
  low-coverage differences). Every tool has an open (unfilled) marker of its own shape and size —
  LongPhase 2 circle, WhatsHap small diamond, HapCUT2 large square, Margin/Ralphi/GCphase triangles
  and cross — so coinciding points nest instead of hiding each other.

**Unphased-SNV total confirmed, 2026-10-06 (author).** The accepted 60× total is 56,076.
The Results range now includes that count, and the resolved total mismatch is no longer an
open question. The old 60× benchmark-composition percentages were removed from the Results
pending replacement category counts; the independently supplied assembly counts and
Supplementary Table 12 already use 56,076. Supplementary Fig. 16a still uses the old
composition source and requires the updated absent/homozygous/heterozygous breakdown.
The author has been asked for those three counts; none was inferred from the new total.

**Deployment-threshold rationale, 2026-10-06 (author-provided correspondence).**
Methods and Supplementary Method 4 now document the 0.05–0.95 threshold sweep over 60 HG002
nanopore runs at 10–20×. The author clarified that B=0.30 was an empirical balance: it removed more switch errors
than B=0.40 at the cost of withholding additional phased SNVs, while retaining most phased
sites. B=0.40 had the lower unit cost. The text does not present 0.30 as a mathematical
optimum or imply a formally enforced cost constraint. This is separate from the classifier metric used to select the checkpoint.
The TODO asking for the reason for choosing 0.30 is resolved; the existing request to provide
the sweep source data and trade-off panel remains.

The supplied screenshot gives B=0.30: 1,863,972 phased SNVs, 1,658 switch errors, 8,569 SNVs
withheld, 1,150 switch errors removed (cost 7.45); B=0.40: 1,866,521, 1,765, 6,020 and 1,043
(cost 5.77). Both imply a baseline of 1,872,541 phased SNVs and 2,808 switch errors.
The table's coverage/replicate/aggregation is unspecified, so its counts were not added as
manuscript results. The accompanying statement that total phased-SNV loss was below 0.2%
needs its denominator and aggregation clarified: this table gives 0.458% at B=0.30 and
0.321% at B=0.40 relative to the common pre-correction phased count. The 0.2% statement
was omitted in favour of the qualitative trade-off explanation requested by the author;
clarifying that unused percentage is not a blocker for this wording change.

**Subsampling interpretation corrected, 2026-10-06 (author request).** The Results section no longer
uses read overlap to justify a single high-coverage subsample. Methods now states
the observed design without the invalid independence rationale: ten nanopore subsamples per
coverage at 10–20×, one at 30–60×, and one HiFi subsample per coverage. The standard deviations
quantify read-subsampling variation conditional on the source data set, not variability among
independent sequencing experiments. Subsampling variability at 30–60× and for HiFi was not
estimated. No additional experiments or measurements are implied. The earlier September n=9 descriptions
refer to the older local logs; they were superseded by the October input data and do not
describe the current manuscript, which uses n=10 at 10–20×.

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

**GIAB v5.0q preprint, 2026-10-07 (author request).** Olson et al., bioRxiv
10.64898/2026.09.23.752440, is the formal v5.0q benchmark paper; it replaces the `@misc`
`giab2025q100` (which pointed at the wrong `T2T-Q100/` directory) as `olson2026giabv5`
(65 authors, from the bioRxiv `citation_author` tags). The release GRCh38 smvar VCF and BED
(`release/.../v5.0q/`) have the same MD5 as the defrabb v0.020 draft that was scored, so no
rescoring. Correction: Methods said v5.0q "adds 701 Mb of autosomal sequence, mainly satellite
and segmental-duplication sequence"; 701 Mb is the T2T assembly figure (Hansen 2026). Measured on
chr1–22 with the GIAB v3.6 stratifications: the two BEDs share 2,496 Mb; v5.0q adds 83 Mb
(16 Mb tandem repeats, 13 Mb homopolymers) and omits 46 Mb (29 Mb segdups). v5.0q assesses
*less* segdup sequence than v4.2.1 (67 vs 84 Mb of 143 Mb) and almost no satellite (2 Mb of
70 Mb), so neither "satellites" nor "segmental duplications" may be claimed as gains; the
preprint's 1.2× segdup gain does not hold on the autosomes. All 2,180,776 het SNVs in the
v5.0q BED are phased. Methods, the Introduction's last benchmark sentence, the Results scope
sentence and the Supp. table of versions were rewritten (Nature Methods register, second
pass after author review); Data availability names the release files and URL. The
Introduction keeps the 701 Mb assembly figure, which is correct for the assembly. Open
opportunity (not done): the release `stvar` benchmark is phased and could score SV phase.

**Issue #1 results written in, 2026-10-08 (author request).** From JHL's
`notes/benchmark_strata/` (numbers rechecked from `item4_strata.tsv`, `item4_overlap.tsv`,
`item3_indel.tsv`). Results: scope sentence now says both truth sets were used in full (the
region-overlap sentences were wrong for BED-free scoring); v5.0q BED-restricted robustness
(2.1–4.0× vs WhatsHap, 2.6–10× vs HapCUT2); new paragraph locating switch errors (93% of
LongPhase 2 errors at 60× coincide with both tools under v4.2.1 vs 37% under v5.0q; shared
regions 1,127–1,492 vs 32–393 at 30–60×; outside-BED sites carry most v5.0q separation;
segdups largest ratio, non-difficult 1.7–2.0×); indel accuracy in the co-phasing paragraph
(8–31× lower indel-pair switch error rate than WhatsHap; GNN −29–39%). Discussion benchmark
paragraph rewritten (two effects; truth-error reading flagged as unverified); indel removed
from the limitations. Abstract: "at high coverage, most switch errors coincide across tools".
Methods: pair-level re-scoring described. Two JHL statements not used (see `[claim]` comment
in results.tex). Tables then packaged (same day): Supplementary Tables 13 (switch errors by truth set, region, stratum; coincident errors) and 14 (indel accuracy), generated by `make_results_figs.py` from the TSVs; the TSVs are three new sheets of `supplementary.xlsx` (Supplementary Data 1). Open:
check coincident v4.2.1 errors in reads before calling them truth errors.

**Benchmark finding promoted, 2026-10-07 (author request).** Abstract now names "the GIAB
v5.0q benchmark derived from the telomere-to-telomere assembly" (145 words). The benchmark
sentence was moved out of the Discussion limitations into a short paragraph of its own (before
the limitations): v4.2.1 convergence vs 4.3–4.8-fold separation under v5.0q, >96% shared
regions, the v5.0q release paper evaluated calls but not phase, and phaser comparisons used
mapping-confined truth sets. Next analyses suggested, not done: indel phase accuracy against
v5.0q `smvar`; switch errors in shared vs v5.0q-only regions and GIAB v3.6 TR/HP/segdup strata;
SV phase against `stvar`; an independent individual (Platinum Pedigree).

**Source baseline moved to release v2.1, 2026-10-07 (author request).** `../longphase` is now
checked out on `main` at the official release v2.1 (`46ba470`). JH tip `f7bd878` is an ancestor;
the two differ only in README images. Since `cc17fb1` (the commit behind the results), commit
`97d7367` made the GNN a default stage of `phase` (`--disableGNN`, `--gnnBreakThreshold` 0.30,
`--gnnPeThreshold` 0.80, `--gnnWindow` 20 — the manuscript's values) and removed the `gnn`
command; the commit reports byte-identical outputs on the demo and HG002 10x_1/20x_1 (SNV-only
and four-class). `--dot` still exists; the GNN now gets the edges in memory. Edits: Supp. Table
of versions and Methods code availability now name v2.1 (`46ba470`), with a `[provenance]`
comment; Supp. Note 1 and the Supp. Fig. 5d legend say the GNN reads the graph in memory.
Line map `cc17fb1` → v2.1: `GNNProcess.cpp:540` → `PhasingProcess.cpp:830`;
`PhasingProcess.cpp:122` → `:161`; `PhasingGraph.cpp:253–266` → `:218–231`;
`PhasingGraph.cpp:838–862` → `:804–828`; `ParsingBam.cpp:226–228` → `:236–238` (the PE header
now says 0 also means no incoming votes). `CompareProcess.cpp` and `ModCallParsingBam.cpp`
references are unchanged. Dated entries below keep their `cc17fb1` line numbers.

**Review correction, 2026-10-06 (author request).** Removed the training-label audit/retraining
TODO from the Discussion and item 12 from `notes/SUSPECTED_ERRORS.md`. No incorrectly labelled
training record had been demonstrated; parser checks alone did not establish a defect in the
actual training data. This concern is withdrawn and is not a submission blocker.

**Codex review applied, 2026-10-05 (two passes).** Verified against source before editing:
`compare` computes Hamming over all common variants incl. indels (`CompareProcess.cpp`:579) while
switch errors are SNV-only; the region filter also applies to the query (`:353`, though N50 is
identical under both truth sets, so the BED was probably not passed);
`run_t2t_validation.sh` samples its background from all pre-correction phased SNVs (:75), tests
the assembly VCF by start coordinate only (:104) and includes chrX/chrY; the indel-cost reduction
is 41-67% (not "at least half"); four-class Hamming falls 34-54% (not "halved").

*Pass 1, corrections:* six overstatements fixed in Results/Discussion ("at least halves", "exactly
as accurate", "halved", indel cost "in the evidence itself", Margin "by fragmenting", "no threshold
on a variant's own votes"); co-phasing Hamming values flagged as SNV+indel (`\todo`); assembly
analysis narrowed to "no assembly VCF record at the same coordinate", chr19 475-fold headline
dropped, rebuild requirements as `\todo`; WhatsHap comparison restated as regional co-location;
benchmark paragraph replaced by the unresolved-contributions sentence; "error probability" ->
"phase-error score" (Methods, Supplementary); Fig. 1 stage label "Evidence calibration" ->
"Evidence weighting"; stale HiFi statements fixed (methods :36, :126); Supplementary "share one
denominator" corrected; N50/BED and paired-difference `\todo`s added; held-out chr17/21/22,
matched-retention comparison promoted to `\todo`. Figures: Fig. 2e
relabelled "switch-error-rate ratio", legend moved off the panel; Fig. 3 colours now match Fig. 2
(hatching for indel/SV runs), panel f from zero; Fig. 4 s.d. on both endpoints; Supp. Fig. 12
capped bin marked censored; legends updated.

*Pass 2, length:* Results 2,575 -> 1,377 words, seven subsections with one finding, one
representative comparison and its cost each (coverage-by-coverage values left to Supp. Tables
7-12); Discussion 1,673 -> 620 words in four paragraphs (contribution; weighting and withholding;
limits; one downstream test). Word counts exclude `\todo`s and comments; Introduction (1,017)
untouched. The cut is reviewable on its own: `notes/length_cut_2026-10-05_{results,discussion}.diff`.

**Style pass, 2026-09-24 (author request).** Removed every ", so " clause (58 in rendered
text, including `\todo`s; `%` comments untouched) from `sections/*.tex`, `main.tex` and
`Supplementary.tex`, rewriting each as a subordinate "because" clause, a semicolon, a new
sentence or a participle. Also cut rhetorical AI-style phrasing: "is not free", "Perhaps
the most consequential finding", "designed to complement…, not to replace it", "conditions
on something else", "one might object", "an expectation, not a result", "a trade-off we
have accepted rather than solved", "The reason is practical.", "honestly", "in any case",
"on the same footing", "altogether … in the meantime", "actually". Wording only; no claim
or number changed.

Figure numbers currently come from `LongPhaseGNN_0902_2-1.pptx` (slides 7–11) and are
approximate to plot resolution; replace with exact values from the `longphase compare`
TSVs.

**GCphase removed from the comparison, 2026-10-07 (author decision).** GCphase was run with the
command from its README (`python GCphase.py -vcf … -bam … -output …`; GitHub `baimawjy/GCphase`
main `ffa7e8b`, 2023-10-17), on the full PEPPER-Margin-DeepVariant output. Its source shows why the
results were near random (read, not run): `get_info.py:18-19` is its only genotype test and skips
records whose genotype starts with `1`; it does not read FILTER, so refCall `0/0` records are kept;
`get_info.py:128-135` compares single read bases with the REF/ALT strings (indels and multi-allelic
sites cannot match); `phasingSNP.py:76-82` drops only sites with ≥85% one allele or a single
minority read; `outputResult.py` rewrites every phased position to `0|1`/`1|0`. In the 10× replicate-1
output, 1,194,969 of 3,470,770 phased sites (34.4%) were refCall `0/0`, 99.4% of them with a PEPPER
VAF ≥ 0.15. GCphase therefore needs a VCF of biallelic heterozygous (`0/1`) SNVs only. Changes:
Methods (comparison paragraph) states the exclusion and the reason; Results drops the GCphase
fold-change and its todo ("three" → "two further phasers"); Fig. 2 legend (f), Supplementary
Table 5 (row removed), Supplementary Fig. 10 caption, Supplementary Table 8 (rows removed, "seven" →
"six configurations") and `make_results_figs.py` (`sfig10` tools, Table 8 loop) updated. The
GCphase entry in Supplementary Table 6 (studies that use LongPhase) is unrelated and kept.
**Not yet regenerated** (no TeX/matplotlib on the analysis machine): `suppfig10_more_tools.pdf` still
draws GCphase — run `python3 figures-source/make_results_figs.py` and `make`. The `gcphase` columns
remain in `supplementary.xlsx` (Supplementary Data 1); delete them or mark them as excluded.

**Review round, 2026-10-07.** (H1) Methods now state that accuracy was scored with
`longphase compare` on chr1–22 without a benchmark BED, name the v4.2.1 hifiasm phase-transfer
file and how it was filtered, and give the out-of-BED shares (9.3% v5.0q, 3.4% v4.2.1).
(H2) MethPhaser rationale: it was given LongPhase 2 SNV-only output (no GNN) so that both runs start
from the same SNV phasing. (H3) HiFi call sets are being regenerated per coverage (current calls all
come from 10×, median DP 10); Methods, Results and Supplementary Table 5 say so. (M1) Down-sampling
seeds, minimap2 2.24 / samtools versions, PEPPER r0.8, WhatsHap/HapCUT2/Margin/Ralphi command lines,
HiFi source and the runtime machine filled in; only the PEPPER model preset is still open.
(M2) Unphased-SNV classification re-run with the final GNN model
(`gnn_prepare/unphased_e6/`, replicate 1, 10–60×): 55,756–58,162 unphased; at 60× 2,215
benchmark-het by position, 2,055 with matching alleles, which equals the `compare` loss. The old
"BED" explanation was wrong; the gap was the matching rule. `COMPOSITION` in `make_results_figs.py`
updated; Supplementary Fig. 16 must be regenerated, and Supplementary Fig. 17 is still the old raster.
(M3) SV/5mC phased fractions replaced by exact values (four-class, before GNN: 5mC 99.0–99.4%,
SV 68.1–70.1%; GNN unphases 1.4–4.6% and 2.4–3.8%). (L1) See item 8(a): the debug fix ships in
v2.1.1 or later.

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

**Results and Discussion editorial revision, 2026-10-08 (Codex).**
Revised the current working-tree text, including the new benchmark-extent description and
standalone benchmark Discussion paragraph. Results retains the competitor/component structure
and uses switch error rate, phased fraction and block N50 consistently. Long sentences were
split, comparator and coverage scopes made explicit, and interpretive claims separated from
measurements. Discussion now follows five paragraphs: contribution, selective withholding,
benchmark dependence, evaluation limits and downstream testing.

The revision removes unsupported causal interpretations of capped read depth and benchmark
VCF absence. The assembly comparison is explicitly exploratory, coordinate-based and not an
independent validation; its pre-correction background remains identified. PE = 0 is described
as either unanimous votes or no incoming votes at a block start, consistent with Methods and
the v2.1 VCF header. The MethPhaser comparison remains provisional. Greater separation under
v5.0q is not presented as independent evidence of benchmark phase accuracy. All 12 Results
TODOs are preserved, and no measurements, analyses, figure artwork or data tables were changed.

Validation: main.pdf rebuilt successfully with TeX Live. Results/Discussion pages 3, 5–9 and 13
were rendered and inspected. No undefined references/citations, missing characters or new
box warnings were found. The existing title/affiliation overfull box and figure-caption
underfull boxes are unchanged. The compiled main document has 23 pages. No hub publication
was performed.

**Figs. 2 and 5 panels reordered, 2026-10-08 (author request).** Accuracy now leads: Fig. 2
a switch error rate, b ratio to comparators, c Hamming distance, d block N50, e switch error
rate against N50 at 10×, f phased SNVs (was a, b, c, d, e, f = phased, rate, Hamming, N50,
ratio, trade-off). Fig. 5 follows the same order (a rate, b ratio, c Hamming, d N50, e phased).
LongPhase 2 is first in both legends. Legends, Results panel citations and the Fig. 5
"panels as in Fig. 2a–d,f" cross-reference updated; the N50 sentence now precedes the
phased-fraction sentence so that panels are cited in order. No data changed. A runtime panel
was not added: the timing todo in Results still has no source table.
Same day, Fig. 2e: the single 10× scatter (the one coverage at which Margin has a lower switch
error rate than LongPhase 2) is replaced by one switch-rate/N50 path per tool over 10–20×, the
coverages at which Margin was run. Results text unchanged (it already gives 10× and 12–20×).
