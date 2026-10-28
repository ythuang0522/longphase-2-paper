# Fig. 1a: input sources tagged (option D3), 2026-10-27 (author decision)

After the Results overview named upstream variant callers and the `modcall` module, the author asked that Fig. 1a show where each evidence class comes from, and that it distinguish the external callers from the new LongPhase 2 module. Six drafts in two rounds (A/B/C, then A3/C2/D3); the author chose D3. Panel b is unchanged.

| Old | New |
|---|---|
| Legend: SNV, Indel, SV / Methylated CpG, Unmethylated CpG | Legend rows tagged by source: dashed grey "Upstream callers" (SNV, Indel, SV); solid navy "LongPhase 2 modcall" (Methylated, Unmethylated) |
| CpG column not marked | Navy "modcall" tag above the CpG column and a light navy band (#E9EEF5) through every read; not yellow, which marks problems in panels b and c |
| Read pitch 74 px, reference at y 151.5 | Read pitch 66 px, reference at y 196 |
| Legend a: "SNVs, small indels, SVs and 5mC sites carried by the same long reads enter one phasing problem; ..." | "SNVs, small indels and SVs from upstream variant callers (dashed tag) and 5mC sites called by the \texttt{modcall} module of \toolname (navy tag), carried by the same long reads, enter one phasing problem; ..." |

All text is at least 17 px (5 pt at 180 mm). Source: `figures-source/make_fig1.py`.
