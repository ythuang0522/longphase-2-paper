#!/usr/bin/env python3
"""Generate supplementary method figures (SVG) for the LongPhase 2 manuscript.

Style follows Fig. 1: white background, flat vector geometry, Helvetica/Arial,
haplotype 1 = blue (#1687C9), haplotype 2 = red (#DC2B23), neutral greys,
amber for uncertain/flagged items. Run:  python3 make_supp_figs.py
Then convert:  for f in *.svg; do rsvg-convert -f pdf -o ${f%.svg}.pdf $f; done
"""
import math, os

H1 = "#1687C9"; H1D = "#103A82"; H2 = "#DC2B23"; H2L = "#F0766C"
INK = "#16233D"; GREY = "#6F8090"; LGREY = "#CBD5DE"; VLGREY = "#EEF2F5"
AMBER = "#E0A030"; AMBERL = "#FCF1C7"; GREEN = "#2E8B57"

STYLE = """
<style>
 text{font-family:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;fill:%s}
 .pl{font-size:22px;font-weight:700}
 .h{font-size:15px;font-weight:600}
 .t{font-size:13px}
 .tb{font-size:13px;font-weight:600}
 .s{font-size:11px;fill:%s}
 .sb{font-size:11px;font-weight:600}
 .m{font-size:13px;font-style:italic}
 .code{font-family:Menlo,Consolas,"Courier New",monospace;font-size:11.5px}
 .w{fill:#ffffff}
</style>
""" % (INK, GREY)

