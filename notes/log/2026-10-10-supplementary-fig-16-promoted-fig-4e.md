# Supplementary Fig. 16 promoted to Fig. 4e–g, 2026-10-10 (author decision, option A of a design discussion)

**Supplementary Fig. 16 promoted to Fig. 4e–g, 2026-10-10 (author decision, option A of a design
discussion).** Reason: Fig. 4 was the thinnest main figure, and no main figure showed what the
network withholds, although the title says "uncertainty-aware". Fig. 4 now has two rows with row
headers and keys as in Fig. 2: row 1 "Calls phased by LongPhase 2 and WhatsHap" (a–d as before;
d title shortened, its detail moved to the y-label), row 2 "SNVs unphased by GNN correction"
(e v5.0q status by coverage, f inside or outside the T2T-HG002 1:1 alignment at 60× against a
random sample of phased SNVs, g the same by chromosome). Greys in e and f: light = cannot be
verified (absent from v5.0q; not aligned 1:1). The in-panel numbers of the old Supplementary
Fig. 16 (totals, 92.6%, 88.2%) were removed (no text inside panels); the "aligned, no record"
split is in the text and Supplementary Table 12 only.
- Results: the two paragraphs on SNVs unphased by GNN correction moved from Part 2 to the end of
  the Fig. 4 text, with one new sentence: they are 15–18% of the calls that LongPhase 2 alone
  left unphased at 10/30/60× (`lp_only_gnn / lp_only`, issue6_composition.tsv), the rest were
  left unphased before correction. Methods and the Supplementary Data 1 paragraph updated;
  Supplementary Fig. 16 and `suppfig16_gnn_removed.pdf` removed (last figure, so no renumbering;
  Supplementary Table 12 stays). `sfig15()` (which drew it) is merged into `fig4()`.
- Considered and not promoted: held-out chromosomes (Supplementary Table 15; an accuracy result),
  read depth (Supplementary Fig. 12; source of the excess depth undetermined), GNN with/without
  (Supplementary Fig. 13; reverses the 2026-10-06/08 decisions and invites a matched-retention
  comparison), reciprocal sets (Supplementary Table 17; rejected earlier as old Fig. 3e).
- Open: runtime (Supplementary Table 16) supports an abstract claim but has no display item; data
  exist at 10× and 60× only. Author decision (2026-10-10): plot runtime across coverage from the
  logs of the paper runs, which hold GNU `time` output at every coverage; no per-chromosome runs
  of WhatsHap or HapCUT2 (they have no thread option, so CPU time goes next to wall time, and
  Methods says that a per-chromosome split shortens their wall time but not their CPU time).
  `notes/runtime/build_runtime.py` now reads all ten coverages; issue #8 asks JHL to run it and,
  optionally, to time LongPhase 2 on one thread at the eight other coverages (about 2 h).
