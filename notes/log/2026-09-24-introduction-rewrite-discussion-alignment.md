# Introduction rewrite and Discussion alignment, 2026-09-24 (later pass)

**Introduction rewrite and Discussion alignment, 2026-09-24 (later pass).** Supersedes
the novelty and HiPhase statements in the entry below. LongHap (Pfennig & Akey, bioRxiv
2026; `pfennig2026longhap`) co-phases SNVs, indels and SVs and adds 5mC in a final
gap-bridging stage, so the four-class novelty sentence was removed from Introduction and
Discussion; both now contrast joint (LongPhase 2) with post-hoc use of methylation
(NanoMethPhase, MethPhaser, HapBridge, LongHap). WhatsHap is stated to co-phase small and
large indels (`martin2016whatshap`), and the HiPhase "HiFi-only joint indel+SV" claim is
gone. First limitation is now 5mC only; the indel-noise sentence was dropped. Third
limitation: LongPhase 1.x per-read `PQ`/`haplotag --log` support described (issues #19,
#28; not cited); GCphase (not learning-based) replaced by NeurHap (`xue2022neurhap`) in
Introduction and Discussion. Benchmark paragraph rewritten from Hansen 2026 and Wagner
2022 (v4.2.1 omits 12% of autosomes; phase on 74% of heterozygous variants, from
trio/WhatsHap agreement; 85→92% coverage exposed 8× more false negatives). Downstream
tools now cite both WhatsHap and LongPhase; the citing-study clause and the only
main-text pointer to Supplementary Table 6 were removed, so Table 6 is now unreferenced
from the main text (open). Final paragraph cut to the four answers to the limitations,
with no numbers and no Fig. 1 reference. Discussion: v4.2.1 exclusions/700 Mb moved to
the Introduction; added 5mC limitations (male LCL autosomes only, tissue dependence,
X inactivation) and the missing comparison with methylation-aware phasers. Word counts:
Introduction ~1,000, Discussion ~1,300.
