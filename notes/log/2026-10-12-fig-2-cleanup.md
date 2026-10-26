# Fig. 2 cleanup, 2026-10-12 (author review)

**Fig. 2 cleanup, 2026-10-12 (author review).** Data origin checked per row: a–c `SNV_Detail` SNV-only
runs; d–f `co-phase_Detail` `Indel` (SNV + indel only; `item3_indel.tsv` `longphase_coh_indel_gnn` and
`whatshap_v28` match it in phased SNVs and SNV switch rate); g–i `co-phase_Detail` `Mod` replicate 1 and
the `MethPhaser` sheet; j–l HiFi `SNV_Detail`. Changes: (1) no s.d. bands in any Fig. 2 panel (they were
visible in b and e only, not in a or d; `line(band=False)`); (2) the dashed `Indel+Mod+SV` path removed
from f, so each row shows only the evidence of its title; (3) d now shows only the indel-pair switch
error rate and e the indel Hamming distance, two lines each (the SNV-pair lines in d had no match in e).
Legend and Results updated: the SNV-pair 3.0–3.7-fold claim cites Supplementary Data 1, the SV + 5mC
block-length sentence cites Supplementary Fig. 15, Supplementary Table 10 and Supplementary Data 1.
- Revised the same day (author): d and e again show SNVs (solid) and indels (dotted) in both panels —
  d SNV pairs and pairs with an indel, e SNV and indel Hamming distance. The SNV Hamming distance of
  the SNV + indel runs is calculated, not scored (`_indel_runs()`; SNVs in one-variant blocks not
  removed, error < 0.3%). Open: rerun `aggregate.py` on the lab server to write the exact SNV
  Hamming (`ham_all`, `ham_n` of `out/*.tsv`) into `item3_indel.tsv`. Results now say that indel
  and SNV Hamming distances are close (LongPhase 2 within 0.1 points, WhatsHap 0.4–0.7 higher).
