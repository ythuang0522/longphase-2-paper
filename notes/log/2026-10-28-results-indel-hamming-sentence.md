# Results: indel Hamming sentence compares tools, 2026-10-28 (author decision, option B)

In the first comparison paragraph of `sections/results.tex`, "decreasing from 6.9% to 3.6%
for LongPhase 2 and remaining at 9.0–13.8% for WhatsHap" described a change within one tool
and gave only the 10× and 60× values. It now reads "LongPhase 2 had 1.8–2.7-fold lower
values than WhatsHap (3.5–7.1% versus 9.0–13.8%), and the fold difference increased with
coverage". Values from `notes/benchmark_strata/item3_indel.tsv`, all ten coverages
(LongPhase 2 maximum 7.08% at 12×, minimum 3.48% at 50×; fold 1.82 at 10× to 2.72 at 60×,
per-replicate means), consistent with the 1.8–2.7-fold in Methods.
