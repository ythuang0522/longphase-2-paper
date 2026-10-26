# HiFi rescored with per-coverage calls, 2026-10-09 (issue #4, `notes/hifi/README.md`)

**HiFi rescored with per-coverage calls, 2026-10-09 (issue #4, `notes/hifi/README.md`).**
PEPPER-Margin-DeepVariant r0.8 `--hifi` was run on each HiFi coverage's own alignment (10–40×
down-sampled from the 48× GIAB Revio BAM with seed 1; 48× used as 50×). SNV-only phasing with
release v2.1 (GNN and `--disableGNN`) and WhatsHap 2.8 `--only-snvs`, scored with `compare`
v2.1 against v5.0q without a BED. `supplementary.xlsx` HiFi rows of `Variant_Calling` and
`SNV_Detail` replaced (no other cell changed); Supplementary Tables 7 and 11 regenerated
(`tables()` only). LongPhase 2 now has 2.2–2.6-fold fewer switch errors than WhatsHap (was
2.5–3.5): abstract, Results HiFi paragraph (title, rates, Hamming no longer lower at 50×,
N50 ratio 4.3; GNN removes 19–25% of HiFi switch errors, was 19–28%), Fig. 5 legend, Methods (model presets, HiFi data, replicates) and
Supplementary Table 5 updated; HiFi `\todo`s removed. `Homo. SNV` counts PASS 1/1 plus
refCall 0/0 records (checked against the nanopore and old HiFi rows); Table 7 caption says so.
**Not done here (no matplotlib fonts/LaTeX on the lab server): Fig. 5 and Supplementary
Fig. 13e,f must be regenerated (`make results-figs`) and the PDFs rebuilt.**
