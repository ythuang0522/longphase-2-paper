# Review round, 2026-10-07

**Review round, 2026-10-07.** (H1) Methods now state that accuracy was scored with
`longphase compare` on chr1–22 without a benchmark BED, name the v4.2.1 hifiasm phase-transfer
file and how it was filtered, and give the out-of-BED shares (9.3% v5.0q, 3.4% v4.2.1).
(H2) MethPhaser rationale: it was given LongPhase 2 SNV-only output (no GNN) so that both runs start
from the same SNV phasing. (H3) HiFi call sets are being regenerated per coverage (current calls all
come from 10×, median DP 10); Methods, Results and Supplementary Table 5 say so. (M1) Down-sampling
seeds, minimap2 2.24 / samtools versions, PEPPER r0.8, WhatsHap/HapCUT2/Margin/Ralphi command lines,
HiFi source and the runtime machine filled in; only the PEPPER model preset is still open.
(M2) Unphased-SNV classification re-run with the final GNN model
(`gnn_prepare/unphased_e6/`, replicate 1, 10–60×): 55,756–58,162 unphased; at 60× 2,215
benchmark-het by position, 2,055 with matching alleles, which equals the `compare` loss. The old
"BED" explanation was wrong; the gap was the matching rule. `COMPOSITION` in `make_results_figs.py`
updated; Supplementary Fig. 16 must be regenerated, and Supplementary Fig. 17 is still the old raster.
(M3) SV/5mC phased fractions replaced by exact values (four-class, before GNN: 5mC 99.0–99.4%,
SV 68.1–70.1%; GNN unphases 1.4–4.6% and 2.4–3.8%). (L1) See item 8(a): the debug fix ships in
v2.1.1 or later.
