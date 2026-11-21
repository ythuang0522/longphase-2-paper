# Methods: constants presented in three levels; new Supplementary Table 12 (parameters)

Author, 2026-11-11 ("Go, as proposed"). Reason: the module subsections held about 45 numeric constants;
each one invites a reviewer question, and the values come from more than two years of development.

Rule (use it for later edits):

1. Parameters that define the model: a symbol in the rule, with the default one time. k (35), tau (0.7),
   theta_read (0.65), theta_var (0.75), theta_PE (0.8), theta_GNN (0.35), alpha, beta, gamma (0.6, 0.2, 0.9).
2. Other user options: the rule in words in Methods; the value only in Supplementary Table 12
   (mapping quality, alignment overlap, SV window and length tolerance, base quality and reduced weight,
   maximum distance, 5mC probability cutoffs, modcall neighbours, GNN window, haplotag majority).
3. Constants fixed in the program: the purpose in words in Methods; the value only in the Supplementary
   Methods (near-unanimous weight 20 and s <= 0.1, SNV-5mC threshold 0.3, single-read guard, tandem-repeat
   weight, fixed qualities 60/30, MR >= 0.7, homopolymer rule, modcall depth bound and six-read filter,
   10-kb deletion exception). Not all constants are user options; do not write that they are.

Changes:

- `sections/methods.tex`: Overview has a second paragraph (parameters are user-adjustable, symbols and
  defaults, Supplementary Table 12, all runs used the defaults, tuning before this study in Supplementary
  Method 3); the sentence "The constants were fixed by a sweep ..." in the voting subsection is removed.
  Numbers removed from: read classification, linkage test, alignment selection, allele extraction, MR
  filter, graph weights, maximum distance, votes, single-read guard, read-based correction weights, GNN
  window size, deletion exception, haplotagging.
- `Supplementary.tex`: new Supplementary Table 12 (user-adjustable parameters, defaults, options; option
  names read from release v2.1.2). Supplementary Tables 12-19 are now 13-20 (all live references changed;
  source comments with older numbers are not changed). Supplementary Method 1 received the homopolymer
  rule and the fixed qualities; Supplementary Method 2 the 0.8/0.2 cutoffs; Supplementary Method 3 is
  retitled "Voting rules, read-based correction and the tuning of their constants" and now holds the vote
  weights, the single-read guard and the read-filter constants (moved from Methods). The GNN score
  threshold has one symbol, theta_GNN (was B). Supplementary Fig. 12b legend points to Supplementary
  Method 3.
- `CLAUDE.md`, `README.md`: generated tables are Supplementary Tables 1-11, 18 and 19.

Known discrepancy, not changed: Supplementary Method 5 writes `--svWindow`/`--svThreshold`; release v2.1.2
`haplotag` has `-w, --sv-window` and `-h, --sv-threshold` (Supplementary Table 12 uses the release names).

Also: `Supplementary.tex` now disables the `--` ligature in typewriter text (microtype), because every
command option was printed with one dash.
