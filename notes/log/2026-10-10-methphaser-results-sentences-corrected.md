# MethPhaser Results sentences corrected, 2026-10-10 (issue #5, author request)

**MethPhaser Results sentences corrected, 2026-10-10 (issue #5, author request).** JHL's rerun
(`eed8109`, `notes/methphaser/`) showed that the old MethPhaser values were its input: 0.0.3 crashed
in every `methphasing` call and the wrapper ignored the exit status. MethPhaser 0.0.4 joins blocks
(no change of phase within a block, phased SNVs unchanged). Check of the rerun: input rows = `SNV_Detail`
`longphase_v2.0.1` replicate 1, LongPhase 2 rows = `co-phase_Detail` `Mod` replicate 1, one assessed
pair added per join. New problem (reply on issue #5): on 3–4 chromosomes per coverage the MethPhaser
block sum exceeds the chromosome length (chr11 at 30×: N50 132.5 Mb), so blocks overlap, and at
30–60× the chr1–22 block sum exceeds the autosome length (the rule that removed the Ralphi N50).
JHL is asked for the cause (MethPhaser itself, or the local `str()` patch or `fix_methphaser_vcf.py`).
- Results (MethPhaser paragraph): every sentence that did not depend on N50 is corrected — switch error
  rate 1.5–1.7-fold lower (was 1.4–1.5), Hamming 1.4-fold lower at 10× and 2.0–2.9-fold at 20–60×
  (was a gap that shrank to 0.2 points), "MethPhaser returned its input blocks unchanged" removed,
  its joins add 2–15% switch errors to the input, joint phasing without GNN equals the input within
  2%, GNN correction accounts for 63–95% of the switch-error gap. The two N50 claims (3–11% longer
  at 20–60×; 2–13% longer before GNN, attributed to 5mC during phasing) are wrong in direction but
  wait for the N50: one red `\todo` replaces them. Numbers in a `[provenance]` comment.
- Not yet changed: Fig. 2g–i and Supplementary Fig. 11 (`make_results_figs.py` `METH`,
  `meth_value()` still hold the input values, so the text and Fig. 2h now disagree), the
  Supplementary Table 5 command line, `notes/SUSPECTED_ERRORS.md` item 1 (left open), the
  `twolinin/longphase` README (SNP+Methylation).
