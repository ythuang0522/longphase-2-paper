# Held-out chromosomes written in; main merged, 2026-10-09 (issue #2; author decision on B)

**Held-out chromosomes written in; main merged, 2026-10-09 (issue #2; author decision on B).**
- `origin/main` (JHL: issue #2 `1702d2c`, HiFi issue #4 `9fb0cc4`/`9054c87`) merged into the
  redesign branch. Conflicts: HiFi paragraph and Fig. 5 legend (main's text, this branch's panel
  letters, Fig. 5 has no ratio panel), README (both entries kept). Fig. 5 and Supplementary
  Fig. 13e,f regenerated from the new HiFi rows; Fig. 5d axis 84–94% (HiFi phased SNVs now 87–92%).
- All `notes/heldout/` numbers recomputed from the raw tables and reproduced; 33.1%/8.3 reproduced
  from `supplementary.xlsx`; PR #42/#52/#82 dates checked in `../longphase`.
- Deployment threshold (author, 2026-10-09): JHL's formal rule stands — largest fraction of switch
  errors removed at ≤10 withheld SNVs per removed error. This supersedes the 2026-10-06 "empirical
  balance" account. Methods and Supplementary Method 4 now say that on chr17/21/22 the cost is 10.5,
  slightly above the limit, and that the threshold was not re-selected there. JHL's "thresholds
  meeting it lay between 0.30 and 0.40 … their optima also fell in it" was rewritten (the rule picks
  one threshold; a sweep limited to 0.30–0.40 cannot have an optimum outside it); a `[check]`
  comment asks JHL which model the full 0.05–0.95 sweep used.
- Results: held-out sentence (2.8–3.9× vs WhatsHap, 3.3–4.9× vs HapCUT2 at 10–20×; 30–60× from
  single runs with 37–83 switch errors); Margin beats LongPhase 2 on chr17/21/22 at 10–12× (0.099 vs
  0.127% at 10×, N50 0.22 vs 0.72 Mb); Part 2 GNN effect gives both 31–33% (genome) and 20–23% /
  14–20% (held-out) with the chromosome-difficulty caveat. Results `\todo` item (i) removed;
  matched-retention and paired-uncertainty items remain.
- New Supplementary Table 15 (`heldout_table()`), v5.0q and v4.2.1, all coverages.
- Not done, by author decision (2026-10-09): the per-run held-out values stay in `notes/heldout/`
  and are not added to Supplementary Data 1; no per-chromosome GNN reduction.
