# Wording review by Codex, 2026-10-09 (50 items; the review file is not kept in the repository)

**Wording review by Codex, 2026-10-09 (50 items; the review file is not kept in the repository).**
Applied (agreed): Supplementary Methods narration, tutorial asides and software-documentation
detail removed (items 6–26: document openings, methylation linking/merging, scanner bookkeeping and
"worth stating" passage, MR rationale, release history, duplicated feature inventory, GPS wording,
storage breakdown, GELU instruction, central-zone repetition, label/loss/selection asides, export
serialization, haplotag commentary); the uncited Supplementary Notes 1–2 deleted (vote-weight
definition moved into Edge features). Two factual fixes: the central-zone text said a distant variant
leaves *fewer* variants in the zone (it leaves more; sentence replaced by the equation), and the S
criterion is now defined exactly (correct detections minus false detections over all errors).
Supplementary Method 3 retitled "Tuning …" and its `\todo` replaced by the limitation (tuned on the
same individual; chr17/21/22 held out from the GNN only). Tables 3, 4 and 6 de-engineered and Table 6
retitled "Selected applications and evaluations" (DeepVariant row, which does not use LongPhase,
removed; promotional asides removed); Table 6 is now cited in the Introduction. Supplementary Figs.
1–7 legends shortened to panel descriptions; Fig. 9 placeholder caption no longer states results.
Schematics: "phase-error score" replaces P(misphased)/P(error)/"predicted error probability"
(Figs. 4–6); Fig. 1a SV weight corrected to the code (ALT Q60, REF Q30, both full weight;
`PhasingGraph.cpp` buildVariantGraph — the figure said 0.1 for REF); Fig. 6 input label is σ(w), not
"raw edge weights"; node-cap and binary-storage notes dropped; Fig. 5c rule written as r ≤ 0.5.
Supplementary Table 12 row labels say "assembly variant record at the same coordinate" and the
caption describes the control as sampled before correction; Tables 9–10 say Hamming distance
includes indels where phased. Main text: abstract (problem statement, N50 at 60× vs SNV-only,
interface compatibility instead of "replaces unchanged"), Introduction (items 36–39, incl. the
v4.2.1 original-vs-phase-transfer distinction), Results headings and two sentences (items 40–42;
the compare reconciliation moved to a `[provenance]` comment), Methods (MethPhaser sentence now says
GNN correction adds to the difference; HiFi replicate sentence deleted), Discussion (item 46).
Not applied: items 1–2, 33 (Supplementary Fig. 17 needs regeneration from source data; still a
`\todo`), 3 and 50 (visible blockers kept; runtime claim in the abstract still rests on plot-read
values, issue #3), 34 (agreed, no change needed), 43 (voting rules and seeds kept in Methods for
reproducibility), 44 (GCphase reason kept as one factual sentence).
