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
  c  node/edge features of a window -> local message passing (star; GATv2)
     and global self-attention over the window (token row; Transformer) ->
     feature fusion (with a skip connection from the input) -> feed-forward
     network (with a skip connection) -> phase-confidence refinement (trigger
     SNP unphased). The block is framed as one of the repeated (GPS) layers;
     layer normalization is omitted (see Supplementary Fig. 6).
  d  two haplotypes carrying SNVs, an SV, an indel and a CpG, and four
     haplotagged reads; row labels sit left of each track.

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
<marker id="aSkip" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="7.5" markerHeight="7.5" orient="auto-start-reverse">
  <path d="M0 0.8 L9.6 5 L0 9.2 z" fill="#6F8090"/></marker>
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

def snp(cx, cy, letter, color, r=21, fs=23.5, fill="#ffffff", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2.6"{d}/>')
    if letter:
        add(f'<text x="{cx:.1f}" y="{cy + fs * 0.35:.1f}" class="nt" fill="{color}" text-anchor="middle" font-size="{fs}">{letter}</text>')

def box(cx, cy, label, color, w=52, h=30, fs=18.5, sw=2.6, dash=None):
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
line(1142, 694, 1142, 1000, "#C9D2DC", 1.6, cap="butt")

# ============================================================================
# Panel a
# ============================================================================
text(24, 44, "a", cls="pl")
LY = 84
snp(48, LY, "A", BLUE, r=15, fs=17);                     text(70, LY + 6, "SNP")
box(126, LY, "", BLUE, w=27, h=21, sw=2.2);              text(148, LY + 6, "Indel")
box(228, LY, "SV", BLUE, w=44, h=25, fs=15.5, sw=2.2);   text(258, LY + 6, "SV")
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
        snp(COLX[0], y, "A", BLUE, r=17, fs=19)
        box(COLX[1], y, "", BLUE, w=27, h=22, sw=2.4)
        if i != 2:                                   # read 3 does not span the SV
            box(COLX[2], y, "SV", BLUE, w=44, h=26, fs=16, sw=2.4)
        snp(COLX[3], y, "T", BLUE, r=17, fs=19)
        lollipop(COLX[4], y, True)
        box(COLX[5], y, "", BLUE, w=27, h=22, sw=2.4)
    else:
        snp(COLX[0], y, "G", RED, r=17, fs=19)
        snp(COLX[3], y, "C", RED, r=17, fs=19)
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
                box(x, yb, "CA", RED, w=58, h=42, fs=26)
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
block_arrow(548, 408, 460)
stage(508, 538, "Reweighted", "graph")

# --- inset 1: uncertain base call -------------------------------------------
BX = -30                                                  # inset offset (raster places it left of the C node)
text(828 + BX, 254, "Uncertain base call", cls="h2", anchor="middle")
text(722 + BX, 324, "Read", anchor="end")
line(748 + BX, 318, 912 + BX, 318, FBLUE, 9, cap="butt")
rect(806 + BX, 342, 46, 102, HILITE, rx=4)
snp(766 + BX, 318, "A", BLUE, r=20, fs=22.5)
snp(830 + BX, 318, "C", BLUE, r=20, fs=22.5, dash="6 4.5")
snp(894 + BX, 318, "T", BLUE, r=20, fs=22.5)
for x1, y1, x2, y2 in ((816, 292, 808, 280), (830, 290, 830, 276), (844, 292, 852, 280)):
    line(x1 + BX, y1, x2 + BX, y2, CYAN, 2.6)            # rays: an uncertain call
text(732 + BX, 378, "Phred quality")
rect(749 + BX, 386, 34, 58, UNPH, rx=1.5); rect(813 + BX, 424, 34, 20, ORANGE, rx=1.5); rect(877 + BX, 394, 34, 50, UNPH, rx=1.5)
line(740 + BX, 444, 920 + BX, 444, NAVY, 2, cap="butt")

# --- inset 2: sequence-context reliability ----------------------------------
text(1200, 254, "Sequence-context reliability", cls="h2", anchor="middle")
text(1058, 320, "Non-repetitive", anchor="end"); text(1058, 342, "context", anchor="end")
for x, ch in zip((1091, 1118, 1145), "GTC"):
    text(x, 306, ch, cls="sm", anchor="middle"); line(x, 314, x, 326, UNPH, 1.6); text(x, 346, ch, cls="sm", anchor="middle")
for x, ch in zip((1279, 1306, 1333), "GCT"):
    text(x, 306, ch, cls="sm", anchor="middle"); line(x, 314, x, 326, UNPH, 1.6); text(x, 346, ch, cls="sm", anchor="middle")
box(1212, 303, "A", BLUE, w=46, h=34, fs=21); box(1212, 349, "CA", RED, w=56, h=34, fs=21)
text(1058, 412, "Tandem-repeat", anchor="end"); text(1058, 434, "context", anchor="end")
for x0 in (1069.2, 1265.2):
    rect(x0, 382, 89.6, 64, HILITE, rx=5)
for x in (1094, 1134, 1290, 1330):
    text(x, 398, "CA", cls="sm", anchor="middle"); line(x, 406, x, 418, UNPH, 1.6); text(x, 438, "CA", cls="sm", anchor="middle")
box(1212, 395, "A", BLUE, w=46, h=34, fs=21); box(1212, 441, "CA", RED, w=56, h=34, fs=21, dash="6 4.5")

# --- inset 3: miscalled SNPs in a CNV ---------------------------------------
text(1548, 254, "Miscalled SNPs in CNV", cls="h2", anchor="middle")
rect(1460, 280, 176, 146, HILITE, rx=6)
for k, (y, right) in enumerate(((306, "A"), (354, "T"), (402, "A"))):
    text(1448, y + 6, f"Read {k + 1}", anchor="end")
    line(1486, y, 1610, y, GREY, 2)
    snp(1486, y, "T", BLUE, r=19, fs=21.5); filtered(1548, y, r=18); snp(1610, y, right, BLUE, r=19, fs=21.5)

# --- pointers from each inset to the evidence it calibrates ------------------
path("M772 234 C776 214 812 212 844 196", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")    # -> C (uncertain call)
path("M1056 236 C1044 220 1018 208 996 194", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")  # -> CA (tandem repeat)
path("M1502 234 C1482 224 1448 218 1416 214", stroke=NAVY, w=2, dash="7 6", arrow="aNavy") # -> spurious CNV link

# --- reweighted graph ---------------------------------------------------------
YT2, YB2 = 518, 580
path(f"M{GXS[1]:.1f} {YB2 + 18} Q{GXS[4]:.1f} 646 {GXS[7]:.1f} {YB2 + 18}", stroke=LRED, w=2.8, op=0.9)
graph(YT2, YB2, reweighted=True)

# --- legend -------------------------------------------------------------------
LGY = 647
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
for s, x in (("Phase evidence", 64), ("Variant type", 183)):
    text(x, 748, s, cls="sm")
text(274, 746, "···", cls="sm")

XS = [83, 129, 175, 221, 267]                              # same node size / pitch as the refined window
YTc, YBc, CTR = 852, 910, 2                                # rows centred on the flow axis (FY = 881)
rect(XS[CTR] - 27, YTc - 31, 54, YBc - YTc + 62, HILITE, rx=8)
window_graph(XS, YTc, YBc, "ATCGT", "GCTAC", r=19, fs=21.5, centre=CTR)
path(f"M{XS[CTR] + 22} 754 C{XS[CTR] + 18} 780 {XS[CTR] + 6} 800 {XS[CTR] + 2} {YTc - 26}", stroke=NAVY, w=1.6, arrow="aNavy")

text(64, 966, "Edge features", cls="h2")
for s, x in (("Link strength", 64), ("Genomic distance", 168)):
    text(x, 992, s, cls="sm")
text(298, 990, "···", cls="sm")
path(f"M132 950 C142 940 148 932 152 {YBc + 8}", stroke=NAVY, w=1.6, arrow="aNavy")

# --- repeated GPS layers: stacked frame around the block ---------------------
FR = (370, 724, 510, 293)                                  # x, y, w, h of the front frame
for k in (2, 1):
    rect(FR[0] + 8 * k, FR[1] - 8 * k, FR[2], FR[3], "none", rx=12, stroke="#C9D2DC", sw=1.6)
rect(*FR, "#ffffff", rx=12, stroke="#B9C4D0", sw=1.6)
text(FR[0] + FR[2] / 2 + 8, 703, "Repeated layers", cls="lbb", anchor="middle", fill=UNPH)

IN_X, IN_Y = 352, 881
path(f"M{XS[-1] + 26} {IN_Y} L{IN_X - 22} {IN_Y}", stroke=BLUE, w=2.4, arrow="aBlue")
add(f'<circle cx="{IN_X}" cy="{IN_Y}" r="13" fill="#ffffff" stroke="{NAVY}" stroke-width="2.4"/>')
path(f"M{IN_X + 10} {IN_Y - 9} C{IN_X + 28} {IN_Y - 30} {IN_X + 30} {IN_Y - 56} {IN_X + 38} {IN_Y - 72}", stroke=BLUE, w=2.4, arrow="aBlue")
path(f"M{IN_X + 10} {IN_Y + 9} C{IN_X + 22} {IN_Y + 22} {IN_X + 24} {IN_Y + 32} {IN_X + 30} {IN_Y + 41}", stroke=BLUE, w=2.4, arrow="aBlue")

# --- local branch: message passing over graph neighbours --------------------
GX, GY = 484, 812
text(GX, 746, "Local message passing", cls="h2", anchor="middle")
add(f'<ellipse cx="{GX}" cy="{GY}" rx="86" ry="46" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="6 5"/>')
neigh = [(GX - 56, GY - 24, "#8FD18A"), (GX + 50, GY - 26, LBLUE), (GX - 50, GY + 22, "#F49AC1"),
         (GX + 56, GY + 20, LRED), (GX + 10, GY + 34, "#B9A5E6")]
for nx, ny, col in neigh:
    dx, dy = GX - nx, GY - ny
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    path(f"M{nx + ux * 10:.1f} {ny + uy * 10:.1f} L{GX - ux * 14:.1f} {GY - uy * 14:.1f}", stroke="#7C8DA0", w=1.8, arrow="aGrey")
for nx, ny, col in neigh:
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="8.5" fill="{col}" stroke="{col}" stroke-width="1"/>')
add(f'<circle cx="{GX}" cy="{GY}" r="11.5" fill="#F6C24E" stroke="#C98A2E" stroke-width="1.6"/>')

# --- global branch: self-attention across the window ------------------------
# (the title sits above the token row, matching the local branch, which keeps
#  the band under the tokens clear for the input skip connection)
TOK = [GX - 75 + 30 * i for i in range(6)]
TY = 926
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
text(GX, 884, "Global self-attention", cls="h2", anchor="middle")

# --- fusion with skip connection, feed-forward network with skip connection --
# (one GPS layer; layer normalization omitted, see Supplementary Fig. 6)
FX, FY = 672, 881
path(f"M{GX + 88} {GY} C{GX + 107} {GY} {FX - 50} {FY - 12} {FX - 19} {FY - 5}", stroke=NAVY, w=2, arrow="aNavy")
path(f"M{TOK[-1] + 22} {TY} C{GX + 129} {TY} {FX - 46} {FY + 12} {FX - 19} {FY + 5}", stroke=NAVY, w=2, arrow="aNavy")
text(604, 800, 'h<tspan font-size="72%" baseline-shift="sub">local</tspan>', cls="lbb", anchor="middle", extra=' font-style="italic"')
text(624, 936, 'h<tspan font-size="72%" baseline-shift="sub">global</tspan>', cls="lbb", anchor="middle", extra=' font-style="italic"')
# skip connection from the input into the fusion node
path(f"M{IN_X} {IN_Y + 14} L{IN_X} 1004 L{FX} 1004 L{FX} {FY + 19}", stroke=UNPH, w=2, arrow="aSkip")
text((IN_X + FX) / 2, 996, "Skip connection", cls="sm", anchor="middle", fill=UNPH)
add(f'<circle cx="{FX}" cy="{FY}" r="17" fill="#EAF4FB" stroke="{NAVY}" stroke-width="2.4"/>')
path(f"M{FX - 9} {FY} L{FX + 9} {FY} M{FX} {FY - 9} L{FX} {FY + 9}", stroke=NAVY, w=2.6)
text(FX - 12, 824, "Feature", cls="h2", anchor="middle"); text(FX - 12, 846, "fusion", cls="h2", anchor="middle")
# feed-forward network
JX = FX + 34
path(f"M{FX + 18} {FY} L719 {FY}", stroke=BLUE, w=2.4, arrow="aBlue")
add(f'<circle cx="{JX}" cy="{FY}" r="3.6" fill="{NAVY}"/>')
for bx, bh in ((722, 44), (764, 62), (806, 44)):
    rect(bx, FY - bh / 2, 18, bh, PURPLE, rx=4, stroke=PURPLED, sw=1.4)
for x1 in (741, 783):
    path(f"M{x1} {FY} L{x1 + 20} {FY}", stroke=BLUE, w=2, arrow="aBlue")
text(773, 938, "Feed-forward", cls="lbb", anchor="middle", fill=PURPLED)
text(773, 958, "network", cls="lbb", anchor="middle", fill=PURPLED)
# skip connection over the feed-forward network
SX = 856
path(f"M{JX} {FY} L{JX} 824 L{SX} 824 L{SX} {FY - 16}", stroke=UNPH, w=2, arrow="aSkip")
text((JX + SX) / 2, 816, "Skip connection", cls="sm", anchor="middle", fill=UNPH)
path(f"M825 {FY} L{SX - 16} {FY}", stroke=BLUE, w=2.4, arrow="aBlue")
add(f'<circle cx="{SX}" cy="{FY}" r="14" fill="#ffffff" stroke="{NAVY}" stroke-width="2.4"/>')
path(f"M{SX - 7} {FY} L{SX + 7} {FY} M{SX} {FY - 7} L{SX} {FY + 7}", stroke=NAVY, w=2.4)
path(f"M{SX + 15} {FY} L902 {FY}", stroke=BLUE, w=2.4, arrow="aBlue")

# refined window: same node size, pitch and rows as the input window on the left
text(1018, 744, "Phase-confidence", cls="h2", anchor="middle"); text(1018, 766, "refinement", cls="h2", anchor="middle")
window_graph([926, 972, 1018, 1064, 1110], YTc, YBc, "ATCGT", "GCTAC", r=19, fs=21.5, centre=2, arcs=True)
path(f"M1018 {YBc + 68} L1018 {YBc + 26}", stroke=NAVY, w=1.6, arrow="aNavy")
text(1018, YBc + 90, "Unphased SNP", anchor="middle")

# ============================================================================
# Panel d
# ============================================================================
# Row labels sit to the left of each track (right-aligned, as in panel a), so
# the tracks are narrower than in the 2026-09-18 raster and four reads fit.
text(1156, 722, "d", cls="pl")
LBX = 1294                                                 # right edge of the label column
TX0, TX1 = 1306, 1642                                      # track extent
COLS = [1330 + 57 * i for i in range(6)]
HY1, HY2 = 744, 806

text(LBX, HY1 + 7, "Haplotype 1", cls="h2", fill=BLUE, anchor="end")
hedge(TX0, TX1, HY1, LBLUE, 7)
snp(COLS[0], HY1, "A", BLUE, r=19, fs=21.5); snp(COLS[1], HY1, "T", BLUE, r=19, fs=21.5)
box(COLS[2], HY1, "SV", BLUE, w=50)
lollipop(COLS[3], HY1, True)
snp(COLS[4], HY1, "A", BLUE, r=19, fs=21.5); snp(COLS[5], HY1, "C", BLUE, r=19, fs=21.5)

text(LBX, HY2 + 7, "Haplotype 2", cls="h2", fill=RED, anchor="end")
hedge(TX0, TX1, HY2, LRED, 7)
snp(COLS[0], HY2, "G", RED, r=19, fs=21.5); snp(COLS[1], HY2, "C", RED, r=19, fs=21.5)
lollipop(COLS[3], HY2, False)
box(COLS[4], HY2, "CA", RED, w=50)
snp(COLS[5], HY2, "T", RED, r=19, fs=21.5)

text(1178, 864, "Haplotagging reads", cls="h2")
for k, (lab, hap, al) in enumerate((("Read 1", 1, "ATAC"), ("Read 2", 1, "ATAC"),
                                    ("Read 3", 2, "GCXT"), ("Read 4", 2, "GCXT"))):
    y = 890 + k * 32
    col, rf = (BLUE, READ_B) if hap == 1 else (RED, READ_R)
    text(LBX, y + 6, lab, anchor="end", fill=col)
    rect(TX0, y - 5, TX1 - TX0, 10, rf, rx=5)
    snp(COLS[0], y, al[0], col, r=12.5, fs=14); snp(COLS[1], y, al[1], col, r=12.5, fs=14)
    if hap == 1:
        box(COLS[2], y, "SV", col, w=36, h=22, fs=13.5, sw=2.2)
        lollipop(COLS[3], y, True, r=6, stem=16, sw=2.8)
        snp(COLS[4], y, al[2], col, r=12.5, fs=14)
    else:
        lollipop(COLS[3], y, False, r=6, stem=16, sw=2.8)
        box(COLS[4], y, "CA", col, w=36, h=22, fs=13.5, sw=2.2)
    snp(COLS[5], y, al[3], col, r=12.5, fs=14)

add("</svg>")

# ============================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(root, "figures", "fig1_overview.svg")
open(dst, "w").write("\n".join(out) + "\n")
print("wrote", dst)
