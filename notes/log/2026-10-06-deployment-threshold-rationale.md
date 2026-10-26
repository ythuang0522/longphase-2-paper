# Deployment-threshold rationale, 2026-10-06 (author-provided correspondence)

**Deployment-threshold rationale, 2026-10-06 (author-provided correspondence).**
Methods and Supplementary Method 4 now document the 0.05–0.95 threshold sweep over 60 HG002
nanopore runs at 10–20×. The author clarified that B=0.30 was an empirical balance: it removed more switch errors
than B=0.40 at the cost of withholding additional phased SNVs, while retaining most phased
sites. B=0.40 had the lower unit cost. The text does not present 0.30 as a mathematical
optimum or imply a formally enforced cost constraint. This is separate from the classifier metric used to select the checkpoint.
The TODO asking for the reason for choosing 0.30 is resolved; the existing request to provide
the sweep source data and trade-off panel remains.

The supplied screenshot gives B=0.30: 1,863,972 phased SNVs, 1,658 switch errors, 8,569 SNVs
withheld, 1,150 switch errors removed (cost 7.45); B=0.40: 1,866,521, 1,765, 6,020 and 1,043
(cost 5.77). Both imply a baseline of 1,872,541 phased SNVs and 2,808 switch errors.
The table's coverage/replicate/aggregation is unspecified, so its counts were not added as
manuscript results. The accompanying statement that total phased-SNV loss was below 0.2%
needs its denominator and aggregation clarified: this table gives 0.458% at B=0.30 and
0.321% at B=0.40 relative to the common pre-correction phased count. The 0.2% statement
was omitted in favour of the qualitative trade-off explanation requested by the author;
clarifying that unused percentage is not a blocker for this wording change.
