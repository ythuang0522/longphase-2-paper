# Runtime: SSD timings adopted; HapCUT2 runs not re-timed left out, 2026-10-28 (author decision)

JHL re-timed all SNV-only runs with inputs and outputs on an NVMe SSD (f1cff54,
`2026-10-28-runtime-ssd.md`). The author chose the SSD times over the HDD times. The HapCUT2 runs that
were not re-timed (nanopore 60×, HiFi 10–50×; storage = HDD in `runtime_ssd.tsv`) are left out instead of
mixing drives (author: "60x is not necessary to claim the speedup").

Reasons: the SSD set has LongPhase 2 on one thread at every coverage and on HiFi; every run was made alone
with the page cache cleared; the HDD wall-clock time of LongPhase 2 was mostly alignment reading; the
v2.1.2 README speed table uses the same SSD.

Changes:
- `make_results_figs.py`: `_runtime(platform)` reads `notes/runtime/runtime_ssd.tsv`, rows with storage =
  SSD only. Supplementary Fig. 10 (nanopore) now has one-thread points at every coverage and no HapCUT2
  point at 60×. Supplementary Table 15: same columns; HapCUT2 "--" at nanopore 60× and on HiFi; the
  24-thread wall-clock column has two decimals. Caption: HapCUT2 not timed at nanopore 60× or on HiFi.
- Supplementary Fig. 10 legend: one thread at every coverage (points); HapCUT2 not timed at 60×.
- Results, runtime subsection: rewritten from the SSD values (one-thread fold against WhatsHap and HapCUT2
  across all coverages, one-thread peak memory, 24-thread time and memory). Per-coverage values in the
  provenance comment.
- Methods, Runtime and memory: SSD, one run at a time with the page cache cleared, LongPhase 2 on 24 and
  one thread, HapCUT2 input without the records it rejects, HapCUT2 timed at nanopore 10–50×. The HDD
  re-timing sentences removed.

| | old (HDD) | new (SSD) |
|---|---|---|
| Results | multithreaded LongPhase 2 shorter wall-clock, less CPU time and, at all coverages but one, less peak memory than WhatsHap and HapCUT2 | one thread: 10.2–20.4× faster than WhatsHap (nanopore), 18.1–34.2× (HiFi), 9.6–11.5× faster than HapCUT2 (nanopore 10–50×); least memory (1.1–1.4 GiB); 24 threads 0.25–0.85 min (nanopore), 0.18–0.48 min (HiFi), 2.1–4.5 GiB |
| Methods drive | hard-disk drive | NVMe solid-state drive |

Follow-up, same day (author): Supplementary Fig. 10a,b have a log time axis (0.1–300 min, ticks 0.1, 1, 10,
100), because the 24-thread wall-clock line (0.25–0.85 min) lay on zero on a linear axis; c stays linear.
Legend: "Time axes in a and b are logarithmic." 60× is kept for all tools (HapCUT2 has no 60× point); cutting every
tool to 50× was proposed by the author and advised against (Figs. 2–5 show 10–60×).

Second follow-up, same day (author: "memory and speed are not the major contributions but the minor
bonus"): Results runtime text cut to one sentence (one thread 9.6–34.2-fold faster than WhatsHap and
HapCUT2 with the least peak memory; 24 threads, 60× nanopore genome in less than one minute). Methods cut to
two sentences (tool, workstation, SSD, one run at a time with the page cache cleared, threads). What the
times include, identical outputs and the HapCUT2 input records moved to the Supplementary Table 15 caption.

Third follow-up, same day (author): `/usr/bin/time` removed from Methods and the Supplementary Table 15 caption.
