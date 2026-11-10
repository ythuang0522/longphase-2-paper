# Results: MethPhaser comparison no longer framed as joint against post hoc 5mC phasing, 2026-11-10 (author decision, option 1)

Reviewer-style reading of Fig. 3d,e: the LongPhase 2 line has GNN correction and the MethPhaser input has none,
so the panel cannot test "joint is more accurate than post hoc". SNV switch errors at 10–60× (provenance comments
of `sections/results.tex`): MethPhaser 2,319 1,508 1,143 946 938 774; LongPhase 2 SNV + 5mC without correction
2,280 1,288 1,015 881 890 736; with correction 1,537 877 658 606 606 485 (correction = 65–95% of the difference).

Change (one sentence pair in the 5mC paragraph of Results): "We then asked whether phasing 5mC together with
sequence variants is more accurate than adding methylation after phasing. MethPhaser adds methylation after
phasing: given …" → "We then compared the joint SNV and 5mC phasing of LongPhase 2 with MethPhaser, which adds
methylation after phasing: given …". The comparison is now of the two tools as a whole (no component attribution
in Results). Not changed: the Hamming sentences of the same paragraph (the joins of MethPhaser raise the share of
SNVs on the wrong haplotype over its input; independent of the correction), Methods ("with GNN correction, they
also include its effect") and Discussion ("most of this difference came from GNN correction"), which already state
the confound. The fair test, MethPhaser on the corrected SNV-only output, is a new run (not done).
