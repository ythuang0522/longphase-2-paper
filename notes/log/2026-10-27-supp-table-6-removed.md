# Supplementary Table 6 (works citing LongPhase) removed, 2026-10-27 (author decision)

The Introduction no longer cited Supplementary Table 6 ("Selected applications and
evaluations of LongPhase") after "(Supplementary Table 6)" was removed from the
downstream-use sentence. The author chose to remove the table rather than cite it
elsewhere: the Introduction cites the primary papers for Clair3, ClairS, ClairS-TO,
EPI2ME wf-human-variation, Sniffles2 and Severus, and the adoption evidence belongs in
the cover letter.

- The longtable `tab:citing` was deleted from `Supplementary.tex`. References cited only
  by it no longer print in the Supplementary bibliography; `references.bib` is unchanged.
- Former Supplementary Tables 7–20 are now Tables 6–19. Every literal reference was
  renumbered (N ≥ 7 → N − 1) in `main.tex`, `sections/*.tex`, `Supplementary.tex`,
  `figures-source/make_results_figs.py` and `results_data.py` (docstrings and comments
  only; no figure text changed), `Makefile`, `README.md`, `CLAUDE.md`,
  `notes/runtime/README.md`, `notes/hifi/README.md` and `notes/SUSPECTED_ERRORS.md`.
  Dated notes (`notes/log/`, `notes/sync_2026-10-16/`, wording reviews) keep the old
  numbers.
- Both PDFs rebuild with no undefined references; the label order in
  `Supplementary.aux` matches the new numbers (calls 6, snvall 7, twobench 8, cophase 9,
  hifi 10, t2t 11, strata 12, indel 13, heldout 14, runtime 15, unphased 16,
  otherphasers 17, seeds 18, sv 19).
- `citing_papers_europepmc.json` stays in the repository but no table uses it.
