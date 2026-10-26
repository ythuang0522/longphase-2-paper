# MethPhaser rescored after the PS-lookup fix, 2026-10-10 (issue #5, JHL `5fb01f5`)

**MethPhaser rescored after the PS-lookup fix, 2026-10-10 (issue #5, JHL `5fb01f5`).** The overlapping
MethPhaser blocks came from `PS=-1` written by the first local patch; the current patch finds the block
from the record position. Phased SNVs unchanged; no overlap left.
- Results: Hamming distance "2.0–2.9-fold" → 2.1–3.0-fold at 20–60×; the N50 `\todo` replaced by one
  sentence: MethPhaser blocks 1.1-fold longer at 10× and 1.3–1.8-fold at 20–60× (0.96–5.49 versus
  0.88–3.09 Mb). Switch error rate (1.5–1.7-fold), joins (+2–15% switch errors; Hamming ×1.04 and
  1.8–2.8), GNN share (63–95%) and phased fractions (within 0.2 points) re-read and unchanged.
  `[provenance]` comment rewritten with the new values.
- Fig. 2g–i and Supplementary Fig. 10 now plot MethPhaser's own output: `results_data.load()` reads the
  `MethPhaser` sheet (`D["meth"]`); the `METH` constants (= the input run) are gone. The nanopore N50
  axis of Fig. 2c,f,i is 0–5.9 Mb (was 0–4.6) so that MethPhaser at 50–60× stays in the panel. No
  other figure changed (pixel comparison).
- Supplementary Table 5, MethPhaser row: the local fix is now described as the PS-lookup fallback.
- `make_results_figs.py` section headers corrected to the current Supplementary figure numbers.
