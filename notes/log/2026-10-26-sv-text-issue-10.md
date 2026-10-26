# SV phasing text rewritten from issue #10 data, Supplementary Table 20 added, 2026-10-26 (author decision)

The author approved the proposed SV text (old | new table) except the abstract, which is to be discussed
separately, and removed the proposed GNN paragraph: "Don't use GNN correction in results. We don't know
how each variant was unphased; GNN is just one of them. Reframe using entire LongPhase 2 whenever possible."

- Results, SV subsection: two paragraphs from `notes/sv_phasing/sv_phasing.tsv` (every coverage, both
  platforms, both inputs, HiPhase on HiFi data, size classes, deletions ≥ 10 kb on HiFi). No with/without-GNN
  statement; the preliminary #136 paragraphs, their provenance comment and both `\todo` marks removed.
- Discussion: SV sentence now "1.3–2.3-fold lower error rates than by WhatsHap, and SVs of at least 1 kb
  with lower error rates than by HiPhase on HiFi data"; `\todo` removed.
- Methods, SV phase evaluation: Sniffles2 with the reference genome; HiPhase v1.7.0 named with WhatsHap as
  a tool that reads only sequence-resolved SVs; records left out of their input (296–580 per run) stated;
  the split-alignment sentence and its `\todo` removed (split-alignment junctions are in the allele paragraph).
- Supplementary Table 20 (new, `sv_table()` → `figures-source/supp_table_sv.tex`, input after Supplementary
  Table 19 so that no table is renumbered): per coverage and tool, given, phased, right, wrong, error rate,
  homozygous in the assembly, no assembly match, error rate 50 bp–1 kb and ≥ 1 kb, deletions ≥ 10 kb.
  LongPhase 2 as released only (no `--disableGNN` rows).
- Abstract unchanged (still "1.4- to 1.7-fold for SVs" with its `\todo`), to be discussed.

**Follow-up, same day (author: "revise both").** Two further sentences that attributed SV unphasing to GNN
correction were reframed:
- Results, four-class phased fractions: the before-correction fractions and "GNN correction then unphased
  0.2–1.8% of the phased 5mC sites and 4.9–8.8% of the phased SVs" replaced by the fractions of LongPhase 2
  as released: indels 30.5–45.4% (`co-phase_Detail`, `longphase_v2.1.2`), 5mC 97.4–99.2% and SVs 66.1–68.5%
  (`notes/sv_mod/sv_mod.tsv`, `gnn_*` columns, all contigs, replicate 1).
- Discussion, limitations: "and the GNN has no SV-specific features; on HiFi data, it unphased similar
  numbers of correctly and incorrectly phased SVs" deleted; no new caveat added.

**Follow-up 2, same day (author).** Discussion, completeness paragraph: "WhatsHap phased more SVs correctly
than LongPhase 2, but 1.5–2.0 times as many incorrectly" (preliminary #136) → "0.7–6.3% more SVs correctly
…, but 1.5–2.3 times as many incorrectly" (SNV + SV input, both platforms, every coverage; WhatsHap /
LongPhase 2 wrong 1.77–2.27 on nanopore and 1.45–1.66 on HiFi data; right +0.7 to +6.3% and +1.9 to +4.9%).
