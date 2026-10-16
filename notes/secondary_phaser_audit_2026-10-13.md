# Secondary phaser scope audit — 2026-10-13

## Findings

Margin, Ralphi and historical GCphase results each contain 60 ONT runs:
10, 12, 14, 16, 18 and 20×, with ten replicates per coverage.
There are no 30–60× or HiFi rows for these tools in the local or current GitHub workbook.

The original data commit explicitly says that blank cells are runs not performed,
and that Margin, Ralphi and GCphase were run on ONT 10–20× only:
[8ff180bc2fa71b90ee46a1c522eeef357bfdcc91](https://github.com/ythuang0522/longphase-2-paper/commit/8ff180bc2fa71b90ee46a1c522eeef357bfdcc91),
2026-10-04, “Supplementary tables for all benchmark runs”.
Thus, the original high-coverage blanks are not omitted measurements.
No source found explains why execution was limited to this range.
Do not attribute it to runtime, memory, tool failure, or a planned design without evidence.

[Issue 2, execution report](https://github.com/ythuang0522/longphase-2-paper/issues/2#issuecomment-6065772628)
also confirms 60 Margin and Ralphi runs each. The held-out analysis rescored existing VCFs;
it did not add new phasing runs.

## Local and GitHub checks

- Local `supplementary.xlsx`, `SNV_Detail`, read through the existing column mapping in
  `figures-source/results_data.py`; all non-empty per-tool records checked.
- Historical benchmark text files, held-out files and scripts, manuscript README and notes.
- Local Git histories and branches of the manuscript and sibling LongPhase repositories,
  and relevant APG worklogs.
- GitHub manuscript main `a066c7e46b3ef9c8efafd4a3c1fe64a0c1624d34`, one commit ahead of the
  local base `0abbda3a2ec49dfaa0f75c160c092aff0a85810a`. Its downloaded workbook has identical
  `SNV_Detail` content; additions are `Unphased_sets` and `SV_5mC_phasing`.
- GitHub manuscript issue comments (22), LongPhase issue/PR discussion comments (316),
  LongPhase PR inventory (64), branch inventories, JH file tree, and author-scoped searches
  for Ralphi and GCphase. No explanation of the 20× limit was found.
- Lab-server paths cited in scripts (`/disk/research/`) are not present on this Mac;
  raw server directories and execution logs were not inspected.

## GCphase is a separate exclusion

Historical workbook values remain but are not used for the comparison. Full-input runs
phased filtered homozygous-reference calls as heterozygous; homozygous-alternate calls
were not converted, so the earlier Methods claim about “every input record” was too broad.

The newer GitHub [GCphase diagnostic](https://github.com/ythuang0522/longphase-2-paper/blob/a066c7e46b3ef9c8efafd4a3c1fe64a0c1624d34/notes/gcphase/README.md)
records controlled chr20, 20× reruns with cleaned input. Hamming distance fell from 35.0%
to 16.0% and switch error rate from 1.40% to 0.51%. These are single-chromosome diagnostics,
not a replacement genome-wide benchmark. No corrected genome-wide run was found.
The exclusion should be described as an input-compatibility problem, not justified by
GCphase having a higher error rate.

## Manuscript edits

Moved Ralphi/Margin from the opening SNV paragraph into a separate closing paragraph of
the phaser-comparison subsection. Grouped the concise GCphase exclusion with them.
Methods explicitly states the 10–20× scope and absence of 30–60× evaluation, and corrects
the GCphase input-handling claim. The reason for choosing the restricted coverage range
remains unresolved. No new benchmarking was performed; no remote changes were merged.
