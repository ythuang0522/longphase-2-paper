# Results: SV subsection opening defines the per-SV error rate, 2026-10-28 (author decision, option B)

The SV subsection started with "We scored the phase of heterozygous deletions and insertions
…" and gave "5.8–11.3% … had the wrong phase" without saying that the measure differs from
the switch error rate of the preceding subsection. It now opens: "Because SVs are sparse, we
scored the phase of each heterozygous deletion and insertion of at least 50 bp called by
Sniffles2, instead of adjacent variant pairs: after each block was oriented by its SNVs, an SV
was wrongly phased when its haplotype disagreed with the T2T-HG002 assembly (Methods)." The
rate sentence names "the SV error rate, the share of phased SVs with the wrong phase", and the
count sentence reads "WhatsHap phased slightly more SVs correctly (0.7–6.3% more) but about
twice as many incorrectly (1.8–2.3 times), and 2.7–3.3 times as many SVs that are homozygous
in the assembly". Numbers unchanged; checked against Supplementary Table 19.

Follow-up (author, lead sentence L1): the subsection now starts "We next asked whether
LongPhase 2 also places SVs on the correct haplotype."

Follow-up (author, option A1): the definition is now two sentences without the
block-orientation step (kept in Methods): "Because SVs are sparse, we scored each
heterozygous deletion and insertion of at least 50 bp called by Sniffles2 separately, not as
adjacent variant pairs. An SV was wrongly phased when it was placed on a different haplotype
from that in the T2T-HG002 assembly (Methods)." No tool is named, so the rule applies to
every phaser.

Follow-up (author, option 1): the lead sentence is now "We next asked whether the lower error
rates of LongPhase 2 extend to SVs.", because the subsection compares phasers.
