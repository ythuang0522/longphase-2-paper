# Methods review, group D: structure, data availability, todo text

2026-11-10. Author-approved draft. No new measurements.

- D1 "Comparison with other methods": the first paragraph is now four (nanopore; PacBio HiFi, with HiPhase
  v1.7.0 as a primary tool; MethPhaser; further phasers: TinkerHap, Margin, Ralphi, GCphase). Content
  unchanged; "Two further phasers … (see below)" removed; HapCUT2 with indels on nanopore data is stated
  with replicate 1. The command-line paragraph is unchanged.
- D2 Data availability: added the dipcall calls and one-to-one regions of T2T-HG002 Q100 v1.1 on GRCh38
  (GIAB `release/AshkenazimTrio/HG002_NA24385_son/v5.0q/dipcall_output/`) and the HiFi Revio alignment
  (GIAB `data/AshkenazimTrio/HG002_NA24385_son/PacBio_HiFi-Revio_20231031/`); both directory listings
  checked on 2026-11-10 (files `GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.vcf.gz`, `.dip.bed`,
  `HG002_PacBio-HiFi-Revio_20231031_48x_GRCh38-GIABv3.bam`). Supplementary Table 19: file name in the
  HiFi row; new row for the assembly calls.
- D3 `\todo` after the unphased-SNV subsection: Supplementary Fig. 6c uses `analyze_unphased.py` and
  `reclassify_unphased.py` (not in the repository); Fig. 5a–g scripts are in `notes/unphased`; Fig. 5h and
  Supplementary Fig. 6d use `run_t2t_validation.sh`. Header comment: Supplementary Tables 12–16.
- Code availability: sentence and `\todo` unchanged (author: the `\todo` is the submission blocker).
