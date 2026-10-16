# GNN retraining for LongPhase v2.1.1 (2026-10)

LongPhase v2.1.1 (`twolinin/longphase` release v2.1.1, commit `f9962dd`) replaces the GNN
model of v2.1 and sets the default break threshold to 0.35. The manuscript now reports
v2.1.1 throughout. This note records what changed in training, which alternatives were
trained, how the released model and its threshold were chosen, and where the evidence is.

## What changed in training

The haplotype-swap augmentation exchanges the two allele nodes of every variant of a
window (and complements the HP feature). After the exchange, every graph edge leaves the
other allele node of its source variant, and its vote weight `w` must be the haplotype vote
of that node. The v2.1 training kept the weight of the node the edge came from, so in every
swapped window (half of the training windows) the edge weights did not match their nodes.
Node features and labels were correct. The v2.1.1 model was trained with the weight taken
from the new source node (`train_gnn_30.py --fix_weights`). Architecture, the 31 node and
6 edge features, data, window extraction, labels, chromosome split, loss and optimizer are
unchanged (Supplementary Table 4).

Two GNN-module fixes in the C++ inference of v2.1.1 also change results slightly: GC content
and sequence entropy are computed as in training (they differed next to reference `N` gaps),
and variants left alone in their phase set after correction are unphased; see
`twolinin/longphase` PR #131 for all changes.

## Alternatives and seeds (`seeds.tsv`)

Two label definitions were trained, each with five seeds (42, 43, 44, 1337, 3407):

- **position**: v5.0q variants matched to the called variants by position (the labels of
  the v2.1 model);
- **ref_alt**: matched by position, REF and ALT, so that calls whose alleles differ from
  the benchmark are unlabelled instead of labelled.

The windows, the split and every other setting were the same. All ten models were applied
with the Python correction pipeline to the 60 nanopore SNV-only runs at 10–20× and scored
with `longphase compare` against v5.0q (whole genome; validation chr15–16; held-out chr17,
chr21, chr22). Each model's break threshold B was calibrated on the validation chromosomes
to the cost of the v2.1 model at B = 0.30 (6.35 phased SNVs withheld per removed switch
error), so that the models are compared at equal cost.

Columns: training (stopped and selected epoch; the checkpoint criterion S with its precision
and recall on chr15–16); classification on the held-out chromosomes (argmax precision,
recall, F1 of the error class); and, at the calibrated threshold, switch errors removed
relative to phasing without GNN and the cost (withheld SNVs per removed error) on the
validation, held-out and whole-genome sets.

| Labels | Validation removed | Held-out removed | Genome removed | Held-out F1 |
|---|---|---|---|---|
| position, mean of 5 seeds | 49.7% (48.1–50.8) | 23.0% (22.4–23.9) | 33.8% (32.9–34.7) | 0.349 |
| ref_alt, mean of 5 seeds | 49.3% (47.9–50.5) | 21.6% (20.8–22.9) | 33.5% (33.1–34.1) | 0.374 |
| v2.1 model, B = 0.30 | 48.5% | 21.2% | 33.2% | 0.340 |

- The ref_alt labels gave higher classification scores (held-out F1 0.367–0.382 against
  0.345–0.355) but removed fewer switch errors on the held-out chromosomes at the same cost
  (mean 21.6% against 23.0%). Correction is judged on the phasing output, so the position
  labels were kept.
- The seed-to-seed spread of the position labels on the held-out chromosomes (22.4–23.9%,
  1.5 points) is about as large as their mean gain over the v2.1 model (1.8 points); every
  position-label seed is above the v2.1 model.
- The released model is the one with the largest switch-error reduction on the validation
  chromosomes, seed 42 with position labels (50.8%). Its calibrated threshold, 0.340, was
  rounded to 0.35, the default of `--gnnBreakThreshold` in v2.1.1.
- The Python-pipeline numbers above are the selection data. The manuscript reports the
  C++ module of the release on the same runs: 34.3% of switch errors removed genome-wide
  at a cost of 7.98 (v2.1: 33.1% at 8.27; `supplementary.xlsx` `SNV_Detail`), and the
  held-out values in `notes/heldout/`.

## Evidence (lab server, not in the repository)

`/ssd/longphase_process/test_pe/gnn_retrain_labelfix/`:

- `model_*/` per model: `best_model.pt`, `model_config.json`, `history.json` (per-epoch
  losses and validation metrics), `test_metrics.json`; `train_*.log`: training logs
  (split, label counts, feature separability, held-out metrics); `run_*.log`/`run_*.sh`:
  drivers.
- `sweep/cmp_*.tsv`: the `longphase compare` reports behind `seeds.tsv`; `run_sweep.sh`.
- `export_*`, `cpp_check/`: ONNX export, embedding and the C++-against-Python check (same
  variants scored, probabilities within 5×10⁻⁵, identical unphase decisions).

The training scripts and logs are not published yet (see `Code availability` in Methods).
