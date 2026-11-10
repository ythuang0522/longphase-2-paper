# Supplementary Tables 5 and 18: legends corrected

2026-11-10 (author decisions after the Supplementary review).

- Supplementary Table 18 (S2, option 1): "SVs and 5mC were not called on the HiFi data." → "5mC was not
  called on the HiFi data; HiFi SV counts are in Supplementary Table 5." HiFi SVs were called with
  Sniffles2 for Fig. 3b, Supplementary Fig. 3 and Supplementary Table 5. The HiFi SV cells stay "--":
  the table counts every SV type on all contigs (nanopore 60x: 17,414 het.), and only the heterozygous
  DEL/INS on chr1-22 are on the writing machine (`notes/sv_phasing/sv_phasing.tsv`; nanopore 60x 15,805).
  Filling the cells needs the HiFi Sniffles2 VCFs of the lab server.
- Supplementary Table 5 (S5): "Source: notes/sv_phasing/sv_phasing.tsv." removed (internal path).

Edited in `figures-source/make_results_figs.py` and, with the same text, in the generated
`figures-source/supp_tables/calls.tex` and `figures-source/supp_table_sv.tex` (no figure regeneration).
