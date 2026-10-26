# Runtime across coverage, 2026-10-10 (issue #8, JHL `baf32b1`)

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
