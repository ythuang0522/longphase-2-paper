# Fig. 3 rebuilt as a two-tool comparison, 2026-10-09 (author: c–f "difficult to understand"; "why is the protagonist WhatsHap and not LongPhase"; the three-tool key did not apply to c; "not yet Nature Methods level")

**Fig. 3 rebuilt as a two-tool comparison, 2026-10-09 (author: c–f "difficult to understand";
"why is the protagonist WhatsHap and not LongPhase"; the three-tool key did not apply to c;
"not yet Nature Methods level").** Every panel now compares LongPhase 2 (red) with WhatsHap
(blue) on the same heterozygous SNV calls, with one key for the figure; HapCUT2 is left out of
Fig. 3a (its phased fraction is in Supplementary Table 8 and the text). Sets are named and
coloured by the tool that **phased** them, not by the tool that left them unphased.
- Row 1, all calls: a, benchmark het. SNVs phased; b, new, share of phased calls on chr1–22 that
  are benchmark het. SNVs (LP2 89.7/91.8/93.1% vs WhatsHap 86.3/89.7/91.5% at 10/30/60×;
  exact now that JHL confirmed the call universe); c, benchmark het. indels phased.
- Row 2, calls phased by one tool only: d, counts with the benchmark-het. part dark (WhatsHap
  only 122–149k, 20–25k benchmark het.; LP2 only 38–54k, 1.0–1.6k); e, wrong phase at those
  benchmark SNVs for the tool that phased them, with its overall rate as a black line and the
  error counts on top; f, read depth at 60× in tints of the tool colour.
- Also visible now, and stated in the Results: about 90% of the calls phased by LP2 only are
  absent from the benchmark, but 92–93% of them lie in segdups or outside the 1:1 alignment,
  where the benchmark does not assess phase.
- Supplementary Table 17 and Supplementary Fig. 12 relabelled the same way (Supp. Fig. 12 colours
  swapped to the tool that phased the set). The interval enrichment is now read as "calls phased
  by one tool only lie in that tool's own switch-error intervals 2.0–9.6× more often". Results,
  Methods, Discussion and the Supplementary Data 1 paragraph rewritten in this framing.
