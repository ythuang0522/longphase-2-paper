# HG008-N and COLO829BL in the manuscript (option A)

Author decision (2026-11-21, option A of `notes/drafts/2026-11-21-other-individuals-options.md`). The COLO829BL data
were ported from the branch `claude/youthful-lovelace-gdc2ku` (commit 61e7d00). The manuscript text of that branch
(Supplementary Fig. 3 and Table 5, 31 items renumbered, "GNN correction", the GNN effect in Results) was not merged.

## Changes

| Where | Old | New |
|---|---|---|
| Results, comparison subsection | One HG008 sentence between the HiFi paragraph and the block-contiguity paragraph | One closing paragraph after block contiguity on HG008-N and COLO829BL; cites Supplementary Note 8 only; no GNN effect |
| Supplementary Note 6 | Data and phase reference of HG008 (last paragraph) | Moved to Note 8; the intro points to Note 8 |
| Supplementary Note 7 | HG008 comparison with WhatsHap and HapCUT2, and the HG008 GNN effect | GNN effect only, for both individuals; COLO829BL (assembly without the evaluated reads) gives the same reduction as HG008-N |
| Supplementary Note 8 | — | New: "Phasing of two further individuals": HG008-N, COLO829BL, phase references (independence), results |
| Supplementary Fig. 17 | HG008, 1 × 4 | 2 × 4: a–d HG008-N, e–h COLO829BL; two-line panel titles |
| Supplementary Table 21 | HG008, 28 rows | Both individuals, 40 rows, one block per individual |
| Supplementary software table | HG008 rows | + COLO829BL reads, COLO829BL assembly, Clair3 1.2.0 |
| Methods | "Second individual" (HG008) | "Further individuals" (HG008-N, COLO829BL); statistics sentence; Data availability with the ONT and SMaHT sources |
| Discussion | "in a second individual"; HG008 limitation | "in two further individuals"; the limitation names one chemistry, one to three down-samplings, the caller change and that only the COLO829BL reference is independent of the reads |
| `references.bib` | — | `sohn2026colo829` (Cell 189, 6630–6647, 2026) |

No Supplementary item was renumbered. The order of first citation is unchanged. Both PDFs build with no undefined
reference.

## Open

- **SMaHT policy:** check the data-use and publication policy of the COLO829BL assembly (`[citation]` comment in Data
  availability).
- **Supplementary Data 1:** the HG008-N and COLO829BL per-run rows are not in it.
- **Abstract:** unchanged.
