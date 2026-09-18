#!/usr/bin/env python3
"""Generate main Figure 1 (method overview) for the LongPhase 2 manuscript.

Vector redraw of the Codex-generated raster reference. Reuses the SVG
primitive class from figures/supp/make_supp_figs.py so the whole figure set
has one source of truth.

Run:      python3 make_fig1.py
Convert:  rsvg-convert -f pdf -o fig1_overview.pdf fig1_overview.svg
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "supp"))
from make_supp_figs import SVG as _SVG

BLUE, BLUED, CYAN = "#1793DA", "#1560BD", "#35BDEC"
RED, REDE         = "#E8232A", "#EE4B52"
NAVY, INKD        = "#12386E", "#0E2A52"
GREYE, GREYR      = "#9FB3C4", "#C2D0DA"
YEL, YELE         = "#FCF4D2", "#EBD98E"
PURP, ORNG, LGREY = "#9A93DC", "#F5A623", "#D6DEE5"
GRN, PNK, VIO     = "#7EC8A0", "#F2A0B4", "#C9A6E0"

STYLE = """
<style>
 text{font-family:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;fill:%s}
 .pl{font-size:19px;font-weight:700;fill:%s}
 .hd{font-size:12.5px;font-weight:700;fill:%s}
 .lb{font-size:11px}
 .lbb{font-size:11px;font-weight:700}
 .sm{font-size:9.5px}
 .nd{font-size:11.5px;font-weight:700}
 .nds{font-size:9.5px;font-weight:700}
 .it{font-size:11.5px;font-style:italic}
