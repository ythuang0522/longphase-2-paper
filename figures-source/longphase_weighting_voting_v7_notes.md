# Scientific basis for panels b and c

Checked against local origin/JH, PhasingGraph.cpp.

- Lines 74–119: pairwise read support is reduced if either allele observation fails the base-quality criterion. This is not a continuous quality-probability model.
- Lines 687–731: high-mismatch variant observations in candidate CNV intervals are removed. Whole reads and all CNVs are not indiscriminately excluded.
- Lines 403–408: outgoing phase votes from repeat-associated indel loci receive reduced weight.
- Lines 215–276: compare combined parallel (REF–REF plus ALT–ALT) versus crossed (REF–ALT plus ALT–REF) support. Ambiguous relationships are suppressed; highly consistent relationships receive stronger phase-vote weight.
- Lines 19–48 and 335–432: accumulated votes from previously processed loci orient the current locus; accepted pairwise relationships then propagate votes downstream. This is forward local propagation, not global longest-path optimization.
- Lines 300–330: the repeated-single-read safeguard uses low-support vote records and stronger alternative evidence. It does not deduplicate molecule identities or implement a universal one-molecule-one-vote rule.

The conceptual figure omits numerical thresholds intentionally. Read-support weighting and phase-vote weighting are distinct and should not be labeled as the same quantity. Generated with the built-in image tool.
