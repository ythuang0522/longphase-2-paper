# LongPhase v2.1.1: retrained GNN model, all LongPhase 2 values updated, 2026-10-16 (JHL request)

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
