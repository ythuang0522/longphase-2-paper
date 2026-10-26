# GIAB v5.0q preprint, 2026-10-07 (author request)

**GIAB v5.0q preprint, 2026-10-07 (author request).** Olson et al., bioRxiv
10.64898/2026.09.23.752440, is the formal v5.0q benchmark paper; it replaces the `@misc`
`giab2025q100` (which pointed at the wrong `T2T-Q100/` directory) as `olson2026giabv5`
(65 authors, from the bioRxiv `citation_author` tags). The release GRCh38 smvar VCF and BED
(`release/.../v5.0q/`) have the same MD5 as the defrabb v0.020 draft that was scored, so no
rescoring. Correction: Methods said v5.0q "adds 701 Mb of autosomal sequence, mainly satellite
and segmental-duplication sequence"; 701 Mb is the T2T assembly figure (Hansen 2026). Measured on
chr1–22 with the GIAB v3.6 stratifications: the two BEDs share 2,496 Mb; v5.0q adds 83 Mb
(16 Mb tandem repeats, 13 Mb homopolymers) and omits 46 Mb (29 Mb segdups). v5.0q assesses
*less* segdup sequence than v4.2.1 (67 vs 84 Mb of 143 Mb) and almost no satellite (2 Mb of
70 Mb), so neither "satellites" nor "segmental duplications" may be claimed as gains; the
preprint's 1.2× segdup gain does not hold on the autosomes. All 2,180,776 het SNVs in the
v5.0q BED are phased. Methods, the Introduction's last benchmark sentence, the Results scope
sentence and the Supp. table of versions were rewritten (Nature Methods register, second
pass after author review); Data availability names the release files and URL. The
Introduction keeps the 701 Mb assembly figure, which is correct for the assembly. Open
opportunity (not done): the release `stvar` benchmark is phased and could score SV phase.
