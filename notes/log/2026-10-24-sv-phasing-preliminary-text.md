# SV phasing accuracy in the text from preliminary results, 2026-10-24 (author decision)

**SV phasing accuracy in the text from preliminary results, 2026-10-24 (author decision).** The
author chose option C (SVs and 5mC in one Fig. 3), agreed on one theme for every variant class
("fewer calls phased, a larger share of them correct") and asked for one message across all variant
types in the abstract, not a separate SV sentence. The text now uses the preliminary numbers of
twolinin/longphase#136 (LongPhase 2 + #136 at b521eb1 and WhatsHap 2.8; nanopore 10× and 30×, HiFi
30×; T2T-HG002 Q100 v1.1 dipcall truth). Red `\todo{}` marks wait for issue #10 (JH).

| Place | Change |
|---|---|
| Abstract | The two platform sentences became one sentence for SNVs, indels and SVs (1.7–5.0-fold SNVs, 1.4–1.7-fold SVs), plus "phases slightly fewer variants, but a larger share of them correctly"; "without retraining" removed for length; "structural variants (SVs)" |
| Introduction, last paragraph | SV phase evaluated against the T2T-HG002 assembly |
| Results, overview | One sentence on the SV truth set |
| Results, new subsection before 5mC | "LongPhase 2 phases SVs with lower error rates than WhatsHap": error rates, right/wrong counts, + indels, deletions ≥ 10 kb, GNN with and without |
| Discussion | Co-phasing paragraph: SV fold range; completeness paragraph: the same pattern for SVs; limitations: one SV caller, assembly call set, GNN without SV features |
| Methods | New subsection "SV phase evaluation" (truth, matching, error rate, conversion for WhatsHap/HiPhase); Code availability: SV runs use the #136 change |
| Fig. 3 caption | `\todo` for the SV row and the new title |
| references.bib | li2018dipcall |

Fig. 3 layout drafts C1 (2 × 4) and C2 (2 × 3) were shown to the author; the figure source is
unchanged until the author chooses.
