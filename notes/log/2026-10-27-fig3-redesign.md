# Fig. 3 redesigned panel by panel, 2026-10-27 (author decision)

The author found the Fig. 3 of 2026-10-26 hard to read: one key listed six tools that only some panels
used, and panel e (phased SNVs, markers side by side) was ugly. The panels were agreed one at a time
from draft PNGs.

| Panel | Before | After |
|---|---|---|
| Keys | One key, six tools, at the top | One key per row on the row-title line (row 1: LongPhase 2, WhatsHap, HiPhase; row 2: LongPhase 2, MethPhaser, HapBridge, LongHap, WhatsHap) |
| a, b | SV error rate against SVs phased correctly | SV error rate against coverage, all sizes |
| c | Median and range of the error rate by platform and size | SVs ≥ 1 kb against coverage, nanopore solid, HiFi dotted |
| d | SNV switch error rate against N50 | SNV switch error rate against coverage, linear axis |
| e | Phased benchmark SNVs, markers side by side | SNV switch error rate against N50 (the former d), linear x-axis |
| f | Six paths, log x-axis | Five paths (LongPhase 2 + indels removed: it coincides with four classes), linear x-axis |

Decisions:
- Short SVs: the author chose a legend sentence (SVs shorter than 1 kb are 90–93% of the SVs scored,
  89.6–92.9% over all runs of a, b) over splitting a, b by size. The 50 bp–1 kb HiFi sentence of the
  Results now cites Supplementary Table 20.
- N50 stays in the main figure (e) because the methylation phasers make longer blocks; phased SNVs
  (LongPhase 2, MethPhaser and HapBridge within 0.2 points) move to the text and Supplementary Table 18.
- Linear switch-error axes in d–f (author). Fig. 2 still uses log axes for the same metric; open.

Text changes: legend of Fig. 3 (`main.tex`); Results citations of Fig. 3e moved to Supplementary
Table 18 for phased fractions and added for MethPhaser and LongHap N50; Supplementary Fig. 17 caption no
longer says "as in Fig. 3a,b" (its plot is unchanged). No numbers changed.
