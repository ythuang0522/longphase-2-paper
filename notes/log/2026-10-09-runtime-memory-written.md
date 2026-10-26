# Runtime and memory written in, 2026-10-09 (issue #3, `notes/runtime/`)

**Runtime and memory written in, 2026-10-09 (issue #3, `notes/runtime/`).** Abstract: "five- to
sixfold faster on one thread at 60×" (was "six- to sevenfold", which compared 24 threads with one).
Results: one-thread times (8.1/18.0 min vs 24.1/96.4 HapCUT2, 25.2/113.8 WhatsHap) and the
24-thread times with their memory cost (63.0 GiB at 60× vs 7.4 GiB on one thread); the runtime
`\todo` removed. Methods: runtime measured once on 10x_1 and 60×, LongPhase 2 timed with 1 and 24
threads. New Supplementary Table 16 (`runtime_table()`); memory in GiB, rounded half-up.