</style>
""" % (NAVY, NAVY, BLUED)


class F(_SVG):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        self.parts[2] = STYLE
        self.add('<defs>'
                 f'<marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUED}"/></marker>'
                 f'<marker id="an" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker>'
                 '</defs>')

    def snp(self, cx, cy, ch, col, r=12.5, dash=False, fill="#fff"):
        d = ' stroke-dasharray="3,2.4"' if dash else ''
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="1.9"{d}/>')
        if ch: self.text(cx, cy + 4, ch, cls="nd", anchor="middle", fill=col)

    def indel(self, cx, cy, ch="", col=BLUE, w=26, h=19, dash=False):
        d = ' stroke-dasharray="3,2.4"' if dash else ''
        self.add(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="2" fill="#fff" stroke="{col}" stroke-width="1.9"{d}/>')
        if ch: self.text(cx, cy + 4, ch, cls="nd", anchor="middle", fill=col)

    def sv(self, cx, cy, col=BLUE, w=30, h=20):
        self.add(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="3.5" fill="#fff" stroke="{col}" stroke-width="1.9"/>')
        self.add(f'<rect x="{cx-w/2+3}" y="{cy-h/2+3}" width="{w-6}" height="{h-6}" rx="2" fill="none" stroke="{col}" stroke-width="1"/>')
        self.text(cx, cy + 3.5, "SV", cls="nds", anchor="middle", fill=col)

    def mc(self, cx, cy, filled=True, r=7):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INKD if filled else "#ffffff"}" stroke="{INKD}" stroke-width="2"/>')

    def xed(self, cx, cy, r=11):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INKD}" stroke-width="1.9"/>')
        k = r * 0.70
        self.add(f'<line x1="{cx-k}" y1="{cy-k}" x2="{cx+k}" y2="{cy+k}" stroke="{INKD}" stroke-width="1.7"/>')
        self.add(f'<line x1="{cx-k}" y1="{cy+k}" x2="{cx+k}" y2="{cy-k}" stroke="{INKD}" stroke-width="1.7"/>')

    def fatarrow(self, x, y1, y2, col=BLUED, sw=11, hw=19, hh=15):
        self.add(f'<path d="M{x-sw/2},{y1} L{x+sw/2},{y1} L{x+sw/2},{y2-hh} '
                 f'L{x+hw/2},{y2-hh} L{x},{y2} L{x-hw/2},{y2-hh} '
                 f'L{x-sw/2},{y2-hh} Z" fill="{col}"/>')

    def band(self, x1, x2, y, col=GREYR, w=7):
        self.add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')

    def arc(self, x1, y1, x2, y2, bow, col, w=1.1):
        self.add(f'<path d="M{x1},{y1} Q{(x1+x2)/2},{(y1+y2)/2-bow} {x2},{y2}" fill="none" stroke="{col}" stroke-width="{w}"/>')


W, H = 1020, 700
S = F(W, H, "Overview of LongPhase 2")
S.line(336, 12, 336, 452, stroke=LGREY, w=1.1)
S.line(14, 458, W - 14, 458, stroke=LGREY, w=1.1)
S.line(770, 468, 770, H - 12, stroke=LGREY, w=1.1)

# ================================ a ========================================
S.text(16, 30, "a", cls="pl")
ly = 26
S.snp(44, ly, "A", BLUE, r=10);  S.text(60, ly + 4, "SNP", cls="lb")
S.indel(112, ly, "", BLUE, w=20, h=16); S.text(126, ly + 4, "Indel", cls="lb")
S.sv(180, ly, BLUE, w=26, h=17); S.text(198, ly + 4, "SV", cls="lb")
S.mc(234, ly, True, r=6);  S.text(244, ly + 4, "5mC", cls="lb")
S.mc(283, ly, False, r=6); S.text(293, ly + 1, "5mC", cls="lb")
S.text(293, ly + 12, "(unmod.)", cls="sm")

cols = [126, 161, 196, 231, 266, 299]
S.text(14, 76, "Reference", cls="lbb")
S.add(f'<line x1="106" y1="72" x2="314" y2="72" stroke="{BLUED}" stroke-width="5.5"/>')
for cx in cols:
    S.add(f'<line x1="{cx}" y1="64" x2="{cx}" y2="80" stroke="{BLUED}" stroke-width="2.6"/>')
    S.add(f'<line x1="{cx}" y1="84" x2="{cx}" y2="300" stroke="{LGREY}" stroke-width="0.9" stroke-dasharray="3,3"/>')
S.add(f'<line x1="{cols[4]}" y1="84" x2="{cols[4]}" y2="300" stroke="{INKD}" stroke-width="1.5" stroke-dasharray="4,3"/>')

READS = [("A", 1, 1, "T", 1, 1), ("G", 0, 0, "C", 0, 0), ("A", 1, 0, "T", 1, 1),
         ("G", 0, 0, "C", 0, 0), ("A", 1, 1, "T", 1, 1), ("G", 0, 0, "C", 0, 0)]
for i, (s1, hi, hs, s2, meth, hi2) in enumerate(READS):
    y = 106 + i * 33
    col = BLUE if s1 == "A" else RED
    S.text(14, y + 4, f"Read {i+1}", cls="lbb")
    S.band(112, 314, y)
    S.snp(cols[0], y, s1, col)
    if hi: S.indel(cols[1], y, "", col)
    if hs: S.sv(cols[2], y, col)
    S.snp(cols[3], y, s2, col)
    S.mc(cols[4], y, bool(meth), r=6.5)
    if hi2: S.indel(cols[5], y, "", col)

# ================================ b ========================================
S.text(344, 30, "b", cls="pl")
gcols = [438 + i * 66 for i in range(8)]

def graph(y1, y2, rw=False):
    top = ["A", "T", "A", "T", "G", "A", None, "C"]
    bot = ["G", "C", "CA", "C", "A", "T", None, "T"]
    S.add(f'<line x1="{gcols[0]}" y1="{y1}" x2="{gcols[7]}" y2="{y1}" stroke="{CYAN}" stroke-width="4.5" opacity="0.9"/>')
    S.add(f'<line x1="{gcols[0]}" y1="{y2}" x2="{gcols[7]}" y2="{y2}" stroke="{REDE}" stroke-width="4.5" opacity="0.9"/>')
    for i in range(7):
        if rw and i in (3, 4):
            continue
        S.add(f'<line x1="{gcols[i]+15}" y1="{y1+9}" x2="{gcols[i+1]-15}" y2="{y2-9}" stroke="{GREYE}" stroke-width="0.85"/>')
        S.add(f'<line x1="{gcols[i]+15}" y1="{y2-9}" x2="{gcols[i+1]-15}" y2="{y1+9}" stroke="{GREYE}" stroke-width="0.85"/>')
    S.arc(gcols[1], y2 + 14, gcols[7], y2 + 14, -30, REDE, w=2.2)
    for i in range(8):
        cx = gcols[i]
        if i == 6:
            S.add(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{INKD}" stroke-width="2.4"/>')
            S.mc(cx, y1, True); S.mc(cx, y2, False)
            continue
        if rw and i == 4:
            S.xed(cx, y1); S.xed(cx, y2); continue
        S.snp(cx, y1, top[i], BLUE)
        if bot[i] == "CA":
            S.indel(cx, y2, "CA", RED, w=34, h=21)
        else:
            S.snp(cx, y2, bot[i], RED, dash=(rw and i == 1))

# CNV bracket
S.rect(gcols[3] - 26, 62, gcols[5] - gcols[3] + 52, 100, fill=YEL, stroke=YELE, sw=0.9, r=3)
S.add(f'<path d="M{gcols[3]-26},54 L{gcols[3]-26},44 L{gcols[5]+26},44 L{gcols[5]+26},54" fill="none" stroke="{BLUED}" stroke-width="1.6"/>')
S.text((gcols[3] + gcols[5]) / 2, 38, "CNV region", cls="hd", anchor="middle")

S.text(378, 96, "Original", cls="hd", anchor="middle"); S.text(378, 112, "graph", cls="hd", anchor="middle")
graph(86, 144)

S.fatarrow(378, 126, 162)
S.text(378, 194, "Evidence", cls="hd", anchor="middle"); S.text(378, 210, "calibration", cls="hd", anchor="middle")

# --- uncertain base call ---
S.text(506, 200, "Uncertain base call", cls="hd", anchor="middle")
S.add(f'<rect x="494" y="214" width="24" height="52" fill="{YEL}"/>')
S.text(424, 232, "Read", cls="lb")
S.band(456, 560, 232, w=6)
S.snp(472, 232, "A", BLUE, r=11)
S.snp(506, 232, "C", BLUE, r=11, dash=True)
S.snp(540, 232, "T", BLUE, r=11)
S.text(424, 268, "Phred quality", cls="lb")
for bx, bh, bc in [(484, 32, "#8CA3B5"), (500, 13, ORNG), (524, 36, "#8CA3B5")]:
    S.add(f'<rect x="{bx}" y="{306-bh}" width="15" height="{bh}" fill="{bc}"/>')
S.add(f'<line x1="472" y1="306" x2="556" y2="306" stroke="{NAVY}" stroke-width="1.4"/>')

# --- sequence-context reliability ---
S.text(706, 200, "Sequence-context reliability", cls="hd", anchor="middle")
def ladder(x0, y, chars, gap=15):
    for k, ch in enumerate(chars):
        xx = x0 + k * gap
        S.text(xx, y - 3, ch, cls="lb", anchor="middle")
        S.text(xx, y + 17, ch, cls="lb", anchor="middle")
        S.add(f'<line x1="{xx}" y1="{y+1}" x2="{xx}" y2="{y+7}" stroke="{NAVY}" stroke-width="0.9"/>')
S.text(636, 222, "Non-repetitive", cls="lb", anchor="middle")
S.text(636, 236, "context", cls="lb", anchor="middle")
ladder(676, 222, ["G", "T", "C"]); S.indel(742, 228, "A", BLUE, w=30, h=19); ladder(776, 222, ["G", "C", "T"])
ladder(676, 250, ["G", "T", "C"]); S.indel(742, 256, "CA", RED, w=32, h=19); ladder(776, 250, ["G", "C", "T"])
S.rect(664, 272, 168, 44, fill=YEL, stroke="none", r=2)
S.text(636, 288, "Tandem-repeat", cls="lb", anchor="middle")
S.text(636, 302, "context", cls="lb", anchor="middle")
for k in range(2):
    for xx in (680 + k * 24, 772 + k * 24):
        S.text(xx, 285, "CA", cls="lb", anchor="middle")
        S.text(xx, 309, "CA", cls="lb", anchor="middle")
        S.add(f'<line x1="{xx}" y1="289" x2="{xx}" y2="299" stroke="{NAVY}" stroke-width="0.9"/>')
S.indel(742, 296, "CA", RED, w=32, h=19, dash=True)

# --- miscalled SNPs in CNV ---
S.text(918, 200, "Miscalled SNPs in CNV", cls="hd", anchor="middle")
S.rect(862, 212, 112, 100, fill=YEL, stroke=YELE, sw=0.9, r=3)
for k, (a, b) in enumerate([("T", "A"), ("T", "T"), ("T", "A")]):
    y = 234 + k * 30
    S.text(856, y + 4, f"Read {k+1}", cls="lb", anchor="end")
    S.band(870, 992, y, w=6)
    S.snp(882, y, a, BLUE, r=11)
    S.xed(918, y, r=9.5)
    S.snp(956, y, b, BLUE, r=11)

S.fatarrow(378, 236, 272)
S.text(378, 362, "Reweighted", cls="hd", anchor="middle"); S.text(378, 378, "graph", cls="hd", anchor="middle")
graph(352, 410, rw=True)

# --- edge legend ---
S.add(f'<line x1="440" y1="438" x2="492" y2="438" stroke="{CYAN}" stroke-width="4.5"/>')
S.text(500, 442, "High-confidence edge", cls="lb")
S.add(f'<line x1="648" y1="438" x2="700" y2="438" stroke="{GREYE}" stroke-width="1"/>')
S.text(708, 442, "Low-confidence edge", cls="lb")
S.xed(866, 438, r=9)
S.text(880, 442, "Filtered variants", cls="lb")

# ================================ c ========================================
S.text(16, 486, "c", cls="pl")
S.text(34, 486, "Node features", cls="hd")
S.text(34, 502, "Phase evidence", cls="sm"); S.text(118, 502, "Variant type", cls="sm")
S.text(196, 502, "Genomic context", cls="sm"); S.text(288, 502, "...", cls="sm")
ncols = [46 + i * 42 for i in range(5)]
S.rect(ncols[2] - 20, 512, 40, 72, fill=YEL, stroke="none", r=3)
S.add(f'<line x1="{ncols[0]}" y1="530" x2="{ncols[4]}" y2="530" stroke="{CYAN}" stroke-width="4"/>')
S.add(f'<line x1="{ncols[0]}" y1="566" x2="{ncols[4]}" y2="566" stroke="{REDE}" stroke-width="4"/>')
for i, (t, b) in enumerate(zip("ATCGT", "GCTAC")):
    S.snp(ncols[i], 530, t, BLUE, r=11)
    S.snp(ncols[i], 566, b, RED, r=11)
S.text(34, 600, "Edge features", cls="hd")
S.text(34, 616, "Link strength", cls="sm"); S.text(106, 616, "Genomic distance", cls="sm")
S.text(200, 616, "Phase set relation", cls="sm"); S.text(298, 616, "...", cls="sm")

S.snp(276, 548, "", NAVY, r=8)
S.add(f'<path d="M286,544 L314,516" stroke="{BLUED}" stroke-width="1.6" marker-end="url(#ab)"/>')
S.add(f'<path d="M286,554 L314,586" stroke="{BLUED}" stroke-width="1.6" marker-end="url(#ab)"/>')

# local attention
S.text(392, 488, "Local attention", cls="hd", anchor="middle")
S.text(392, 503, "GATv2", cls="hd", anchor="middle")
S.add(f'<ellipse cx="392" cy="546" rx="62" ry="34" fill="none" stroke="{BLUED}" stroke-width="1.1" stroke-dasharray="4,3"/>')
for (dx, dy, c) in [(-34, -14, GRN), (34, -16, "#7FB3E8"), (-40, 12, PNK), (-2, 26, VIO), (34, 20, "#F08CA0")]:
    S.snp(392 + dx, 546 + dy, "", c, r=7.5, fill=c)
    S.add(f'<path d="M{392+dx*0.55},{546+dy*0.55} L{392+dx*0.30},{546+dy*0.30}" stroke="{NAVY}" stroke-width="1" marker-end="url(#an)"/>')
S.snp(392, 546, "", ORNG, r=8.5, fill=ORNG)

# transformer
S.text(392, 600, "Window-wide attention", cls="hd", anchor="middle")
S.text(392, 615, "Transformer", cls="hd", anchor="middle")
for k in range(6):
    xx = 340 + k * 21
    S.rect(xx, 624, 15, 15, fill=(ORNG if k == 1 else "#B8C6D2"), r=2)
for k in range(5):
    S.arc(348 + k * 21, 642, 348 + (k + 1) * 21, 642, -9, BLUED, w=0.9)
S.text(392, 664, "Genomic window", cls="lb", anchor="middle")

S.text(476, 534, "h", cls="it"); S.text(484, 537, "local", cls="sm")
S.text(476, 620, "h", cls="it"); S.text(484, 623, "global", cls="sm")
S.add(f'<path d="M456,540 L520,556" stroke="{NAVY}" stroke-width="1.2" marker-end="url(#an)"/>')
S.add(f'<path d="M456,626 L520,580" stroke="{NAVY}" stroke-width="1.2" marker-end="url(#an)"/>')
S.text(536, 528, "Additive fusion", cls="hd", anchor="middle")
S.add(f'<circle cx="536" cy="568" r="13" fill="#fff" stroke="{BLUED}" stroke-width="1.8"/>')
S.text(536, 574, "+", cls="nd", anchor="middle", fill=BLUED)
S.add(f'<path d="M288,552 L318,552 L318,686 L524,686 L524,582" stroke="{NAVY}" stroke-width="1.1" fill="none" marker-end="url(#an)"/>')

S.text(586, 548, "FFN", cls="hd", anchor="middle")
for k in range(3):
    S.rect(566 + k * 14, 556, 10, 34, fill=PURP, r=2)
S.add(f'<path d="M550,568 L562,568" stroke="{NAVY}" stroke-width="1.2" marker-end="url(#an)"/>')
S.text(586, 606, "Residual + norm", cls="lb", anchor="middle")
S.add(f'<path d="M612,568 L636,568" stroke="{NAVY}" stroke-width="1.2" marker-end="url(#an)"/>')

S.text(684, 492, "Phase-confidence refinement", cls="hd", anchor="middle")
rcols = [630 + i * 27 for i in range(5)]
S.arc(rcols[0], 520, rcols[4], 520, 16, CYAN, w=3.5)
S.arc(rcols[0], 580, rcols[4], 580, -16, REDE, w=3.5)
for i, (t, b) in enumerate(zip("ATCGT", "GCTAC")):
    grey = (i == 2)
    S.snp(rcols[i], 532, t, "#9AA9B8" if grey else BLUE, r=11)
    S.snp(rcols[i], 568, b, "#9AA9B8" if grey else RED, r=11)
S.text(rcols[2] + 6, 602, "Unphased SNP", cls="lb", anchor="middle")

# ================================ d ========================================
S.text(786, 486, "d", cls="pl")
hx = [852 + i * 29 for i in range(6)]
S.text(784, 512, "Haplotype 1", cls="sm", fill=BLUE)
S.text(784, 544, "Haplotype 2", cls="sm", fill=RED)
S.add(f'<line x1="{hx[0]}" y1="508" x2="{hx[5]}" y2="508" stroke="{CYAN}" stroke-width="4"/>')
S.add(f'<line x1="{hx[0]}" y1="540" x2="{hx[5]}" y2="540" stroke="{REDE}" stroke-width="4"/>')
S.snp(hx[0], 508, "A", BLUE, r=10.5); S.snp(hx[1], 508, "T", BLUE, r=10.5)
S.sv(hx[2], 508, BLUE, w=26, h=18); S.mc(hx[3], 508, True, r=6.5)
S.snp(hx[4], 508, "A", BLUE, r=10.5); S.snp(hx[5], 508, "C", BLUE, r=10.5)
S.snp(hx[0], 540, "G", RED, r=10.5); S.snp(hx[1], 540, "C", RED, r=10.5)
S.mc(hx[3], 540, False, r=6.5)
S.indel(hx[4], 540, "CA", RED, w=28, h=19); S.snp(hx[5], 540, "T", RED, r=10.5)

S.text(896, 570, "Haplotagging reads", cls="hd", anchor="middle")
for k, hap1 in enumerate([True, True, False]):
    y = 592 + k * 34
    S.text(784, y + 4, f"Read {k+1}", cls="sm", fill=BLUED)
    S.band(hx[0] - 14, hx[5] + 14, y, col=(CYAN if hap1 else REDE), w=4)
    if hap1:
        S.snp(hx[0], y, "A", BLUE, r=10.5); S.snp(hx[1], y, "T", BLUE, r=10.5)
        S.sv(hx[2], y, BLUE, w=26, h=18); S.mc(hx[3], y, True, r=6.5)
        S.snp(hx[4], y, "A", BLUE, r=10.5); S.snp(hx[5], y, "C", BLUE, r=10.5)
    else:
        S.snp(hx[0], y, "G", RED, r=10.5); S.snp(hx[1], y, "C", RED, r=10.5)
        S.mc(hx[3], y, False, r=6.5)
        S.indel(hx[4], y, "CA", RED, w=28, h=19); S.snp(hx[5], y, "T", RED, r=10.5)

S.save("fig1_overview.svg")
