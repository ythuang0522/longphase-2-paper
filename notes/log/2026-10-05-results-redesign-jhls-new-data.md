# Results redesign from JHL's new data, 2026-10-05

**Results redesign from JHL's new data, 2026-10-05.** Inputs: JHL's seven commits of 26 Sep – 5 Oct
(`supplementary.xlsx`, HiFi/MethPhaser/Venn/composition JSX drafts, `run_t2t_validation.sh`,
`unphase_validation_*`). Changes:

- **Figures regenerated as vectors from exact data** by `figures-source/make_results_figs.py`
  (+ `results_data.py`): Fig. 2 SNV-only vs WhatsHap/HapCUT2 (runtime panel dropped — no exact
  source); Fig. 3 two benchmarks as grouped bars incl. WhatsHap with indels and LongPhase 2
  +indel/+indel+SV (LongPhase 1.0 and uncorrected v4.2.1 dropped — plot-read only); Fig. 4 merges
  old Figs. 4+5 (switch-rate vs N50 trade-off at 10×/60×, SNV vs four-class across coverage);
  **new Fig. 5 HiFi**; Fig. 6 composition (exact), T2T-assembly status, per-chromosome depletion,
  WhatsHap give-up comparison and cross-enrichment. Old PNGs removed; old Fig. 6 kept as Supp. Fig. 13.
- **New Supplementary items**: Figs. 10 (Margin/Ralphi/GCphase), 11 (MethPhaser), 12 (depth of
  give-up sets), 13 (old Fig. 6 raster), 14 (all co-phasing configurations); Tables 7 (call sets),
  8 (SNV-only, 7 tools), 9 (two benchmarks), 10 (co-phasing), 11 (HiFi), 12 (T2T classification);
  Supplementary Data 1 = `supplementary.xlsx`. Supp. Table 5 gained Margin/Ralphi/GCphase/
  MethPhaser/HiFi rows (versions todo).
- **Results rewritten** (7 subsections). All numbers exact; n = 10 at 10× for LongPhase 2 too (the
  xlsx has seed 10), so the abstract's 2.9 became 2.8-fold, correction is 31–33% (not 31–34%),
  N50 loss 2–5% from 30× (40× is 4.9%), WhatsHap phases 0.7–1.0 pp more. New findings: SV/5mC
  co-phasing costs no accuracy after correction (SNV+5mC 0.0227% = SNV-only, +8% N50); correction
  halves the indel cost; LongPhase 2 with indels beats WhatsHap with indels 3.0–3.7× (Hamming 3.5 vs
  9.3%); HiFi transfer without retraining (19–28% of switches removed; 2.5–3.5× fewer than WhatsHap);
  88% of GNN-removed SNVs lie outside the 1:1 T2T alignment (94× depletion), half the assessable rest
  are not variants; LongPhase/WhatsHap give-ups are each enriched up to 10× in the other's errors;
  Margin has fewer switches at 10× only by 3× shorter blocks. Methods gained "Analysis of unphased
  SNVs" and the HiFi/extra-tool runs; statistics paragraph now n = 10 throughout.
- **Discussion revised**: co-phasing paragraph (per-class costs; WhatsHap shows the same indel noise),
  benchmark inversion now WhatsHap(indels)/HapCUT2, network paragraph reinterpreted through the
  assembly analysis and the WhatsHap complementarity, HiFi transfer, Margin caveat; limitations
  updated (HiFi tested on one individual; MethPhaser compared). ~1,700 words (texcount), up from
  ~1,400; the Margin and Ralphi/NeurHap sentences are the cheapest cuts.

**New blocking flags from this data (all `\todo` in the text):**
1. ~~**Variant caller**~~ — resolved the same day (author): PEPPER-Margin-DeepVariant, see below.
2. **MethPhaser output equals its input** to every digit at all six coverages (= uncorrected
   SNV-only LongPhase 2, replicate 1). Probably the input VCF was scored or MethPhaser did not run.
   Partly resolved 2026-10-10 (issue #5): MethPhaser 0.0.3 crashed silently; the 0.0.4 rerun joins
   blocks. Open: its output blocks overlap, so its N50 is not usable yet (entry of 2026-10-10 below).
3. ~~**HiFi call sets are coverage-independent**~~ — resolved 2026-10-09 (issue #4, see below). Was: (2,367,609–2,367,619 het SNVs at 10–50×): one call
   set reused, so the 87% phased fraction at 10× is not comparable with ONT; HiFi data source,
   caller and commands missing from Methods.
4. **Unphased-SNV total resolved (author, 2026-10-06): 56,076 at 60×.** The old composition
   total of 60,267 is superseded. Its three benchmark-classification counts still need replacement
   from the confirmed set; 549 sites inside the benchmark BED (413 variants), `compare`'s net loss
   of 2,055 phased benchmark SNVs and the old 2,411 heterozygotes have different eligibility rules.
5. **(Resolved 2026-10-07 — GCphase removed; see the entry below.)** GCphase Hamming 32–40% (near random).
6. Runtimes, SV/5mC phased fractions and Supp. Fig. 13 values still have no exact source; the
   WhatsHap-only median depth (18×) and zero-entropy share (57.6%) come only from a commit message.

Todo count after this pass: Results 10, Methods 20, Supplementary 18 (incl. generated tables).
