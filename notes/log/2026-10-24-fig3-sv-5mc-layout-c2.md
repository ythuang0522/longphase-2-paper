# Fig. 3 becomes SVs and 5mC, layout C2, 2026-10-24 (author decision)

**Fig. 3 becomes SVs and 5mC, layout C2, 2026-10-24 (author decision).** After draft PNGs C1 (2 × 4)
and C2 (2 × 3), the author chose C2. `fig3_methylation()` is replaced by `fig3_sv_methylation()`
(`figures/fig3_sv_methylation.pdf`; the old `fig3_methylation.pdf` was deleted).

| Panel | Old | New |
|---|---|---|
| a | SNVs + 5mC: accuracy and contiguity | Nanopore: SV error rate against SVs phased correctly |
| b | SNVs + 5mC: Hamming distance | PacBio HiFi: the same |
| c | SNVs + 5mC: phased SNVs | SV error rate by size class at 30× |
| d | By evidence type | SNVs + 5mC: accuracy and contiguity (old a) |
| e | — | SNVs + 5mC: phased SNVs (old c) |
| f | — | By evidence type (old d) |

- The 5mC Hamming panel (old b) is Supplementary Fig. 16e; Supplementary Fig. 16 is now 1 × 5 with
  two-line panel titles, and its caption covers Figs. 2 and 3.
- SV values come from `notes/sv_phasing/sv_phasing_preliminary.tsv` (the #136 numbers) until
  issue #10 delivers `notes/sv_phasing/sv_phasing.tsv`; `sv_rows()` switches automatically. With the
  preliminary file, a and b have two nanopore points and one HiFi point per tool, HiPhase is not in
  the key, and c shows deletions ≥ 10 kb only. The caption `\todo` says so.
- References updated: Results (SV subsection a–c; 5mC subsection a→d, b→Supplementary Fig. 16e,
  c→e, d→f; four-class paragraph d→f), Discussion (a→d), Fig. 3 caption (rewritten), Supplementary
  Fig. 16 caption, CLAUDE.md, README.
- No other figure changed (the other PDFs regenerate byte-identical).