class SVG:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                      f'<title>{title}</title>', STYLE,
                      '<defs>'
                      f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GREY}"/></marker>'
                      f'<marker id="arrd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
                      '</defs>',
                      f'<rect width="{w}" height="{h}" fill="#ffffff"/>']
    def add(self, s): self.parts.append(s)
    def text(self, x, y, s, cls="t", anchor="start", fill=None, rot=None):
        s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        f = f' fill="{fill}"' if fill else ""
        r = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
        self.add(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{f}{r}>{s}</text>')
    def line(self, x1, y1, x2, y2, stroke=GREY, w=1.2, dash=None, arrow=False, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = ' marker-end="url(#arr)"' if arrow else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{d}{a}/>')
    def path(self, d, stroke=GREY, w=1.2, fill="none", dash=None, arrow=False, op=1):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        a = ' marker-end="url(#arr)"' if arrow else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{dd}{a}/>')
    def rect(self, x, y, w, h, fill=VLGREY, stroke="none", sw=1, r=3, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')
    def circle(self, cx, cy, r, fill="#fff", stroke=INK, sw=1.5):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def node(self, cx, cy, label, color, r=11, filled=True, cls="sb"):
        if filled:
            self.circle(cx, cy, r, fill=color, stroke=color)
            self.text(cx, cy + 4, label, cls=cls, anchor="middle", fill="#fff")
        else:
            self.circle(cx, cy, r, fill="#fff", stroke=color, sw=1.8)
            self.text(cx, cy + 4, label, cls=cls, anchor="middle", fill=color)
    def panel(self, x, y, letter, title=None):
        self.text(x, y, letter, cls="pl")
        if title: self.text(x + 22, y, title, cls="h")
    def read(self, x1, x2, y, color=LGREY, w=5):
        self.line(x1, y, x2, y, stroke=color, w=w, cap="round")
    def save(self, name):
        self.add('</svg>')
        with open(name, "w") as f: f.write("\n".join(self.parts))
        print("wrote", name)

# ----------------------------------------------------------------------------
# S1  Read-level allele extraction and pre-graph filters
# ----------------------------------------------------------------------------
def fig_s1():
    S = SVG(1100, 560, "Read-level allele observations and filters")
    # a: allele observations from one read
    S.panel(20, 34, "a", "Allele observations extracted from one alignment")
    y0 = 90
    S.text(52, y0 + 4, "Ref", cls="s", anchor="end")
    S.line(60, y0, 520, y0, stroke=INK, w=2)
    cols = [(80, "SNV", "A/G"), (170, "Indel", "T/TAC"), (270, "SV", "DEL 1.2 kb"), (380, "5mC", "CpG"), (470, "SNV", "C/T")]
    for x, k, lab in cols:
        S.line(x, y0 - 6, x, y0 + 6, stroke=INK, w=2)
        S.text(x, y0 - 12, k, cls="sb", anchor="middle")
        S.text(x, y0 + 20, lab, cls="s", anchor="middle")
    yr = y0 + 48
    S.text(52, yr + 4, "Read", cls="s", anchor="end")
    S.read(60, 510, yr, color=LGREY, w=8)
    # observations
    obs = [(80, "G", "Q=22", H2), (170, "+AC", "CIGAR I", H1), (270, "DEL", "CIGAR D / RNAMES", H1), (380, "m", "ML=0.93", H2), (470, "C", "Q=9", H1)]
    for x, a, src, c in obs:
        S.node(x, yr, a if len(a) <= 2 else "", c, r=10)
        if len(a) > 2: S.text(x, yr + 4, a, cls="sb", anchor="middle", fill="#fff")
        S.text(x, yr + 30, src, cls="s", anchor="middle")
    # weights table
    ty = yr + 62
    S.text(30, ty, "Observation quality used for edge weighting", cls="tb")
    rows = [("SNV", "Phred base quality; edge weight 1 if both bases ≥ Q12, else 0.1"),
            ("Indel", "CIGAR I/D starting at the site; fixed high quality; tandem-repeat indels flagged"),
            ("SV", "caller read list → ALT (high quality); unlisted reads → REF (lower quality)"),
            ("5mC", "modcall read lists, strand-matched; fixed high quality")]
    for i, (k, v) in enumerate(rows):
        yy = ty + 20 + i * 18
        S.text(30, yy, k, cls="sb"); S.text(80, yy, v, cls="s")
    # b: homopolymer SNV filter
    S.panel(580, 34, "b", "Homopolymer SNV filter (nanopore)")
    yb = 80
    seq = "G T A A A A A C A A A A T G"
    S.text(590, yb, "Ref", cls="s")
    S.rect(625 + 2 * 22 - 11, yb - 14, 22 * 5, 20, fill=AMBERL, r=4)
    S.rect(625 + 8 * 22 - 11, yb - 14, 22 * 4, 20, fill=AMBERL, r=4)
    for i, ch in enumerate(seq.split()):
        S.text(625 + i * 22, yb, ch, cls="code", anchor="middle", fill=INK)
    S.line(625 + 5 * 22, yb + 12, 625 + 5 * 22, yb + 30, stroke=H2, w=2)
    S.line(625 + 7 * 22, yb + 12, 625 + 7 * 22, yb + 30, stroke=H2, w=2)
    S.text(625 + 5 * 22, yb + 44, "SNV₁", cls="sb", anchor="middle")
    S.text(625 + 7 * 22, yb + 44, "SNV₂", cls="sb", anchor="middle")
    S.text(590, yb + 70, "Both SNVs in homopolymers of length ≥ 3 and ≤ 2 bp apart", cls="s")
    S.text(590, yb + 86, "→ downstream SNV removed from all reads", cls="s")
    # c: overlapping alignment filter
    S.panel(580, 210, "c", "Overlapping-alignment filter")
    yc = 250
    S.line(590, yc, 1080, yc, stroke=INK, w=1.5)
    S.read(620, 850, yc + 22, color=H1, w=6); S.text(612, yc + 26, "A₁", cls="sb", anchor="end")
    S.read(760, 1050, yc + 44, color=H1, w=6); S.text(752, yc + 48, "A₂", cls="sb", anchor="end")
    S.rect(760, yc + 12, 90, 40, fill=AMBERL, r=3, op=0.8)
    S.text(805, yc + 70, "overlap", cls="s", anchor="middle")
    S.text(590, yc + 96, "Two alignments of one read; overlap / combined span ≥ 0.2", cls="s")
    S.text(590, yc + 112, "→ the shorter alignment (A₁) is discarded", cls="s")
    # d: tandem-repeat indel flag
    S.panel(580, 400, "d", "Tandem-repeat indel flag")
    yd = 440
    seq2 = "G CA CA CA CA CA T"
    S.rect(615, yd - 14, 150, 20, fill=AMBERL, r=4)
    x = 600
    for tok in seq2.split():
        S.text(x, yd, tok, cls="code", anchor="middle", fill=INK)
        x += 30
    S.text(690, yd + 30, "+CA / −CA indel inside a CA repeat", cls="s", anchor="middle")
    S.text(590, yd + 60, "Flagged indels stay in the graph but vote with weight 0.1", cls="s")
    S.text(590, yd + 76, "and contribute 0.1 to read haplotype assignment", cls="s")
    # a (cont.): CNV note
    S.text(30, 460, "See Supplementary Fig. 4 for the copy-number-aware filter applied after these steps.", cls="s")
    S.save("suppfig1_observations.svg")

# ----------------------------------------------------------------------------
# S2  Pairwise support, edge weights and vote rules
# ----------------------------------------------------------------------------
def fig_s2():
    S = SVG(1100, 600, "Pairwise allele support and vote weighting")
    S.panel(20, 34, "a", "Four allele-pair weights between two variants")
    ux, vx = 200, 480
    yt, yb = 120, 220
    S.text(ux, 78, "variant u", cls="h", anchor="middle"); S.text(vx, 78, "variant v", cls="h", anchor="middle")
    S.node(ux, yt, "r", H1, r=14); S.node(ux, yb, "a", H2, r=14)
    S.node(vx, yt, "r", H1, r=14); S.node(vx, yb, "a", H2, r=14)
    S.text(ux - 24, yt + 4, "uʳ", cls="m", anchor="end"); S.text(ux - 24, yb + 4, "uᵃ", cls="m", anchor="end")
    S.text(vx + 24, yt + 4, "vʳ", cls="m"); S.text(vx + 24, yb + 4, "vᵃ", cls="m")
    S.line(ux + 14, yt, vx - 14, yt, stroke=H1, w=6); S.text((ux + vx) / 2, yt - 12, "wᵣᵣ = 9", cls="tb", anchor="middle")
    S.line(ux + 14, yb, vx - 14, yb, stroke=H2, w=5); S.text((ux + vx) / 2, yb + 24, "wₐₐ = 7", cls="tb", anchor="middle")
    S.line(ux + 12, yt + 8, vx - 12, yb - 8, stroke=LGREY, w=2.5); S.line(ux + 12, yb - 8, vx - 12, yt + 8, stroke=LGREY, w=2.5)
    S.text(vx - 40, (yt + yb) / 2 - 14, "wᵣₐ = 1", cls="s", anchor="end"); S.text(vx - 40, (yt + yb) / 2 + 22, "wₐᵣ = 0.1", cls="s", anchor="end")
    S.text(40, 280, "P = wᵣᵣ + wₐₐ = 16   (cis: same haplotype carries r and r)", cls="t")
    S.text(40, 300, "Q = wᵣₐ + wₐᵣ = 1.1   (trans)", cls="t")
    S.text(40, 328, "similarity  s = min(P,Q) / max(P,Q) = 0.07", cls="t")
    S.text(40, 356, "Per read: +1 if both bases ≥ Q12, else +0.1 (grey edges here carry a low-quality read).", cls="s")
    # b: vote decision rules
    S.panel(600, 34, "b", "Vote rules for the pair (u, v)")
    rows = [("s > 0.7", "no vote (uninformative pair)", GREY),
            ("s > 0.3 for SNV–5mC pairs", "no vote", GREY),
            ("0.1 < s ≤ 0.7", "vote for larger of P, Q; weight 1", INK),
            ("s ≤ 0.1, or one side has no support", "vote; weight 20 (near-unanimous)", GREEN),
            ("u is a tandem-repeat indel", "vote; weight 0.1", AMBER)]
    y = 80
    S.rect(600, y - 16, 470, 22 * len(rows) + 10, fill=VLGREY, r=6)
    for cond, act, c in rows:
        S.text(612, y + 2, cond, cls="sb", fill=c); S.text(830, y + 2, act, cls="s")
        y += 22
    S.text(600, y + 20, "The vote is expressed as a haplotype for v using the haplotype already", cls="s")
    S.text(600, y + 36, "assigned to u: P favours vʳ on hap(uʳ), Q favours vʳ on hap(uᵃ).", cls="s")
    # c: one-long-read guard
    S.panel(600, 300, "c", "Single-read guard")
    y = 340
    S.text(600, y, "Among the votes received by v, count those whose pair is supported by", cls="s")
    S.text(600, y + 16, "a single read (P + Q ≤ 1). If more than three such votes exist, h₁ and h₂", cls="s")
    S.text(600, y + 32, "are recomputed from high-consistency (s < 0.2), non-indel votes only,", cls="s")
    S.text(600, y + 48, "preventing one chimeric ultra-long read from dominating a sparse region.", cls="s")
    # d: what the DOT graph stores
    S.panel(20, 420, "d", "Exported graph (DOT)")
    S.text(40, 456, '1001.1 -> 1543.1 [label=16.0]', cls="code")
    S.text(40, 474, '1001.2 -> 1543.2 [label=1.1]', cls="code")
    S.text(40, 500, "position.allele → position.allele, label = accumulated haplotype vote weight at the source;", cls="s")
    S.text(40, 516, "one edge per voting pair; parsed by the GNN module together with INFO/PE, H1, H2.", cls="s")
    S.save("suppfig2_pair_support.svg")

# ----------------------------------------------------------------------------
# S3  Multi-neighbour voting and phasing entropy
# ----------------------------------------------------------------------------
def fig_s3():
    S = SVG(1100, 520, "Multi-neighbour voting and phasing entropy")
    S.panel(20, 34, "a", "Variant v receives weighted votes from up to k = 35 upstream variants")
    xs = [80, 160, 240, 320, 400, 480]
    yt, yb = 130, 210
    labels = ["v₋₅", "v₋₄", "v₋₃", "v₋₂", "v₋₁", "v"]
    hp = [1, 2, 1, 1, 2, None]
    for x, lab, h in zip(xs, labels, hp):
        S.text(x, 100, lab, cls="m", anchor="middle")
        if h == 1:
            S.node(x, yt, "r", H1, r=11); S.node(x, yb, "a", H2, r=11)
        elif h == 2:
            S.node(x, yt, "r", H2, r=11); S.node(x, yb, "a", H1, r=11)
        else:
            S.node(x, yt, "r", GREY, r=11, filled=False); S.node(x, yb, "a", GREY, r=11, filled=False)
    # votes to v
    votes = [(0, 1, 20, H1), (1, 1, 1, H1), (2, 1, 1, H1), (3, 2, 1, H2), (4, 1, 0.1, H1)]
    for i, hap, w, c in votes:
        x = xs[i]
        d = f"M{x+11},{yt if hap==1 else yb} C{(x+xs[5])/2},{yt-60 if hap==1 else yb+60} {(x+xs[5])/2},{yt-60 if hap==1 else yb+60} {xs[5]-11},{yt if hap==1 else yb}"
        S.path(d, stroke=c, w=max(1, min(6, 1 + math.log10(w + 1) * 3)), op=0.8)
        S.text((x + xs[5]) / 2 + (i - 2) * 6, (yt - 66 + i * 5) if hap == 1 else (yb + 60), f"{w:g}", cls="sb", anchor="middle", fill=c)
    S.text(560, yt + 4, "votes for hap 1", cls="s"); S.text(560, yb + 4, "votes for hap 2", cls="s")
    S.text(40, 290, "h₁(v) = 20 + 1 + 1 + 0.1 = 22.1        h₂(v) = 1", cls="t")
    S.text(40, 314, "v assigned to haplotype 1;  tie h₁ = h₂ opens a new phase block (PS = position of first variant)", cls="s")
    # b: entropy
    S.panel(640, 34, "b", "Phasing entropy PE")
    S.text(660, 76, "PE(v) = − Σ pᵢ log₂ pᵢ,   pᵢ = hᵢ / (h₁ + h₂)", cls="t")
    # small bars examples
    ex = [("22.1 : 1", 22.1, 1), ("3 : 1", 3, 1), ("4 : 3", 4, 3), ("5 : 5", 5, 5)]
    x0 = 660
    for i, (lab, a, b) in enumerate(ex):
        y = 110 + i * 46
        tot = a + b
        S.text(x0, y + 14, lab, cls="sb")
        S.rect(x0 + 60, y, 200 * a / tot, 18, fill=H1, r=2)
        S.rect(x0 + 60 + 200 * a / tot, y, 200 * b / tot, 18, fill=H2, r=2)
        p1, p2 = a / tot, b / tot
        pe = -(p1 * math.log2(p1) + p2 * math.log2(p2)) if p2 > 0 else 0
        S.text(x0 + 275, y + 14, f"PE = {pe:.3f}", cls="tb", fill=AMBER if pe >= 0.8 else INK)
    S.rect(x0 + 55, 150, 330, 76, fill="none", stroke=AMBER, sw=1.5, dash="4,3", r=4)
    S.text(x0 + 60, 312, "PE ≥ 0.80 triggers a GNN window (Supplementary Fig. 6)", cls="s", fill=AMBER)
    S.text(x0, 340, "Written to VCF as INFO/PE, INFO/H1, INFO/H2 for every phased variant.", cls="s")
    # c: read-quality weighting reminder
    S.panel(20, 380, "c", "Block formation")
    S.text(40, 412, "Variants are visited in coordinate order. Each assigned variant casts votes to its next k neighbours", cls="s")
    S.text(40, 428, "within 300 kb; a variant that receives no informative vote, or a tie, starts a new block. Blocks with a", cls="s")
    S.text(40, 444, "single variant are dropped. Haplotype labels are propagated along the block to produce phased GTs (0|1 / 1|0).", cls="s")
    S.save("suppfig3_voting_entropy.svg")

# ----------------------------------------------------------------------------
# S4  Copy-number-aware filter
# ----------------------------------------------------------------------------
def fig_s4():
    S = SVG(1100, 560, "Copy-number-aware filtering of unreliable heterozygous sites")
    S.panel(20, 34, "a", "Clipping-based detection of copy-number-altered intervals")
    x0, x1, yb = 60, 1040, 190
    S.line(x0, yb, x1, yb, stroke=INK, w=1.5)
    S.text(x0, yb + 18, "genomic position →", cls="s")
    # front clips (up) and back clips (down)
    import random
    random.seed(3)
    for x in range(x0 + 10, x1, 14):
        up = random.randint(0, 1); dn = random.randint(0, 1)
        if 380 <= x <= 420: up += random.randint(4, 8)
        if 640 <= x <= 690: dn += random.randint(4, 8)
        if 420 < x < 640: up += random.randint(0, 2); dn += random.randint(0, 1)
        if up: S.rect(x - 4, yb - 8 * up, 8, 8 * up, fill=H1, r=1)
        if dn: S.rect(x - 4, yb, 8, 8 * dn, fill=H2L, r=1)
    S.text(x0, yb - 90, "alignments starting (front-clipped)", cls="s", fill=H1)
    S.text(x0, yb + 40, "alignments ending (back-clipped)", cls="s", fill=H2L)
    S.rect(380, yb - 105, 310, 175, fill=AMBERL, r=4, op=0.5)
    S.text(535, yb - 112, "candidate CNV interval", cls="sb", anchor="middle", fill=AMBER)
    S.text(700, yb - 60, "open: ≥ 5 front-clips at one position", cls="s")
    S.text(700, yb - 44, "extend: running (starts − ends) > 0, ≤ 200 kb", cls="s")
    S.text(700, yb - 28, "close: back-clips ≥ pull-down count", cls="s")
    # b: mismatch scoring within interval
    S.panel(20, 290, "b", "Removing heterozygous calls whose ALT reads carry the mismatches")
    yv = 340
    S.text(40, yv - 8, "Variant inside interval; other heterozygous sites on the same reads shown as ticks", cls="s")
    reads = [("REF", H1, [0, 0, 0, 1, 0, 0, 0]), ("REF", H1, [0, 0, 0, 0, 0, 1, 0]), ("REF", H1, [0, 0, 0, 0, 0, 0, 0]),
             ("ALT", H2, [1, 1, 0, 1, 1, 1, 0]), ("ALT", H2, [1, 0, 1, 1, 1, 0, 1]), ("ALT", H2, [0, 1, 1, 1, 0, 1, 1])]
    for i, (al, c, mm) in enumerate(reads):
        y = yv + 20 + i * 22
        S.text(60, y + 4, al, cls="sb", anchor="end", fill=c)
        S.read(80, 560, y, color=LGREY, w=6)
        S.node(320, y, "", c, r=7)
        for j, m in enumerate(mm):
            xx = 110 + j * 65
            if xx == 320: continue
            S.line(xx, y - 6, xx, y + 6, stroke=H2 if m else GREY, w=2 if m else 1)
    S.text(600, yv + 30, "mean mismatches per read", cls="sb")
    S.text(600, yv + 50, "REF-supporting reads:  0.7", cls="s", fill=H1)
    S.text(600, yv + 66, "ALT-supporting reads:  4.7", cls="s", fill=H2)
    S.text(600, yv + 92, "ratio = ALT / (REF + ALT) = 0.87  ≥ 0.7", cls="tb")
    S.text(600, yv + 112, "→ site removed from all reads before graph construction", cls="s")
    S.text(600, yv + 140, "Targets heterozygous calls created by collapsed", cls="s")
    S.text(600, yv + 156, "paralogues or copy-number change, whose ALT allele", cls="s")
    S.text(600, yv + 172, "co-occurs with a paralogue-specific mismatch pattern.", cls="s")
    S.save("suppfig4_cnv_filter.svg")

# ----------------------------------------------------------------------------
# S5  Read-based correction
# ----------------------------------------------------------------------------
def fig_s5():
    S = SVG(1100, 520, "Read-based correction")
    S.panel(20, 34, "a", "Step 1: assign each read to a haplotype from the initial phase")
    xs = [120, 200, 280, 360, 440, 520]
    yv = 80
    for i, x in enumerate(xs):
        S.text(x, yv, f"v{i+1}", cls="m", anchor="middle")
    reads = [([1, 1, 1, 1, None, 1], "hap 1  (5/5)", H1, True),
             ([2, 2, None, 2, 2, 2], "hap 2  (5/5)", H2, True),
             ([1, 1, 2, 1, 1, None], "hap 1  (4/5 = 0.80)", H1, True),
             ([1, 2, 2, 1, None, None], "untagged (2/4 = 0.50)", GREY, False),
             ([None, None, 2, None, None, None], "untagged (< 2 alleles)", GREY, False)]
    for i, (al, lab, c, ok) in enumerate(reads):
        y = yv + 30 + i * 30
        S.read(90, 560, y, color=LGREY if not ok else (H1 if c == H1 else H2L), w=6)
        for x, a in zip(xs, al):
            if a is None: continue
            S.node(x, y, "r" if a == 1 else "a", H1 if a == 1 else H2, r=8, cls="s")
        S.text(580, y + 4, lab, cls="s", fill=c)
    S.text(40, 260, "A read is tagged when max(n₁,n₂)/(n₁+n₂) > 0.65 and it carries ≥ 2 informative alleles;", cls="s")
    S.text(40, 276, "SNV and SV alleles count 1, indels 0.1, 5mC 0.", cls="s")
    # b: re-derive variant phase
    S.panel(20, 320, "b", "Step 2: re-derive each variant's phase from tagged reads")
    y = 360
    S.text(40, y, "For variant v₃:", cls="tb")
    S.text(40, y + 22, "hap-1 reads with REF + hap-2 reads with ALT  = n₁ = 1", cls="s")
    S.text(40, y + 38, "hap-1 reads with ALT + hap-2 reads with REF  = n₂ = 2", cls="s")
    S.text(40, y + 60, "confidence ρ = max(n₁,n₂)/(n₁+n₂) = 0.67  ≤ 0.75", cls="tb", fill=AMBER)
    S.text(40, y + 80, "→ v₃ left unphased (GT 0/1, no PS)", cls="s", fill=AMBER)
    S.text(560, y, "For variant v₁:", cls="tb")
    S.text(560, y + 22, "n₁ = 3,  n₂ = 0,  ρ = 1.00 > 0.75", cls="s")
    S.text(560, y + 42, "→ phase confirmed: REF on hap 1, ALT on hap 2 (GT 0|1)", cls="s", fill=GREEN)
    S.text(560, y + 70, "Only variants supported by the two read populations keep a", cls="s")
    S.text(560, y + 86, "phase; assignments driven by a few chimeric or mis-mapped", cls="s")
    S.text(560, y + 102, "reads are removed. Thresholds: --readConfidence 0.65,", cls="s")
    S.text(560, y + 118, "--snpConfidence 0.75.", cls="s")
    S.save("suppfig5_read_correction.svg")

# ----------------------------------------------------------------------------
# S6  GNN window construction
# ----------------------------------------------------------------------------
def fig_s6():
    S = SVG(1100, 600, "Window construction for the graph neural network")
    S.panel(20, 34, "a", "A window is opened around every phased variant with PE ≥ 0.8")
    n = 13; x0 = 90; dx = 70; yt, yb = 130, 200
    center = 6
    for i in range(n):
        x = x0 + i * dx
        c1, c2 = (H1, H2) if i % 5 != 3 else (H2, H1)
        if i == center:
            S.rect(x - 22, yt - 24, 44, yb - yt + 48, fill=AMBERL, r=6)
        S.node(x, yt, "r", c1, r=10, cls="s"); S.node(x, yb, "a", c2, r=10, cls="s")
        lab = "c" if i == center else (f"{i-center:+d}" if abs(i - center) <= 2 or i in (0, n - 1) else "")
        if i == 0: lab = "−20"
        if i == n - 1: lab = "+20"
        S.text(x, yt - 32, lab, cls="s", anchor="middle")
    # edges: sample some DOT edges
    import random
    random.seed(7)
    for i in range(n):
        for j in range(i + 1, min(n, i + 4)):
            if random.random() < 0.7:
                xi, xj = x0 + i * dx, x0 + j * dx
                S.path(f"M{xi+8},{yt-6} Q{(xi+xj)/2},{yt-40-(j-i)*8} {xj-8},{yt-6}", stroke=H1, w=1.2, op=0.5)
                S.path(f"M{xi+8},{yb+6} Q{(xi+xj)/2},{yb+40+(j-i)*8} {xj-8},{yb+6}", stroke=H2, w=1.2, op=0.5)
    # cross edge near center
    xi, xj = x0 + 5 * dx, x0 + 7 * dx
    S.line(xi + 8, yt + 6, xj - 8, yb - 6, stroke=GREY, w=1.5, dash="3,3")
    S.text(560, 270, "center zone: predictions kept", cls="s", anchor="middle", fill=AMBER)
    S.rect(x0 + 3.5 * dx, 100, 5 * dx, 150, fill="none", stroke=AMBER, sw=1.2, dash="4,3", r=6)
    S.text(40, 305, "• up to 20 variants on each side (≤ 41 variants, ≤ 82 allele nodes; windows above 256 nodes are skipped)", cls="s")
    S.text(40, 321, "• nodes: one per allele; SNV, indel, SV and 5mC records are merged and sorted by position", cls="s")
    S.text(40, 337, "• edges: DOT edges with both endpoints in the window, symmetrized, plus one self-loop per node (mean of incident edge features)", cls="s")
    S.text(40, 353, "• predictions of the two allele nodes are averaged; a variant covered by several windows receives the mean", cls="s")
    # b: bridge vertex
    S.panel(20, 400, "b", "Bridge vertex feature")
    xb = 60; y = 450
    pts = [(xb + i * 45, y + (0 if i % 2 == 0 else 22)) for i in range(9)]
    for i in range(8):
        if i == 3: continue
        S.line(*pts[i], *pts[i + 1], stroke=GREY, w=1.5)
    S.line(*pts[3], *pts[4], stroke=GREY, w=1.5)
    S.line(*pts[2], *pts[4], stroke=GREY, w=1.5) if False else None
    for i, (px, py) in enumerate(pts):
        S.circle(px, py, 7, fill=AMBER if i == 4 else "#fff", stroke=AMBER if i == 4 else GREY, sw=1.5)
    S.text(xb + 4 * 45, y + 50, "removing this variant disconnects the window → is_bridge = 1", cls="s", anchor="middle", fill=AMBER)
    # c: center mask formula
    S.panel(600, 400, "c", "Center-zone mask")
    S.text(620, 440, "r = |pos − pos_c| / max offset in window", cls="s")
    S.text(620, 458, "kept if r ≤ min(1, 10 / round(20·r_max))", cls="s")
    S.text(620, 476, "so that predictions are read only where both", cls="s")
    S.text(620, 492, "sides of the variant are visible to the network.", cls="s")
    S.save("suppfig6_gnn_window.svg")

# ----------------------------------------------------------------------------
# S7  GNN architecture
# ----------------------------------------------------------------------------
def fig_s7():
    S = SVG(1100, 640, "Graph neural network architecture")
    def box(x, y, w, h, label, sub=None, fill=VLGREY, stroke=LGREY, tc=INK):
        S.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1, r=6)
        S.text(x + w / 2, y + h / 2 + (4 if not sub else -2), label, cls="tb", anchor="middle", fill=tc)
        if sub: S.text(x + w / 2, y + h / 2 + 14, sub, cls="s", anchor="middle")
    # inputs
    box(40, 60, 200, 44, "node features", "N × 31", fill="#fff", stroke=INK)
    box(40, 120, 200, 44, "edge features", "N × N × 6", fill="#fff", stroke=INK)
    box(40, 180, 200, 44, "adjacency", "N × N (undirected + self-loops)", fill="#fff", stroke=INK)
    # input processing
    box(290, 60, 180, 44, "BatchNorm (frozen)", "per-feature standardization")
    box(290, 120, 180, 44, "Linear 31 → 128", "+ GELU")
    S.line(240, 82, 290, 82, arrow=True); S.line(380, 104, 380, 120, arrow=True)
    # layer block
    lx, ly, lw, lh = 520, 40, 540, 400
    S.rect(lx, ly, lw, lh, fill="none", stroke=INK, sw=1.2, r=10, dash="6,4")
    S.text(lx + 12, ly + 20, "GPS layer  × 4   (hidden 128, 4 heads)", cls="h")
    # local branch
    box(lx + 30, ly + 50, 220, 70, "Local: GATv2", "attention over xᵢ, xⱼ and edge eᵢⱼ", fill="#E3F1FA", stroke=H1)
    S.text(lx + 140, ly + 132, "softmax over incoming edges of i;", cls="s", anchor="middle")
    S.text(lx + 140, ly + 146, "edge encoder Wₑ (6 → 128) per layer", cls="s", anchor="middle")
    # global branch
    box(lx + 290, ly + 50, 220, 70, "Global: self-attention", "softmax(QKᵀ/√d) V over all N nodes", fill="#FBE7E6", stroke=H2)
    S.text(lx + 400, ly + 132, "Q, K, V, O projections 128 → 128;", cls="s", anchor="middle")
    S.text(lx + 400, ly + 146, "window-wide context", cls="s", anchor="middle")
    # combine
    box(lx + 160, ly + 175, 220, 40, "x + local + global", "additive fusion, residual")
    S.line(lx + 140, ly + 120, lx + 200, ly + 175, arrow=True); S.line(lx + 400, ly + 120, lx + 340, ly + 175, arrow=True)
    box(lx + 160, ly + 230, 220, 34, "LayerNorm")
    box(lx + 160, ly + 279, 220, 44, "FFN 128 → 256 → 128", "GELU, residual")
    box(lx + 160, ly + 338, 220, 34, "LayerNorm")
    for y1, y2 in [(ly + 215, ly + 230), (ly + 264, ly + 279), (ly + 323, ly + 338)]:
        S.line(lx + 270, y1, lx + 270, y2, arrow=True)
    S.line(470, 142, lx + 30, ly + 85, arrow=True)
    S.line(470, 142, lx + 290, ly + 85, arrow=True)
    # loop arrow
    S.path(f"M{lx+380},{ly+355} L{lx+520},{ly+355} L{lx+520},{ly+85} L{lx+512},{ly+85}", stroke=GREY, w=1.2, dash="3,3", arrow=True)
    S.text(lx + 528, ly + 220, "×4", cls="sb")
    # classifier
    box(560, 480, 240, 44, "concat [hᵢ | Σwᵢⱼ | max wᵢⱼ]", "130 features", fill="#fff", stroke=INK)
    box(830, 480, 220, 44, "Linear 130→128, GELU", "Linear 128→2, softmax")
    S.line(lx + 270, ly + 372, lx + 270, 480, arrow=True)
    S.line(800, 502, 830, 502, arrow=True)
    box(830, 550, 220, 44, "P(misphased) per allele node", "averaged over the two alleles", fill=AMBERL, stroke=AMBER)
    S.line(940, 524, 940, 550, arrow=True)
    # edge context from edge features
    S.path("M240,142 L260,142 L260,470 L560,470 L560,480", stroke=GREY, w=1, dash="3,3", arrow=True)
    S.text(270, 462, "edge context (sum, max of raw edge weight over incoming edges)", cls="s")
    # params
    S.text(40, 560, "687,358 parameters; weights compiled into the binary; dense O(N²) attention is inexpensive for N ≤ 256.", cls="s")
    S.text(40, 578, "Exact GELU; LayerNorm ε = 10⁻⁵; LeakyReLU slope 0.2; nodes without incoming edges attend uniformly to all nodes.", cls="s")
    S.save("suppfig7_gnn_architecture.svg")

# ----------------------------------------------------------------------------
# S8  Unphasing and phase-set splitting
# ----------------------------------------------------------------------------
def fig_s8():
    S = SVG(1100, 480, "Unphasing and phase-set splitting")
    S.panel(20, 34, "a", "Before correction: one phase set")
    xs = [80 + i * 70 for i in range(10)]
    yt, yb = 110, 170
    flagged = 5
    for i, x in enumerate(xs):
        S.node(x, yt, "r", H1, r=10, cls="s"); S.node(x, yb, "a", H2, r=10, cls="s")
        if i < 9:
            S.line(x + 10, yt, xs[i + 1] - 10, yt, stroke=H1, w=2); S.line(x + 10, yb, xs[i + 1] - 10, yb, stroke=H2, w=2)
        if i in (3, 7):
            S.path(f"M{x+8},{yt-6} Q{(x+xs[i+2])/2},{yt-45} {xs[i+2]-8},{yt-6}", stroke=H1, w=1.5, op=0.6)
    S.rect(xs[flagged] - 20, yt - 22, 40, yb - yt + 44, fill="none", stroke=AMBER, sw=2, r=6)
    S.text(xs[flagged], yb + 40, "P(error) = 0.62 ≥ 0.30", cls="sb", anchor="middle", fill=AMBER)
    S.text(xs[0], 220, "PS = 1001 for all ten variants;  GT 0|1 / 1|0", cls="s")
    S.panel(20, 270, "b", "After correction: variant unphased, block split")
    yt2, yb2 = 340, 400
    for i, x in enumerate(xs):
        if i == flagged:
            S.node(x, yt2, "r", GREY, r=10, filled=False, cls="s"); S.node(x, yb2, "a", GREY, r=10, filled=False, cls="s")
            S.text(x, yb2 + 30, "GT 0/1, PS removed", cls="s", anchor="middle")
            continue
        S.node(x, yt2, "r", H1, r=10, cls="s"); S.node(x, yb2, "a", H2, r=10, cls="s")
        if i < 9 and i != flagged - 1 and i + 1 != flagged:
            S.line(x + 10, yt2, xs[i + 1] - 10, yt2, stroke=H1, w=2); S.line(x + 10, yb2, xs[i + 1] - 10, yb2, stroke=H2, w=2)
    S.path(f"M{xs[3]+8},{yt2-6} Q{(xs[3]+xs[5])/2},{yt2-45} {xs[5]-8},{yt2-6}", stroke=LGREY, w=1.5, dash="3,3")
    S.text(xs[2], yb2 + 55, "PS = 1001 (largest component keeps the original ID)", cls="s", anchor="middle")
    S.text(xs[7] + 35, yb2 + 55, "PS = 1436 (position of first variant)", cls="s", anchor="middle")
    S.rect(xs[0] - 20, yt2 - 24, xs[4] - xs[0] + 40, 88, fill="none", stroke=H1D, sw=1, dash="4,3", r=6)
    S.rect(xs[6] - 20, yt2 - 24, xs[9] - xs[6] + 40, 88, fill="none", stroke=H1D, sw=1, dash="4,3", r=6)
    S.text(760, 330, "Connectivity is re-checked over the surviving DOT edges", cls="s")
    S.text(760, 346, "of each phase set; edges through the unphased variant", cls="s")
    S.text(760, 362, "(dashed) no longer count. Genotypes are never flipped.", cls="s")
    S.save("suppfig8_unphase_split.svg")

# ----------------------------------------------------------------------------
# S9  modcall
# ----------------------------------------------------------------------------
def fig_s9():
    S = SVG(1100, 600, "Allele-specific methylation calling (modcall)")
    S.panel(20, 34, "a", "Per-read CpG state from ML probability")
    x0, x1, y = 60, 460, 90
    S.line(x0, y, x1, y, stroke=INK, w=1.5)
    for p, lab in [(0, "0"), (0.2, "0.2"), (0.8, "0.8"), (1, "1")]:
        xx = x0 + p * (x1 - x0); S.line(xx, y - 5, xx, y + 5, stroke=INK, w=1.5); S.text(xx, y + 20, lab, cls="s", anchor="middle")
    S.rect(x0, y - 30, 0.2 * (x1 - x0), 22, fill="#E3F1FA", r=3); S.text(x0 + 0.1 * (x1 - x0), y - 14, "unmethylated", cls="sb", anchor="middle", fill=H1)
    S.rect(x0 + 0.2 * (x1 - x0), y - 30, 0.6 * (x1 - x0), 22, fill=VLGREY, r=3); S.text(x0 + 0.5 * (x1 - x0), y - 14, "noise (ignored)", cls="sb", anchor="middle", fill=GREY)
    S.rect(x0 + 0.8 * (x1 - x0), y - 30, 0.2 * (x1 - x0), 22, fill="#FBE7E6", r=3); S.text(x0 + 0.9 * (x1 - x0), y - 14, "methylated", cls="sb", anchor="middle", fill=H2)
    S.text(x0, y + 44, "ML tag / 255; thresholds --modThreshold 0.8, --unModThreshold 0.2", cls="s")
    # b: strand pairing + genotype
    S.panel(20, 170, "b", "CpG strand pairing and site genotype")
    y = 215
    S.text(40, y, "5′ … C G … 3′   forward-strand reads report C;  reverse-strand reads report the G position", cls="s")
    S.text(40, y + 16, "→ reverse-strand calls are mapped to the forward CpG coordinate and the two strands are pooled", cls="s")
    S.text(40, y + 44, "m = methylated reads, u = unmethylated reads, noise = depth − m − u", cls="s")
    S.text(40, y + 70, "heterozygous (allele-specific) if  min(m,u)/max(m,u) ≥ 0.6  and  noise/depth ≤ 0.2", cls="tb")
    S.text(40, y + 90, "otherwise homozygous methylated (m ≥ u) or unmethylated → excluded from phasing", cls="s")
    # example bars
    ex = [("m=14, u=12, noise=2", 14, 12, 2, True), ("m=25, u=2, noise=1", 25, 2, 1, False), ("m=9, u=8, noise=11", 9, 8, 11, False)]
    for i, (lab, m, u, nz, ok) in enumerate(ex):
        yy = y + 115 + i * 26; tot = m + u + nz; w = 260
        S.rect(40, yy, w * m / tot, 16, fill=H2, r=2); S.rect(40 + w * m / tot, yy, w * u / tot, 16, fill=H1, r=2); S.rect(40 + w * (m + u) / tot, yy, w * nz / tot, 16, fill=LGREY, r=2)
        S.text(310, yy + 12, lab, cls="s"); S.text(470, yy + 12, "0/1" if ok else ("1/1" if m >= u and nz / tot <= 0.2 else "excluded (noise)"), cls="sb", fill=GREEN if ok else GREY)
    # c: SNV co-segregation
    S.panel(600, 34, "c", "Refinement by co-segregation with SNVs")
    xs = [650, 730, 810, 890, 970]
    kinds = ["SNV", "CpG", "SNV", "CpG", "CpG"]
    yt, yb = 110, 170
    for x, k in zip(xs, kinds):
        S.text(x, 86, k, cls="s", anchor="middle")
        if k == "SNV":
            S.node(x, yt, "r", H1, r=10, cls="s"); S.node(x, yb, "a", H2, r=10, cls="s")
        else:
            S.circle(x, yt, 10, fill=INK, stroke=INK); S.circle(x, yb, 10, fill="#fff", stroke=INK)
    S.line(xs[0] + 10, yt, xs[1] - 10, yt, stroke=GREEN, w=4); S.line(xs[0] + 10, yb, xs[1] - 10, yb, stroke=GREEN, w=4)
    S.text((xs[0] + xs[1]) / 2, yt - 18, "strong", cls="sb", anchor="middle", fill=GREEN)
    S.line(xs[1] + 10, yt, xs[2] - 10, yt, stroke=GREEN, w=4); S.line(xs[1] + 10, yb, xs[2] - 10, yb, stroke=GREEN, w=4)
    S.line(xs[2] + 10, yt, xs[3] - 10, yt, stroke=LGREY, w=2); S.line(xs[2] + 10, yb, xs[3] - 10, yb, stroke=LGREY, w=2)
    S.text((xs[2] + xs[3]) / 2, yt - 18, "weak", cls="sb", anchor="middle", fill=GREY)
    S.line(xs[3] + 10, yt, xs[4] - 10, yt, stroke=AMBER, w=3); S.line(xs[3] + 10, yb, xs[4] - 10, yb, stroke=AMBER, w=3)
    S.text((xs[3] + xs[4]) / 2, yt - 18, "CpG–CpG", cls="sb", anchor="middle", fill=AMBER)
    S.text(620, 215, "strong anchor: CpG state co-segregates with an SNV within the next", cls="s")
    S.text(620, 231, "20 variants on > max(6, (d₁+d₂)/4) reads with majority ratio ≥ 0.9", cls="s")
    S.text(620, 255, "weak CpG: no qualifying SNV link; accepted only if it co-segregates", cls="s")
    S.text(620, 271, "with an already accepted CpG (iterative expansion, 2 rounds)", cls="s")
    S.text(620, 295, "adjacent CpG coordinates are merged and represented by the first", cls="s")
    # d: output
    S.panel(600, 340, "d", "Output VCF record")
    S.text(620, 372, 'chr1  10469  .  N  .  .  PASS  RS=P;MR=read3,read7,...;NR=read1,read4,...', cls="code")
    S.text(620, 390, 'GT:MD:UD:DP  0/1:14:12:28', cls="code")
    S.text(620, 416, "RS strand; MR/NR methylated and unmethylated read names (used by phase", cls="s")
    S.text(620, 432, "to attach 5mC alleles to reads); MD/UD/DP depths. Phased output adds PS and 0|1.", cls="s")
    S.save("suppfig9_modcall.svg")

# ----------------------------------------------------------------------------
# S10  Evaluation metrics
# ----------------------------------------------------------------------------
def fig_s10():
    S = SVG(1100, 520, "Phasing evaluation metrics")
    S.panel(20, 34, "a", "Switch errors, flips and Hamming distance within one block")
    xs = [230 + i * 70 for i in range(10)]
    truth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    query = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]
    for row, (lab, hap, y) in enumerate([("truth h₀", truth, 100), ("query h₀", query, 150)]):
        S.text(200, y + 4, lab, cls="sb", anchor="end")
        for x, a in zip(xs, hap):
            S.node(x, y, str(a), H1 if a == 0 else H2, r=11, cls="s")
    sw_t = "".join("0" if truth[i] == truth[i + 1] else "1" for i in range(9))
    sw_q = "".join("0" if query[i] == query[i + 1] else "1" for i in range(9))
    S.text(200, 204, "switch encoding (query)", cls="sb", anchor="end")
    for i in range(9):
        x = (xs[i] + xs[i + 1]) / 2
        c = H2 if sw_q[i] == "1" else GREY
        S.text(x, 204, sw_q[i], cls="tb", anchor="middle", fill=c)
        if sw_q[i] == "1": S.line(x, 165, x, 190, stroke=H2, w=1.5, dash="3,2")
    S.text(60, 240, "switch errors = Hamming(switch(truth), switch(query)) = 4", cls="s", anchor="end") if False else None
    S.text(100, 240, "switch errors = number of positions where the switch encodings differ = 4", cls="t")
    S.text(100, 262, "switch/flip decomposition: two adjacent switches (positions 7–8) form one flip; isolated switches = 2, flips = 1", cls="s")
    S.text(100, 284, "Hamming distance = min over the two orientations of misassigned variants = min(5, 5) = 5 of 10 (50%)", cls="s")
    S.text(100, 306, "(per-block minimum, summed over blocks, divided by variants compared)", cls="s")
    # b: block N50 and phased fraction
    S.panel(20, 350, "b", "Block statistics")
    S.text(40, 384, "Blocks are intersected: only variants heterozygous in both files and phased in both are compared; singleton blocks are ignored.", cls="s")
    S.text(40, 402, "Phased SNV (%) = truth heterozygous SNVs phased by the query / all truth heterozygous SNVs (same for indels, SVs, 5mC).", cls="s")
    S.text(40, 420, "Block N50 = span of the block at which the cumulative span of query blocks, sorted by length, reaches 50% of the total.", cls="s")
    S.text(40, 438, "Switch error rate (%) = switch errors / assessed variant pairs × 100. Cross-tool comparisons use SNVs only (--only-snvs).", cls="s")
    S.text(40, 466, "Implemented in longphase compare (re-implementation of whatshap compare; identical values, parallel over chromosomes).", cls="s")
    S.save("suppfig10_metrics.svg")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for f in (fig_s1, fig_s2, fig_s3, fig_s4, fig_s5, fig_s6, fig_s7, fig_s8, fig_s9, fig_s10):
        f()
