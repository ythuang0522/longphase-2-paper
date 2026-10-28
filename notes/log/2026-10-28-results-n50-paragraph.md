# Results: Fig. 2 N50 paragraph compares every tool in each panel, 2026-10-28 (author decision, option A)

The paragraph opened with "Lower switch error rates were accompanied by similar block
contiguity (Fig. 2e–h)", which is false for panels f and h; it compared LongPhase 2 only with
WhatsHap in panel e, and two sentences gave within-tool changes ("Adding indels lengthened the
blocks of WhatsHap by 31–59% but increased its SNV switch error rate by 17–20%"; "the HiFi
blocks of LongPhase 2 were 14–18% longer than without them"). The first five sentences now
state the contrast per panel against every plotted tool: e, up to 11% shorter than WhatsHap
and HapCUT2 at 10–20× and 2–5% longer at 30–60×; f, WhatsHap and HapCUT2 blocks 1.1–1.3- and
1.3–1.4-fold longer at 3.0–3.7- and 3.5–4.8-fold higher switch error rates; g, within 3%; h,
WhatsHap, HapCUT2 and HiPhase 1–8%, 10–17% and 11–17% longer at 2.3–2.9-, 2.9–3.5- and
1.6–1.9-fold higher rates. N50 ratios computed with the Fig. 2 data getters of
`make_results_figs.py` (all plotted coverages; HapCUT2 with indels replicate 1 at 10 and
20–60×). The last three sentences (indels phased, HiFi vs nanopore blocks, runtime) are
unchanged.
