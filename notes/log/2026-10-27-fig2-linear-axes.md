# Fig. 2 switch-error axes changed from log to linear, 2026-10-27 (author decision)

After Fig. 3 moved to linear switch-error axes the same day, the author compared Fig. 2 with log and
linear axes (draft PNGs) and chose linear, so that one metric uses one scale in Figs. 2 and 3.

| Panel | Before (log) | After (linear, from 0) |
|---|---|---|
| a | 0.018–0.32% | 0–0.3% |
| b | 0.018–1.4% | 0–1.0% |
| c | 0.018–0.32% | 0–0.20% |
| d | 0.018–0.32% | 0–0.3% |
| e | x 0.018–0.32% | x 0–0.3% |
| f | x 0.018–0.45% | x 0–0.4% |
| g | x 0.025–0.2% | x 0–0.20% |
| h | x 0.025–0.35% | x 0–0.3% |

Effects the author saw before deciding: on the linear axis the HiFi gaps (c, d) are clearer; in b, the
LongPhase 2 SNV-pair and indel-pair lines lie close together near 0 because the axis reaches 1% for the
WhatsHap indel pairs; the LongPhase 2 paths in e and f are steep.

Code: `_log_rate_axis()` replaced by `_rate_axis()`; `_tradeoff_axis()` is linear and takes `xticks`;
`_rate_ticks()` gives every label on an axis the same number of decimals (also applied to Fig. 3d–f, whose
tick labels now read 0.00–0.20 and 0.0–0.3). Legend: "(log scale)" removed from the Fig. 2 legend. Fig. 4d,e
and Supplementary Fig. 14c keep their log switch-error axes: the author saw linear drafts of both and
kept log (Fig. 4d,e spans three decades, so five of six rows merge near 0 on a linear axis). No numbers or text claims changed.
