# Methods: the two \todo marks removed

2026-11-10 (author decision: figure and training scripts need not be public).

- `\todo` after "Analysis of unphased SNVs" (scripts behind Supplementary Fig. 6c) removed; its content is
  now a `%  [provenance]` comment at the same place.
- Code availability: "The GNN training code, the trained model and the scripts used for the analyses and
  figures are available in the same repository." + `\todo` → "The trained GNN model is included in the
  repository." The earlier sentence was not true: the training code is only in the local `GNN source/`
  folder and the analysis and figure scripts are in the manuscript repository, not in
  `twolinin/longphase`. The model weights are in the release (`GNNWeights.h`).
- No `\todo` remains in `sections/*.tex` or `Supplementary.tex`.
