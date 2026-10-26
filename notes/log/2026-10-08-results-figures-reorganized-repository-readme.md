# Results figures reorganized after the repository README, 2026-10-08 (author request)

**Results figures reorganized after the repository README, 2026-10-08 (author request).**
The author asked for the four comparisons of the `twolinin/longphase` README (SNV, SNV+indel,
SNV+5mC, evidence combinations; SNV+5mC had never been shown), for no ratio panels ("switch error
rate and Hamming distance already show it"), and for Supplementary analyses that show the
strengths of LongPhase 2 to move into the main figures.
- **Fig. 2** (`fig2_phaser_comparison.pdf`, label `fig:phasers`): one row per evidence type
  (SNV vs WhatsHap/HapCUT2; SNV+indel vs WhatsHap; SNV+5mC vs MethPhaser, replicate 1) × four
  columns (switch error rate, Hamming distance, N50, phased fraction). The indel row promotes
  Supplementary Table 14: panel e adds indel-pair switch error rates (dotted), panel f is the indel
  Hamming distance, so no main panel shows the mixed SNV+indel Hamming value any more. The ratio
  panel and the Margin trade-off panel are gone (Margin/Ralphi stay in Supplementary Fig. 10).
  MethPhaser's switch error rate comes from its input run (identical counts, asserted in code).
- **Fig. 3** (new, `fig3_evidence_classes.pdf`, `fig:evidence`): SNV, +5mC, +indels and all four
  classes (all with GNN correction): switch error rate, N50 and the switch-rate/N50 path per
  configuration beside WhatsHap with and without indels. This relaxes the 2026-10-06 rule: the
  per-configuration comparison *with* GNN is now a main figure; with/without-GNN stays Supplementary.
- **Fig. 4** (former Fig. 3, `fig4_two_benchmarks.pdf`): the two near-identical Hamming panels are
  replaced by Supplementary Table 13 content: c, 60× switch errors shared by all three tools
  (93% of LongPhase 2's under v4.2.1, 37% under v5.0q); d,e, v5.0q switch error rate by region at
  10× and 60× (genome-wide, v5.0q regions, not difficult, segmental duplications, outside both).
- **Fig. 5**: ratio panel removed (four panels, same columns as Fig. 2). The former Fig. 4
  (co-phasing) is absorbed into Figs. 2e–h and 3.
- Colours: MethPhaser purple `#6A3D9A`; configuration colours (Fig. 3 and Supplementary Figs. 14,
  15) SNV red, +5mC `#1B9E77`, +indel `#C66A00`, all four black, checked with the dataviz palette
  validator against WhatsHap blue.
- Text: Results Part 1 reordered to follow the figures (SNV → indel/5mC co-phasing → evidence
  classes → benchmarks → HiFi → unphased). New numbers, all from Supplementary Data 1: LongPhase 2
  vs MethPhaser 1.4–1.5-fold lower switch error rate, longer N50 at 20–60×; before GNN correction
  joint 5mC phasing made as many switch errors as MethPhaser (736 vs 743 at 60×), so the rate gap
  is the GNN and the N50 gap is joint phasing. The four-class vs WhatsHap+indel N50 gap is 2–21%
  over all ten coverages (was "2–19%", computed on six). The duplicated after-GNN sentences in Part 2
  now point to Fig. 3.
- Same day, Codex review of the redesign (all points checked against Supplementary Data 1 and the
  issue #1 TSVs; author approved fixes 1–5): Fig. 3 heading now "Adding 5mC or indels lengthens
  phase blocks, and 5mC does so at similar switch error rates" (5mC adds 1–23 switch errors per
  genome; adding SVs to indels shortens N50 at 30× and to indels+5mC at 50×); GNN removal of
  indel-pair switch errors 24–39% over all ten coverages (was 29–39%); SVs+5mC give *similar*
  indel-pair rates (0.104 vs 0.101% at 10×). Fig. 4d,e lead with the v5.0q benchmark regions; the
  outside-both row sits below a dashed line, labelled exploratory, and the Results paragraph follows
  that order. Discussion no longer says coincident disagreement is "more consistent with" v4.2.1
  phase-transfer errors: it states that the two truth sets differ in phase in commonly assessed
  regions, that WhatsHap and HapCUT2 (no trained parameters) also agree with v5.0q there, and that
  the phase-transfer explanation is unverified. Codex's concern that the v5.0q-trained GNN explains
  the benchmark contrast does not hold: uncorrected LongPhase 2 shows it too (60×: 1,708 vs 743
  switch errors; shared regions 1,193 vs 41). Open author decision: headline fold changes are still
  genome-wide (truth VCF in full); inside the benchmark regions they are 2.1–4.0× (WhatsHap) and
  2.6–10× (HapCUT2).
