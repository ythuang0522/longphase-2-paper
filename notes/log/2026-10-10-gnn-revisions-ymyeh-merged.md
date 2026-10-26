# GNN revisions by YMYEH merged, 2026-10-10 (`GNN_revisions_YMYEH_1010.zip`, based on `d765603`)

**GNN revisions by YMYEH merged, 2026-10-10 (`GNN_revisions_YMYEH_1010.zip`, based on `d765603`).**
Three-way merge into the current text; the `_YMYEH_1010` file names, the review-copy code in
`make_supp_figs.py` and the `% [YMYEH]` review comments were dropped. Every technical change was
checked against v2.1 (`../longphase`) and `GNN source/train_gnn_29.py`:
- Target: the GNN predicts label-defined phase-disagreement onsets (isolated disagreements and the
  first variant of a disagreeing run), the positives of the binary labels; the score is called the
  onset score. Author decision (2026-10-10): his wording also in the abstract, Introduction,
  Fig. 1c,d legend, Results opening paragraph and Discussion ("onset-prediction score").
- Methods GNN section reordered (target, window, features, branches, scoring zone, unphasing,
  training, labels, checkpoint, threshold, inference); the "GNN correction and phase-set update"
  subsection is merged into it. New: the four feature groups; local GATv2 vs global attention roles;
  binary mode in training and inference; correct nodes resampled per minibatch (`BalancedFocalLoss`);
  S = R(2 − 1/P) = (TP − FP)/(TP + FN), per threshold, P − 1 when P ≤ 0.5 (`net_gain_score`).
- Supplementary Method 4 / Tables 1, 3: gt_ref/gt_alt = first/second GT component
  (`PhasingProcess.cpp:439`); genomic context from the reference and the variant positions (the
  reference is mandatory in `phase`, `Phasing.cpp:230`); running mean only over windows whose
  scoring zone holds the variant (`PhasingProcess.cpp:815–825`); the isolated-node sentence removed
  (every node has a self-loop, `PhasingProcess.cpp:788` and PyG `GATv2Conv` defaults, so the
  no-incoming-edge branch in `GNNModel.h:291` is never reached).
- Supplementary Figs. 4–6 regenerated: "onset score" labels, signed r in Fig. 5, "isolated nodes"
  row removed from Fig. 6 (SVGs identical to YMYEH's).
