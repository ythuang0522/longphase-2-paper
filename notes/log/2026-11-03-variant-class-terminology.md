# "Variant class" replaces "evidence class/type", 2026-11-03 (author decision)

The text used three names for SNVs, indels, SVs and 5mC: "classes", "variant classes" and "evidence
classes/types". "Evidence" also names read support (evidence weighting, Fig. 1b; the GNN feature group
"Phasing evidence"), so the author chose "variant class" everywhere (options: variant class, marker type,
evidence type, signal/site type).

- Abstract: "these classes" → "these variant classes".
- Results: "four classes of evidence" → "four variant classes"; subsection heading "across evidence types"
  → "across variant classes"; "four evidence classes" and "Each evidence class" → "variant class(es)".
- Discussion: "The evidence classes contributed differently" → "The variant classes ...".
- Fig. 3f: panel title "By evidence type" → "By variant class" (`make_results_figs.py`, regenerated);
  legend "The same by evidence type" → "The same by variant class".
- Supplementary: haplotag "four classes of evidence are collected" → "evidence from the four variant
  classes is collected"; Supplementary Table 17 caption "evidence classes" → "variant classes".
- CLAUDE.md: Fig. 3f description updated. Dated notes and `%` comments keep the old wording.
