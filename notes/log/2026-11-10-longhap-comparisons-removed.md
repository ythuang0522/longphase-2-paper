# LongHap comparisons removed; results retained locally, 2026-11-10

Author request: remove LongHap comparisons from the paper and keep their results in the current folder.

- Removed numerical comparisons from Results and Discussion and the LongHap run description from Methods.
- Kept the brief Introduction citation and bibliography entry as related work.
- Removed LongHap from Fig. 3d-f, Supplementary Fig. 1e, Supplementary Table 4 and the software table (Supplementary Table 19).
- Updated figure captions and the description of Supplementary Data 1.
- Archived all 18 LongHap rows from `Other_phasers` in `notes/competitors/longhap_hidden_rows.tsv`; the submission sheet now has 47 runs. Scripts and existing results notes remain in place.
- Saved the removed source passages in `notes/competitors/longhap_removed_comparisons.tex.md`.
- Extended the figure generator's existing `HIDE` mechanism to LongHap. The archived data remain available for restoration. The workbook builder excludes both LongHap and HapBridge.
- Preserved the existing uncommitted changes to the variant-class Results, landscape Supplementary Table 6 and its source data/code.

Validation:

- Rebuilt Supplementary.pdf (45 pages) and main.pdf (29 pages) with TeX Live; both builds exited successfully.
- No undefined references, missing characters or overfull boxes. The existing five underfull boxes in main and 21 float-placement warnings in Supplementary are unchanged.
- PDF text scan: one LongHap mention in the main Introduction; none in Supplementary or either revised comparison figure.
- Rendered and inspected both full revised figures, magnified changed panels, and their manuscript pages. Reviewed the edited Results, Discussion, Methods, Supplementary Data description and table pagination. PDF word-bound checks, corrected for landscape-page rotation, found no text outside page bounds.
- Archived values match all 18 original rows and 15 columns exactly. Retained workbook rows match except sequential No. renumbering. Only the Other_phasers worksheet XML changed; all unrelated XLSX package members remain byte-identical.
- Removing `lh` from `HIDE` loads all 18 archived rows for figure/table generation.
- Independent text review found no actionable issues. Supplementary first-citation order is unchanged.
- Fig. 3f N50 range reduced from 8.6 to 4.7 Mb to fit the remaining data (maximum 4.196 Mb).

