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
per-variant uncertainty strip and the unphased SNV to d; dashed low-confidence
edges and a down-weighted-allele legend in b; the block split when unphasing disconnects a phase set (`GNNProcess.cpp:540`, branch `JH`) is
now stated only in Methods, the Fig. 1 legend having been cut to ~100 words (2026-09-24); panel a has a heading and tighter
reads, no panel carries a heading, the sequence-context inset is coloured by haplotype, and the compacted top half brings the
canvas to 1680×1046. Plain wording in the figure: "phasing uncertainty" for phasing entropy
(the caption names PE once and points to Methods), "haplotype block" / "block membership"
instead of phase set. Wording rule (author, 2026-09-24): headings and captions say "phasing
uncertainty" (entropy is only one measure of it); body text says "haplotype block" for phase set
and keeps "phasing entropy" only where a sentence is about the metric's value (Results, Fig. 6c).
Panel c shows the uncertainty bars with a y-axis label and no threshold line, and node (31) and
edge (6) feature-vector strips segmented by feature group (16/6/5/4 and 3/1/1/1, from
`GNNProcess.cpp` nf[0..30] and ep[0..5] and the Methods grouping). Open polish: the PDF still embeds five Type 3 fonts (rsvg-convert output).

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
8. **Source fixes, uncommitted** in the working tree of `../longphase` (commit before the
   release): (a) `PhasingGraph.cpp:253–266` at cc17fb1, the `else if` that assigns vote
   weight 20 chained off `if(debug)` instead of the edge-threshold test, fixed 2026-09-20;
   (b) `GNNModel.h` lines 6, 43 and 60 described the edge tensor and encoder as 7-wide
   (`[N, N, 7]`, `[7,128]`) although `kEdgeFeat` is 6, comment corrected 2026-09-20.
   `findBestEdgePair` still takes an unused `isONT`.
   Two text errors traced to the same file were corrected on 2026-09-19: `--distance` is a
   gap test that skips a variant (:350), not a 300 kb cap on edges or votes, and the
   weight-20 upgrade also fires irrespective of s when one pairing has < 1 unit of support.
9. **Main Figs. 2–6 are raster exports** (PNG from the pptx) with in-figure titles,
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
selection criterion S (P > 0.5) contradicts the deployed 0.30 threshold, and test
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
