# Figs. 2 and 3 restructured: accuracy with contiguity, completeness with the unphased analysis, 2026-10-09 (author request)

**Figs. 2 and 3 restructured: accuracy with contiguity, completeness with the unphased analysis,
2026-10-09 (author request).** The author found Fig. 2 much larger than Fig. 3 although the two
were correlated, and feared that its N50 and phased-fraction columns told reviewers that accuracy
came at the cost of contiguity and completeness. Main figures go from six to five.
- **Fig. 2** (`fig2_phaser_comparison.pdf`, `fig:phasers`): same three rows (SNV vs
  WhatsHap/HapCUT2; SNV+indel vs WhatsHap; SNV+5mC vs MethPhaser), now three columns: switch error
  rate, Hamming distance, and SNV switch error rate against block N50 (one path per tool over all
  plotted coverages). Panels c and f add LongPhase 2 with all four evidence classes (black).
- **Fig. 3** (new, `fig3_phased_unphased.pdf`, label `fig:unphased`): a, phased benchmark het.
  SNVs (former Fig. 2d); b, phased benchmark het. indels (former 2h); c, new: net additional SNV
  calls phased by WhatsHap, split into calls matched to a v5.0q het. SNV and other calls; d–f,
  former Fig. 6a–c. Former Fig. 3 (evidence classes) dropped: Supplementary Fig. 15 shows every
  configuration; its Results paragraph moved into Part 2 (after-GNN configuration sentences).
- **Supplementary Table 17** (new, generated): Venn counts and the net difference behind Fig. 3c.
- Text: the SNV paragraph now says the lower error rates were not obtained with shorter blocks
  (N50 up to 11% shorter at 10–20×, 1–5% longer from 30×; before GNN correction 1.9–2.5-fold
  fewer switch errors than WhatsHap at 0.97–1.07× its N50; four-class blocks 6–50% longer than
  WhatsHap SNV-only at 2.5–3.1-fold lower rates). A new paragraph before the unphased paragraph
  (which moved up, before Fig. 4) explains that the phased-fraction metric counts only calls that
  match a benchmark het. SNV, and that 65–80% of the additional calls phased by WhatsHap do not
  (10/30/60×, replicate 1). The phased-fraction gap is 0.6–0.9 points before GNN correction; the
  GNN adds 0.1–0.3. One Discussion sentence added (limitations paragraph on withholding).
- Caveat found while checking the author's argument: the calls the GNN removes are mostly absent
  from the benchmark, but they are only ~1/6 of the LongPhase 2-only unphased set, and the 0.7–1.0
  point gap in Fig. 3a is in benchmark het. SNVs by construction. The text therefore claims only
  the net composition. **Issue #6** (JHL) asks for the per-set benchmark composition, WhatsHap's
  accuracy at the matched sites, the per-set depth summaries (closes the depth `\todo`) and the
  script behind `UnphaseVenn3.jsx`. Precision at every coverage was judged unnecessary.
- Cross-references updated: Methods source-data `\todo` (Figs. 2–5), Supplementary block-N50
  paragraph (Figs. 2c,f,i and 5c), Supplementary Fig. 12 legend (Fig. 3d), Supplementary Data 1
  paragraph, Fig. 5 legend ("panels as in Fig. 2a–d" removed).
- Same day, Fig. 2c,f (author: "All four classes are difficult to understand by a reviewer"):
  the black four-class path is removed from the SNV row (c), so each row compares the tools on
  the same input. In f it is a dashed red LongPhase 2 line, "LongPhase 2, + SVs and 5mC", in the
  row key; the legend says that WhatsHap cannot use SVs or 5mC. The SNV paragraph keeps the
  four-class vs SNV-only WhatsHap numbers, now cited to Supplementary Tables 8 and 10.
- Same day, Fig. 3e,f redesigned (author: "difficult to understand ... a reviewer [should] easily
  get the message without reading the explanation in text"). e: absolute share of each tool-only
  set inside the other tool's switch-error intervals beside a grey "expected at random" bar (all
  SNVs assessed for that tool), fold change printed on top, group labels in the panel. f: the
  three 60× density curves are replaced by 100% bars of three depth classes (< 20× few reads,
  20–89×, ≥ 90× excess reads; the cap bin is inside the last class); per-coverage curves stay in
  Supplementary Fig. 12. Results add the absolute shares (10–12% vs 1.1–2.3%) and the ≥ 90× share
  (29% vs 3–4%). Methods `\todo` on switch-error intervals now points to Fig. 3c–f and issue #6.
