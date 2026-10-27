# Results memory clause rewritten for v2.1.2, 2026-10-27 (author decision)

The SNV-only runtime sentence of the Results said that LongPhase 2 was faster "at the cost of higher peak
memory", with a red `\todo` that gave the v2.1.2 values. The author chose option A of two wordings (A keeps
the memory result, B drops the clause):

| Old | New |
|---|---|
| …achieved shorter wall-clock times and used less CPU time than \whatshap and \hapcut, at the cost of higher peak memory (…).\todo{…} | …achieved shorter wall-clock times, used less CPU time and, at all coverages but one, less peak memory than \whatshap and \hapcut (…). |

Check against `notes/runtime/runtime.tsv` and `runtime_hifi.tsv` (LongPhase 2 with 24 threads, the others
single-threaded): wall-clock and CPU time lower than both tools at every coverage on both platforms; peak
memory lower than both everywhere except nanopore 12× against WhatsHap (1.66 versus 1.62 GiB). HapCUT2 is
higher at every coverage (6.4–19.6 GiB). README "still open" line updated.
