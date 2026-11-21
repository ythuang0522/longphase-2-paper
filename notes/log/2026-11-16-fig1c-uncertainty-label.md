# 2026-11-16 Fig. 1c: phasing-uncertainty bar chart replaced by a label

Author: the per-variant phasing-uncertainty bar chart in Fig. 1c was too detailed for the method
overview; phasing entropy is part of the GNN stage, not a separate feature. Options offered:
A remove fully (caption changed to "candidate variants"), B label only, C no change. Author chose B
after a draft PNG.

- `figures-source/make_fig1.py`: removed the five bars, both axes and the rotated "Phasing
  uncertainty" axis title; the yellow trigger column now covers the window nodes only, with the
  label "High uncertainty" above it. Layout of the rest of panel c unchanged.
- Fig. 1 legend (`main.tex`, panel c): unchanged; it already says "variants with high phasing
  uncertainty".
- README figure note updated.
