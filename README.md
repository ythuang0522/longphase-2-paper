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

## Comparison with further phasers (2026-10-17)

Supplementary Data 1, sheet `Other_phasers` (71 runs); commands, inputs and full tables in
`notes/competitors/README.md`, scripts in `notes/competitors/scripts/`. In the manuscript since
2026-10-19 as Supplementary Table 18, one Results paragraph, Methods and one Discussion sentence (log
entries at the end). HiPhase (SNV-only) is also in Figs. 2c,f and 4b, Supplementary Fig. 16e,
Supplementary Table 11 and the abstract; HapBridge and LongHap (SNVs with 5mC) are in Fig. 2d and
Supplementary Fig. 16a,d since 2026-10-20; TinkerHap and the LongHap all-variant runs are not in the figures.

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
analysis (the v5.0q-without-BED item: on 2026-09-24 the authors said both truth sets
were scored within their benchmark BEDs and Methods was changed accordingly; **this was
wrong** — JHL's reproduction of all 1,024 runs on 2026-10-08 (issue #1) showed that every
table was scored without a BED, and Methods now says so): the
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
   Partly resolved 2026-10-10 (issue #5): MethPhaser 0.0.3 crashed silently; the 0.0.4 rerun joins
   blocks. Open: its output blocks overlap, so its N50 is not usable yet (entry of 2026-10-10 below).
3. ~~**HiFi call sets are coverage-independent**~~ — resolved 2026-10-09 (issue #4, see below). Was: (2,367,609–2,367,619 het SNVs at 10–50×): one call
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

**Results figures reorganized after the repository README, 2026-10-08 (author request).**
The author asked for the four comparisons of the `twolinin/longphase` README (SNV, SNV+indel,
SNV+5mC, evidence combinations; SNV+5mC had never been shown), for no ratio panels ("switch error
rate and Hamming distance already show it"), and for Supplementary analyses that show the
strengths of LongPhase 2 to move into the main figures.
- **Fig. 2** (`fig2_phaser_comparison.pdf`, label `fig:phasers`): one row per evidence type
  (SNV vs WhatsHap/HapCUT2; SNV+indel vs WhatsHap; SNV+5mC vs MethPhaser, replicate 1) × four
  columns (switch error rate, Hamming distance, N50, phased fraction). The indel row promotes
  Supplementary Table 14: panel e adds indel-pair switch error rates (dotted), panel f is the indel
  Hamming distance, so no main panel shows the mixed SNV+indel Hamming value any more. The ratio
  panel and the Margin trade-off panel are gone (Margin/Ralphi stay in Supplementary Fig. 10).
  MethPhaser's switch error rate comes from its input run (identical counts, asserted in code).
- **Fig. 3** (new, `fig3_evidence_classes.pdf`, `fig:evidence`): SNV, +5mC, +indels and all four
  classes (all with GNN correction): switch error rate, N50 and the switch-rate/N50 path per
  configuration beside WhatsHap with and without indels. This relaxes the 2026-10-06 rule: the
  per-configuration comparison *with* GNN is now a main figure; with/without-GNN stays Supplementary.
- **Fig. 4** (former Fig. 3, `fig4_two_benchmarks.pdf`): the two near-identical Hamming panels are
  replaced by Supplementary Table 13 content: c, 60× switch errors shared by all three tools
  (93% of LongPhase 2's under v4.2.1, 37% under v5.0q); d,e, v5.0q switch error rate by region at
  10× and 60× (genome-wide, v5.0q regions, not difficult, segmental duplications, outside both).
- **Fig. 5**: ratio panel removed (four panels, same columns as Fig. 2). The former Fig. 4
  (co-phasing) is absorbed into Figs. 2e–h and 3.
- Colours: MethPhaser purple `#6A3D9A`; configuration colours (Fig. 3 and Supplementary Figs. 14,
  15) SNV red, +5mC `#1B9E77`, +indel `#C66A00`, all four black, checked with the dataviz palette
  validator against WhatsHap blue.
- Text: Results Part 1 reordered to follow the figures (SNV → indel/5mC co-phasing → evidence
  classes → benchmarks → HiFi → unphased). New numbers, all from Supplementary Data 1: LongPhase 2
  vs MethPhaser 1.4–1.5-fold lower switch error rate, longer N50 at 20–60×; before GNN correction
  joint 5mC phasing made as many switch errors as MethPhaser (736 vs 743 at 60×), so the rate gap
  is the GNN and the N50 gap is joint phasing. The four-class vs WhatsHap+indel N50 gap is 2–21%
  over all ten coverages (was "2–19%", computed on six). The duplicated after-GNN sentences in Part 2
  now point to Fig. 3.
- Same day, Codex review of the redesign (all points checked against Supplementary Data 1 and the
  issue #1 TSVs; author approved fixes 1–5): Fig. 3 heading now "Adding 5mC or indels lengthens
  phase blocks, and 5mC does so at similar switch error rates" (5mC adds 1–23 switch errors per
  genome; adding SVs to indels shortens N50 at 30× and to indels+5mC at 50×); GNN removal of
  indel-pair switch errors 24–39% over all ten coverages (was 29–39%); SVs+5mC give *similar*
  indel-pair rates (0.104 vs 0.101% at 10×). Fig. 4d,e lead with the v5.0q benchmark regions; the
  outside-both row sits below a dashed line, labelled exploratory, and the Results paragraph follows
  that order. Discussion no longer says coincident disagreement is "more consistent with" v4.2.1
  phase-transfer errors: it states that the two truth sets differ in phase in commonly assessed
  regions, that WhatsHap and HapCUT2 (no trained parameters) also agree with v5.0q there, and that
  the phase-transfer explanation is unverified. Codex's concern that the v5.0q-trained GNN explains
  the benchmark contrast does not hold: uncorrected LongPhase 2 shows it too (60×: 1,708 vs 743
  switch errors; shared regions 1,193 vs 41). Open author decision: headline fold changes are still
  genome-wide (truth VCF in full); inside the benchmark regions they are 2.1–4.0× (WhatsHap) and
  2.6–10× (HapCUT2).

**HiFi rescored with per-coverage calls, 2026-10-09 (issue #4, `notes/hifi/README.md`).**
PEPPER-Margin-DeepVariant r0.8 `--hifi` was run on each HiFi coverage's own alignment (10–40×
down-sampled from the 48× GIAB Revio BAM with seed 1; 48× used as 50×). SNV-only phasing with
release v2.1 (GNN and `--disableGNN`) and WhatsHap 2.8 `--only-snvs`, scored with `compare`
v2.1 against v5.0q without a BED. `supplementary.xlsx` HiFi rows of `Variant_Calling` and
`SNV_Detail` replaced (no other cell changed); Supplementary Tables 7 and 11 regenerated
(`tables()` only). LongPhase 2 now has 2.2–2.6-fold fewer switch errors than WhatsHap (was
2.5–3.5): abstract, Results HiFi paragraph (title, rates, Hamming no longer lower at 50×,
N50 ratio 4.3; GNN removes 19–25% of HiFi switch errors, was 19–28%), Fig. 5 legend, Methods (model presets, HiFi data, replicates) and
Supplementary Table 5 updated; HiFi `\todo`s removed. `Homo. SNV` counts PASS 1/1 plus
refCall 0/0 records (checked against the nanopore and old HiFi rows); Table 7 caption says so.
**Not done here (no matplotlib fonts/LaTeX on the lab server): Fig. 5 and Supplementary
Fig. 13e,f must be regenerated (`make results-figs`) and the PDFs rebuilt.**

**Held-out chromosomes written in; main merged, 2026-10-09 (issue #2; author decision on B).**
- `origin/main` (JHL: issue #2 `1702d2c`, HiFi issue #4 `9fb0cc4`/`9054c87`) merged into the
  redesign branch. Conflicts: HiFi paragraph and Fig. 5 legend (main's text, this branch's panel
  letters, Fig. 5 has no ratio panel), README (both entries kept). Fig. 5 and Supplementary
  Fig. 13e,f regenerated from the new HiFi rows; Fig. 5d axis 84–94% (HiFi phased SNVs now 87–92%).
- All `notes/heldout/` numbers recomputed from the raw tables and reproduced; 33.1%/8.3 reproduced
  from `supplementary.xlsx`; PR #42/#52/#82 dates checked in `../longphase`.
- Deployment threshold (author, 2026-10-09): JHL's formal rule stands — largest fraction of switch
  errors removed at ≤10 withheld SNVs per removed error. This supersedes the 2026-10-06 "empirical
  balance" account. Methods and Supplementary Method 4 now say that on chr17/21/22 the cost is 10.5,
  slightly above the limit, and that the threshold was not re-selected there. JHL's "thresholds
  meeting it lay between 0.30 and 0.40 … their optima also fell in it" was rewritten (the rule picks
  one threshold; a sweep limited to 0.30–0.40 cannot have an optimum outside it); a `[check]`
  comment asks JHL which model the full 0.05–0.95 sweep used.
- Results: held-out sentence (2.8–3.9× vs WhatsHap, 3.3–4.9× vs HapCUT2 at 10–20×; 30–60× from
  single runs with 37–83 switch errors); Margin beats LongPhase 2 on chr17/21/22 at 10–12× (0.099 vs
  0.127% at 10×, N50 0.22 vs 0.72 Mb); Part 2 GNN effect gives both 31–33% (genome) and 20–23% /
  14–20% (held-out) with the chromosome-difficulty caveat. Results `\todo` item (i) removed;
  matched-retention and paired-uncertainty items remain.
- New Supplementary Table 15 (`heldout_table()`), v5.0q and v4.2.1, all coverages.
- Not done, by author decision (2026-10-09): the per-run held-out values stay in `notes/heldout/`
  and are not added to Supplementary Data 1; no per-chromosome GNN reduction.

**Threshold sweep and HiFi check, 2026-10-09.**
- Author: there is one released GNN (e6), and the full 0.05–0.95 sweep was done on it. The
  "later models were swept over 0.30–0.40" sentence and its `[check]` comment are deleted from
  Supplementary Method 4.
- Issue #4 (HiFi) checked: every value in JHL's comment reproduces from `supplementary.xlsx`
  (switch errors, 2.2–2.6-fold rate ratio, Hamming lower at 10–40× only, N50 within 3.1%, 0.4–0.5
  points more phased SNVs for WhatsHap, GNN removes 19–25%, N50 ratio 4.3). Two stale sentences
  that 9fb0cc4 left were fixed: the old HiFi description and its "being regenerated" `\todo` in
  Methods (duplicating the new HiFi data sentence), and "HiFi call-set handling remains to be
  confirmed" in the Discussion. JHL's view that more HiFi replicates are unnecessary is unchanged
  in Methods ("could be drawn … but were not").
- Same day, Discussion after issues #2 and #4: the limitations paragraph reports the held-out
  result (advantage unchanged; GNN removes 14–23% vs 31–33% at cost 10.5 vs 8.3; chr17/21/22 held out
  from network training only, not from the 2023–2024 constant tuning) instead of asking for it; the
  Margin sentence adds 10–12× on the held-out chromosomes. Supplementary Fig. 13e gains a held-out
  line (nanopore, chr17/21/22), legend moved above the data. No main-figure change.

**Figure style pass, Figs. 2–6, 2026-10-09 (author request: top-tier journal standard).**
Tighter tick/label paddings (2 pt ticks, 2.5 pt labels); Fig. 2 y-labels aligned per column across
rows (`align_ylabels()`); Fig. 4 legend entry "(c)" replaced by an in-panel label, bold group
headers, no y spine in the bar panel; Fig. 5 and Fig. 6c tick labels without excess decimals; Fig. 6
one colour key ("Both tools"), no inner legend in b (dashed line = no enrichment, in the legend),
plain x label in c with the capped-depth bin labelled in place. Arial/Arial-Bold embedded in all.

**Supplementary figure review, 2026-10-09 (author request).**
- All automatic linear tick locators now use steps of 1, 2 or 5 (`_tidy_ticks()` in `save()`), so no
  axis shows labels such as 0.025 or 77.5; applies to main and Supplementary figures. Hamming axes in
  Supplementary Figs. 14d and 15 start at zero.
- Supplementary Fig. 10: plain decimal labels on the log axes (no 10^x), LongPhase 2 first in the
  key, "WhatsHap". Fig. 11: open markers and the Fig. 2 glyphs (MethPhaser triangle). Fig. 12: the
  censored-depth label sits inside the grey band, clear of the lines. Fig. 15: "GNN" no longer
  lower-cased by `str.capitalize()`, open markers with the Fig. 3 glyphs per configuration
  (`CFGM`). Fig. 16: keys above the panels instead of below.
- Supplementary Fig. 2e (schematic): "Suppl. Fig. 4" spelled out. Supplementary Fig. 4a: the initial-phasing box reads "LongPhase 2" (was "LongPhase", which could be read as LongPhase 1).
- Not changed: schematics 1 and 3–8 (consistent and legible at print size); Supplementary Fig. 9 is
  still a placeholder and Fig. 17 still the old raster (both `\todo`s, need source data).

**Wording review by Codex, 2026-10-09 (50 items; the review file is not kept in the repository).**
Applied (agreed): Supplementary Methods narration, tutorial asides and software-documentation
detail removed (items 6–26: document openings, methylation linking/merging, scanner bookkeeping and
"worth stating" passage, MR rationale, release history, duplicated feature inventory, GPS wording,
storage breakdown, GELU instruction, central-zone repetition, label/loss/selection asides, export
serialization, haplotag commentary); the uncited Supplementary Notes 1–2 deleted (vote-weight
definition moved into Edge features). Two factual fixes: the central-zone text said a distant variant
leaves *fewer* variants in the zone (it leaves more; sentence replaced by the equation), and the S
criterion is now defined exactly (correct detections minus false detections over all errors).
Supplementary Method 3 retitled "Tuning …" and its `\todo` replaced by the limitation (tuned on the
same individual; chr17/21/22 held out from the GNN only). Tables 3, 4 and 6 de-engineered and Table 6
retitled "Selected applications and evaluations" (DeepVariant row, which does not use LongPhase,
removed; promotional asides removed); Table 6 is now cited in the Introduction. Supplementary Figs.
1–7 legends shortened to panel descriptions; Fig. 9 placeholder caption no longer states results.
Schematics: "phase-error score" replaces P(misphased)/P(error)/"predicted error probability"
(Figs. 4–6); Fig. 1a SV weight corrected to the code (ALT Q60, REF Q30, both full weight;
`PhasingGraph.cpp` buildVariantGraph — the figure said 0.1 for REF); Fig. 6 input label is σ(w), not
"raw edge weights"; node-cap and binary-storage notes dropped; Fig. 5c rule written as r ≤ 0.5.
Supplementary Table 12 row labels say "assembly variant record at the same coordinate" and the
caption describes the control as sampled before correction; Tables 9–10 say Hamming distance
includes indels where phased. Main text: abstract (problem statement, N50 at 60× vs SNV-only,
interface compatibility instead of "replaces unchanged"), Introduction (items 36–39, incl. the
v4.2.1 original-vs-phase-transfer distinction), Results headings and two sentences (items 40–42;
the compare reconciliation moved to a `[provenance]` comment), Methods (MethPhaser sentence now says
GNN correction adds to the difference; HiFi replicate sentence deleted), Discussion (item 46).
Not applied: items 1–2, 33 (Supplementary Fig. 17 needs regeneration from source data; still a
`\todo`), 3 and 50 (visible blockers kept; runtime claim in the abstract still rests on plot-read
values, issue #3), 34 (agreed, no change needed), 43 (voting rules and seeds kept in Methods for
reproducibility), 44 (GCphase reason kept as one factual sentence).

**Supplementary Fig. 17 deleted, 2026-10-09 (author).** The old pptx raster (former main Fig. 6)
held plot-read values and interpretive text the analysis did not support, and its panel a was
superseded by Supplementary Fig. 16a. Removed with it: the two Results sentences quoting its values
(PE = 0 in 43%/21–23% of unphased benchmark heterozygotes; 46–50% clustered and 38–49% low-GQ
benchmark-absent calls) and the Methods `\todo` clause on its bins. The Discussion now says the GNN
"may" find candidates an entropy threshold would miss. No issue opened (author); the three shares
can be recomputed from the unphased-SNV lists if wanted later.

**Runtime and memory written in, 2026-10-09 (issue #3, `notes/runtime/`).** Abstract: "five- to
sixfold faster on one thread at 60×" (was "six- to sevenfold", which compared 24 threads with one).
Results: one-thread times (8.1/18.0 min vs 24.1/96.4 HapCUT2, 25.2/113.8 WhatsHap) and the
24-thread times with their memory cost (63.0 GiB at 60× vs 7.4 GiB on one thread); the runtime
`\todo` removed. Methods: runtime measured once on 10x_1 and 60×, LongPhase 2 timed with 1 and 24
threads. New Supplementary Table 16 (`runtime_table()`); memory in GiB, rounded half-up.

**Results rewritten to follow the figures across coverage, 2026-10-09 (author request).** The
author objected that the Results quoted 10× and 60× values while every figure plots 10–60×. Each
paragraph now follows its figure panel by panel and states the coverage dependence (where the
tools converge, diverge or cross over; e.g. the SNV advantage widens from 2.8× at 10× to a stable
3.4–3.7× at 20–60×; the indel-pair advantage grows from 8× to 31× because WhatsHap's rate does not
fall with coverage; v4.2.1 errors of LongPhase 2 stay at 1,635–1,820 at every coverage while
v5.0q errors fall 3.1-fold). Every range was recomputed over all plotted coverages (header
comment "COVERAGE RULE"). Corrections found while doing so:
- WhatsHap's N50 advantage over LongPhase 2 with indels was "14–28%" (10/20/…/60× only); it is
  14–34% over the plotted coverages (28–34% at 10–18×).
- "GNN correction reduced the additional error associated with indels by 41–67%" held for the
  four-class configuration only; over the indel-containing configurations it is 41–71%.
- Segmental-duplication ratios at 10× were count ratios (5.2, 5.7); Fig. 4d plots rates, so the
  text now gives rate ratios (5.0/5.5 at 10×, 4.3/6.5 at 60×).
- "75% of WhatsHap's and 62% of HapCUT2's switch errors at 60× lie outside both benchmarks" omitted
  that 70% of LongPhase 2's do too; all three are now given, with the 10× shares (29/46/43%).
- Margin: "lower rates at 12–20×" became "equal at 12×, 1.2–1.5-fold higher at 14–20×".
- The caveat "Absence from this VCF does not by itself establish that a call is erroneous" had
  been merged into a `%` comment line and was invisible in the PDF; restored to the text.
- Fig. 6c: the uncommitted median depths are no longer quoted; the text gives depth shares from the
  2× histograms of `UnphaseVenn3.jsx` (the figure source), and the `\todo` now asks for those
  summaries in Supplementary Data 1.
Results prose is ~500 words longer than before (texcount 3,203 incl. `\todo` text, was 2,671).

**Required-validation `\todo` closed without new experiments, 2026-10-09 (author: "no new
experiments").** The Results `\todo` on matched retention and paired uncertainty is gone.
- Paired uncertainty answered from Supplementary Data 1: Supplementary Table 8 has a new column,
  switch error rate ÷ that of LongPhase 2 in the same down-sampling replicate (mean (s.d.) at
  10–20×; `rate_ratio()` in `make_results_figs.py`, column spacing 2.4 pt to fit). Results: per
  replicate, LongPhase 2 is 2.8–4.1× below WhatsHap and 3.2–5.1× below HapCUT2 at 10–20×; GNN
  correction removes 30–36% of switch errors per replicate. The Methods `\todo` "Report paired
  replicate-wise correction effects" is resolved by one sentence in Statistics and reproducibility.
- Matched retention (network vs entropy threshold, support threshold, random, HapCUT2 confidence)
  demoted to an `[optional experiment]` comment next to the GNN paragraph. The Discussion already
  states it as an open limitation; no claim depends on it.

**Hamming re-score and T2T rebuild `\todo`s demoted to limitations, 2026-10-09 (author: no new
experiments).**
- Hamming: no Hamming value of an indel-containing configuration is quoted in the Results; Methods
  now says the metric includes indels and is not comparable between configurations with and
  without indels, which are compared by SNV switch error rate. The re-score clause is removed from
  the Methods `\todo` (region-filter commands and metric table remain).
- T2T assembly analysis (Results and Supplementary Fig. 16 `\todo`s): not rebuilt. Autosome-only
  shares derived from the existing per-chromosome counts (9.6% vs 92.9%, odds ratio 124; two new
  rows in Supplementary Table 12, generated). Results and Methods now state the limits: chrX/chrY
  included in the headline counts, start-coordinate matching without allele comparison,
  background containing later-unphased sites (biases towards no difference; expected-value
  estimate in a `[limitation]` comment), raw dipcall BED, same assembly as v5.0q.
- Results `\todo`s left: two Supplementary Data 1 deposits (Fig. 6c depth summaries; SV and 5mC
  phased counts), no new analysis needed.

**Figs. 2 and 3 restructured: accuracy with contiguity, completeness with the unphased analysis,
2026-10-09 (author request).** The author found Fig. 2 much larger than Fig. 3 although the two
were correlated, and feared that its N50 and phased-fraction columns told reviewers that accuracy
came at the cost of contiguity and completeness. Main figures go from six to five.
- **Fig. 2** (`fig2_phaser_comparison.pdf`, `fig:phasers`): same three rows (SNV vs
  WhatsHap/HapCUT2; SNV+indel vs WhatsHap; SNV+5mC vs MethPhaser), now three columns: switch error
  rate, Hamming distance, and SNV switch error rate against block N50 (one path per tool over all
  plotted coverages). Panels c and f add LongPhase 2 with all four evidence classes (black).
- **Fig. 3** (new, `fig3_phased_unphased.pdf`, label `fig:unphased`): a, phased benchmark het.
  SNVs (former Fig. 2d); b, phased benchmark het. indels (former 2h); c, new: net additional SNV
  calls phased by WhatsHap, split into calls matched to a v5.0q het. SNV and other calls; d–f,
  former Fig. 6a–c. Former Fig. 3 (evidence classes) dropped: Supplementary Fig. 15 shows every
  configuration; its Results paragraph moved into Part 2 (after-GNN configuration sentences).
- **Supplementary Table 17** (new, generated): Venn counts and the net difference behind Fig. 3c.
- Text: the SNV paragraph now says the lower error rates were not obtained with shorter blocks
  (N50 up to 11% shorter at 10–20×, 1–5% longer from 30×; before GNN correction 1.9–2.5-fold
  fewer switch errors than WhatsHap at 0.97–1.07× its N50; four-class blocks 6–50% longer than
  WhatsHap SNV-only at 2.5–3.1-fold lower rates). A new paragraph before the unphased paragraph
  (which moved up, before Fig. 4) explains that the phased-fraction metric counts only calls that
  match a benchmark het. SNV, and that 65–80% of the additional calls phased by WhatsHap do not
  (10/30/60×, replicate 1). The phased-fraction gap is 0.6–0.9 points before GNN correction; the
  GNN adds 0.1–0.3. One Discussion sentence added (limitations paragraph on withholding).
- Caveat found while checking the author's argument: the calls the GNN removes are mostly absent
  from the benchmark, but they are only ~1/6 of the LongPhase 2-only unphased set, and the 0.7–1.0
  point gap in Fig. 3a is in benchmark het. SNVs by construction. The text therefore claims only
  the net composition. **Issue #6** (JHL) asks for the per-set benchmark composition, WhatsHap's
  accuracy at the matched sites, the per-set depth summaries (closes the depth `\todo`) and the
  script behind `UnphaseVenn3.jsx`. Precision at every coverage was judged unnecessary.
- Cross-references updated: Methods source-data `\todo` (Figs. 2–5), Supplementary block-N50
  paragraph (Figs. 2c,f,i and 5c), Supplementary Fig. 12 legend (Fig. 3d), Supplementary Data 1
  paragraph, Fig. 5 legend ("panels as in Fig. 2a–d" removed).
- Same day, Fig. 2c,f (author: "All four classes are difficult to understand by a reviewer"):
  the black four-class path is removed from the SNV row (c), so each row compares the tools on
  the same input. In f it is a dashed red LongPhase 2 line, "LongPhase 2, + SVs and 5mC", in the
  row key; the legend says that WhatsHap cannot use SVs or 5mC. The SNV paragraph keeps the
  four-class vs SNV-only WhatsHap numbers, now cited to Supplementary Tables 8 and 10.
- Same day, Fig. 3e,f redesigned (author: "difficult to understand ... a reviewer [should] easily
  get the message without reading the explanation in text"). e: absolute share of each tool-only
  set inside the other tool's switch-error intervals beside a grey "expected at random" bar (all
  SNVs assessed for that tool), fold change printed on top, group labels in the panel. f: the
  three 60× density curves are replaced by 100% bars of three depth classes (< 20× few reads,
  20–89×, ≥ 90× excess reads; the cap bin is inside the last class); per-coverage curves stay in
  Supplementary Fig. 12. Results add the absolute shares (10–12% vs 1.1–2.3%) and the ≥ 90× share
  (29% vs 3–4%). Methods `\todo` on switch-error intervals now points to Fig. 3c–f and issue #6.

**Issue #6 results written in, 2026-10-09 (JHL, `notes/unphased/`, commits 273b1fe, 8b7ee5e,
07fb243; author approved all proposed changes).** JHL's scorer reproduces `compare` exactly
(`issue6_checks.tsv`), the matched part of Fig. 3c equals the `compare` difference exactly
(`issue6_reconcile.tsv`), and his depth histograms equal `UnphaseVenn3.jsx`.
- Fig. 3 now reads `notes/unphased/` (composition, intervals, depth TSVs) instead of the JSX
  constants. c: the additional calls phased by WhatsHap split four ways (het. in benchmark, hom.,
  absent, other allele or chrX/Y). e: **replaced** — the other tool's wrong phase (block-wise
  Hamming error) at the benchmark het. SNVs of each tool-only set, beside its genome-wide Hamming
  distance, numbers of wrongly phased SNVs on top. The interval enrichment moved to the text and
  Supplementary Table 17.
- Supplementary Table 17 rebuilt: composition of all five sets, the other tool's errors and the
  interval co-location, the net difference. Supplementary Data 1 gains three sheets
  (`Unphased_composition`, `Unphased_intervals`, `Unphased_depth`); the Supplementary Data 1
  paragraph lists them.
- Results: composition (LP2-only 15–20% benchmark het., 70–76% absent; phased by both 91–95% and
  4.5–8.0%); WhatsHap wrong at 22.9/15.9/10.0% of the LP2-only benchmark SNVs (3–6× its
  genome-wide rate); the symmetric result is stated (LP2 wrong at 13.9–16.7% of the WhatsHap-only
  benchmark SNVs, 2.6–9.9×, at 13–25× fewer sites); inside the benchmark regions 92.0% of 3,684
  LP2-only sites at ≥ 90× (60×) are false calls; LP2-only sites are *less* often in segdups or
  outside the 1:1 alignment than the other sets (54–75% vs 88–94%), so the source of the excess
  depth is stated as undetermined. The last two numbers come from the lab-server site table and
  were not recomputed here (provenance comment). One Discussion sentence added.
- Corrected: the "expected" share of Fig. 3e/Table 17 is over all heterozygous SNV calls the tool
  phased, not "assessed" SNVs (legend, Results, Methods). Methods now define the call universe,
  the classes, the wrong-phase rule and the switch-error interval. The depth `\todo` in Results is
  closed (Supplementary Data 1); the Methods `\todo` is reduced to the Supplementary Fig. 16a
  script (`analyze_unphased.py`), which issue #6 did not cover.

**Fig. 3 rebuilt as a two-tool comparison, 2026-10-09 (author: c–f "difficult to understand";
"why is the protagonist WhatsHap and not LongPhase"; the three-tool key did not apply to c;
"not yet Nature Methods level").** Every panel now compares LongPhase 2 (red) with WhatsHap
(blue) on the same heterozygous SNV calls, with one key for the figure; HapCUT2 is left out of
Fig. 3a (its phased fraction is in Supplementary Table 8 and the text). Sets are named and
coloured by the tool that **phased** them, not by the tool that left them unphased.
- Row 1, all calls: a, benchmark het. SNVs phased; b, new, share of phased calls on chr1–22 that
  are benchmark het. SNVs (LP2 89.7/91.8/93.1% vs WhatsHap 86.3/89.7/91.5% at 10/30/60×;
  exact now that JHL confirmed the call universe); c, benchmark het. indels phased.
- Row 2, calls phased by one tool only: d, counts with the benchmark-het. part dark (WhatsHap
  only 122–149k, 20–25k benchmark het.; LP2 only 38–54k, 1.0–1.6k); e, wrong phase at those
  benchmark SNVs for the tool that phased them, with its overall rate as a black line and the
  error counts on top; f, read depth at 60× in tints of the tool colour.
- Also visible now, and stated in the Results: about 90% of the calls phased by LP2 only are
  absent from the benchmark, but 92–93% of them lie in segdups or outside the 1:1 alignment,
  where the benchmark does not assess phase.
- Supplementary Table 17 and Supplementary Fig. 12 relabelled the same way (Supp. Fig. 12 colours
  swapped to the tool that phased the set). The interval enrichment is now read as "calls phased
  by one tool only lie in that tool's own switch-error intervals 2.0–9.6× more often". Results,
  Methods, Discussion and the Supplementary Data 1 paragraph rewritten in this framing.
- Same day, superseded: the author could not read the six-panel symmetric version and said the
  design should have been discussed first, and that its message had drifted ("both tools trade
  off" instead of "LongPhase 2's trade-off is right"). Agreed core message: LongPhase 2 phases
  about 1% fewer benchmark SNVs; most calls it leaves unphased are not benchmark SNVs; WhatsHap
  often phases the others wrongly. **Fig. 3 is now a 2 × 2 grid (option A + depth kept):**
  a completeness, b precision (LongPhase 2 vs WhatsHap, one key); c calls left unphased by
  LongPhase 2 but phased by WhatsHap (wrong / correct benchmark SNVs / other, with "N wrong = X%
  of the benchmark SNVs"); d read depth at 60× of the calls left unphased by one tool only, with
  the 92% false-call note on the ≥ 90× segment. Phased indels moved to the text (Supplementary
  Table 9); the reverse set and interval co-location to the text and Supplementary Table 17.
  Supplementary Fig. 12 named and coloured as in d (left unphased by …). Results rewritten as
  three run-in paragraphs following a–b, c and d.
- Same day, Fig. 3c made two-sided (author's option B): one bar per tool and coverage for the
  calls left unphased by that tool only, coloured by that tool; shades = benchmark SNVs the other
  tool phased wrongly / correctly / not a benchmark SNV. All in-panel annotations removed from c
  and d (author: "Nature figures are not this text-heavy; describe it in the main text"). Fig. 3b
  still has 10/30/60× only: issue #7 asks JHL for the phased chr1–22 het. SNV call counts of every
  run so that b can show every coverage with replicate means, as a does.
- Same day, indel completeness back in the main figure (author's option B): Fig. 3 top row is
  a SNV completeness, b precision, c indel completeness; bottom row d calls left unphased by one
  tool only, e their read depth. The Results indel sentence now cites Fig. 3c and adds that
  WhatsHap's indel-pair switch error rate is 8–31 times that of LongPhase 2 (Fig. 2d).
- Same day, issue #7 (JHL, d765603, `notes/unphased/phased_calls_chr1_22.tsv`, 128 runs): phased
  het. SNV calls on chr1–22 of every SNV-only run of LongPhase 2 and WhatsHap; the 10/30/60×
  replicate-1 counts equal the issue #6 values (asserted in code). Fig. 3b now shows precision at
  every coverage with replicate s.d. (LongPhase 2 89.4–93.1%, WhatsHap 86.2–91.5%; higher for
  LongPhase 2 in every replicate, difference 3.2 → 1.5 points). New Precision column in
  Supplementary Table 8 (LongPhase 2 and WhatsHap rows); Supplementary Data 1 gains the
  `Phased_calls` sheet. Results, Methods, Fig. 3 legend and the Supplementary Data 1 paragraph
  updated. Issue #7 closed.
- Same day, indel completeness removed from Fig. 3 again (author: keep it out while the SNV
  analysis alone carries the argument). Checked first: the indel panel added nothing to the SNV
  argument, which rests on a (completeness), b (precision), c (composition and the other tool's
  phase at the matched calls) and d (depth). No indel precision exists to pair with it: issue #7
  counted SNV calls only, and `phased_indel` / `pindel_pct` count benchmark-matched indels only.
  Fig. 3 is again a 2 × 2 grid: a SNV completeness, b precision, c calls left unphased by one
  tool only, d their read depth. The Results indel sentence now cites Supplementary Table 9
  (WhatsHap − LongPhase 2 = 2.44 at 10× rising monotonically to 4.49 at 60×, so the 2.4–4.5
  range is in the table). Panel letters updated in the Fig. 3 legend, Results, Methods `\todo`,
  Supplementary Data 1 paragraph and Supplementary Fig. 12 legend. Scope of the claim: the SNV
  analysis supports "LongPhase 2 trades about 1% of benchmark SNVs for higher precision", not
  "every SNV it leaves unphased would be phased wrongly": WhatsHap phases 77–90% of the matched
  calls in the LongPhase 2-only set correctly (18,263 / 16,809 / 22,256 at 10/30/60×).
- Same day, Fig. 3c,d replaced by one net panel (author's option A, after a discussion round).
  The author wanted direct evidence that the calls LongPhase 2 leaves unphased are calling errors;
  the one-sided sets and the depth panel only compared the two tools. Agreed limit: the T2T-HG002
  assembly verifies a call only where it aligns 1:1 to GRCh38; outside, "not mappable" means "cannot
  be verified", not "error". Fig. 3 is now one row: a completeness, b precision, c additional calls
  phased by WhatsHap on chr1–22 (lp_only − wh_only per class; `net_classes()`): 107,510 / 77,083 /
  65,314 at 10/30/60×; het. SNV 20.7 / 23.9 / 36.4% (equals the replicate-1 Phased_SNV gap),
  of which phased wrongly 5,212 / 2,926 / 2,313 (net); homozygous or other allele 12.8 / 6.1 /
  6.1%; no benchmark record 66.6 / 70.0 / 57.5%. Read depth moved to Supplementary Fig. 12 (text
  kept). Results paragraph rewritten around the net values (one-sided details kept); Methods
  defines the net set; legend, Supplementary Data 1 paragraph and Supplementary Fig. 12 legend
  updated. **Open (`\todo`, issue #8):** split "no benchmark record" by `in_dipcall_1to1` of the
  issue #6 site table (`notes/unphased/assembly_split.py` → `assembly_split.tsv`); Fig. 3c then
  shows "calling error (benchmark or assembly)" and "cannot be verified" without code changes.
  Region choice: raw dipcall 1:1 BED (as Supplementary Table 16), not the curated benchmark BED.
- Same day, after reading GIAB v5.0q (olson2026giabv5; the paper evaluates variant accuracy, not
  phase), the net panel was replaced (author: "do it"). Fig. 3c = genotype errors phased: calls at
  positions with a homozygous v5.0q record that each tool phased (background + that tool only):
  LongPhase 2 14,444 / 9,828 / 8,497, WhatsHap 27,135 / 13,706 / 11,815 at 10/30/60× (1.4–1.9×).
  Fig. 4d,e gains the row "v5.0q regions not in v4.2.1" (region `v5only`): WhatsHap and HapCUT2
  5.6–9.3× and 7.5–12× the LongPhase 2 rate (15–41 LongPhase 2 errors) vs 1.7–2.6× and 2.1–9.8× in
  the shared regions. Results: genotype-error paragraph (other allele 1.3–1.4×, no record
  1.3–1.4×), depth paragraph adds the ≥ 2× coverage share (28% / 17% at 30/60× for calls left
  unphased by LongPhase 2 alone vs 7% / 2%) with the GIAB paralog-mismapping citation, and the
  regions-added sentence; one Discussion sentence. F1 (harmonic mean of precision and phased
  fraction): LongPhase 2 higher in all 64 paired runs, by 0.8–1.0 points at 10–18× and 0.3 at
  50–60×; new F1 column in Supplementary Table 8, a sentence in Results, defined in Methods; not a
  panel (derived from a and b). Issue #8 dropped: `assembly_split.py` deleted, `\todo` removed.
- 2026-10-09: Fig. 4d,e gains the row "v5.0q regions also in v4.2.1" (region `shared`) directly
  above "v5.0q regions not in v4.2.1", so the GIAB v5.0q contrast (WhatsHap / LongPhase 2 1.7–2.6×
  in shared regions vs 5.6–9.3× in added regions, all ten coverages) reads in adjacent rows; the
  region analysis stays in Fig. 4, not Fig. 2 (it needs both benchmarks, and Fig. 2 is organised by
  evidence type). Fig. 4 legend d,e updated; one number-free sentence in the Fig. 2 Results
  paragraph points to Fig. 4d,e.
- 2026-10-09: Fig. 4d,e row labels in forest-plot form: "v5.0q benchmark regions" with four
  indented subsets ("Outside difficult regions", "Segmental duplications", "Shared with v4.2.1",
  "Added in v5.0q"), left-aligned, and "Outside both benchmarks" below the dashed line; the
  repeated "v5.0q regions," prefix and the in-panel "(exploratory)" were removed (the legend keeps
  "exploratory"). Legend d,e reworded to match.

**Figs. 3 and 4 swapped, 2026-10-09 (author decision).** The two-benchmark figure is now Fig. 3
(`fig3_two_benchmarks.pdf`, `fig3()`, `fig:benchmarks`) and the completeness figure Fig. 4
(`fig4_phased_unphased.pdf`, `fig4()`, `fig:unphased`). Reason: after the Fig. 2 result, the
largest risk for a reviewer is that v4.2.1 shows only 1.2–1.3-fold at 30–60×; the completeness gap
(about 1 point) is the smaller risk and follows. Fig. 3d,e also tells where the advantage occurs,
directly after Fig. 2. Rejected: the benchmark figure before Fig. 2 (the first data figure would
show near parity, Fig. 3b repeats Fig. 2a, and the v4.2.1 interpretation is untested). Old Fig. 3
stays a main figure. Results: the benchmark paragraphs moved before the completeness paragraphs
("Both tools received" → "All three tools received"); text and figure contents unchanged.
Literal references updated in Methods (now `\ref`), the Supplementary Data 1 paragraph (Fig. 4b,c)
and CLAUDE.md. Historical entries above keep the old numbers. Open: integration of Fig. 4 with
Fig. 5 (HiFi), both thin; under discussion with the author.

**Fig. 5 (HiFi) merged into Figs. 2 and 4, 2026-10-09 (author decision, option C of a design
discussion).** Main figures go from five to four, one message each: Fig. 2 accuracy and contiguity,
Fig. 3 benchmarks, Fig. 4 completeness.
- **Fig. 2** gains a fourth row, "SNV phasing, PacBio HiFi" (j switch error rate, k Hamming distance,
  l switch error rate against N50; LongPhase 2 vs WhatsHap, one replicate per coverage, 10–50×).
  j and k use the same axes as the nanopore rows; l has its own N50 axis (0–0.7 Mb), stated in the
  legend. The HiFi N50-by-coverage panel (old Fig. 5c) is replaced by the path in l. Height
  150 → 198 mm; `main.tex` limits it to 0.64\textheight in the draft so that the legend fits.
- **Fig. 4** gains b, HiFi completeness (old Fig. 5d); precision and genotype errors move to c and d
  and are titled "nanopore" because no HiFi precision or genotype-error counts exist.
- Rejected: option A (Fig. 4 as two rows, nanopore completeness and all HiFi metrics; two messages
  in one figure) and C' (HiFi row in Fig. 2 only; Fig. 4 stays thin).
- Results: the HiFi paragraph moved to directly after the MethPhaser paragraph (Fig. 2j–l); its
  phased-fraction clause moved to the completeness paragraph with the HiFi trend (87% at 10× to
  92% at 20–50×, Fig. 4b, Supplementary Table 11). `fig5()` and `figures/fig5_hifi.pdf` removed.
  Literal references updated: Methods (Figs. 2–4, Fig. 4c,d), Supplementary block-N50 paragraph
  (Figs. 2c,f,i,l) and Supplementary Data 1 paragraph (Figs. 2–4, Fig. 4c,d).

**Supplementary Fig. 16 promoted to Fig. 4e–g, 2026-10-10 (author decision, option A of a design
discussion).** Reason: Fig. 4 was the thinnest main figure, and no main figure showed what the
network withholds, although the title says "uncertainty-aware". Fig. 4 now has two rows with row
headers and keys as in Fig. 2: row 1 "Calls phased by LongPhase 2 and WhatsHap" (a–d as before;
d title shortened, its detail moved to the y-label), row 2 "SNVs unphased by GNN correction"
(e v5.0q status by coverage, f inside or outside the T2T-HG002 1:1 alignment at 60× against a
random sample of phased SNVs, g the same by chromosome). Greys in e and f: light = cannot be
verified (absent from v5.0q; not aligned 1:1). The in-panel numbers of the old Supplementary
Fig. 16 (totals, 92.6%, 88.2%) were removed (no text inside panels); the "aligned, no record"
split is in the text and Supplementary Table 12 only.
- Results: the two paragraphs on SNVs unphased by GNN correction moved from Part 2 to the end of
  the Fig. 4 text, with one new sentence: they are 15–18% of the calls that LongPhase 2 alone
  left unphased at 10/30/60× (`lp_only_gnn / lp_only`, issue6_composition.tsv), the rest were
  left unphased before correction. Methods and the Supplementary Data 1 paragraph updated;
  Supplementary Fig. 16 and `suppfig16_gnn_removed.pdf` removed (last figure, so no renumbering;
  Supplementary Table 12 stays). `sfig15()` (which drew it) is merged into `fig4()`.
- Considered and not promoted: held-out chromosomes (Supplementary Table 15; an accuracy result),
  read depth (Supplementary Fig. 12; source of the excess depth undetermined), GNN with/without
  (Supplementary Fig. 13; reverses the 2026-10-06/08 decisions and invites a matched-retention
  comparison), reciprocal sets (Supplementary Table 17; rejected earlier as old Fig. 3e).
- Open: runtime (Supplementary Table 16) supports an abstract claim but has no display item; data
  exist at 10× and 60× only. Author decision (2026-10-10): plot runtime across coverage from the
  logs of the paper runs, which hold GNU `time` output at every coverage; no per-chromosome runs
  of WhatsHap or HapCUT2 (they have no thread option, so CPU time goes next to wall time, and
  Methods says that a per-chromosome split shortens their wall time but not their CPU time).
  `notes/runtime/build_runtime.py` now reads all ten coverages; issue #8 asks JHL to run it and,
  optionally, to time LongPhase 2 on one thread at the eight other coverages (about 2 h).

**MethPhaser Results sentences corrected, 2026-10-10 (issue #5, author request).** JHL's rerun
(`eed8109`, `notes/methphaser/`) showed that the old MethPhaser values were its input: 0.0.3 crashed
in every `methphasing` call and the wrapper ignored the exit status. MethPhaser 0.0.4 joins blocks
(no change of phase within a block, phased SNVs unchanged). Check of the rerun: input rows = `SNV_Detail`
`longphase_v2.0.1` replicate 1, LongPhase 2 rows = `co-phase_Detail` `Mod` replicate 1, one assessed
pair added per join. New problem (reply on issue #5): on 3–4 chromosomes per coverage the MethPhaser
block sum exceeds the chromosome length (chr11 at 30×: N50 132.5 Mb), so blocks overlap, and at
30–60× the chr1–22 block sum exceeds the autosome length (the rule that removed the Ralphi N50).
JHL is asked for the cause (MethPhaser itself, or the local `str()` patch or `fix_methphaser_vcf.py`).
- Results (MethPhaser paragraph): every sentence that did not depend on N50 is corrected — switch error
  rate 1.5–1.7-fold lower (was 1.4–1.5), Hamming 1.4-fold lower at 10× and 2.0–2.9-fold at 20–60×
  (was a gap that shrank to 0.2 points), "MethPhaser returned its input blocks unchanged" removed,
  its joins add 2–15% switch errors to the input, joint phasing without GNN equals the input within
  2%, GNN correction accounts for 63–95% of the switch-error gap. The two N50 claims (3–11% longer
  at 20–60×; 2–13% longer before GNN, attributed to 5mC during phasing) are wrong in direction but
  wait for the N50: one red `\todo` replaces them. Numbers in a `[provenance]` comment.
- Not yet changed: Fig. 2g–i and Supplementary Fig. 11 (`make_results_figs.py` `METH`,
  `meth_value()` still hold the input values, so the text and Fig. 2h now disagree), the
  Supplementary Table 5 command line, `notes/SUSPECTED_ERRORS.md` item 1 (left open), the
  `twolinin/longphase` README (SNP+Methylation).

**GNN revisions by YMYEH merged, 2026-10-10 (`GNN_revisions_YMYEH_1010.zip`, based on `d765603`).**
Three-way merge into the current text; the `_YMYEH_1010` file names, the review-copy code in
`make_supp_figs.py` and the `% [YMYEH]` review comments were dropped. Every technical change was
checked against v2.1 (`../longphase`) and `GNN source/train_gnn_29.py`:
- Target: the GNN predicts label-defined phase-disagreement onsets (isolated disagreements and the
  first variant of a disagreeing run), the positives of the binary labels; the score is called the
  onset score. Author decision (2026-10-10): his wording also in the abstract, Introduction,
  Fig. 1c,d legend, Results opening paragraph and Discussion ("onset-prediction score").
- Methods GNN section reordered (target, window, features, branches, scoring zone, unphasing,
  training, labels, checkpoint, threshold, inference); the "GNN correction and phase-set update"
  subsection is merged into it. New: the four feature groups; local GATv2 vs global attention roles;
  binary mode in training and inference; correct nodes resampled per minibatch (`BalancedFocalLoss`);
  S = R(2 − 1/P) = (TP − FP)/(TP + FN), per threshold, P − 1 when P ≤ 0.5 (`net_gain_score`).
- Supplementary Method 4 / Tables 1, 3: gt_ref/gt_alt = first/second GT component
  (`PhasingProcess.cpp:439`); genomic context from the reference and the variant positions (the
  reference is mandatory in `phase`, `Phasing.cpp:230`); running mean only over windows whose
  scoring zone holds the variant (`PhasingProcess.cpp:815–825`); the isolated-node sentence removed
  (every node has a self-loop, `PhasingProcess.cpp:788` and PyG `GATv2Conv` defaults, so the
  no-incoming-edge branch in `GNNModel.h:291` is never reached).
- Supplementary Figs. 4–6 regenerated: "onset score" labels, signed r in Fig. 5, "isolated nodes"
  row removed from Fig. 6 (SVGs identical to YMYEH's).

**Todo triage, 2026-10-10 (author).** Removed as not blocking: the Methods `\todo`s on the per-run
threshold sweep and trade-off panel (Supplementary Method 4 gives the criterion and the result), on
region-filter commands and a metric table (scoring used no benchmark BED; Methods and Supplementary
Method 6 define eligibility, numerators, denominators and blocks), and on the v5.0q chr1–22 command
and source data (author: a Nature paper does not print the awk command; the chr1–22 restriction is
stated in Methods and Supplementary Table 5; the awk provenance comment stays).
- Supplementary Fig. 9 (calibration placeholder) removed with its `\todo` in Supplementary Method 3;
  no sentence cited it. Supplementary Figs. 10–15 are now 9–14: literal references renumbered in
  `sections/results.tex`, `Supplementary.tex` (Supplementary Data 1), source comments,
  `make_results_figs.py` section headers and CLAUDE.md. The PDF file names (`suppfig10_*`–`suppfig15_*`)
  keep their old numbers. Earlier entries in this log use the old numbers.
- Still open: the MethPhaser N50 sentence (waits for JHL, issue #5), SV and 5mC counts to
  Supplementary Data 1 (`q10_sv_mod.tsv`), `analyze_unphased.py` and the training/analysis scripts
  in the public repository.
- Supplementary Method 2: the scanner-constant `\todo` replaced by a "Choice of constants" paragraph
  (author: inspection of HG002 clipping profiles at CNV segments with many false SNV calls, no sweep;
  A from the read length; absolute counts at every coverage; sensitivity not assessed).
- Supplementary Method 2, "State": the ramp state no longer cites breakage–fusion–bridge cycles (a
  tumour-genome mechanism; the scanner was designed on HG002, author 2026-10-10).
- Supplementary Table 5, MethPhaser row: command line added from `notes/methphaser/README.md`
  (haplotag v2.0.2, primary records, `meth_phaser_parallel` `-vc`/`-g`, post-processing, the local
  `str()` fix and the VCF repair by `fix_methphaser_vcf.py`).

**MethPhaser rescored after the PS-lookup fix, 2026-10-10 (issue #5, JHL `5fb01f5`).** The overlapping
MethPhaser blocks came from `PS=-1` written by the first local patch; the current patch finds the block
from the record position. Phased SNVs unchanged; no overlap left.
- Results: Hamming distance "2.0–2.9-fold" → 2.1–3.0-fold at 20–60×; the N50 `\todo` replaced by one
  sentence: MethPhaser blocks 1.1-fold longer at 10× and 1.3–1.8-fold at 20–60× (0.96–5.49 versus
  0.88–3.09 Mb). Switch error rate (1.5–1.7-fold), joins (+2–15% switch errors; Hamming ×1.04 and
  1.8–2.8), GNN share (63–95%) and phased fractions (within 0.2 points) re-read and unchanged.
  `[provenance]` comment rewritten with the new values.
- Fig. 2g–i and Supplementary Fig. 10 now plot MethPhaser's own output: `results_data.load()` reads the
  `MethPhaser` sheet (`D["meth"]`); the `METH` constants (= the input run) are gone. The nanopore N50
  axis of Fig. 2c,f,i is 0–5.9 Mb (was 0–4.6) so that MethPhaser at 50–60× stays in the panel. No
  other figure changed (pixel comparison).
- Supplementary Table 5, MethPhaser row: the local fix is now described as the PS-lookup fallback.
- `make_results_figs.py` section headers corrected to the current Supplementary figure numbers.

**Runtime across coverage, 2026-10-10 (issue #8, JHL `baf32b1`).** `notes/runtime/runtime.tsv` now has
replicate 1 at all ten coverages from the GNU `time` output of the paper runs. Missing: HapCUT2 at 30× and
40× (logs overwritten on 2026-07-18 by a rerun stopped after 3–5 s); LongPhase 2 on one thread exists at
10× and 60× only (optional step 2 not done).
- New Supplementary Fig. 10 (`sfig_runtime()`, `suppfig_runtime.pdf`): wall-clock time, CPU time and peak
  memory across coverage; HapCUT2 line broken at 30–40×, LongPhase 2 one thread as points. It is cited
  between Supplementary Figs. 9 and 11, so the former 10–14 are now 11–15 (literal references in Results,
  Supplementary Data 1, source comments, `make_results_figs.py` headers and CLAUDE.md). The Supplementary
  Data 1 paragraph cited read depth as "Supplementary Fig. 12" after the Fig. 9 removal (should have been
  11); after this shift it is correct again.
- Supplementary Table 16: one row per coverage, four groups (LongPhase 2 24 threads, LongPhase 2 one
  thread, WhatsHap, HapCUT2) × wall, CPU, memory; "--" where no value exists.
- Results: wall time 4.6–17.6 min (24 threads) vs 25.2–113.8 (WhatsHap) and 24.1–96.4 (HapCUT2); CPU time
  1.8-fold less than WhatsHap at 10× and 2.6–4.5-fold at 12–60×, 1.8–2.8-fold less than HapCUT2; CPU
  growth 2.5- vs 4.5- and 4.0-fold; one thread unchanged (8.1 and 18.0 min); memory 36.0–63.0 GiB with 24
  threads. Abstract ("five- to sixfold faster on one thread at 60×") unchanged and still correct.
- Methods: timing per coverage from the paper runs, one-thread runs with no other jobs, HapCUT2 30–40×
  not available, and why CPU time is reported next to wall time (no thread option; a per-chromosome split
  shortens wall time only).
- Note: the 24-thread LongPhase 2 wall time is irregular (10.2 min at 20× after 6.6 at 18×; 16.3 at 60×
  below 17.6 at 50×) while its CPU time rises smoothly; the text therefore carries the trend with CPU time.
- Supplementary Data 1 paragraph now lists the `MethPhaser` sheet (issue #5).

**Results and Discussion revision, 2026-10-10 (Codex; final author-approved structure).**
Results has six declarative, unnumbered subsection headings and no run-in headings:
overview, phaser comparisons, benchmark context, completeness and genotype errors,
GNN-unphased SNVs, and internal modules. The final section's opening transition
preserves the comparison-then-modules order. Paragraph openings state the findings;
CLAUDE.md and the Results structure comment record this convention. Discussion has
seven focused paragraphs without subheadings: contribution, uncertainty measures,
retention trade-offs, truth-set disagreement, benchmark extent, generalization, and
remaining scope/downstream tests. Results figure pages are flushed before Discussion.

The comparison heading covers evidence types and sequencing platforms without claiming
similar contiguity for every comparison or universal superiority over Margin. The
Ralphi paragraph reports its higher switch error rates; the accuracy/contiguity
trade-off applies to Margin only. Ralphi's block N50 is not comparable (Supplementary
Table 8 and Supplementary Fig. 9c). The MethPhaser paragraph explicitly attributes the
lower Hamming distance to LongPhase 2. The genotype-error heading names WhatsHap;
the assembly heading specifies 60×; and the one-third reduction refers to genome-wide
SNV switch error rates. Repeated heading claims were removed from the assembly and
internal-module paragraph openings.

The revision separates accuracy from contiguity, completeness from call composition,
and assembly findings from their limitations. It clarifies identical SNV inputs,
modcall, GNN prediction versus subsequent unphasing/block splitting, and the separate
sources of training reads and labels. The accepted Hamming-denominator correction is
991–1,565 assessable benchmark-matching SNVs. Numerical anchors retained include the
uncorrected accuracy/contiguity comparison (1.9–2.5-fold lower rates, N50 3% shorter to
7% longer), CPU-time growth (2.5/4.5/4.0-fold), 8–31-fold lower indel-pair rates, and
2.1–10-fold lower rates inside v5.0q benchmark regions. The previously checked
13–25-fold ratio uses assessed benchmark-matching calls (23,690/19,996/24,719 versus
1,549/1,565/991); CPU-time growth uses 816→2,067 s, 1,504→6,817 s and 1,443→5,754 s.
Within-BED comparisons use rates per assessed pair with both variants inside the BED.

Benchmark-absence cautions, uncertain-region limits, unverified truth-set disagreements,
the explicit 60×/90× depth definition, citation keys, figure references and the SV/5mC
data-deposit TODO remain. The 15–41 errors remain neutral count context. No data,
figure artwork, Methods or Supplementary content changed in this editorial revision.

Validation: main.pdf rebuilt with TeX Live (26 pages); revised Results pages rendered
and inspected. Exactly six subsection headings and no paragraph headings. No undefined
references/citations or missing characters. Existing title/affiliation overfull and
caption underfull warnings remain. git diff --check passes.

**Supplementary structure and wording, 2026-10-10 (Codex; revised review plan).**
- Added all six Supplementary Methods to the contents page.
- Method 3 now separates the tuned constants from their selection history and refers
  to the main Methods for the voting rule and base-quality weighting. The same-individual
  tuning and non-held-out chromosome caveats remain explicit. Constants now use plain
  names rather than unused parameter symbols; their values are unchanged. Supplementary
  Fig. 2b points to the main Methods for the voting rules.
- Method 4 keeps the main Methods' use-first, training-second order. Its title now
  names features, architecture, inference, training, threshold selection and export. Scoring-zone
  and inference details have their own paragraph, and training augmentations follow
  labels and class balance/loss. Model values, equations and selection criteria are unchanged.
- Method 6 separates block intersection, switch errors/flips, Hamming distance,
  phased fraction and block N50. Each metric carries its own denominator; the duplicate
  switch-rate definition is removed. N50 now explicitly excludes query phase sets with
  fewer than two variants and uses their first-to-last variant spans independently of
  truth/query intersection, consistent with `../longphase/CompareProcess.cpp:487-504`.
  Method 6 starts on a fresh page to keep its heading with the metric definitions.
- Supplementary Data 1 has an unnumbered two-column inventory of its 11 sheets,
  defining all six composition codes (`lp_only`, `wh_only`, `lp_only_phase`,
  `lp_only_gnn`, `both`, `background`), run coverage and figure/table links. The
  distinction between `both` (unphased by both) and `background` (phased by both) is
  explicit, with their corresponding Table 17 row labels.
  Calls left unphased by both tools are correctly limited to the composition and depth
  sheets; the intervals sheet contains the two tool-only groups. The inventory uses
  `tabular`, so it does not advance the table counter.
- Shortened the Table 17 caption in `figures-source/make_results_figs.py` and ran
  its `tables()` function to regenerate `figures-source/supp_tables.tex`. The caption
  retains the call universe, benchmark categories, graph/GNN stage split and three-part
  table description; it refers to main Methods, "Analysis of unphased SNVs", for
  wrong phase, switch-error intervals and expected share. The caption now defines
  fold as inside divided by expected. No definitions were moved.
- Converted Table 5 to `longtable` with continuation headers and a wider Notes column,
  retaining every row verbatim. It now fits on page 12, including the full LongPhase 1.0
  commit and LongPhase 2 v2.1 commit `46ba470`, without footer overlap or clipping.
  Table 6 starts on page 13; the tables are in the correct order.

Validation: Supplementary.pdf rebuilt (36 pages; previously 35) and main.pdf rebuilt
(26 pages) with TeX Live. Revised Methods, contents, Tables 5–6 and 17, and Data 1 pages
were rendered and inspected. All 17 table labels/numbers are unchanged. All Table 5
rows are unchanged. The generated Tables 7–17 diff contains only the Table 17 caption;
all data rows are unchanged. Main PDF text is identical to the previous committed PDF.
No undefined references, undefined citations or missing characters; `git diff --check`
passes. The former Table 5 height warning is resolved. The existing Table 17 middle
column-width warning (9.25 pt), main title/affiliation and underfull warnings remain.
No figure artwork, numerical results, main manuscript source or internal notes changed.

**Fig. 2 cleanup, 2026-10-12 (author review).** Data origin checked per row: a–c `SNV_Detail` SNV-only
runs; d–f `co-phase_Detail` `Indel` (SNV + indel only; `item3_indel.tsv` `longphase_coh_indel_gnn` and
`whatshap_v28` match it in phased SNVs and SNV switch rate); g–i `co-phase_Detail` `Mod` replicate 1 and
the `MethPhaser` sheet; j–l HiFi `SNV_Detail`. Changes: (1) no s.d. bands in any Fig. 2 panel (they were
visible in b and e only, not in a or d; `line(band=False)`); (2) the dashed `Indel+Mod+SV` path removed
from f, so each row shows only the evidence of its title; (3) d now shows only the indel-pair switch
error rate and e the indel Hamming distance, two lines each (the SNV-pair lines in d had no match in e).
Legend and Results updated: the SNV-pair 3.0–3.7-fold claim cites Supplementary Data 1, the SV + 5mC
block-length sentence cites Supplementary Fig. 15, Supplementary Table 10 and Supplementary Data 1.
- Revised the same day (author): d and e again show SNVs (solid) and indels (dotted) in both panels —
  d SNV pairs and pairs with an indel, e SNV and indel Hamming distance. The SNV Hamming distance of
  the SNV + indel runs is calculated, not scored (`_indel_runs()`; SNVs in one-variant blocks not
  removed, error < 0.3%). Open: rerun `aggregate.py` on the lab server to write the exact SNV
  Hamming (`ham_all`, `ham_n` of `out/*.tsv`) into `item3_indel.tsv`. Results now say that indel
  and SNV Hamming distances are close (LongPhase 2 within 0.1 points, WhatsHap 0.4–0.7 higher).

**Fig. 2c evidence-type panel, 2026-10-13 (author decision, option A of three).** The accuracy–contiguity
panels of the SNV and indel rows (former c and f) are one tall panel, c, spanning both rows: SNV switch
error rate against block N50 for LongPhase 2 with SNVs, SNVs + indels, and SNVs + indels + SVs + 5mC
(`co-phase_Detail` `Indel+Mod+SV`), and for WhatsHap with SNVs and SNVs + indels. Marker = tool, line style =
evidence (solid SNVs, dashed + indels, dash-dot with filled markers for all four classes); no HapCUT2
(author: it is in a and b). Message: each evidence class lengthens the blocks of LongPhase 2 at a small
switch-error cost, and with all four classes it reaches the block N50 of WhatsHap with indels (4.10 vs
4.19 Mb at 60×) at a 3.6-fold lower SNV switch error rate. Rejected: B (row 2 as an all-evidence row,
indel Hamming to the Supplementary) and C (HiFi row out of Fig. 2). Panels are now a–k: d,e unchanged;
5mC row g–i → f–h; HiFi row j–l → i–k. Results (Fig. 2c added to the evidence-class sentences at the
SNV, indel and post-correction paragraphs), legend and Supplementary Data 1 description (Fig. 2f–h)
updated. Supplementary Fig. 15 still shows all seven configurations with and without GNN correction.

**Fig. 2 two-row layout, 2026-10-13 (author decision).** The four-row figure (11 panels, four row keys,
a five-entry legend for c) carried too much. Now two rows, seven panels: row 1 a SNV switch error rate
(former a), b SNV + indel switch error rate (former d), c evidence-type accuracy–contiguity (unchanged);
row 2 d,e SNV + 5mC vs MethPhaser (former f,h), f,g HiFi (former i,k). One figure-level key at the top
(tools; line styles of b and c by panel letter) replaces the row keys and the c legend; the dotted
indel lines in b now have hollow markers, so filled markers mean four-class phasing only. The
Hamming-distance column (former b, e, g, j) is new Supplementary Fig. 16 (`sfig16()`), added at the end
so that no Supplementary figure is renumbered; it keeps the HiFi 50× value at which LongPhase 2 has the
higher Hamming distance visible. Legend, Results panel letters and Hamming citations (Supplementary
Fig. 16a–d; MethPhaser also Supplementary Fig. 11c), Supplementary Data 1 description (Fig. 2d,e;
Supplementary Figs. 9 and 11–16) updated. Height 198 → 122 mm.
- Superseded the same day by **proposal A** (author: a five-panel draft with the key in an empty slot
  was rejected as ugly; six panels preferred). Fig. 2 is a 3 × 2 grid, one type of plot per row: row 1
  switch error rate against coverage — a SNV (WhatsHap, HapCUT2), b SNV + indel, c PacBio HiFi; row 2
  switch error rate against N50 — d by evidence type (former c), e SNV + 5mC vs MethPhaser, f HiFi
  (own x-axis 0.025–0.2%). Title on the panel-letter line (`letter(..., title=)`, placed by `save()`),
  tool key at the top, line-style keys inside b and d, lines 0.75 pt and markers at 0.8 size
  (`_light()`). HapCUT2 is now solid in every figure (`STY`), so dashed means "+ indels" only.
  Supplementary Fig. 16 (`suppfig16_fig2_coverage.pdf`) is a 5mC switch error rate against coverage
  (former Fig. 2d) and b–e the Hamming distances. Results letters: evidence panel c → d, HiFi
  i/f → c, HiFi N50 → f, 5mC switch error rate → Supplementary Fig. 16a, Hamming 16a–d → 16b–e.
  Height 104 mm.
- Same day: Fig. 2 d and e swapped (d SNV + 5mC vs MethPhaser, e evidence-type summary), so that each
  evidence class is met before the panel that combines them and e sits below b (same WhatsHap runs).
  The first Results section was condensed from ten paragraphs (about 1,050 words) to five (about 620),
  cited in panel order a–f: SNV (a; held-out chromosomes, Margin/Ralphi and runtime as one sentence
  each), indels (b), HiFi accuracy (c), 5mC vs MethPhaser (d), contiguity by evidence type and on HiFi
  (e, f). Removed detail is listed in the `[provenance]` comment at the end of the section.

**Opening SNV comparison, 2026-10-13 (author review).** Replaced selected coverage endpoints
and coverage-specific fold differences with switch error rate ranges for LongPhase 2, WhatsHap
and HapCUT2, plus fold-reduction ranges over all tested coverages. Removed the paired-replicate
claim from this paragraph and retained Supplementary Table 8. Other Results sentences are unchanged.

**Results metric explanation and flow, 2026-10-13 (author review).** Added a brief distinction
between block-wise Hamming distance (fraction of misassigned variants) and switch error rate
(errors in phase relationships between consecutive variants). Merged the newly covered-region
comparison into the benchmark section and made the v5.0q-versus-v4.2.1 region definition explicit.
Moved the chr17/21/22 comparator result to the GNN evaluation paragraph, which now identifies
these chromosomes as excluded from GNN training. Retained the figure and table references.

**Hamming explanation shortened, 2026-10-13 (author review).** Replaced the separate metric
explanation with a comma-delimited phrase directly after block-wise Hamming distances:
"reflecting the fraction of misassigned variants within blocks".

**Hamming apposition, 2026-10-13 (author review).** Removed "reflecting" from the inline
explanation, leaving "the fraction of misassigned variants within blocks" between commas.

**Secondary phaser placement and scope, 2026-10-13 (author review).** Moved Ralphi/Margin
results to an independent closing paragraph of the first comparison subsection and grouped
the GCphase exclusion there. Checked local data, Git histories, worklogs and GitHub, including
the newer remote workbook: all three have only 60 ONT runs at 10–20×. Original data commit
`8ff180b` states that blank cells are runs not performed. No reason for the 20× limit was
found. Methods now states the coverage scope and corrects GCphase input handling. See
`notes/secondary_phaser_audit_2026-10-13.md` for evidence and the remote chr20 GCphase diagnostic.

**Secondary comparisons hidden, 2026-10-13 (author decision).** Commented out the standalone
Ralphi/Margin/GCphase Results paragraph and removed the Margin interpretation from rendered
Discussion, retaining it in a source comment. No replacement Discussion paragraph was added.
Supplementary data and methods remain available.

**Runtime sentence condensed, 2026-10-13 (author review).** Replaced detailed timing, thread
counts and memory ranges in the opening comparison paragraph with one sentence stating shorter
wall-clock time with multithreading, lower CPU time and higher peak memory. Numerical results
and execution settings remain in Methods, Supplementary Fig. 10 and Table 16.

**Runtime placement, 2026-10-13 (author review).** Moved the concise runtime sentence after
all accuracy and contiguity comparisons, at the end of the first phaser-comparison subsection.
Specified nanopore SNV phasing there to keep its scope clear after the HiFi and co-phasing results.

**Comparison paragraphs consolidated, 2026-10-13 (author review).** Reduced six paragraphs
to four: nanopore SNV/indel accuracy, HiFi accuracy, SNV/5mC comparison, and contiguity with the
short runtime sentence at the end. Joined the SNV and indel results with "When indels were
included". Removed the forward-looking phased-fraction transition; numerical results are unchanged.

**Direct phrasing, 2026-10-13 (author review).** Replaced all six rendered "so that"
occurrences across Results, Methods and Supplementary Methods with direct statements or
compact descriptions. Updated the remaining figure-layout source comment as well. Numerical
claims and method definitions are unchanged.

**Results findings only, 2026-10-13 (author review).** Removed the MethPhaser setup sentence
(method description and supplied pre-GNN SNV input) from Results. The input setup remains in Methods.

**HiFi emphasis, 2026-10-13 (author-approved revision).** The HiFi comparison now opens
with the accuracy finding. Moved the use of the nanopore-trained network without retraining
to the GNN evaluation paragraph, beside the measured HiFi correction effect.

**LongPhase v2.1.1: retrained GNN model, all LongPhase 2 values updated, 2026-10-16 (JHL request).**
The manuscript now reports release v2.1.1 (`twolinin/longphase` `f9962dd`, PR #131) instead of
v2.1. The update corrects an error in the training of the v2.1 model; the differences in the
reported results are small (switch errors with GNN correction mostly 0–5% lower, the rest
unchanged in substance).

- **What was wrong.** The haplotype-swap augmentation exchanged the two allele nodes of every
  variant but kept each edge's vote weight from the node it came from, so the edge weights of
  half of the training windows did not match their nodes. Node features and labels were correct.
- **What was tried.** The model was retrained with the weights fixed, with two label
  definitions (benchmark matched by position, as before, or by position, REF and ALT), each with
  five seeds (42, 43, 44, 1337, 3407). All ten models were applied to the 60 nanopore runs at
  10–20× with the threshold set to the cost of the v2.1 model on chr15–16. The REF/ALT labels
  classified better but removed fewer switch errors on the held-out chromosomes; the
  position-matched labels were kept and seed 42 (best on the validation chromosomes) released,
  threshold 0.35. Details: `notes/gnn_retrain/` (`seeds.tsv`), Methods, Supplementary Method 4,
  Supplementary Tables 4 and 18 (new). The C++ module of v2.1.1 also has the GNN fixes of PR #131
  (GC/entropy as in training, singleton cleanup, merged 5mC nodes, SV features).
- **Every value that depends on LongPhase 2 with GNN correction was recomputed automatically**
  from new runs, by the same scripts as before (no hand-copied values):
  - nanopore, 7 configurations × 64 runs, rerun on `/disk` one at a time with `-t 24`
    (`/disk/research/v2.1.1/run.sh`); HiFi SNV-only 10–50× with the release binary;
  - `supplementary.xlsx`: `longphase_v2.1` blocks renamed `longphase_v2.1.1` and refilled
    (`SNV_Detail`, `co-phase_Detail`), `SV_5mC_phasing`, and the sheets that are one TSV each
    (`notes/v2.1.1/update_xlsx.py`, which first checked that every old sheet equals its v2.1
    source);
  - `20260924_GIAB421.txt`, `20260924_v50q.txt`, `20260924_cophase_v50q.txt`: GNN rows only;
  - `notes/benchmark_strata/` (items 3, 4), `notes/heldout/`, `notes/unphased/` (issue #6, #7),
    `notes/sv_mod/`, `unphase_validation_results.txt` (T2T), Fig. 4e composition,
    `notes/runtime/` (24 threads from the rerun; one thread re-timed);
  - every number in the text was recomputed by `notes/v2.1.1/claims.py`, which reproduces the
    v2.1 text from the committed v2.1 data before giving the v2.1.1 values;
  - the JSX drafts (`notes/v2.1.1/update_jsx.py`).
  Runs without GNN correction are unchanged (v2.1.1 `--disableGNN` reproduces them; checked).
- **Main changes in the text** (v2.1 → v2.1.1): abstract 2.8–4.8-fold → 2.9–5.0-fold fewer
  switch errors than WhatsHap and HapCUT2 (nanopore), HiFi 2.2–2.6 → 2.4–2.8-fold, four-class N50 gain
  44% (4.14 vs 2.87 Mb at 60×), "five- to sixfold faster on one thread at 60×" unchanged (now 5.1 and
  6.0-fold); v5.0q spread at 30–60× 4.3–4.8 → 4.3–5.0-fold; within v5.0q benchmark regions 2.1–10 →
  2.1–9.5-fold; T2T-validated unphased SNVs 56,076 → 62,230; runtime with 24 threads 4.6–17.6 →
  3.5–16.9 min and peak memory 36.0–63.0 → 19.3–30.1 GiB (GNN correction now runs inside `phase`),
  one thread 8.1/18.0 → 8.3/19.1 min (re-timed 2026-10-16, idle machine). Every other change is in
  the last digit. Each changed sentence keeps its provenance comment, with the v2.1.1 source added.
- **Corrected along the way:** "four-class phasing produced the longest blocks at every
  coverage" was already untrue at 50× in v2.1 (SNV+indel+5mC 0.1% longer); now also at 12 and
  30×, and the sentence says so.
- **Figures regenerated on the lab server with Liberation Sans (2026-10-16).** Arial is not
  installed here, so `figures-source/make_results_figs.py` was run on a copy of the repository with
  `"font.family"` set to Liberation Sans (same glyph widths as Arial, so the layout is unchanged;
  the script itself still says Arial). All of these were checked by eye against the v2.1.1 data;
  a run of the same script on the v2.1 data (a066c7e) differs from it in every one of them:
  - Fig. 2 `figures/fig2_phaser_comparison.pdf`, Fig. 3 `fig3_two_benchmarks.pdf`,
    Fig. 4 `fig4_phased_unphased.pdf`;
  - Supplementary `suppfig10_more_tools.pdf`, `suppfig_runtime.pdf` (24 threads from the rerun,
    one thread re-timed), `suppfig11_methphaser.pdf`, `suppfig12_giveup_depth.pdf`,
    `suppfig13_gnn_effect.pdf`, `suppfig14_cophase_gnn.pdf`, `suppfig15_cophasing_all.pdf`;
  - Supplementary Figs. 4 and 5 (`suppfig4_gnn_overview.pdf`, `suppfig5_gnn_window.pdf`,
    threshold 0.35) converted from their SVGs with headless Chrome (no `rsvg-convert` here).
  `figures-source/supp_tables.tex` from the same run equals the committed one.
- **Still to check or rebuild (author, writing machine):**
  - `main.pdf` and `Supplementary.pdf`: not rebuilt (no TeX here); run `make`;
  - the twelve PDFs above use Liberation Sans: `make results-figs` and `rsvg-convert` of
    Supplementary Figs. 4–5 on the Mac give the Arial versions if the font must match exactly;
  - runtime: done (below, HapCUT2 30× and 40× re-timed); `suppfig_runtime.pdf` is Liberation Sans too;
  - not data-dependent, no change needed: Fig. 1 and Supplementary Figs. 1–3 and 6–8 (their
    numbers are worked examples); `figures/supp/imagen/*.png` and
    `figures-source/longphase_parallel_consistent_v22.png` are old drafts not used by any `.tex`;
  - the nine JSX drafts: done, rendered to PDF (below); their PNGs are the old v2.1 versions;
  - not rerun: the held-out indel tables (`notes/heldout/`, SNV only was rescored);
    `input_md5.txt` of `notes/benchmark_strata/` still lists the v2.1 inputs;
    the slim data archive still holds the v2.1 VCFs.
- **Done: HiFi runtime of all three tools (2026-10-17).** LongPhase 2 (10–50×) and WhatsHap (10×,
  20×) re-timed on HiFi, one at a time on an idle machine, because the original runs had shared
  it (LongPhase 20× 25% CPU, WhatsHap 10–20× 73–82%); output identical to the original VCFs,
  details in `notes/runtime/README.md`. New `notes/runtime/runtime_hifi.tsv`; Supplementary
  Table 16 has a HiFi block (table caption and Methods updated). No Results sentence (the Results no longer have a runtime paragraph); the ratios are in
  a provenance comment (CPU time 4.0–7.8-fold less than WhatsHap, 3.2–5.1-fold less than HapCUT2).
  The HiFi JSX drafts (`HifiCompare*.jsx` and PDFs) now include HapCUT2. Figures of the
  professor (`figures/`, made by `make_results_figs.py`) are left as in 2511af2 (author request,
  2026-10-17: update the data and JHL's figures only): Supplementary Fig. 10 stays nanopore only and
  Fig. 4b keeps its two tools. If they are to show the HiFi runtime or HapCUT2, the data are in
  `notes/runtime/runtime_hifi.tsv` and `SNV_Detail`; the two-row Supplementary Fig. 10 code is
  in commit d022b71.
- **Done: HapCUT2 on the PacBio HiFi data (2026-10-16).** HapCUT2 1.3.4 (`--pacbio 1`) on the
  same per-coverage HiFi calls and BAMs, 10–50×, replicate 1, scored like the other HiFi runs;
  details, commands and the records HapCUT2 cannot read in `notes/hifi/README.md`. Changed:
  `supplementary.xlsx` `SNV_Detail` (the empty `hapcut2_v134` block of the HiFi rows, by
  `notes/hifi/add_hapcut2.py`; no other cell), Fig. 2j–l (HapCUT2 added; Liberation Sans),
  Supplementary Table 11 (HapCUT2 rows), abstract ("2.4- to 2.8-fold fewer than WhatsHap" →
  "2.4- to 3.5-fold fewer than both"), Results (HiFi paragraph: 2.9–3.5-fold lower than HapCUT2,
  Hamming of three tools; completeness: WhatsHap and HapCUT2 0.4–0.5 points more), Fig. 2 legend,
  Methods and Supplementary Table 5 (`--pacbio 1`, dropped records). Not changed: Fig. 4b
  (completeness, LongPhase 2 and WhatsHap only, as in Fig. 4a), the HiFi JSX drafts.
- **Done: HapCUT2 re-timed at 30× and 40× (2026-10-16).** The original logs of these two runs were
  overwritten in July, so the runtime table had no HapCUT2 value there. Both runs were repeated
  with the same binaries, commands and inputs, one at a time with no other job running
  (`/ssd/longphase_process/runtime/run_hapcut2_30_40.sh`); the phased genotypes are identical to
  the paper's VCFs (every record's chrom, pos and sample column). 30×: 59.4 min wall, 59.0 min CPU,
  11.3 GiB; 40×: 75.6, 75.2 min, 14.0 GiB. Changed: `notes/runtime/` (both build scripts, both
  TSVs, README), Supplementary Table 16 (`supp_tables.tex`) and Fig. 10 (`suppfig_runtime.pdf`,
  HapCUT2 line no longer broken), Results (CPU time 2.0–3.1 → 2.0–3.2-fold lower than HapCUT2,
  3.23 at 40×; "at every coverage" instead of "at the coverages with available timing data"),
  Methods and both captions (the re-timing replaces "not available"). Wall-time and memory ranges
  are unchanged.
- **Done: the nine JSX drafts rendered to PDF (2026-10-16).** The `.jsx` drafts at the
  repository root hold the v2.1.1 values (`notes/v2.1.1/update_jsx.py`; HiFi legend
  "LongPhase 2.1.1", phased-SNV axis widened to 86–93%). Instead of new screenshots, each draft is
  rendered to a vector PDF of the same name by `notes/v2.1.1/render_jsx_pdf.py` (headless Chrome,
  React 18 + Recharts 2; width = old screenshot width / 2; Helvetica/Arial replaced by the system
  font on the lab server, Libre Franklin as a web font in the two unphased drafts). **The PDFs are
  the current versions; the PNGs of the same name are the old v2.1 screenshots** and are kept
  only for comparison:
  - [x] `CophaseGroupCompare.pdf` (old: `.png`)
  - [x] `PhasingBenchmarkBars.pdf` (old: `.png`)
  - [x] `PhasingBenchmarkBarsRow.pdf` (old: `.png`)
  - [x] `PhasingBenchmarkCompare.pdf` (old: `.png`)
  - [x] `HifiCompare.pdf` (old: `.png`)
  - [x] `HifiCompare3.pdf` (old: `.png`)
  - [x] `MethPhaserCompare.pdf` (old: `.png`)
  - [x] `UnphasedComposition.pdf` (old: `.png`)
  - [x] `UnphaseVenn3.pdf` (old: `.png`; the "LongPhase only — phase" label of panel C, clipped
    in the draft and the old screenshot, now fits: left margin of that panel 118 → 130)


**Remote-data/local-writing merge, 2026-10-16 (author rule).** Synced to `a8f4237` and retained
local figure design and manuscript writing. All data use the remote v2.1.1 inputs; Figure 2
keeps the local two-row, six-panel layout (d MethPhaser, e evidence types), with remote HiFi
HapCUT2 values in c/f and Supplementary Fig. 16e. Local title, prose organization and hidden
secondary-phaser text are retained. Data-derived claims were refreshed, including claims
outside Git conflicts. Corrected the all-configuration indel-pair reduction to 22–40%.
Rebuilt the figures and both PDFs (27/39 pages); fixed table overflow with column spacing.
Full conflict inventory, calculations, data hashes and validation: `notes/sync_2026-10-16/`.
Original local work remains in stash `3cb51b087b8edc310a84069330f582adad04abbf`.

**Further phasers, 2026-10-17 to 2026-10-18.** Results and reasons in
"Comparison with further phasers" above; commands, inputs and full tables in
`notes/competitors/README.md`, run scripts in `notes/competitors/scripts/`. All replicate 1, the
paper's inputs, default parameters or the documented workflow, scored like `SNV_Detail`.
- Added runs:
  - nanopore 10–60×: LongHap 0.2.0 (SNVs with and without 5mC; all variant types with 5mC,
    Sniffles SVs made sequence-resolved by `merge_sv.py`), HapBridge ec48f02 on the MethPhaser
    input (`local_counter.patch`: two undefined debug counters, phasing unchanged), TinkerHap
    1.0.0, HapCUT2 with `--indels 1`;
  - HiFi 10–50×: HiPhase 1.7.0 and TinkerHap 1.0.0 with indels (their default) and on an
    SNV-only input VCF (neither has an SNV-only option; the PEPPER calls restricted to SNVs, the
    set WhatsHap `--only-snvs` phases), LongPhase 2.1.1 `--indels`, WhatsHap 2.8 with indels,
    HapCUT2 with `--indels 1`;
  - HiPhase timed on an idle machine (50×: 12.2 min wall, 187 CPU-min with indels; 10.4 and 173
    on SNVs only).
- Changed: `supplementary.xlsx` new sheet `Other_phasers` (71 rows, by
  `notes/competitors/build_sheet.py`; no other sheet changed); `Supplementary.tex` sheet
  inventory (13 → 14 sheets, row for `Other_phasers`); this README (section above).
- Not changed: main text, Methods, figures (including the JSX drafts) and every other
  Supplementary table. Whether and how to use these results is for the authors to decide.

**Abstract GNN sentence, 2026-10-19 (author request).** The two sentences on the method are one
sentence. The abstract no longer uses "phase-disagreement onsets" (author decision, replaces the
2026-10-10 rule for the abstract only); it says that the GNN unphases likely misphased variants.
The phasing-uncertainty clause is removed from the abstract: phasing entropy was built for the
GNN, so the abstract names only the GNN (author). The Introduction, Fig. 1 legend, Results and Methods keep the term.


**Sentence-level wording revision, 2026-10-19 (author-approved review).** Applied the
20 reviewed wording recommendations across the abstract, Introduction, Results, Discussion,
Methods, supplementary methods and Supplementary Table 12 caption. GNN correction is
defined by its operation; error-rate comparisons and threshold-selection terminology are
explicit; redundant narration and development-history phrasing are revised. Numerical
results and scientific limitations are retained. The four proposed paragraph-level changes
are deferred: the Introduction pipeline inventory, Results evaluation setup, unphased-SNV
Methods structure and Supplementary Table 18 caption are unchanged. The metric comparisons
also remain in their original paragraph. The Table 12 caption is synchronized with
`figures-source/make_results_figs.py`. Both PDFs rebuilt successfully (27 and 39 pages);
rendered revised pages checked, with no undefined references, missing characters or
overfull boxes in the build logs. No figure artwork was changed.

**Unphased-SNV Methods paragraph breaks, 2026-10-19 (author approval of change 3 only).**
Separated the existing analysis text into three paragraphs: GNN-removed SNVs, assembly
comparison, and the comparison between LongPhase 2 and WhatsHap. Only the opening wording
was clarified; all analysis definitions, numerical values and limitations were retained.
Changes 1, 2 and 4 remain deferred. Rebuilt `main.pdf` (27 pages), checked pages 22--23
visually, and confirmed no undefined references, missing characters or overfull boxes.

**Further phasers in the manuscript, 2026-10-19 (author request).** Used the `Other_phasers`
sheet (JHL, 2026-10-17/18) in the text; no new runs. New Supplementary Table 18 (`other_phasers_table()`
in `make_results_figs.py`): five comparison blocks (nanopore SNV + 5mC, SNV + indel, all classes +
5mC; HiFi SNV-only, SNV + indel), LongPhase 2 first in each block, with the switch error rate relative
to LongPhase 2; the GNN-model table is now Supplementary Table 19 (two references renumbered).
Results: one paragraph after the MethPhaser paragraph (HiPhase 1.7–1.9-fold, TinkerHap, HapBridge 1.5-fold,
LongHap 2.2–5.3-fold, with its 18–22% Hamming distances), ratios in its provenance comment; "three tools"
made explicit where the paragraph made it ambiguous; the runtime sentence now covers both platforms.
Methods: one passage on the four phasers in "Comparison with other methods"; the HiFi runtime
sentence rewritten to state that wall-clock times of the re-timed HiFi runs had the alignment file
in the page cache and that CPU time is the cross-platform measure (Table 16 caption to match, and it
now says LongPhase 2 was re-timed at every coverage). Discussion: one sentence after the LongHap
contrast (1.5–1.7-fold vs MethPhaser and HapBridge, 2.2–5.3-fold vs LongHap; most of the MethPhaser
gap from GNN correction). Supplementary Table 5: rows for HapBridge, LongHap, TinkerHap and HiPhase,
HapCUT2 indel runs. New reference `hartmann2025tinkerhap` (GigaScience 2025). Supplementary Data 1
paragraph: tables 7–11, 13, 14, 17 and 18. Rebuilt: main.pdf 28 pages, Supplementary.pdf 42 pages,
no undefined references, overfull boxes or missing characters.

**HiPhase in the HiFi comparison, 2026-10-19 (author decision: "HiPhase must be included as the
official PacBio phaser").** HiPhase 1.7.0 (SNV-only input VCF, sheet `Other_phasers`) is now a fourth
tool in Fig. 2c,f, Supplementary Fig. 16e and Supplementary Table 11 (`hiphase()` in
`make_results_figs.py`; teal, down triangle, in the top key). Layout and message unchanged. Results
HiFi paragraph: 1.7–1.9-fold vs HiPhase at every coverage; the Hamming sentence corrected for four
tools (LongPhase 2 lowest at 10, 30 and 40×, HiPhase at 20×, WhatsHap at 50×; LongPhase 2 is no
longer the highest at 50×). The further-phasers paragraph keeps only HiPhase with indels. Fig. 2
legend (c,f), Supplementary Fig. 16 legend (e), Table 11 caption and Methods name HiPhase. Fig. 4b
(HiFi completeness) also shows HiPhase (author, same day; key entry in row 1, legend and the Results
completeness sentence: HiPhase phased 0.2–0.3 points more benchmark SNVs than LongPhase 2, WhatsHap
and HapCUT2 0.4–0.5). Rebuilt: 28 and 42 pages, clean logs.
Related descriptions changed to match (author, same day): Fig. 4 row 1 title "Calls phased by
LongPhase 2, WhatsHap and HiPhase" and legend title; abstract HiFi clause now "1.7- to 3.5-fold
lower rates than HiPhase, WhatsHap and HapCUT2" (was 2.4- to 3.5-fold than both); `Other_phasers`
row of the Supplementary Data 1 table names the figures and tables that use the HiPhase values.

**HiFi precision in Fig. 4, 2026-10-19 (issue #9; author approved the figure first).** JHL counted
the phased heterozygous SNV calls on chr1–22 of the HiFi SNV-only runs (4393308,
`notes/unphased/phased_calls_hifi_chr1_22.tsv`). Fig. 4 is now a 4 × 2 grid without row titles:
a nanopore completeness, b nanopore precision, c HiFi completeness, d HiFi precision (LongPhase 2,
WhatsHap, HiPhase), e genotype errors phased, f–h SNVs unphased by GNN (former e–g). Every
`fig:unphased` panel reference in Results and Methods remapped (Methods had cited c for the
genotype errors; now e), legend rewritten, Supplementary Data 1 rows updated (Fig. 4b,d and 4e).
Results: one sentence after the nanopore F1 sentence (HiFi precision 92.2–95.0% LongPhase 2,
90.3–94.6% WhatsHap, 91.1–93.9% HiPhase; lead over WhatsHap 1.8 → 0.3 points, over HiPhase
1.1–1.5), values in its provenance comment. Supplementary Table 11 has a Precision column
(LongPhase 2, WhatsHap, HiPhase; -- for the others). Sheet `Phased_calls` now has a `platform` column
and the 15 HiFi rows (143 rows), from the new `notes/unphased/phased_calls_sheet.tsv`, which
`notes/v2.1.1/update_xlsx.py` now reads. Rebuilt: 28 and 42 pages, clean logs.

**Platform labels in Fig. 2, 2026-10-20 (author request).** Readers could not tell from the panels
or the Results that a, b, d and e are nanopore results. Every Fig. 2 panel title now starts with the
platform ("Nanopore: …", "PacBio HiFi: …"; e is "Nanopore: by evidence type"); each panel line of
the legend starts with "Nanopore data:" or "PacBio HiFi (Revio) data:"; the Results sentences for
a, b, d and e say "nanopore data" (SNV-only, indel, 5mC and block N50 sentences). No values changed.

**HapBridge and LongHap in Fig. 2d, 2026-10-20 (author decision).** The Introduction names four
methylation-aware tools, but Fig. 2d showed MethPhaser only. HapBridge and LongHap (SNVs with 5mC),
replicate 1 from the `Other_phasers` sheet (`meth_other()`), are now in Fig. 2d and Supplementary
Fig. 16a,d (HapBridge orange "P", LongHap green "X"; both in the top tool key). NanoMethPhase stays
out: it assigns methylation to an existing phase and has no switch error rate of its own. The LongHap
all-variant runs stay in Table 18 only (Fig. 2e already carries five lines). Results: the 5mC
paragraph now covers all three tools (HapBridge 1.5-fold switch error, 1.1–1.6-fold Hamming, N50
0.95–1.36-fold; LongHap 2.2–5.3-fold, N50 1.5–2.1-fold at 20–60× with 18–20% Hamming against
1.6–3.4%, 0.41 vs 0.88 Mb and 60% vs 78% phased at 10×; LongHap four-class 2.4–4.5-fold with
19.5–21.9% Hamming), and the HapBridge and LongHap sentences left the "not shown in Fig. 2"
paragraph. The earlier combined LongHap ranges (N50 1.3–2.1-fold, Hamming 18–22% vs 1.6–6.9%) mixed
the two configurations and were split. Fig. 2 legend (d), Supplementary Fig. 16 legend (a, d) and the
`Other_phasers` row of the Supplementary Data 1 table updated. No new runs.