- Same day, superseded: the author could not read the six-panel symmetric version and said the
  design should have been discussed first, and that its message had drifted ("both tools trade
  off" instead of "LongPhase 2's trade-off is right"). Agreed core message: LongPhase 2 phases
  about 1% fewer benchmark SNVs; most calls it leaves unphased are not benchmark SNVs; WhatsHap
  often phases the others wrongly. **Fig. 3 is now a 2 × 2 grid (option A + depth kept):**
  a completeness, b precision (LongPhase 2 vs WhatsHap, one key); c calls left unphased by
  LongPhase 2 but phased by WhatsHap (wrong / correct benchmark SNVs / other, with "N wrong = X%
  of the benchmark SNVs"); d read depth at 60× of the calls left unphased by one tool only, with
  the 92% false-call note on the ≥ 90× segment. Phased indels moved to the text (Supplementary
  Table 9); the reverse set and interval co-location to the text and Supplementary Table 17.
  Supplementary Fig. 12 named and coloured as in d (left unphased by …). Results rewritten as
  three run-in paragraphs following a–b, c and d.
- Same day, Fig. 3c made two-sided (author's option B): one bar per tool and coverage for the
  calls left unphased by that tool only, coloured by that tool; shades = benchmark SNVs the other
  tool phased wrongly / correctly / not a benchmark SNV. All in-panel annotations removed from c
  and d (author: "Nature figures are not this text-heavy; describe it in the main text"). Fig. 3b
  still has 10/30/60× only: issue #7 asks JHL for the phased chr1–22 het. SNV call counts of every
  run so that b can show every coverage with replicate means, as a does.
- Same day, indel completeness back in the main figure (author's option B): Fig. 3 top row is
  a SNV completeness, b precision, c indel completeness; bottom row d calls left unphased by one
  tool only, e their read depth. The Results indel sentence now cites Fig. 3c and adds that
  WhatsHap's indel-pair switch error rate is 8–31 times that of LongPhase 2 (Fig. 2d).
- Same day, issue #7 (JHL, d765603, `notes/unphased/phased_calls_chr1_22.tsv`, 128 runs): phased
  het. SNV calls on chr1–22 of every SNV-only run of LongPhase 2 and WhatsHap; the 10/30/60×
  replicate-1 counts equal the issue #6 values (asserted in code). Fig. 3b now shows precision at
  every coverage with replicate s.d. (LongPhase 2 89.4–93.1%, WhatsHap 86.2–91.5%; higher for
  LongPhase 2 in every replicate, difference 3.2 → 1.5 points). New Precision column in
  Supplementary Table 8 (LongPhase 2 and WhatsHap rows); Supplementary Data 1 gains the
  `Phased_calls` sheet. Results, Methods, Fig. 3 legend and the Supplementary Data 1 paragraph
  updated. Issue #7 closed.
- Same day, indel completeness removed from Fig. 3 again (author: keep it out while the SNV
  analysis alone carries the argument). Checked first: the indel panel added nothing to the SNV
  argument, which rests on a (completeness), b (precision), c (composition and the other tool's
  phase at the matched calls) and d (depth). No indel precision exists to pair with it: issue #7
  counted SNV calls only, and `phased_indel` / `pindel_pct` count benchmark-matched indels only.
  Fig. 3 is again a 2 × 2 grid: a SNV completeness, b precision, c calls left unphased by one
  tool only, d their read depth. The Results indel sentence now cites Supplementary Table 9
  (WhatsHap − LongPhase 2 = 2.44 at 10× rising monotonically to 4.49 at 60×, so the 2.4–4.5
  range is in the table). Panel letters updated in the Fig. 3 legend, Results, Methods `\todo`,
  Supplementary Data 1 paragraph and Supplementary Fig. 12 legend. Scope of the claim: the SNV
  analysis supports "LongPhase 2 trades about 1% of benchmark SNVs for higher precision", not
  "every SNV it leaves unphased would be phased wrongly": WhatsHap phases 77–90% of the matched
  calls in the LongPhase 2-only set correctly (18,263 / 16,809 / 22,256 at 10/30/60×).
- Same day, Fig. 3c,d replaced by one net panel (author's option A, after a discussion round).
  The author wanted direct evidence that the calls LongPhase 2 leaves unphased are calling errors;
  the one-sided sets and the depth panel only compared the two tools. Agreed limit: the T2T-HG002
  assembly verifies a call only where it aligns 1:1 to GRCh38; outside, "not mappable" means "cannot
  be verified", not "error". Fig. 3 is now one row: a completeness, b precision, c additional calls
  phased by WhatsHap on chr1–22 (lp_only − wh_only per class; `net_classes()`): 107,510 / 77,083 /
  65,314 at 10/30/60×; het. SNV 20.7 / 23.9 / 36.4% (equals the replicate-1 Phased_SNV gap),
  of which phased wrongly 5,212 / 2,926 / 2,313 (net); homozygous or other allele 12.8 / 6.1 /
  6.1%; no benchmark record 66.6 / 70.0 / 57.5%. Read depth moved to Supplementary Fig. 12 (text
  kept). Results paragraph rewritten around the net values (one-sided details kept); Methods
  defines the net set; legend, Supplementary Data 1 paragraph and Supplementary Fig. 12 legend
  updated. **Open (`\todo`, issue #8):** split "no benchmark record" by `in_dipcall_1to1` of the
  issue #6 site table (`notes/unphased/assembly_split.py` → `assembly_split.tsv`); Fig. 3c then
  shows "calling error (benchmark or assembly)" and "cannot be verified" without code changes.
  Region choice: raw dipcall 1:1 BED (as Supplementary Table 16), not the curated benchmark BED.
- Same day, after reading GIAB v5.0q (olson2026giabv5; the paper evaluates variant accuracy, not
  phase), the net panel was replaced (author: "do it"). Fig. 3c = genotype errors phased: calls at
  positions with a homozygous v5.0q record that each tool phased (background + that tool only):
  LongPhase 2 14,444 / 9,828 / 8,497, WhatsHap 27,135 / 13,706 / 11,815 at 10/30/60× (1.4–1.9×).
  Fig. 4d,e gains the row "v5.0q regions not in v4.2.1" (region `v5only`): WhatsHap and HapCUT2
  5.6–9.3× and 7.5–12× the LongPhase 2 rate (15–41 LongPhase 2 errors) vs 1.7–2.6× and 2.1–9.8× in
  the shared regions. Results: genotype-error paragraph (other allele 1.3–1.4×, no record
  1.3–1.4×), depth paragraph adds the ≥ 2× coverage share (28% / 17% at 30/60× for calls left
  unphased by LongPhase 2 alone vs 7% / 2%) with the GIAB paralog-mismapping citation, and the
  regions-added sentence; one Discussion sentence. F1 (harmonic mean of precision and phased
  fraction): LongPhase 2 higher in all 64 paired runs, by 0.8–1.0 points at 10–18× and 0.3 at
  50–60×; new F1 column in Supplementary Table 8, a sentence in Results, defined in Methods; not a
  panel (derived from a and b). Issue #8 dropped: `assembly_split.py` deleted, `\todo` removed.
- 2026-10-09: Fig. 4d,e gains the row "v5.0q regions also in v4.2.1" (region `shared`) directly
  above "v5.0q regions not in v4.2.1", so the GIAB v5.0q contrast (WhatsHap / LongPhase 2 1.7–2.6×
  in shared regions vs 5.6–9.3× in added regions, all ten coverages) reads in adjacent rows; the
  region analysis stays in Fig. 4, not Fig. 2 (it needs both benchmarks, and Fig. 2 is organised by
  evidence type). Fig. 4 legend d,e updated; one number-free sentence in the Fig. 2 Results
  paragraph points to Fig. 4d,e.
- 2026-10-09: Fig. 4d,e row labels in forest-plot form: "v5.0q benchmark regions" with four
  indented subsets ("Outside difficult regions", "Segmental duplications", "Shared with v4.2.1",
  "Added in v5.0q"), left-aligned, and "Outside both benchmarks" below the dashed line; the
  repeated "v5.0q regions," prefix and the in-panel "(exploratory)" were removed (the legend keeps
  "exploratory"). Legend d,e reworded to match.
