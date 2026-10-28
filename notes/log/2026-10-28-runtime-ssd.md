# Runtime re-timed on an SSD, 2026-10-28

SNV-only phasing of replicate 1 (nanopore R10.4.1 10–60×,
PacBio HiFi 10–50×) was timed again on the same workstation with inputs and outputs on an SSD (ext4,
NVMe) instead of the hard-disk drive of the paper's runs: one run at a time on an idle machine, page cache
cleared before every run, one run each, `/usr/bin/time -v`, the commands of `notes/runtime/README.md`.
LongPhase 2 is the v2.1.2 release binary, with 24 threads and with one thread (one thread now at every
coverage, not only 10 and 60×; HiFi one thread is new). Every output is identical to the paper's
(LongPhase 2 with one thread identical to 24 threads; HapCUT2 phased GT and PS identical at 10, 14, 16 and
18×, the coverages where the paper's run had the same input). HapCUT2 input: the same calls as the other
tools, with the records HapCUT2 rejects (GT not two alleles from {0,1,2}: refCall `./.`, 278–682 at 12× and
20–60×, and one `2/3` at 12×) removed by our script. HapCUT2 at nanopore 60× and on HiFi data was not
re-timed and keeps the HDD value (marked \*): where it was re-timed with the same input, the SSD time was
within 2.5% of the HDD time. Data: `notes/runtime/runtime_ssd.tsv` (`build_runtime_ssd.py`, scripts in
`notes/runtime/ssd/`) and the new `Runtime` sheet of `supplementary.xlsx` (HDD and SSD values,
`build_runtime_sheet.py`).

Wall-clock time in minutes, CPU time (user + sys) in parentheses; WhatsHap and HapCUT2 run on one thread:

| Nanopore | LongPhase 2, 24 threads | LongPhase 2, 1 thread | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|---|---|---|---|
| 10× | 0.25 (4.2) | 2.5 (2.7) | 25.7 (25.7) | 24.2 (24.2) |
| 12× | 0.28 (4.8) | 2.9 (3.1) | 38.4 (38.4) | 30.6 (30.6) |
| 14× | 0.30 (5.4) | 3.1 (3.4) | 51.2 (51.2) | 35.2 (35.2) |
| 16× | 0.32 (5.8) | 3.5 (3.8) | 60.2 (60.2) | 40.0 (39.9) |
| 18× | 0.35 (6.5) | 3.8 (4.1) | 71.3 (71.3) | 43.1 (43.0) |
| 20× | 0.38 (7.0) | 4.1 (4.5) | 83.4 (83.4) | 47.0 (47.0) |
| 30× | 0.48 (9.9) | 5.7 (6.3) | 110.7 (110.7) | 63.6 (63.5) |
| 40× | 0.62 (13.0) | 7.3 (8.1) | 124.3 (124.3) | 80.3 (80.3) |
| 50× | 0.73 (16.0) | 8.9 (9.9) | 138.7 (138.7) | 92.1 (92.1) |
| 60× | 0.85 (18.5) | 10.4 (11.6) | 147.5 (147.5) | 96.4\* (95.9) |

| HiFi | LongPhase 2, 24 threads | LongPhase 2, 1 thread | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|---|---|---|---|
| 10× | 0.18 (2.0) | 1.3 (1.4) | 22.9 (23.0) | 19.5\* (19.4) |
| 20× | 0.27 (4.1) | 2.1 (2.3) | 70.7 (70.7) | 44.6\* (44.4) |
| 30× | 0.33 (5.9) | 2.8 (3.1) | 91.9 (91.9) | 44.7\* (44.5) |
| 40× | 0.40 (7.6) | 3.5 (4.0) | 101.3 (101.3) | 59.8\* (59.5) |
| 50× | 0.48 (9.2) | 4.0 (4.6) | 106.9 (106.9) | 59.5\* (59.1) |

Peak resident memory (GiB):

| Nanopore | LongPhase 2, 24 threads | LongPhase 2, 1 thread | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|---|---|---|---|
| 10× | 2.49 | 1.16 | 1.56 | 6.59 |
| 12× | 2.56 | 1.28 | 1.71 | 7.54 |
| 14× | 3.16 | 1.26 | 1.89 | 8.28 |
| 16× | 2.74 | 1.28 | 2.06 | 8.94 |
| 18× | 2.78 | 1.29 | 2.21 | 9.60 |
| 20× | 3.01 | 1.21 | 2.34 | 10.22 |
| 30× | 3.30 | 1.29 | 2.89 | 13.39 |
| 40× | 3.76 | 1.39 | 3.43 | 16.57 |
| 50× | 4.32 | 1.38 | 3.94 | 19.74 |
| 60× | 4.47 | 1.22 | 4.46 | 19.44\* |

| HiFi | LongPhase 2, 24 threads | LongPhase 2, 1 thread | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|---|---|---|---|
| 10× | 2.11 | 1.14 | 1.54 | 7.12\* |
| 20× | 2.52 | 1.23 | 2.35 | 11.42\* |
| 30× | 2.60 | 1.19 | 3.01 | 14.29\* |
| 40× | 2.62 | 1.19 | 3.62 | 17.21\* |
| 50× | 2.97 | 1.19 | 4.09 | 19.56\* |

- **One thread** (wall-clock time against WhatsHap and HapCUT2, which have no thread option): LongPhase 2 is
  10.2–20.4-fold faster than WhatsHap and 9.3–11.5-fold faster than HapCUT2 on nanopore data, 18.1–34.2-fold
  and 14.7–21.6-fold on HiFi data. Its peak memory (1.1–1.4 GiB) is the lowest of the three at every coverage.
- **24 threads:** wall-clock time 103–229-fold below WhatsHap and 97–132-fold below HapCUT2 on nanopore data
  (125–276 and 107–167-fold on HiFi); CPU time 6.2–11.9 and 5.2–6.9-fold lower (11.3–17.3 and 6.4–10.9 on
  HiFi). Peak memory 2.1–4.5 GiB: above WhatsHap except on HiFi at 30–50× (equal at nanopore 60×), 2.6–6.6
  times below HapCUT2.
- **Against the HDD values** (Supplementary Table 16): LongPhase 2 with 24 threads has about the same CPU
  time on both drives but a much shorter wall-clock time on the SSD (nanopore 0.25–0.85 against 2.9–16.1 min),
  so its HDD wall-clock time is mostly spent reading the alignments. With 24 threads its peak memory is
  higher on the SSD (2.1–4.5 against 1.4–3.5 GiB, same binary; not investigated). WhatsHap is within ±4% of
  the HDD time at 10–18× (nanopore) and 10 and 30× (HiFi), but 12–30% slower at nanopore 20–60× and 8–12% at
  HiFi 20, 40, 50× (CPU time likewise; not investigated).

- **HDD (current figure) against SSD.** Supplementary Fig. 10a and the Wall columns of Supplementary Table 16
  show HDD wall-clock time, the time a user waits; panel b and the CPU columns show CPU time. Fold change of
  LongPhase 2 against each tool:

  | | HDD (Supplementary Fig. 10 and Table 16 now) | SSD |
  |---|---|---|
  | 24 threads, wall-clock, vs WhatsHap | nanopore 6.7–14.6×, HiFi 14.8–24.2× | nanopore 103–229×, HiFi 125–276× |
  | 24 threads, wall-clock, vs HapCUT2 | nanopore 5.3–8.8×, HiFi 10.1–17.1× | nanopore 97–132×, HiFi 107–167× |
  | 24 threads, CPU time, vs WhatsHap | nanopore 5.0–10.4×, HiFi 9.7–14.2× | nanopore 6.2–11.9×, HiFi 11.3–17.3× |
  | 24 threads, CPU time, vs HapCUT2 | nanopore 4.2–6.1×, HiFi 5.9–10.1× | nanopore 5.2–6.9×, HiFi 6.4–10.9× |
  | 1 thread, wall-clock, vs WhatsHap | nanopore 7.9× (10×), 8.9× (60×); no HiFi | nanopore 10.2–20.4× (10.2× at 10×, 14.2× at 60×), HiFi 18.1–34.2× |
  | 1 thread, wall-clock, vs HapCUT2 | nanopore 7.6× (10×), 7.6× (60×); no HiFi | nanopore 9.3–11.5× (9.6× at 10×, 9.3× at 60×), HiFi 14.7–21.6× |

  The abstract's "up to 8.9-fold faster on one thread" is the HDD value at 60× (7.6–8.9-fold); on the SSD
  it is 9.3–14.2-fold at 60× and up to 20.4-fold (nanopore) or 34.2-fold (HiFi) across coverages.

**Still to do — HDD or SSD times in the comparison** (author's decision): Supplementary Fig. 10, Supplementary Table 16,
  the runtime paragraph of Results, the abstract's 8.9-fold and the Methods sentence "input and
  output on a hard-disk drive" all still use the HDD runs. Using the SSD values means replacing
  `runtime.tsv`/`runtime_hifi.tsv` by `runtime_ssd.tsv` in `make_results_figs.py` (which can then also plot
  the one-thread line at every coverage), and rewriting those sentences with the ranges above.
