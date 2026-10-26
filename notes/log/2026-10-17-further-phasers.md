# Further phasers, 2026-10-17 to 2026-10-18

**Further phasers, 2026-10-17 to 2026-10-18.** Results and reasons in
"Comparison with further phasers" above; commands, inputs and full tables in
`notes/competitors/README.md`, run scripts in `notes/competitors/scripts/`. All replicate 1, the
paper's inputs, default parameters or the documented workflow, scored like `SNV_Detail`.
- Added runs:
  - nanopore 10–60×: LongHap 0.2.0 (SNVs with and without 5mC; all variant types with 5mC,
    Sniffles SVs made sequence-resolved by `merge_sv.py`), HapBridge ec48f02 on the MethPhaser
    input (`local_counter.patch`: two undefined debug counters, phasing unchanged), TinkerHap
    1.0.0, HapCUT2 with `--indels 1`;
  - HiFi 10–50×: HiPhase 1.7.0 and TinkerHap 1.0.0 with indels (their default) and on an
    SNV-only input VCF (neither has an SNV-only option; the PEPPER calls restricted to SNVs, the
    set WhatsHap `--only-snvs` phases), LongPhase 2.1.1 `--indels`, WhatsHap 2.8 with indels,
    HapCUT2 with `--indels 1`;
  - HiPhase timed on an idle machine (50×: 12.2 min wall, 187 CPU-min with indels; 10.4 and 173
    on SNVs only).
- Changed: `supplementary.xlsx` new sheet `Other_phasers` (71 rows, by
  `notes/competitors/build_sheet.py`; no other sheet changed); `Supplementary.tex` sheet
  inventory (13 → 14 sheets, row for `Other_phasers`); this README (section above).
- Not changed: main text, Methods, figures (including the JSX drafts) and every other
  Supplementary table. Whether and how to use these results is for the authors to decide.
