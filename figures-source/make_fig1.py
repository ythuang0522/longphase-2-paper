#!/usr/bin/env python3
"""Generate Figure 1 (figures/fig1_overview.svg; convert to PDF with rsvg-convert).

Single vector source for all four panels, drawn in the house style of the
original 2026-09-18 master (Helvetica Neue, navy text, blue/red haplotypes).
Layout follows the 2026-09-18 redesign raster:

  a  two-row legend (no panel headings anywhere); reference with seven variant columns; six
     reads at 74 px pitch, carrying SNV / indel (boxes with sequence) / SV alleles and a
     CpG (methylated = filled lollipop, unmethylated = open) on the read line;
     reads 3 and 4 disagree at the fifth column (the SNV unphased in c). The
     columns are the same alleles as the haplotypes in d.
  b  original graph (all edges high-confidence, long-range read links drawn as
     arcs) -> evidence calibration (uncertain base call with Phred bars,
     sequence-context reliability as haplotype 1 (blue) over haplotype 2 (red)
     sequences, miscalled SNVs in a CNV) -> reweighted graph
     (down-weighted C and CA dashed, their edges low-confidence dashed, filtered
     CNV variants); grey cross-links are left unstyled.
  c  per-variant phasing uncertainty bars (y-axis label; trigger orange, no
     threshold line) above the window; three example node and edge features
     each, then an ellipsis, below it -> local message passing (star;
     GATv2) and global self-attention over the window (token row; Transformer)
     -> feature fusion (with a skip connection from the input h(l)) ->
     feed-forward network (with a skip connection) -> phase-confidence
     refinement (trigger SNV unphased; neighbours still linked, so the haplotype
     block stays intact). The block is framed as one of the four repeated (GPS) layers;
     layer normalization is omitted (see Supplementary Fig. 6).
  d  two haplotypes carrying the alleles of a, the unphased SNV in grey, a
     per-variant uncertainty strip and four haplotagged reads;
     row labels sit left of each track.

Panels c and d are drawn in a 1680 x 1072 frame and lifted 26 px by a group
transform, the height saved by compacting a and b.

Fonts: nothing prints below 5 pt at 180 mm width (1 px = 0.30 pt; .sm = 17 px).

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

HEADER = """<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="1046" viewBox="0 0 1680 1046">
<title>LongPhase 2 overview: evidence-calibrated phasing graph and graph-transformer phase-error detection</title>
<defs>
<style>
 text{font-family:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;
      letter-spacing:.005em}
 .pl{font-size:26.5px;font-weight:700}
 .h1{font-size:21.5px;font-weight:600}
 .h2{font-size:19.5px;font-weight:700}
 .lb{font-size:17.5px;font-weight:400}
 .lbb{font-size:17.5px;font-weight:600}
 .sm{font-size:17px;font-weight:400}
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
<rect width="1680" height="1046" fill="#ffffff"/>"""

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

def lowconf(x1, x2, y):
    """Down-weighted (low-confidence) edge: thin, dashed, haplotype 2 colour."""
    line(x1, y, x2, y, RED, 2.6, cap="butt", op=0.75, dash="8 6")

def cross(x1, x2, yt, yb, w=1.9, op=0.85):
    line(x1, yt, x2, yb, GREY, w, op=op)
    line(x1, yb, x2, yt, GREY, w, op=op)

# separators
line(498, 22, 498, 634, "#C9D2DC", 1.6, cap="butt")
line(24, 650, 1656, 650, "#C9D2DC", 1.6, cap="butt")
line(1142, 668, 1142, 1026, "#C9D2DC", 1.6, cap="butt")

# ============================================================================
# Panel a
# ============================================================================
text(24, 44, "a", cls="pl")
# Legend on two rows. Indel alleles are boxes carrying their sequence (reference
# "A", insertion "CA"), as in panels b and d.
LY, LY2 = 72, 106
snp(48, LY, "A", BLUE, r=15, fs=17);                     text(70, LY + 6, "SNV")
box(140, LY, "CA", BLUE, w=40, h=24, fs=16.5, sw=2.2);   text(166, LY + 6, "Indel")
box(250, LY, "SV", BLUE, w=44, h=25, fs=16.5, sw=2.2);   text(280, LY + 6, "SV")
lollipop(48, LY2 - 4, True, r=7.5, stem=22);             text(64, LY2 + 6, "Methylated CpG")
lollipop(232, LY2 - 4, False, r=7.5, stem=22);           text(248, LY2 + 6, "Unmethylated CpG")

# Seven variant columns, the same alleles as the phased haplotypes in panel d:
# SNV, SNV, SV, CpG, SNV (conflicting read support; unphased in c), indel, SNV.
RX0, RX1 = 150, 478
COLX = [170 + 48 * i for i in range(7)]
text(138, 158, "Reference", cls="h1", anchor="end")
rect(RX0, 145, RX1 - RX0, 13, NAVY)
for x in COLX:
    rect(x - 2.6, 133, 5.2, 37, NAVY, rx=2)
READS_Y = [210 + 74 * i for i in range(6)]
for x in COLX:
    line(x, 176, x, READS_Y[-1] + 22, "#B9C4D0", 1.5, dash="4 6")
CONFLICT = ["C", "T", "T", "C", "C", "T"]            # column 5 allele per read (reads 3, 4 disagree)
for i, y in enumerate(READS_Y):
    hap1 = i % 2 == 0
    col = BLUE if hap1 else RED
    text(138, y + 6, f"Read {i + 1}", anchor="end")
    rect(RX0, y - 6.5, RX1 - RX0, 13, READ, rx=6.5)
    snp(COLX[0], y, "A" if hap1 else "G", col, r=17, fs=19)
    snp(COLX[1], y, "T" if hap1 else "C", col, r=17, fs=19)
    if hap1 and i != 2:                              # read 3 does not span the SV
        box(COLX[2], y, "SV", BLUE, w=44, h=26, fs=16.5, sw=2.4)
    lollipop(COLX[3], y, hap1)
    snp(COLX[4], y, CONFLICT[i], col, r=17, fs=19)
    box(COLX[5], y, "A" if hap1 else "CA", col, w=40, h=26, fs=16.5, sw=2.4)
    snp(COLX[6], y, "G" if hap1 else "A", col, r=17, fs=19)

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
            hedge(x1, x2, yt, LBLUE, 9.5); lowconf(x1, x2, yb)
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
            if i == 2:                              # indel column: reference A / insertion CA
                box(x, yt, "A", BLUE, w=58, h=42, fs=26)
                box(x, yb, "CA", RED, w=58, h=42, fs=26, dash=("6 4.5" if reweighted else None))
            else:
                snp(x, yt, TOP[i], BLUE, r=r, fs=fs)
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
block_arrow(548, 384, 440)
stage(482, 512, "Reweighted", "graph")

# --- inset 1: uncertain base call -------------------------------------------
BX = -30                                                  # inset offset (raster places it left of the C node)
text(828 + BX, 254, "Uncertain base call", cls="h2", anchor="middle")
text(722 + BX, 324, "Read", anchor="end")
line(748 + BX, 318, 912 + BX, 318, FRED, 9, cap="butt")
rect(806 + BX, 342, 46, 88, HILITE, rx=4)
snp(766 + BX, 318, "G", RED, r=20, fs=22.5)
snp(830 + BX, 318, "C", RED, r=20, fs=22.5, dash="6 4.5")
box(894 + BX, 318, "CA", RED, w=48, h=36, fs=20)
for x1, y1, x2, y2 in ((816, 292, 808, 280), (830, 290, 830, 276), (844, 292, 852, 280)):
    line(x1 + BX, y1, x2 + BX, y2, CYAN, 2.6)            # rays: an uncertain call
text(732 + BX, 362, "Phred quality")
rect(749 + BX, 378, 34, 52, UNPH, rx=1.5); rect(813 + BX, 410, 34, 20, ORANGE, rx=1.5); rect(877 + BX, 386, 34, 44, UNPH, rx=1.5)
line(740 + BX, 430, 920 + BX, 430, NAVY, 2, cap="butt")

# --- inset 2: sequence-context reliability ----------------------------------
# Each context is the haplotype 1 sequence (top, blue) over the haplotype 2
# sequence (bottom, red); ticks join identical flanking bases, the boxed
# alleles are the indel. The CA insertion is solid in unique sequence and
# dashed (down-weighted) inside the CA repeat, where its placement is ambiguous.
text(1200, 254, "Sequence-context reliability", cls="h2", anchor="middle")
def ctx_row(yt, yb, flanks, dash):
    for x, ch in flanks:
        text(x, yt + 6, ch, cls="sm", fill=BLUE, anchor="middle")
        line(x, yt + 11, x, yb - 13, UNPH, 1.6)
        text(x, yb + 6, ch, cls="sm", fill=RED, anchor="middle")
    box(1212, yt, "A", BLUE, w=46, h=30, fs=20); box(1212, yb, "CA", RED, w=56, h=30, fs=20, dash=dash)
text(1058, 310, "Non-repetitive", anchor="end"); text(1058, 332, "context", anchor="end")
ctx_row(296, 334, list(zip((1091, 1118, 1145, 1279, 1306, 1333), "GTCGCT")), None)
text(1058, 392, "Tandem-repeat", anchor="end"); text(1058, 414, "context", anchor="end")
for x0 in (1069.2, 1265.2):
    rect(x0, 364, 89.6, 70, HILITE, rx=5)
ctx_row(380, 418, [(x, "CA") for x in (1094, 1134, 1290, 1330)], "6 4.5")

# --- inset 3: miscalled SNPs in a CNV ---------------------------------------
text(1548, 254, "Miscalled SNVs in CNV", cls="h2", anchor="middle")
rect(1460, 280, 176, 146, HILITE, rx=6)
for k, (y, right) in enumerate(((306, "A"), (354, "T"), (402, "A"))):
    text(1448, y + 6, f"Read {k + 1}", anchor="end")
    line(1486, y, 1610, y, GREY, 2)
    snp(1486, y, "T", BLUE, r=19, fs=21.5); filtered(1548, y, r=18); snp(1610, y, right, BLUE, r=19, fs=21.5)

# --- pointers from each inset to the evidence it calibrates ------------------
path("M772 234 C776 214 812 212 844 196", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")    # -> C (uncertain call)
path("M1056 236 C1044 220 1018 208 996 194", stroke=NAVY, w=2, dash="7 6", arrow="aNavy")  # -> CA (tandem repeat)
path("M1470 236 C1420 232 1290 226 1248 198", stroke=NAVY, w=2, dash="7 6", arrow="aNavy") # -> miscalled G/A in the CNV

# --- reweighted graph ---------------------------------------------------------
YT2, YB2 = 492, 554
path(f"M{GXS[1]:.1f} {YB2 + 18} Q{GXS[4]:.1f} 620 {GXS[7]:.1f} {YB2 + 18}", stroke=LRED, w=2.8, op=0.9)
graph(YT2, YB2, reweighted=True)

# --- legend -------------------------------------------------------------------
LGY = 621
hedge(700, 748, LGY, LBLUE, 9.5);            text(758, LGY + 6, "High-confidence edge")
lowconf(960, 1008, LGY);                     text(1018, LGY + 6, "Low-confidence edge")
snp(1222, LGY, "", RED, r=14, dash="5 4");   text(1244, LGY + 6, "Down-weighted allele")
filtered(1454, LGY, r=14);                   text(1476, LGY + 6, "Filtered variant")

# Panels c and d are drawn in their original frame and lifted by the 26 px
# saved in panels a and b.
add('<g transform="translate(0,-26)">')

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
XS = [83, 129, 175, 221, 267]                              # same node size / pitch as the refined window
YTc, YBc, CTR = 852, 910, 2                                # rows centred on the flow axis (FY = 881)

# --- per-variant phasing uncertainty (phasing entropy): the trigger exceeds the threshold
# (bar chart with its own y-axis label; no threshold line in the overview)
PE_BASE, AX = 812, 64
rect(XS[CTR] - 27, 742, 54, YBc + 31 - 742, HILITE, rx=8)  # trigger column: bar + window nodes
for x, h in zip(XS, (16, 22, 62, 12, 18)):
    trig = x == XS[CTR]
    rect(x - 11, PE_BASE - h, 22, h, ORANGE if trig else GREY, rx=2, stroke="#C97A0E" if trig else "none", sw=1.2)
line(AX, PE_BASE, 292, PE_BASE, UNPH, 1.4, cap="butt")
line(AX, 718, AX, PE_BASE, UNPH, 1.4, cap="butt")
for dx, s in ((-20, "Phasing"), (-3, "uncertainty")):
    text(AX + dx, 765, s, cls="sm", anchor="middle", extra=f' transform="rotate(-90 {AX + dx} 765)"')
window_graph(XS, YTc, YBc, "ATCGT", "GCTAC", r=19, fs=21.5, centre=CTR)

# --- node and edge features of the window (below it) -------------------------
text(40, 972, "Node features", cls="h2")
for k, s in enumerate(("Phase evidence", "Variant type", "Genomic context", "…")):
    text(40, 996 + 19 * k, s, cls="sm")
path(f"M104 954 C108 946 118 940 {XS[1] - 4} {YBc + 22}", stroke=NAVY, w=1.6, arrow="aNavy")
text(190, 972, "Edge features", cls="h2")
for k, s in enumerate(("Link strength", "Genomic distance", "Block membership", "…")):
    text(190, 996 + 19 * k, s, cls="sm")
path(f"M238 954 C240 944 244 934 244 {YBc + 8}", stroke=NAVY, w=1.6, arrow="aNavy")

# --- repeated GPS layers: stacked frame around the block ---------------------
FR = (370, 724, 510, 293)                                  # x, y, w, h of the front frame
for k in (2, 1):
    rect(FR[0] + 8 * k, FR[1] - 8 * k, FR[2], FR[3], "none", rx=12, stroke="#C9D2DC", sw=1.6)
rect(*FR, "#ffffff", rx=12, stroke="#B9C4D0", sw=1.6)
text(FR[0] + FR[2] / 2 + 8, 699, "Repeated layer ×4", cls="lbb", anchor="middle", fill=UNPH)

IN_X, IN_Y = 352, 881
path(f"M{XS[-1] + 26} {IN_Y} L{IN_X - 22} {IN_Y}", stroke=BLUE, w=2.4, arrow="aBlue")
add(f'<circle cx="{IN_X}" cy="{IN_Y}" r="13" fill="#ffffff" stroke="{NAVY}" stroke-width="2.4"/>')
text(343, 926, 'h<tspan font-size="85%" baseline-shift="super">(l)</tspan>', cls="lbb", anchor="end", extra=' font-size="20" font-style="italic"')
path(f"M{IN_X + 10} {IN_Y - 9} C{IN_X + 28} {IN_Y - 30} {IN_X + 30} {IN_Y - 56} {IN_X + 38} {IN_Y - 72}", stroke=BLUE, w=2.4, arrow="aBlue")
path(f"M{IN_X + 10} {IN_Y + 9} C{IN_X + 22} {IN_Y + 22} {IN_X + 24} {IN_Y + 32} {IN_X + 30} {IN_Y + 41}", stroke=BLUE, w=2.4, arrow="aBlue")

# --- local branch: message passing over graph neighbours --------------------
GX, GY = 484, 812
text(GX, 746, "Local message passing", cls="h2", anchor="middle")
add(f'<ellipse cx="{GX}" cy="{GY}" rx="86" ry="46" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="6 5"/>')
neigh = [(GX - 56, GY - 24, BLUE), (GX + 50, GY - 26, BLUE), (GX - 50, GY + 22, RED),
         (GX + 56, GY + 20, RED), (GX + 10, GY + 34, BLUE)]
for nx, ny, col in neigh:
    dx, dy = GX - nx, GY - ny
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    path(f"M{nx + ux * 10:.1f} {ny + uy * 10:.1f} L{GX - ux * 14:.1f} {GY - uy * 14:.1f}", stroke="#7C8DA0", w=1.8, arrow="aGrey")
for nx, ny, col in neigh:
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="8.5" fill="{col}" stroke="{col}" stroke-width="1"/>')
add(f'<circle cx="{GX}" cy="{GY}" r="11.5" fill="{ORANGE}" stroke="#C97A0E" stroke-width="1.6"/>')

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
    col, sc = (ORANGE, "#C97A0E") if i == 3 else (GREY, UNPH)
    rect(tx - 8, TY - 8, 16, 16, col, rx=2.5, stroke=sc, sw=1.2)
path(f"M{TOK[0] - 14} {TY + 16} L{TOK[0] - 14} {TY + 24} L{TOK[-1] + 14} {TY + 24} L{TOK[-1] + 14} {TY + 16}", stroke=NAVY, w=1.4)
text(GX, 884, "Global self-attention", cls="h2", anchor="middle")

# --- fusion with skip connection, feed-forward network with skip connection --
# (one GPS layer; layer normalization omitted, see Supplementary Fig. 6)
FX, FY = 672, 881
path(f"M{GX + 88} {GY} C{GX + 107} {GY} {FX - 50} {FY - 12} {FX - 19} {FY - 5}", stroke=NAVY, w=2, arrow="aNavy")
path(f"M{TOK[-1] + 22} {TY} C{GX + 129} {TY} {FX - 46} {FY + 12} {FX - 19} {FY + 5}", stroke=NAVY, w=2, arrow="aNavy")
text(604, 798, 'h<tspan font-size="85%" baseline-shift="sub">local</tspan>', cls="lbb", anchor="middle", extra=' font-size="20" font-style="italic"')
text(626, 938, 'h<tspan font-size="85%" baseline-shift="sub">global</tspan>', cls="lbb", anchor="middle", extra=' font-size="20" font-style="italic"')
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
text(1018, YBc + 90, "Unphased SNV", anchor="middle")

# ============================================================================
# Panel d
# ============================================================================
# Row labels sit to the left of each track (right-aligned, as in panel a).
# Columns follow panel a: SNV, SNV, SV, CpG, the SNV unphased in c (grey),
# indel, SNV.
text(1156, 722, "d", cls="pl")
LBX = 1294                                                 # right edge of the label column
TX0, TX1 = 1306, 1652                                      # track extent
COLS = [1328 + 51 * i for i in range(7)]
UP = 4                                                     # unphased column
HY1, HY2 = 748, 808


def hap_row(y, hap):
    col = BLUE if hap == 1 else RED
    text(LBX, y + 7, f"Haplotype {hap}", cls="h2", fill=col, anchor="end")
    hedge(TX0, TX1, y, LBLUE if hap == 1 else LRED, 7)
    snp(COLS[0], y, "A" if hap == 1 else "G", col, r=19, fs=21.5)
    snp(COLS[1], y, "T" if hap == 1 else "C", col, r=19, fs=21.5)
    if hap == 1:
        box(COLS[2], y, "SV", BLUE, w=46)
    lollipop(COLS[3], y, hap == 1)
    snp(COLS[UP], y, "C" if hap == 1 else "T", UNPH, r=19, fs=21.5, fill=UNPHF)
    box(COLS[5], y, "A" if hap == 1 else "CA", col, w=46)
    snp(COLS[6], y, "G" if hap == 1 else "A", col, r=19, fs=21.5)

hap_row(HY1, 1)
hap_row(HY2, 2)

# per-variant phasing uncertainty (phasing entropy, PE) reported with the phased output
PEB = 874
text(LBX, PEB - 20, "Phasing", anchor="end"); text(LBX, PEB - 1, "uncertainty", anchor="end")
for i, (x, h) in enumerate(zip(COLS, (6, 8, 7, 5, 26, 9, 6))):
    rect(x - 8, PEB - h, 16, h, ORANGE if i == UP else GREY, rx=1.5,
         stroke="#C97A0E" if i == UP else "none", sw=1.2)
line(TX0, PEB, TX1, PEB, UNPH, 1.4, cap="butt")

text(1178, 912, "Haplotagging reads", cls="h2")
for k, (lab, hap) in enumerate((("Read 1", 1), ("Read 2", 1), ("Read 3", 2), ("Read 4", 2))):
    y = 938 + k * 32
    col, rf = (BLUE, READ_B) if hap == 1 else (RED, READ_R)
    text(LBX, y + 6, lab, anchor="end", fill=col)
    rect(TX0, y - 5, TX1 - TX0, 10, rf, rx=5)
    snp(COLS[0], y, "A" if hap == 1 else "G", col, r=13.5, fs=16.5)
    snp(COLS[1], y, "T" if hap == 1 else "C", col, r=13.5, fs=16.5)
    if hap == 1:
        box(COLS[2], y, "SV", col, w=38, h=24, fs=16.5, sw=2.2)
    lollipop(COLS[3], y, hap == 1, r=6, stem=16, sw=2.8)
    snp(COLS[UP], y, "C" if hap == 1 else "T", UNPH, r=13.5, fs=16.5, fill=UNPHF)
    box(COLS[5], y, "A" if hap == 1 else "CA", col, w=38, h=24, fs=16.5, sw=2.2)
    snp(COLS[6], y, "G" if hap == 1 else "A", col, r=13.5, fs=16.5)

add("</g>")
add("</svg>")

# ============================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(root, "figures", "fig1_overview.svg")
open(dst, "w").write("\n".join(out) + "\n")
print("wrote", dst)
