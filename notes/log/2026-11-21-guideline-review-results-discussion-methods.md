# Guideline review fixes: Results, Discussion, Methods

2026-11-21. Review of the main text against `../../*_WRITING_GUIDELINES.md`; the author asked to fix Results, then Discussion, then Methods. No number changed; every new range was checked against Supplementary Tables 1 and 21.

Results
- Fig. 2 SNV sentences (nanopore, HiFi, HiFi + indels): one trend sentence, then LongPhase 2 against the strongest other tool with rates, other tools as folds only (Results guideline §5, four numbers per sentence). Nanopore folds split by tool: 2.9--3.9 vs WhatsHap, 3.3--5.0 vs HapCUT2 (Supplementary Table 1, rate ratio).
- Contiguity paragraph: removed the switch-error folds that repeated the previous paragraph.
- Further individuals: rates of WhatsHap and HapCUT2 removed from the text (in Supplementary Table 21); added the rank at every coverage (LongPhase 2 < WhatsHap < HapCUT2, every replicate). No new Supplementary citation, so no renumbering.
- Two-benchmark subsection: new lead sentence with the main finding (§1).
- "vs" -> "versus".
- Not changed: title of subsection 2 (options to the author first).

Discussion
- Paragraph 1: the further individuals are compared with WhatsHap and HapCUT2 only.
- Paragraph 2: the MethPhaser mechanism shortened to cause + result; the switch-error counting point stays in the Results.
- Closing: "current phasers" -> "the phasers compared here".
- Not changed: new interpretation paragraph for Fig. 2 (draft to the author first).

Methods
- "phased before correction" -> "before GNN-based unphasing" (project term rule).
- Maximum-distance skip moved from the graph subsection to the voting subsection.
- Supplementary pointers moved to the first sentence of "Input alignments and variant calls" and "Read-based correction and phasing entropy".
- minimap2 v2.24 with citation, samtools v1.23.1, PEPPER-Margin-DeepVariant citation (versions from Supplementary Table 20 and Note 6).
- "as in compare" and "FORMAT/DP" replaced by plain wording.

Author decisions (same day)
- Results subsection 2 title, option A: "\toolname has lower switch error rates than other phasers for SNVs and indels on both platforms".
- Discussion, option Y: new paragraph on the Fig. 2 result after the MethPhaser paragraph (cause: multi-neighbour voting weighted by sequence context, "consistent with"; cost: contiguity; HiFi narrowing). Discussion is now above the 1,000--1,200-word range of the guideline; the author accepted this.

Later the same day (author)
- LongHap removed from the abstract: 5mC comparison 1.5--5.4-fold -> 1.5--1.8-fold, "a methylation-aware phaser" (MethPhaser only). Discussion paragraph 1 changed the same way.
- Word counts are not a constraint for this paper: the 150-word abstract rule was removed from CLAUDE.md.
- Abstract, option A: new sentence "With 24 threads, 	oolname phased a 60× nanopore genome in less than one minute." before the closing sentence, so that "fast" has a result in the abstract.
