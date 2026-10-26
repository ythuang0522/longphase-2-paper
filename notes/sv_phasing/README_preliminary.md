# SV phasing accuracy (Fig. 3a–c, issue #10)

`sv_phasing_preliminary.tsv` holds the values that JH posted in twolinin/longphase#136 (comments
6368208659 and 6370206728, 2026-10-23): LongPhase 2 v2.1.1 + #136 (commit b521eb1), with and
without GNN, against WhatsHap 2.8 `--indels`; HG002 replicate 1, nanopore 10× and 30×, HiFi 30×;
Sniffles 2.8.0 with read names; truth = T2T-HG002 Q100 v1.1 dipcall VCF; matching rules in Methods
("SV phase evaluation"). Columns follow issue #10; NA = not reported in the comment. The DEL ≥ 10 kb
rows are deletions only. `phased_hom_in_truth` (171 and 458) is the ONT 30× value in comment
6370206728.

`make_results_figs.py` reads `sv_phasing.tsv` (issue #10, every coverage and HiPhase) when it
exists, and this preliminary file otherwise.
