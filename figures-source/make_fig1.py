#!/usr/bin/env python3
"""Generate Figure 1 (figures/fig1_overview.svg; convert to PDF with rsvg-convert).

Single vector source for all four panels, drawn in the house style of the
original 2026-09-18 master (Helvetica Neue, navy text, blue/red haplotypes).
Layout follows the 2026-09-18 redesign raster:

  a  legend on one row; reference with six variant columns; six reads that fill
     the panel, carrying SNV / indel / SV alleles and a CpG (methylated = filled
     lollipop, unmethylated = open) on the read line.
  b  original graph (all edges high-confidence, long-range read links drawn as
     arcs) -> evidence calibration (uncertain base call with Phred bars,
     sequence-context reliability, miscalled SNPs in a CNV) -> reweighted graph
     (down-weighted C and CA, filtered CNV variants, low-confidence edges thin).
  c  node/edge features of a window -> local graph attention (message-passing
     star; GATv2) and window-wide self-attention (token row; Transformer) ->
     feature fusion -> feed-forward layers (unlabelled purple bars) ->
     phase-confidence refinement (trigger SNP unphased). Residual connections
     and normalization are deliberately omitted (see Supplementary Fig. 7).
  d  two haplotypes carrying SNVs, an SV, an indel and a CpG, and three
     haplotagged reads.

Run:   python3 figures-source/make_fig1.py        (from the repository root)
       rsvg-convert -f pdf -o figures/fig1_overview.pdf figures/fig1_overview.svg
"""
import os

NAVY, BLUE, LBLUE, FBLUE = "#103A82", "#1687C9", "#6CC8EE", "#C5E6F6"
RED, LRED, FRED = "#DC2B23", "#F0766C", "#F9CFC9"
GREY, UNPH, UNPHF = "#9BA9B8", "#6F8090", "#EEF1F4"
HILITE, INK, ARROW = "#FCF1C7", "#16233D", "#8FA3B6"
PURPLE, PURPLED = "#9B8CD8", "#6F5EB8"
READ, READ_B, READ_R = "#C6D0DA", "#D9EEF9", "#FBE1DE"
ORANGE, CYAN = "#F2A33C", "#29B6E8"

HEADER = """<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="1020" viewBox="0 0 1680 1020">
<title>LongPhase 2 overview: evidence-calibrated phasing graph and graph-transformer phase-error detection</title>
<defs>
<style>
 text{font-family:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;
      letter-spacing:.005em}
 .pl{font-size:30px;font-weight:700}
 .h1{font-size:21.5px;font-weight:600}
 .h2{font-size:19.5px;font-weight:700}
 .lb{font-size:17.5px;font-weight:400}
 .lbb{font-size:17.5px;font-weight:600}
 .sm{font-size:15px;font-weight:400}
 .num{font-size:17px;font-weight:600}
 .nt{font-weight:700}
</style>
<marker id="aNavy" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M0 0.8 L9.6 5 L0 9.2 z" fill="#103A82"/></marker>
<marker id="aGrey" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
  <path d="M0 0.8 L9.6 5 L0 9.2 z" fill="#7C8DA0"/></marker>
<marker id="aBlue" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M0 0.8 L9.6 5 L0 9.2 z" fill="#1687C9"/></marker>
</defs>
<rect width="1680" height="1020" fill="#ffffff"/>"""

out = [HEADER]
def add(s): out.append(s)

