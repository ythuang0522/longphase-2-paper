"""Drafts 10A (one figure, three steps) and 10B (two figures)."""
from panels10 import *

# ------------------------------------------------------------------ 10A --
F = Fig(160, 84)
F.letter(1, 5, "a", "Alignment selection")
align_select(F, 0, 7, 50)
F.line(53, 3, 53, 34, color=LGREY, lw=0.4)
F.letter(56, 5, "b", "Allele extraction")
allele_extract(F, 56, 7, 104)
F.line(1, 37, 159, 37, color=LGREY, lw=0.4)
F.letter(1, 43, "c", "Copy-number-aware filter")
clip_profile(F, 2, 47, 66, h=30)
mr_examples(F, 74, 45, 86)
F.save("draft_10A")

# ------------------------------------------------------------------ 10B-1 --
F = Fig(160, 64)
F.letter(1, 5, "a", "Alignment selection")
align_select(F, 0, 7, 50)
F.line(53, 3, 53, 34, color=LGREY, lw=0.4)
F.letter(56, 5, "b", "Allele extraction")
allele_extract(F, 56, 7, 104)
F.line(1, 37, 159, 37, color=LGREY, lw=0.4)
F.letter(1, 43, "c", "Indel in a tandem repeat")
tr_indel(F, 0, 44)
F.letter(81, 43, "d", "Homopolymer SNVs (nanopore)")
hp_snv(F, 80, 44)
F.save("draft_10B_fig1")

# ------------------------------------------------------------------ 10B-2 --
F = Fig(160, 50)
F.letter(1, 5, "a", "Interval detection")
clip_profile(F, 2, 8, 72, h=36, detail=True)
F.line(78, 3, 78, 47, color=LGREY, lw=0.4)
F.letter(81, 5, "b", "Site removal")
mr_examples(F, 80, 7, 80)
F.save("draft_10B_fig2")
