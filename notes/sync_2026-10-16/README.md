# Remote data and local manuscript merge — 2026-10-16

User rule: use the latest remote data; retain the local figure design and manuscript writing style. Resolve factual changes from the data, and ask the author about unresolved content choices.

- Software: `main` advanced from `46ba470` to `f9962dd` (v2.1.1).
- Manuscript: `main` advanced from `0abbda3` to `a8f4237`.
- Original local work is preserved in Git stash `3cb51b087b8edc310a84069330f582adad04abbf`, including untracked files. The stash has not been dropped.
- `conflicts.md` records all 16 textual conflict blocks in eight files and the ten binary overlaps before resolution.
- `remote_claims.tsv` contains the output of the remote `notes/v2.1.1/claims.py` on the current data.
- Local edits are retained as uncommitted changes on top of the remote manuscript commit.

## Resolution

Preserve the local two-row, six-panel Figure 2, its panel order, the local typography and line styles, and Supplementary Figure 16. Add the remote HapCUT2 HiFi results to the existing accuracy and contiguity panels and the supplementary Hamming panel. Figure 4b retains the two-tool comparison.

Keep the local Results organization and condensed writing, including the decision to hide secondary-phaser comparisons. Update benchmark values, model details, version identifiers, dataset descriptions, and scientific claims from the remote data. Retain both README histories.

Generated figures and document PDFs must be rebuilt from these merged sources; neither side's old PDF can establish the merged result.

## Validation completed

- All 16 text conflict blocks and ten binary overlaps resolved under the author rule; no unresolved content choices.
- 62 tracked XLSX, TSV, TXT, JSX and JS files match `origin/main` byte for byte (`data_integrity.json`).
- Twelve merge-sensitive numeric claims recomputed and checked (`manuscript_claims_check.py` and `.json`).
- Supplementary Table 15 uses the remote threshold-selection criterion: validation chromosomes chr15/chr16, cost 6.35. Old local criterion removed.
- Supplementary tables retain all remote data and captions. Table 17 uses slightly narrower column spacing to fit the page. Table 4's value column is wider to prevent footer overlap; Table 18 has slightly narrower column spacing.
- Supplementary title now matches the local main manuscript title.
- Results figures regenerated with embedded Arial/Arial Bold, preserving the local layouts. Full figure renders, enlarged views, document contact sheets and figure pages were inspected. No SVG source was edited in this merge.
- Forced LaTeX builds completed: `main.pdf` 27 pages, `Supplementary.pdf` 39 pages. Final logs have no undefined references, missing characters, overfull boxes or oversized floats. Nonfatal underfull-line and float-placement warnings remain.
- PDF page-bound checks pass for both documents (`pdf_checks.json`). This is not an exhaustive proof of all text collisions.
- `git diff --check` passes. No commit or push was performed.

Numeric corrections beyond direct conflicts include the held-out ratio (2.7–5.1-fold), Methods block-length/Hamming ranges, and the all-configuration indel-pair error reduction (22–40%; the remote prose's 24–39% describes indels alone).
