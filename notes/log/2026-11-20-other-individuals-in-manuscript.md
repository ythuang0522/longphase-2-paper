# Two further individuals in the manuscript: Supplementary Fig. 3 and Table 5

Author decision (2026-11-20, option A): the HG008-N (`2026-11-13-hg008-external-validation.md`) and COLO829BL
(`2026-11-19-colo829bl-results.md`) validations of the released model go in as one Results paragraph with one
Supplementary figure and one table. Placement: last paragraph of the comparison subsection (`\toolname reduces switch
error rates across variant classes and sequencing platforms`).

## Changes

- **Results** (`sections/results.tex`): new paragraph at the end of the comparison subsection.
  - Switch error rate against WhatsHap: 1.8–3.6-fold lower (HG008-N) and 2.2–2.4-fold lower (COLO829BL).
  - Switch error rate against HapCUT2: 2.4–5.4-fold and 3.2–4.9-fold lower.
  - GNN correction removed 15–20% and 19–20% of switch errors.
  - Completeness is 0.6–1.0 point below WhatsHap, and N50 is within 5% of WhatsHap's.
  - The one exception in Hamming distance is stated (COLO829BL 30×).
  - The `[optional experiment]` comment no longer lists a second individual.
- **Methods** (`sections/methods.tex`):
  - new subsection "Evaluation in other individuals": data, callers, seeds, truth construction, and the
    non-independence of the truth sets;
  - one sentence in Statistics and reproducibility;
  - HG008-N and COLO829BL sources in Data availability.
  - `[citation]` comments mark two missing references: the HG008 data descriptor and the SMaHT COLO829 reference.
    They also flag that the SMaHT data-use policy must be checked.
- **Discussion** (`sections/discussion.tex`): the generalization paragraph no longer says "All data came from HG002" or
  "Evaluation in other individuals … is needed". It now reports transfer to the two individuals and their limits:
  - one chemistry;
  - coverage up to 30×;
  - one or three seeds;
  - truth that is not independent of the HG008-N reads.
- **Supplementary** (`Supplementary.tex`):
  - new Supplementary Fig. 3 (`suppfig_other_individuals.pdf`);
  - new Supplementary Table 5 (`supp_tables/individuals.tex`);
  - six rows in the software table: HG008-N and COLO829BL reads and assemblies, Clair3 1.2.0, dipcall.
- **Generator** (`figures-source/make_results_figs.py`): `sfig_other_individuals()` and
  `other_individuals_table()`. Both read `notes/{hg008,colo829}_validation/results/*_runs.tsv`.
  - The new figure was generated alone and its fonts were checked (ArialMT and Arial-BoldMT embedded).
  - The tables were regenerated: the only other changes are renumbered references in three captions (`calls`, `hifi`,
    `runtime`).

## Renumbering

The order follows first citation, checked after the change.

| Item | Old | New |
|---|---|---|
| Supplementary Figs. | 3–18 | 4–19 |
| Supplementary Tables | 5–19 | 6–20 |

- **Where:** every reference with a tilde in `main.tex`, `sections/*.tex`, `Supplementary.tex` and the generator strings,
  outside comments.
- **Ranges:** two ranges in the Supplementary Data 1 sentence moved correctly (`5--10`, `7--10`). That sentence lists only
  items whose data are in `supplementary.xlsx`, so the new items are not added to it.
- **CLAUDE.md:** the numbering note and the figure notes are updated.

## Raw data

The raw numbers are now committed (author: "just the raw numbers for generating figures; keep the session ID"). For
COLO829BL, the per-chromosome and genome-wide scorer output and the depth files are in
`notes/colo829_validation/results/raw/`. The VCFs are not committed. They were in the cloud session
`session_016MpzQAd54HaJjtG7j5Wqwe`, as listed in `notes/colo829_validation/README.md`.

## Build

- **Toolchain:** built in the cloud container (TeX Live 2023 Debian, `naturemag.bst` from texlive-publishers).
- **`main.pdf`:** 30 pages, was 28.
- **`Supplementary.pdf`:** 45 pages, was 44.
- **Warnings:** no undefined references.

## Open

- **References:** the two `[citation]` items above.
- **Supplementary Data 1:** the HG008-N and COLO829BL per-run rows are not in it (JHL's file).
- **Abstract:** unchanged. It could take one clause on transfer to two further individuals (author to decide; 150-word
  limit).