# ---------------------------------------------------------------- primitives
def text(x, y, s, cls="lb", fill=NAVY, anchor="start", extra=""):
    add(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>')

def line(x1, y1, x2, y2, stroke, w, cap="round", op=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}" stroke-opacity="{op}"{d}/>')

def path(d, stroke=NAVY, w=2, dash=None, arrow=None, op=1.0, fill="none"):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    a = f' marker-end="url(#{arrow})"' if arrow else ""
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="{op}"{dd}{a}/>')

def rect(x, y, w, h, fill, rx=3, stroke="none", sw=1, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def snp(cx, cy, letter, color, r=21, fs=17, fill="#ffffff", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2.6"{d}/>')
    if letter:
        add(f'<text x="{cx:.1f}" y="{cy + fs * 0.35:.1f}" class="nt" fill="{color}" text-anchor="middle" font-size="{fs}">{letter}</text>')

def box(cx, cy, label, color, w=52, h=30, fs=15, sw=2.6, dash=None):
    rect(cx - w / 2, cy - h / 2, w, h, "#ffffff", rx=4, stroke=color, sw=sw, dash=dash)
    if label:
        add(f'<text x="{cx:.1f}" y="{cy + fs * 0.35:.1f}" class="nt" fill="{color}" text-anchor="middle" font-size="{fs}">{label}</text>')

def filtered(cx, cy, r=21):
    k = r * 0.6
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>')
    add(f'<path d="M{cx - k:.1f} {cy - k:.1f} L{cx + k:.1f} {cy + k:.1f} M{cx + k:.1f} {cy - k:.1f} L{cx - k:.1f} {cy + k:.1f}" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')

def lollipop(cx, cy, filled, r=8.5, stem=30, sw=3.2):
    """CpG marker: head centred on the line at (cx, cy), stem hanging below."""
    line(cx, cy + r, cx, cy + stem, INK, sw)
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{INK if filled else "#ffffff"}" stroke="{INK}" stroke-width="2.6"/>')

def hedge(x1, x2, y, color, w):
    add(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="butt"/>')

def cross(x1, x2, yt, yb, w=1.9, op=0.85):
    line(x1, yt, x2, yb, GREY, w, op=op)
    line(x1, yb, x2, yt, GREY, w, op=op)

# separators
line(498, 22, 498, 660, "#C9D2DC", 1.6, cap="butt")
line(24, 676, 1656, 676, "#C9D2DC", 1.6, cap="butt")
line(1238, 694, 1238, 1000, "#C9D2DC", 1.6, cap="butt")

# ============================================================================
# Panel a
# ============================================================================
text(24, 44, "a", cls="pl")
LY = 84
snp(48, LY, "A", BLUE, r=15, fs=15);                     text(70, LY + 6, "SNP")
box(126, LY, "", BLUE, w=27, h=21, sw=2.2);              text(148, LY + 6, "Indel")
box(228, LY, "SV", BLUE, w=44, h=25, fs=14.5, sw=2.2);   text(258, LY + 6, "SV")
lollipop(302, LY - 4, True, r=7.5, stem=22);             text(318, LY + 6, "5mC")
lollipop(374, LY - 4, False, r=7.5, stem=22);            text(390, LY + 6, "5mC")
text(390, LY + 24, "(unmodified)", cls="sm")

RX0, RX1 = 150, 472
COLX = [170, 226, 282, 338, 394, 450]
text(138, 158, "Reference", cls="h1", anchor="end")
rect(RX0, 145, RX1 - RX0, 13, NAVY)
for x in COLX:
    rect(x - 2.6, 133, 5.2, 37, NAVY, rx=2)
READS_Y = [218 + 80 * i for i in range(6)]
for x in COLX:
    line(x, 176, x, READS_Y[-1] + 22, "#B9C4D0", 1.5, dash="4 6")
for i, y in enumerate(READS_Y):
    hap1 = i % 2 == 0
    text(138, y + 6, f"Read {i + 1}", anchor="end")
    rect(RX0, y - 6.5, RX1 - RX0, 13, READ, rx=6.5)
    if hap1:
        snp(COLX[0], y, "A", BLUE, r=17, fs=17)
        box(COLX[1], y, "", BLUE, w=27, h=22, sw=2.4)
        if i != 2:                                   # read 3 does not span the SV
            box(COLX[2], y, "SV", BLUE, w=44, h=26, fs=15, sw=2.4)
        snp(COLX[3], y, "T", BLUE, r=17, fs=17)
        lollipop(COLX[4], y, True)
        box(COLX[5], y, "", BLUE, w=27, h=22, sw=2.4)
    else:
        snp(COLX[0], y, "G", RED, r=17, fs=17)
        snp(COLX[3], y, "C", RED, r=17, fs=17)
        lollipop(COLX[4], y, False)

# ============================================================================
# Panel b
# ============================================================================
text(516, 44, "b", cls="pl")
GXS = [730 + 125.7 * i for i in range(8)]          # 8 variant columns
TOP = ["A", "T", "A", "T", "G", "A", None, "C"]     # column 7 is the CpG
BOT = ["G", "C", "CA", "C", "A", "T", None, "T"]

def graph(yt, yb, reweighted):
    r, fs = 26, 20.8
    for i in range(7):
        x1, x2 = GXS[i], GXS[i + 1]
        cross(x1, x2, yt, yb)
        if not reweighted:
            hedge(x1, x2, yt, LBLUE, 9.5); hedge(x1, x2, yb, LRED, 9.5)
        elif i in (3, 4):                           # through the filtered variant: faded
            hedge(x1, x2, yt, FBLUE, 6); hedge(x1, x2, yb, FRED, 6)
        elif i < 3:                                 # down-weighted C / CA: low confidence
            hedge(x1, x2, yt, LBLUE, 9.5); line(x1, yb, x2, yb, GREY, 2.2)
        else:
            hedge(x1, x2, yt, LBLUE, 9.5); hedge(x1, x2, yb, LRED, 9.5)
    for i, x in enumerate(GXS):
        if i == 6:
            line(x, yt, x, yb + 24, INK, 3.2)
            add(f'<circle cx="{x:.1f}" cy="{yt}" r="10" fill="{INK}" stroke="{INK}" stroke-width="2.6"/>')
            add(f'<circle cx="{x:.1f}" cy="{yb}" r="10" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>')
        elif reweighted and i == 4:
            filtered(x, yt); filtered(x, yb)
        else:
            snp(x, yt, TOP[i], BLUE, r=r, fs=fs)
            if BOT[i] == "CA":
                box(x, yb, "CA", RED, w=58, h=42, fs=21)
            else:
                snp(x, yb, BOT[i], RED, r=r, fs=fs, dash=("6 4.5" if reweighted and i == 1 else None))

# --- original graph -----------------------------------------------------------
YT, YB = 104, 166
rect(1061.1, 72, 343.4, 128, HILITE, rx=7)
path("M1077.1 56 L1077.1 44 L1388.5 44 L1388.5 56", stroke=NAVY, w=2.2)
text(1232.8, 30, "CNV region", cls="h1", anchor="middle")
# long-range read links that calibration will expose as unreliable
path(f"M{GXS[1]:.1f} {YB + 16} Q{GXS[4]:.1f} 272 {GXS[7]:.1f} {YB + 16}", stroke=LRED, w=2.8, op=0.9)
path(f"M{GXS[2]:.1f} {YB + 18} Q{GXS[4]:.1f} 250 {GXS[6]:.1f} {YB + 18}", stroke=GREY, w=2.2, op=0.6)
graph(YT, YB, reweighted=False)

def stage(y1, y2, s1, s2):
    text(512, y1, s1, cls="h1", extra=' font-size="24"'); text(512, y2, s2, cls="h1", extra=' font-size="24"')

def block_arrow(x, y1, y2, hw=17, hh=20, sw=7):
    add(f'<path d="M{x - sw} {y1} L{x + sw} {y1} L{x + sw} {y2 - hh} L{x + hw} {y2 - hh} L{x} {y2} L{x - hw} {y2 - hh} L{x - sw} {y2 - hh} Z" fill="{ARROW}" stroke="none"/>')

stage(138, 168, "Original", "graph")
block_arrow(548, 190, 262)
stage(330, 360, "Evidence", "calibration")
block_arrow(548, 408, 482)
stage(530, 560, "Reweighted", "graph")

# --- inset 1: uncertain base call -------------------------------------------
BX = -30                                                  # inset offset (raster places it left of the C node)
text(828 + BX, 254, "Uncertain base call", cls="h2", anchor="middle")
text(722 + BX, 324, "Read", anchor="end")
line(748 + BX, 318, 912 + BX, 318, FBLUE, 9, cap="butt")
rect(806 + BX, 342, 46, 102, HILITE, rx=4)
snp(766 + BX, 318, "A", BLUE, r=20, fs=16)
snp(830 + BX, 318, "C", BLUE, r=20, fs=16, dash="6 4.5")
snp(894 + BX, 318, "T", BLUE, r=20, fs=16)
for x1, y1, x2, y2 in ((816, 292, 808, 280), (830, 290, 830, 276), (844, 292, 852, 280)):
    line(x1 + BX, y1, x2 + BX, y2, CYAN, 2.6)            # rays: an uncertain call
text(732 + BX, 378, "Phred quality")
rect(749 + BX, 386, 34, 58, UNPH, rx=1.5); rect(813 + BX, 424, 34, 20, ORANGE, rx=1.5); rect(877 + BX, 394, 34, 50, UNPH, rx=1.5)
line(740 + BX, 444, 920 + BX, 444, NAVY, 2, cap="butt")
path(f"M{830 + BX} 456 L{830 + BX} 486", stroke=ARROW, w=6, arrow="aGrey")

# --- inset 2: sequence-context reliability ----------------------------------
text(1200, 254, "Sequence-context reliability", cls="h2", anchor="middle")
text(1058, 320, "Non-repetitive", anchor="end"); text(1058, 342, "context", anchor="end")
for x, ch in zip((1091, 1118, 1145), "GTC"):
    text(x, 306, ch, cls="sm", anchor="middle"); line(x, 314, x, 326, UNPH, 1.6); text(x, 346, ch, cls="sm", anchor="middle")
for x, ch in zip((1279, 1306, 1333), "GCT"):
    text(x, 306, ch, cls="sm", anchor="middle"); line(x, 314, x, 326, UNPH, 1.6); text(x, 346, ch, cls="sm", anchor="middle")
box(1212, 303, "A", BLUE, w=46, h=34, fs=19); box(1212, 349, "CA", RED, w=56, h=34, fs=19)
text(1058, 412, "Tandem-repeat", anchor="end"); text(1058, 434, "context", anchor="end")
for x0 in (1069.2, 1265.2):
    rect(x0, 382, 89.6, 64, HILITE, rx=5)
for x in (1094, 1134, 1290, 1330):
    text(x, 398, "CA", cls="sm", anchor="middle"); line(x, 406, x, 418, UNPH, 1.6); text(x, 438, "CA", cls="sm", anchor="middle")
box(1212, 395, "A", BLUE, w=46, h=34, fs=19); box(1212, 441, "CA", RED, w=56, h=34, fs=19, dash="6 4.5")

# --- inset 3: miscalled SNPs in a CNV ---------------------------------------
text(1548, 254, "Miscalled SNPs in CNV", cls="h2", anchor="middle")
rect(1460, 280, 176, 146, HILITE, rx=6)
for k, (y, right) in enumerate(((306, "A"), (354, "T"), (402, "A"))):
    text(1448, y + 6, f"Read {k + 1}", anchor="end")
    line(1486, y, 1610, y, GREY, 2)
    snp(1486, y, "T", BLUE, r=19, fs=15.5); filtered(1548, y, r=18); snp(1610, y, right, BLUE, r=19, fs=15.5)
path("M1548 438 L1548 482", stroke=ARROW, w=6, arrow="aGrey")

# --- pointers from each inset to the evidence it calibrates ------------------
path("M772 234 C776 214 812 212 844 196", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")    # -> C (uncertain call)
path("M1056 236 C1044 220 1018 208 996 194", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")  # -> CA (tandem repeat)
path("M1502 234 C1482 224 1448 218 1416 214", stroke=NAVY, w=2, dash="7 6", arrow="aNavy") # -> spurious CNV link

# --- reweighted graph ---------------------------------------------------------
YT2, YB2 = 540, 602
path(f"M{GXS[1]:.1f} {YB2 + 18} Q{GXS[4]:.1f} 668 {GXS[7]:.1f} {YB2 + 18}", stroke=LRED, w=2.8, op=0.9)
graph(YT2, YB2, reweighted=True)

# --- legend -------------------------------------------------------------------
LGY = 660
hedge(700, 748, LGY, LBLUE, 9.5);            text(760, LGY + 6, "High-confidence edge")
line(1076, LGY, 1124, LGY, GREY, 2.2);       text(1136, LGY + 6, "Low-confidence edge")
filtered(1420, LGY, r=15);                   text(1444, LGY + 6, "Filtered variants")

# ============================================================================
# Panel c
# ============================================================================
def window_graph(xs, yt, yb, top, bot, r, fs, centre=None, w_h=7, w_x=1.8, arcs=False):
    n = len(xs)
    for i in range(n - 1):
        x1, x2 = xs[i], xs[i + 1]
        skip = arcs and centre is not None and centre in (i, i + 1)
        cross(x1, x2, yt, yb, w=w_x if not skip else w_x * 0.9, op=0.85 if not skip else 0.6)
        if not skip:
            hedge(x1, x2, yt, LBLUE, w_h); hedge(x1, x2, yb, LRED, w_h)
    if arcs and centre is not None:
        xl, xr = xs[centre - 1], xs[centre + 1]
        d = xr - xl
        path(f"M{xl:.1f} {yt - 4} Q{(xl + xr) / 2:.1f} {yt - 0.9 * d:.0f} {xr:.1f} {yt - 4}", stroke=LBLUE, w=w_h)
        path(f"M{xl:.1f} {yb + 4} Q{(xl + xr) / 2:.1f} {yb + 0.9 * d:.0f} {xr:.1f} {yb + 4}", stroke=LRED, w=w_h)
    for i, x in enumerate(xs):
        if centre is not None and i == centre and arcs:
            snp(x, yt, top[i], UNPH, r=r, fs=fs, fill=UNPHF); snp(x, yb, bot[i], UNPH, r=r, fs=fs, fill=UNPHF)
        else:
            snp(x, yt, top[i], BLUE, r=r, fs=fs); snp(x, yb, bot[i], RED, r=r, fs=fs)

text(24, 722, "c", cls="pl")
text(64, 722, "Node features", cls="h2")
for s, x in (("Phase evidence", 64), ("Variant type", 183), ("Genomic context", 287)):
    text(x, 748, s, cls="sm")
text(410, 746, "···", cls="sm")

XS = [84, 142, 200, 258, 316]
YTc, YBc, CTR = 852, 910, 2
rect(XS[CTR] - 29, YTc - 33, 58, YBc - YTc + 66, HILITE, rx=8)
window_graph(XS, YTc, YBc, "ATCGT", "GCTAC", r=21, fs=17, centre=CTR)
path(f"M{XS[CTR] + 22} 754 C{XS[CTR] + 18} 780 {XS[CTR] + 6} 800 {XS[CTR] + 2} {YTc - 26}", stroke=NAVY, w=1.6, arrow="aNavy")

text(64, 966, "Edge features", cls="h2")
for s, x in (("Link strength", 64), ("Genomic distance", 168), ("Phase-set relation", 302)):
    text(x, 992, s, cls="sm")
text(430, 990, "···", cls="sm")
path(f"M148 950 C158 940 164 932 170 {YBc + 8}", stroke=NAVY, w=1.6, arrow="aNavy")

IN_X, IN_Y = 456, 881
path(f"M{XS[-1] + 26} {IN_Y} L{IN_X - 22} {IN_Y}", stroke=BLUE, w=2.4, arrow="aBlue")
add(f'<circle cx="{IN_X}" cy="{IN_Y}" r="13" fill="#ffffff" stroke="{NAVY}" stroke-width="2.4"/>')
path(f"M{IN_X + 10} {IN_Y - 9} C{IN_X + 28} {IN_Y - 30} {IN_X + 32} {IN_Y - 60} {IN_X + 42} {IN_Y - 72}", stroke=BLUE, w=2.4, arrow="aBlue")
path(f"M{IN_X + 10} {IN_Y + 9} C{IN_X + 28} {IN_Y + 26} {IN_X + 34} {IN_Y + 44} {IN_X + 52} {IN_Y + 52}", stroke=BLUE, w=2.4, arrow="aBlue")

GX, GY = 604, 812
text(GX, 746, "Local graph attention", cls="h2", anchor="middle")
add(f'<ellipse cx="{GX}" cy="{GY}" rx="90" ry="46" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="6 5"/>')
neigh = [(GX - 58, GY - 24, "#8FD18A"), (GX + 52, GY - 26, LBLUE), (GX - 52, GY + 22, "#F49AC1"),
         (GX + 58, GY + 20, LRED), (GX + 10, GY + 34, "#B9A5E6")]
for nx, ny, col in neigh:
    dx, dy = GX - nx, GY - ny
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    path(f"M{nx + ux * 10:.1f} {ny + uy * 10:.1f} L{GX - ux * 14:.1f} {GY - uy * 14:.1f}", stroke="#7C8DA0", w=1.8, arrow="aGrey")
for nx, ny, col in neigh:
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="8.5" fill="{col}" stroke="{col}" stroke-width="1"/>')
add(f'<circle cx="{GX}" cy="{GY}" r="11.5" fill="#F6C24E" stroke="#C98A2E" stroke-width="1.6"/>')

TOK = [GX - 75 + 30 * i for i in range(6)]
TY = 940
rect(TOK[0] - 22, TY - 22, TOK[-1] - TOK[0] + 44, 42, "#EAF4FB", rx=8)
for i, tx in enumerate(TOK):
    for j, tx2 in enumerate(TOK):
        if j <= i or not (i == 3 or j == 3 or abs(i - j) == 1):
            continue
        d = abs(tx2 - tx)
        path(f"M{tx} {TY - 9} Q{(tx + tx2) / 2:.1f} {TY - 12 - 0.42 * d:.0f} {tx2} {TY - 9}", stroke=BLUE, w=1.1, op=0.75)
for i, tx in enumerate(TOK):
    col, sc = ("#F5A623", "#C97A0E") if i == 3 else ("#9BA9B8", "#6F8090")
    rect(tx - 8, TY - 8, 16, 16, col, rx=2.5, stroke=sc, sw=1.2)
path(f"M{TOK[0] - 14} {TY + 16} L{TOK[0] - 14} {TY + 24} L{TOK[-1] + 14} {TY + 24} L{TOK[-1] + 14} {TY + 16}", stroke=NAVY, w=1.4)
text(GX, 992, "Window-wide self-attention", cls="h2", anchor="middle")

# two parallel branches -> feature fusion -> refinement (FFN, residual and
# normalization are implementation details; see Supplementary Fig. 7)
FX, FY = 820, 881
path(f"M{GX + 92} {GY} C{GX + 140} {GY} {FX - 60} {FY - 12} {FX - 21} {FY - 5}", stroke=NAVY, w=2, arrow="aNavy")
path(f"M{TOK[-1] + 22} {TY} C{GX + 150} {TY} {FX - 60} {FY + 12} {FX - 21} {FY + 5}", stroke=NAVY, w=2, arrow="aNavy")
text(752, 800, 'h<tspan font-size="72%" baseline-shift="sub">local</tspan>', cls="lbb", anchor="middle", extra=' font-style="italic"')
text(756, 936, 'h<tspan font-size="72%" baseline-shift="sub">global</tspan>', cls="lbb", anchor="middle", extra=' font-style="italic"')
add(f'<circle cx="{FX}" cy="{FY}" r="19" fill="#ffffff" stroke="{NAVY}" stroke-width="2.4"/>')
path(f"M{FX - 10} {FY} L{FX + 10} {FY} M{FX} {FY - 10} L{FX} {FY + 10}", stroke=NAVY, w=2.6)
text(FX + 30, 840, "Feature fusion", cls="h2", anchor="middle")
path(f"M{FX + 21} {FY} L{FX + 26} {FY}", stroke=BLUE, w=2.4)
for bx in (FX + 28, FX + 58, FX + 88):                 # feed-forward layers (unlabelled)
    rect(bx, 852, 20, 58, PURPLE, rx=5, stroke=PURPLED, sw=1.4)
path(f"M{FX + 112} {FY} L982 {FY}", stroke=BLUE, w=2.4, arrow="aBlue")

text(1100, 724, "Phase-confidence", cls="h2", anchor="middle"); text(1100, 746, "refinement", cls="h2", anchor="middle")
window_graph([1012, 1056, 1100, 1144, 1188], 800, 866, "ATCGT", "GCTAC", r=19, fs=15.5, centre=2, w_h=6.5, w_x=1.6, arcs=True)
path("M1100 934 L1100 892", stroke=NAVY, w=1.6, arrow="aNavy")
text(1100, 956, "Unphased SNP", anchor="middle")

# ============================================================================
# Panel d
# ============================================================================
text(1252, 722, "d", cls="pl")
COLS = [1344, 1392, 1450, 1508, 1556, 1604]

text(1274, 744, "Haplotype 1", cls="h2", fill=BLUE)
hedge(1322, 1626, 780, LBLUE, 7)
snp(COLS[0], 780, "A", BLUE, r=20, fs=16); snp(COLS[1], 780, "T", BLUE, r=20, fs=16)
box(COLS[2], 780, "SV", BLUE)
lollipop(COLS[3], 780, True)
snp(COLS[4], 780, "A", BLUE, r=20, fs=16); snp(COLS[5], 780, "C", BLUE, r=20, fs=16)

text(1274, 828, "Haplotype 2", cls="h2", fill=RED)
hedge(1322, 1626, 864, LRED, 7)
snp(COLS[0], 864, "G", RED, r=20, fs=16); snp(COLS[1], 864, "C", RED, r=20, fs=16)
lollipop(COLS[3], 864, False)
box(COLS[4], 864, "CA", RED)
snp(COLS[5], 864, "T", RED, r=20, fs=16)

text(1274, 904, "Haplotagging reads", cls="h2")
for k, (lab, hap, al) in enumerate((("Read 1", 1, "ATAC"), ("Read 2", 1, "ATAC"), ("Read 3", 2, "GCXT"))):
    y = 934 + k * 33
    col, rf = (BLUE, READ_B) if hap == 1 else (RED, READ_R)
    text(1312, y + 6, lab, anchor="end", fill=col)
    rect(1322, y - 5, 304, 10, rf, rx=5)
    snp(COLS[0], y, al[0], col, r=12.5, fs=11.5); snp(COLS[1], y, al[1], col, r=12.5, fs=11.5)
    if hap == 1:
        box(COLS[2], y, "SV", col, w=36, h=22, fs=11, sw=2.2)
        lollipop(COLS[3], y, True, r=6, stem=16, sw=2.8)
        snp(COLS[4], y, al[2], col, r=12.5, fs=11.5)
    else:
        lollipop(COLS[3], y, False, r=6, stem=16, sw=2.8)
        box(COLS[4], y, "CA", col, w=36, h=22, fs=11, sw=2.2)
    snp(COLS[5], y, al[3], col, r=12.5, fs=11.5)

add("</svg>")

# ============================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(root, "figures", "fig1_overview.svg")
open(dst, "w").write("\n".join(out) + "\n")
print("wrote", dst)
