# Caller, abstract and Results wording, 2026-10-05 (later pass, author request)

**Caller, abstract and Results wording, 2026-10-05 (later pass, author request).**
- **Small-variant caller is PEPPER-Margin-DeepVariant** (`shafin2021margin`), not Clair3: changed in
  Methods (input paragraph, Benchmark data, comparison methods), Results, Supp. Table 5 and the
  generated Supp. Table 7 caption. Clair3 v2.0.1 and the `sup_v500` model todo are gone; a new todo
  asks for the PEPPER release, model preset and confirmation that its phased output was discarded.
  The Clair3 version-dating comments in Methods are kept as history, marked superseded. Clair3 is
  still cited where it is a downstream pipeline that embeds LongPhase (abstract, Discussion, Supp. Table 6).
- **Abstract** now reports HiFi (2.5–3.5-fold fewer switch errors than WhatsHap, network not
  retrained); opening sentence tightened to stay at 150 words (texcount).
- **Results wording review**: "correction" defined once and used for the step (the network only
  where the model itself is meant); "genuine heterozygotes" → "benchmark heterozygotes" (the
  composition counts benchmark-VCF records outside the BED), also in the Discussion and Supp. Fig. 13;
  "give-ups" removed; per-chromosome values described as ratios of the outside-alignment share, not
  "depletion"; odds ratio stated as such; GCphase "order of magnitude" → "four to seven times";
  Margin "made the fewest switch errors" → lowest rate; HiFi N50 ratio 4.6 (was "five times");
  WhatsHap indel cost 17–20% (was 18–20%), Hamming ratio 37–56% (was "less than half", true only
  from 16×); co-phasing heading now names methylation only (SVs add 1% N50) and "at least halves";
  interpretive clauses on depth and caller artefacts softened to "consistent with"; three ", so"
  clauses removed (style rule of 2026-09-24).
