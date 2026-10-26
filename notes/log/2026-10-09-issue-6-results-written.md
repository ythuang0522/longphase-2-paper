# Issue #6 results written in, 2026-10-09 (JHL, `notes/unphased/`, commits 273b1fe, 8b7ee5e, 07fb243; author approved all proposed changes)

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
