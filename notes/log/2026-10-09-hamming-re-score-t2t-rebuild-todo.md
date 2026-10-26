# Hamming re-score and T2T rebuild `\todo`s demoted to limitations, 2026-10-09 (author: no new experiments)

**Hamming re-score and T2T rebuild `\todo`s demoted to limitations, 2026-10-09 (author: no new
experiments).**
- Hamming: no Hamming value of an indel-containing configuration is quoted in the Results; Methods
  now says the metric includes indels and is not comparable between configurations with and
  without indels, which are compared by SNV switch error rate. The re-score clause is removed from
  the Methods `\todo` (region-filter commands and metric table remain).
- T2T assembly analysis (Results and Supplementary Fig. 16 `\todo`s): not rebuilt. Autosome-only
  shares derived from the existing per-chromosome counts (9.6% vs 92.9%, odds ratio 124; two new
  rows in Supplementary Table 12, generated). Results and Methods now state the limits: chrX/chrY
  included in the headline counts, start-coordinate matching without allele comparison,
  background containing later-unphased sites (biases towards no difference; expected-value
  estimate in a `[limitation]` comment), raw dipcall BED, same assembly as v5.0q.
- Results `\todo`s left: two Supplementary Data 1 deposits (Fig. 6c depth summaries; SV and 5mC
  phased counts), no new analysis needed.
