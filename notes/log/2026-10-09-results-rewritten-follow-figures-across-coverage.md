# Results rewritten to follow the figures across coverage, 2026-10-09 (author request)

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
