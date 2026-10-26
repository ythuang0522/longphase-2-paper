# Source baseline moved to release v2.1, 2026-10-07 (author request)

**Source baseline moved to release v2.1, 2026-10-07 (author request).** `../longphase` is now
checked out on `main` at the official release v2.1 (`46ba470`). JH tip `f7bd878` is an ancestor;
the two differ only in README images. Since `cc17fb1` (the commit behind the results), commit
`97d7367` made the GNN a default stage of `phase` (`--disableGNN`, `--gnnBreakThreshold` 0.30,
`--gnnPeThreshold` 0.80, `--gnnWindow` 20 — the manuscript's values) and removed the `gnn`
command; the commit reports byte-identical outputs on the demo and HG002 10x_1/20x_1 (SNV-only
and four-class). `--dot` still exists; the GNN now gets the edges in memory. Edits: Supp. Table
of versions and Methods code availability now name v2.1 (`46ba470`), with a `[provenance]`
comment; Supp. Note 1 and the Supp. Fig. 5d legend say the GNN reads the graph in memory.
Line map `cc17fb1` → v2.1: `GNNProcess.cpp:540` → `PhasingProcess.cpp:830`;
`PhasingProcess.cpp:122` → `:161`; `PhasingGraph.cpp:253–266` → `:218–231`;
`PhasingGraph.cpp:838–862` → `:804–828`; `ParsingBam.cpp:226–228` → `:236–238` (the PE header
now says 0 also means no incoming votes). `CompareProcess.cpp` and `ModCallParsingBam.cpp`
references are unchanged. Dated entries below keep their `cc17fb1` line numbers.
