# Fig. 3 SV row redrawn from issue #10 data (option 2), JH's v2.1.2 commits merged, 2026-10-26 (author decision)

**Merge.** JH pushed `2a24859` (issue #10 SV phasing data, `notes/sv_phasing/`) and `1bd99b4` (LongPhase
v2.1.2: runs with SVs or 5mC repeated, data, figures and text updated) onto `b12ab40`. The local Fig. 3
work of 2026-10-20 to 2026-10-24 was uncommitted. The local tree was saved as a stash ("backup before
merging origin v2.1.2 + issue 10, 2026-10-26"), fast-forwarded to `origin/main`, and the merge was
resolved as follows:
- `main.tex` abstract and `sections/discussion.tex`: local text, with JH's v2.1.2 numbers (MethPhaser and
  HapBridge 1.5–1.8-fold, LongHap 2.2–5.4-fold) and JH's `\todo` on the speed claim.
- `sections/methods.tex`: JH's text (release v2.1.2 for every result; the "except the SV phasing results"
  clause and its `\todo` are gone, because the SV runs also use v2.1.2).
- `sections/results.tex`: local structure (5mC subsection, SV subsection); JH's v2.1.2 numbers moved into
  the relocated MethPhaser/HapBridge/LongHap paragraphs, with JH's provenance comment; JH's block-contiguity
  numbers and memory `\todo`; JH's evidence-class paragraph (reversed four-class N50 statement) with the
  local Fig. 3f reference. JH's `\todo{Issue \#10 …}` merged into the SV subsection `\todo`.
- `figures-source/make_results_figs.py`: local code, sheet block `longphase_v2.1.1` renamed `longphase_v2.1.2`
  (as in `supplementary.xlsx`). All results figures re-rendered locally with Arial.
- `README.md`: local version; JH's v2.1.2 section moved to `2026-10-26-longphase-v2-1-2-rerun.md`.
- The local preliminary `notes/sv_phasing/README.md` is now `README_preliminary.md` (JH's README took the name).

**Fig. 3a–c (option 2).** The author chose option 2 of two (option 1: c = error rate by size class at 30×).
- a nanopore, b PacBio HiFi: SV error rate against SVs phased correctly, one point per coverage, solid
  SNVs + SVs, dashed SNVs + indels + SVs (dashed = "+ indels", as in f); LongPhase 2 with GNN, WhatsHap,
  HiPhase (HiFi).
- c: error rate of SVs ≥ 1 kb (DEL + INS, 1–10 kb and ≥ 10 kb) against coverage, nanopore and HiFi side by
  side with one y axis. LongPhase 2 is lower than WhatsHap and HiPhase at every coverage, with both inputs
  (HiFi SNV + SV: 7.8–9.1% against HiPhase 10.9–13.3%; + indels 8.5–9.6% against 11.2–14.4%).
- Legend a–c updated; the preliminary `\todo` of the legend removed. The Results SV paragraph lost its
  panel-c citation (the ≥ 10 kb deletion sentence) and keeps a `\todo` until it is rewritten from the
  issue #10 data.
