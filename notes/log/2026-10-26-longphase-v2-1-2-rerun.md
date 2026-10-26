# LongPhase v2.1.2 rerun (JH), 2026-10-26

Moved from JH's README section of commit 1bd99b4 when it was merged with the local Fig. 3 work.

**LongPhase v2.1.2: faster and leaner release, SV block rule and bug fixes; affected runs repeated, 2026-10-26.**
The manuscript now reports release v2.1.2 (`twolinin/longphase` tag v2.1.2, `6b8f2dd`, PR #137) instead of
v2.1.1. The release changes three things that touch the manuscript: (1) `phase`, `modcall` and
`haplotag` use much less memory and time (PR #135); (2) with an SV file, a variant whose votes all come
from SVs starts a new block, so an SV is no longer the only link between two blocks (`--sv-join-blocks`
restores the old behaviour), and `--sv-threshold` is 0.20 with `--ont` (0.10 with `--pb`, as before);
(3) bug fixes: deletions supported by split alignments are phased (PR #136), SV alleles are no longer
removed by the copy-number filter, GNN correction keeps the phase of deletions of at least 10 kb with
unanimous votes, `modcall` takes calls at CIGAR operation boundaries from the right operation, and
`haplotag` deletion votes go to the right haplotype. Every run whose output can change was repeated; the
effect on accuracy is small and the gain is in memory and CPU time.

- **What was rerun** (`/disk/research/v2.1.2`, scripts in `/ssd/longphase_process/v2.1.2`):
  - nanopore, the five configurations with SVs or 5mC (SNV+5mC, SNV+indel+5mC, SNV+SV, SNV+indel+SV,
    all four), with and without GNN correction, all 64 runs (640 runs), with Sniffles 2.8.0 re-called
    with `--reference` and `modcall` re-run with v2.1.2 (the paper's calls had no `--reference`);
  - HiFi SNV+SV and SNV+indel+SV, 10–50× (issue #10, `notes/sv_phasing/`);
  - SNV-only and SNV+indel output does not change: the 71 SNV-only runs repeated for timing (64 nanopore
    `-t 24`, nanopore `-t 1` at 10× and 60×, HiFi 10–50×) are identical to v2.1.1 apart from the header,
    and so are the SNV+indel runs at 10–60× replicate 1. Their values are unchanged.
- **Accuracy** (`longphase compare` against v5.0q chr1–22, every run against the paper's;
  `/ssd/longphase_process/v2.1.2/cmp_paper.py`):
  - phased SNVs within ±0.01% in every run;
  - SNV switch error rate within ±0.002 percentage points per coverage mean (relative −5.1% to +2.3% per
    run); with SVs lower in 56 of 60 configuration × coverage means (2 equal, 2 higher by at most
    0.0002 points); block N50 −2.0% to +3.3%; Hamming −0.55 to +0.59 points;
  - SVs: wrong phase 8.21% → 8.19% of the matched SVs (replicate 1, 30 runs, T2T-HG002 truth).
- **Memory and time** (HDD, one run at a time, page cache cleared before each run; `notes/runtime/`):
  - nanopore SNV-only, 24 threads, 10–20× (60 runs, medians): wall 4.8 → 4.3 min (−11%), CPU 13.8 →
    6.3 min (−55%), peak memory 22.9 → 1.7 GiB (−93%); 60×: 15.5 → 14.8 min, 30.1 → 3.5 GiB;
  - one thread: 10× 8.3 → 3.2 min, 60× 19.1 → 12.8 min; peak memory 6.3 and 7.4 → 1.2 GiB;
  - HiFi 10–50×, 24 threads: CPU 6.0–14.3 → 2.5–10.0 min, peak memory 16.7–22.6 → 1.4–1.7 GiB;
  - against WhatsHap and HapCUT2 (their values unchanged): one thread 7.6–8.9-fold faster at 10× and 60×
    (was 2.9–6.0-fold); peak memory with 24 threads below WhatsHap's at every coverage except 12×
    (1.66 vs 1.62 GiB) and below HapCUT2's.
- **Updated automatically** (scripts in `notes/v2.1.2/`, each first checked that the old values equal
  the v2.1.1 sources; no hand-copied values):
  - `supplementary.xlsx` (`update_xlsx.py`, `update_variant_calling.py`, `notes/sv_mod/build_sheet.py`):
    `SNV_Detail` and `co-phase_Detail` block `longphase_v2.1.1` renamed `longphase_v2.1.2`; the Mod, SV,
    Indel+SV, Mod+Indel and Indel+Mod+SV rows of both LongPhase blocks (640 runs; the block without GNN
    correction keeps its label `longphase_v2.0.1`, now v2.1.2 `--disableGNN` for these rows);
    `Variant_Calling` heterozygous and homozygous SVs and heterozygous 5mC sites (new calls); `SV_5mC_phasing`;
    `Indel_accuracy`. The `LongPhase 2.1.1 (--indels)` HiFi rows of `Other_phasers` are unchanged (identical
    output) and keep their label;
  - `20260924_v50q.txt`, `20260924_cophase_v50q.txt`, `20260924_GIAB421.txt`: rows of the runs with SVs
    (`update_txt.py`);
  - `notes/runtime/` (`build_runtime.py`, `build_all_tools_runtime.py`), `notes/heldout/`,
    `notes/benchmark_strata/` (item 3), `notes/sv_mod/`, `notes/sv_phasing/` (issue #10);
  - figures from `figures-source/make_results_figs.py` (run on a copy with Liberation Sans, as for v2.1.1):
    Fig. 2 and Supplementary Figs. 10, 11, 14, 15 and 16 changed and were replaced; the others were rendered
    from the v2.1.1 data with the same script and environment and are identical to the v2.1.2 renders, so
    the committed files were kept (a re-render differs only in bytes). `figures-source/supp_tables.tex`:
    Supplementary Tables 7, 9, 10, 14, 16 and 18 changed; the caption of Table 16 now says that only
    WhatsHap at 10 and 20× on HiFi data was re-timed with the alignment file in the page cache;
  - the JSX drafts with LongPhase 2 values (`update_jsx.py`) and their PDFs (`render_jsx_pdf.py`).
- **Text** (numbers from `notes/v2.1.2/claims.py`, a copy of the v2.1.1 script run on the committed v2.1.1
  data and on this tree, and `claims_extra.py` for values it does not compute):
  - Results: MethPhaser 1.5–1.8-fold (was 1.5–1.7) and 1.4–3.1-fold Hamming (1.3–2.9), LongPhase 2 N50
    0.87–3.12 Mb, GNN share 66–95%; HapBridge 1.5–1.6-fold, Hamming 1.2–1.5-fold, N50 0.95–1.34-fold;
    LongHap 2.2–5.4-fold, N50 1.4–2.1-fold at 20–60×, LongPhase 2 Hamming 1.7–3.4%, N50 0.87 Mb at 10×;
    four-class blocks 6–21% shorter than WhatsHap with indels at 10–40× (within 1.4% at 50–60×);
  - Results, evidence classes: before correction SVs change N50 by at most 0.2% (was +1–2%), 5mC 2–14%,
    four-class 31–74%, indel rates +22–33%; GNN reduction 31–37% / 37–43%, 40–71% of the additional
    error, 21–39% at indel pairs; N50 loss 12–21% / 0.3–9%; after correction 5mC N50 +8–16% from 18×,
    four-class 18–46% longer than SNV-only with 14–27% higher rates; indel-pair change at most 7%;
  - **one statement reversed:** four-class blocks are no longer the longest except at three coverages;
    they are within 1.7% of SNV + indel + 5mC blocks, which are longer at every coverage except 30 and 40×,
    because an SV no longer joins two blocks on its own (the sentence says so);
  - Results, phased fractions (four-class, replicate 1): SVs 70.9–72.5% (was 68.1–70.0%), GNN unphases
    4.9–8.8% of them (4.5–8.8%); 5mC and indel fractions unchanged;
  - Discussion: 1.5–1.8-fold (MethPhaser, HapBridge) and 2.2–5.4-fold (LongHap);
  - unchanged: every SNV-only and SNV + indel value (abstract fold changes, v4.2.1/v5.0q spreads, held-out,
    strata, unphased SNVs, precision, T2T validation, HiFi comparison), and the abstract's 44% four-class
    N50 gain at 60×.
- **Methods and Supplementary, facts only:** release v2.1.2 and commit; Sniffles2 `--output-rnames
  --reference`; SV alleles from split-alignment junctions; `--sv-threshold` 20% (nanopore) / 10% (HiFi);
  the SV block rule; SV alleles kept by the copy-number filter; GNN keeps large deletions with PE 0;
  runtime protocol (LongPhase 2 timed in separate runs, one at a time).

**Still to do (red `\todo{}` in the text where it applies; search `todo{LongPhase v2.1.2` and `todo{Issue \#10`):**

| Item | Where | What to fix |
|---|---|---|
| a | new figure (main text) | SV phasing accuracy figure from `notes/sv_phasing/`; layout to agree with the author |
| b | `sections/results.tex` (end of the four-class phased-fraction paragraph, `\todo{Issue \#10`) and Methods | Results and Methods paragraphs on SV phasing accuracy; how to report HiPhase on HiFi |
| c | `main.tex` abstract ("five- to sixfold faster on one thread at 60×") | now 7.6-fold (HapCUT2) and 8.9-fold (WhatsHap): 12.8 vs 96.4 and 113.8 min |
| c | `sections/results.tex`, end of the block-contiguity paragraph ("at the cost of higher peak memory") | no longer holds: with 24 threads 1.4–3.5 GiB on nanopore data, below WhatsHap (1.5–4.0 GiB) except at 12× (1.66 vs 1.62) and below HapCUT2; HiFi 1.4–1.7 GiB, below both |
| f | `main.pdf`, `Supplementary.pdf` | rebuild with `make` and check the new `\todo` marks and Supplementary Tables 7, 9, 10, 14, 16, 18 |

- a. **SV phasing accuracy figure** (issue #10): data in `notes/sv_phasing/`; the layout is to be agreed
  with the author.
- b. **Results and Methods paragraphs on SV phasing accuracy**: how to report that HiPhase phases 7–19%
  more SVs correctly on HiFi data (error rates similar to LongPhase 2) is the author's decision.
- c. **Abstract speed claim and Results memory clause**: "five- to sixfold faster on one thread at 60×"
  is now 7.6-fold (HapCUT2) and 8.9-fold (WhatsHap); "at the cost of higher peak memory" no longer holds.
  Left as they are, marked, for the author to reword.
- e. **Not changed:** Fig. 1 and Supplementary Figs. 1–8 (schematics; Supplementary Fig. 7 shows
  `modcall`, whose description is unchanged); Figs. 3 and 4 and Supplementary Figs. 9, 12 and 13 (SNV-only
  data, identical output); Supplementary Tables 1–4, 6, 8, 11–13, 15, 17 and 19; the JSX drafts
  `UnphaseVenn3` and `UnphasedComposition` (SNV-only); the `Other_phasers` HiFi rows labelled
  `LongPhase 2.1.1 (--indels)` (identical output); the README sections above (history).
- f. **`main.pdf` and `Supplementary.pdf` were not rebuilt** (no TeX here); run `make`.
