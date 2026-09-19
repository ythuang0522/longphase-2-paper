#!/usr/bin/env python3
"""Generate the eight supplementary method figures (SVG) for the LongPhase 2 manuscript.

Design rules (Nature figure style)
----------------------------------
* Canvas width 780 px == 160 mm (\\textwidth). 1 px ~= 0.58 pt, so the body face
  (10 px) prints at ~5.8 pt and panel letters (14 px) at ~8 pt -- inside the
  5-7 pt window Nature asks for.
* The figure carries labels, values, equations and short noun phrases only.
  Explanatory sentences belong in the legend, never in the artwork.
* Flat vector geometry, hairlines, white background, no gradients or shadows.
* Colour is semantic and colour-blind safe: haplotype 1 blue, haplotype 2
  vermilion, neutral grey for structure, amber only for flagged / thresholded
  items, green only for an accepted decision.
* Sub- and superscripts are typeset with <tspan>, never with Unicode
  subscript characters: Helvetica has no glyph for most of them and the
  renderer silently substitutes a different face.

All text is written as raw SVG markup, so literal <, > and & must be escaped
in the source strings (they are, as &lt; &gt; &amp;).

Run:      python3 make_supp_figs.py
Convert:  for f in *.svg; do rsvg-convert -f pdf -o ${f%.svg}.pdf $f; done
"""
import math, os, random

# ---------------------------------------------------------------- palette ---
H1     = "#1687C9"   # haplotype 1 (as in Fig. 1)
H1L    = "#DCEAF6"
H1E    = "#6CC8EE"   # haplotype-1 bar / high-confidence edge (Fig. 1)
H2     = "#DC2B23"   # haplotype 2 (as in Fig. 1)
H2L    = "#FAE3DD"
H2E    = "#F0766C"   # haplotype-2 bar (Fig. 1)
INK    = "#16233D"
GREY   = "#6E7C8C"
LGREY  = "#C7D1DB"
VLGREY = "#F1F4F7"
BAND   = "#F7F9FB"
HEADF  = "#E4EAF0"
AMBER  = "#B8860B"
AMBERL = "#FBF0D5"
GREEN  = "#1F7A4D"
GREENL = "#E4F1EA"
TEAL   = "#217F76"   # local branch (never a haplotype)
TEALL  = "#DCEDEB"
PURP   = "#5B4B9E"   # global branch
PURPL  = "#E6E2F2"

MINUS = "−"

STYLE = """
<style>
 text{font-family:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;fill:%s}
 .pl{font-size:14px;font-weight:700}
 .h{font-size:11px;font-weight:600}
 .t{font-size:10px}
 .tb{font-size:10px;font-weight:600}
 .s{font-size:9px;fill:%s}
 .sb{font-size:9px;font-weight:600}
 .n{font-size:8.5px;font-weight:700}
 .m{font-size:10px;font-style:italic}
 .mb{font-size:10px;font-style:italic;font-weight:600}
 .eq{font-size:10.5px}
 .code{font-family:"SF Mono",Menlo,Consolas,"Courier New",monospace;font-size:9px}
</style>
""" % (INK, GREY)


def sub(s):
    """Subscript. baseline-shift does not accumulate, unlike a dy pair."""
    return f'<tspan font-size="72%" baseline-shift="sub">{s}</tspan>'


def sup(s):
    return f'<tspan font-size="72%" baseline-shift="super">{s}</tspan>'


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            f'<title>{title}</title>', STYLE,
            '<defs>'
            f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GREY}"/></marker>'
            f'<marker id="arrd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="arra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>'
            '</defs>',
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>']

    # ---- primitives --------------------------------------------------------
    def add(self, s): self.parts.append(s)

    def text(self, x, y, s, cls="t", anchor="start", fill=None, rot=None):
        f = f' fill="{fill}"' if fill else ""
        r = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{f}{r}>{s}</text>')

    def halo_text(self, x, y, s, cls="sb", anchor="middle", fill=None, pad=3, hw=None):
        """Text on a white plate, for labels that sit on top of lines."""
        w = hw or (len(str(s)) * 5.0 + 2 * pad)
        x0 = {"middle": x - w / 2, "start": x - pad, "end": x - w + pad}[anchor]
        self.rect(x0, y - 9, w, 12, fill="#ffffff", r=1)
        self.text(x, y, s, cls=cls, anchor=anchor, fill=fill)

    def line(self, x1, y1, x2, y2, stroke=GREY, w=1, dash=None, arrow=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#{arrow})"' if arrow else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{d}{a}/>')

    def path(self, d, stroke=GREY, w=1, fill="none", dash=None, arrow=None, op=1):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#{arrow})"' if arrow else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{dd}{a}/>')

    def rect(self, x, y, w, h, fill=VLGREY, stroke="none", sw=0.8, r=2, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')

    def circle(self, cx, cy, r, fill="#fff", stroke=INK, sw=1.2):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # ---- composites --------------------------------------------------------
    def node(self, cx, cy, label, color, r=8, filled=True, sw=None):
        """Allele node. Lettered nodes use the Fig. 1 glyph (white disc, coloured
        ring, coloured bold letter); unlettered nodes are solid dots."""
        if filled and label:
            self.circle(cx, cy, r, fill="#fff", stroke=color, sw=sw or 1.8)
            self.text(cx, cy + 3, label, cls="n", anchor="middle", fill=color)
        elif filled:
            self.circle(cx, cy, r, fill=color, stroke=color, sw=0)
        else:
            self.circle(cx, cy, r, fill="#fff", stroke=color, sw=sw or 1.4)
            if label: self.text(cx, cy + 3, label, cls="n", anchor="middle", fill=color)

    def panel(self, x, y, letter, title=None):
        self.text(x, y, letter, cls="pl")
        if title: self.text(x + 14, y, title, cls="h")

    def rule(self, x1, y, x2, stroke=LGREY, w=0.8):
        self.line(x1, y, x2, y, stroke=stroke, w=w, cap="butt")

    def read(self, x1, x2, y, color=LGREY, w=4):
        self.line(x1, y, x2, y, stroke=color, w=w, cap="round")

    def callout(self, x, y, w, h, fill=VLGREY, accent=None):
        self.rect(x, y, w, h, fill=fill, r=2)
        if accent: self.rect(x, y, 2.2, h, fill=accent, r=0)

    def table(self, x, y, cols, rows, header=None, rowh=16, pad=6,
              cell_cls=None, row_tint=None, text_colors=None):
        total = sum(cols)
        yy = y
        if header:
            self.rect(x, yy, total, rowh, fill=HEADF, r=0)
            cx = x
            for w, htxt in zip(cols, header):
                self.text(cx + pad, yy + rowh - 5, htxt, cls="sb", fill=INK)
                cx += w
            yy += rowh
        for i, row in enumerate(rows):
            tint = (row_tint[i] if row_tint else None) or (BAND if i % 2 else "#ffffff")
            self.rect(x, yy, total, rowh, fill=tint, r=0)
            cx = x
            for j, (w, cell) in enumerate(zip(cols, row)):
                cls = (cell_cls[j] if cell_cls else ("tb" if j == 0 else "t"))
                col = text_colors[i][j] if text_colors else None
                self.text(cx + pad, yy + rowh - 5, cell, cls=cls, fill=col)
                cx += w
            yy += rowh
        self.rect(x, y, total, yy - y, fill="none", stroke=LGREY, sw=0.8, r=0)
        if header:
            self.rule(x, y + rowh, x + total, stroke=LGREY)
        return yy

    def frac(self, x, y, num, den, cls="t", width=None):
        """Stacked fraction, bar centred on (x, y)."""
        w = width or 60
        self.text(x, y - 3.5, num, cls=cls, anchor="middle")
        self.rule(x - w / 2, y, x + w / 2, stroke=INK, w=0.8)
        self.text(x, y + 10.5, den, cls=cls, anchor="middle")
        return w

    def chip(self, x, y, label, w=None, fill=VLGREY, tc=INK):
        w = w or (5.6 * len(label) + 14)
        self.rect(x, y, w, 17, fill=fill, r=8)
        self.text(x + w / 2, y + 12, label, cls="s", anchor="middle", fill=tc)
        return w

    def save(self, name):
        self.add('</svg>')
        with open(name, "w") as f:
            f.write("\n".join(self.parts))
        print("wrote", name)


W = 780


# ============================================================================
# S1  Read-level allele observations and pre-graph filters
# ============================================================================
def fig_s1():
    S = SVG(W, 790, "Read-level allele observations and pre-graph filters")
    XL, XR = 16, 424
    S.line(404, 18, 404, 300, stroke=LGREY, w=0.8)

    # -- a ---------------------------------------------------------------
    S.panel(XL, 24, "a", "Allele observations from one alignment")
    xs = [78, 146, 214, 282, 350]
    y0 = 66
    S.text(56, y0 + 3, "reference", cls="s", anchor="end")
    S.line(66, y0, 384, y0, stroke=INK, w=1.2)
    for x, (k, lab) in zip(xs, [("SNV", "A/G"), ("indel", "T/TAC"), ("SV", "DEL 1.2 kb"),
                                ("5mC", "CpG"), ("SNV", "C/T")]):
        S.line(x, y0 - 4, x, y0 + 4, stroke=INK, w=1.2)
        S.text(x, y0 - 9, k, cls="sb", anchor="middle", fill=INK)
        S.text(x, y0 + 15, lab, cls="s", anchor="middle")

    yr = y0 + 46
    S.text(56, yr + 3, "read", cls="s", anchor="end")
    S.read(66, 384, yr, color=LGREY, w=5)
    for x, (a, src, c) in zip(xs, [("G", "Q 22", H2), ("+AC", "CIGAR I", H1),
                                   ("DEL", "CIGAR D", H1), ("m", "ML 0.93", H2),
                                   ("C", "Q 9", H1)]):
        if len(a) <= 1:
            S.node(x, yr, a, c, r=8)
        else:
            S.rect(x - 15, yr - 8, 30, 16, fill=c, r=8)
            S.text(x, yr + 3, a, cls="n", anchor="middle", fill="#fff")
        S.text(x, yr + 22, src, cls="s", anchor="middle")

    S.text(XL, 158, "observation quality entering the edge weight", cls="sb", fill=INK)
    S.table(XL, 166, [42, 130, 188],
            [("SNV", "aligned base, Phred Q", "1 if both bases ≥ Q12, else 0.1"),
             ("indel", "CIGAR I/D at the site", "1; 0.1 if in a tandem repeat"),
             ("SV", "caller read list", "1 for ALT, 0.1 for REF"),
             ("5mC", "modcall read lists", "1, strand matched")],
            header=("class", "source", "weight"))

    # -- d (left column, bottom) -----------------------------------------
    S.panel(XL, 268, "d", "Tandem-repeat indel flag")
    yd = 296
    S.rect(74, yd - 11, 132, 16, fill=AMBERL, r=2)
    x = 64
    for tok in "G CA CA CA CA CA T".split():
        S.text(x, yd + 3, tok, cls="code", anchor="middle", fill=INK)
        x += 24
    S.text(226, yd + 3, "+CA / " + MINUS + "CA inside the repeat", cls="s")
    S.text(XL, yd + 22, "→ the indel stays in the graph but votes with weight 0.1",
           cls="sb", fill=AMBER)

    # -- b ---------------------------------------------------------------
    S.panel(XR, 24, "b", "Homopolymer SNV filter (nanopore, --ont)")
    yb, x0, dx = 62, 466, 17
    S.text(XR + 12, yb + 3, "ref", cls="s", anchor="end")
    S.rect(x0 + 2 * dx - 8.5, yb - 11, dx * 5, 16, fill=AMBERL, r=2)
    S.rect(x0 + 8 * dx - 8.5, yb - 11, dx * 4, 16, fill=AMBERL, r=2)
    for i, ch in enumerate("G T A A A A A C A A A A T G".split()):
        S.text(x0 + i * dx, yb + 3, ch, cls="code", anchor="middle", fill=INK)
    for i, lab in ((5, "SNV" + sub("1")), (7, "SNV" + sub("2"))):
        S.line(x0 + i * dx, yb + 9, x0 + i * dx, yb + 22, stroke=H2, w=1.4)
        S.text(x0 + i * dx, yb + 33, lab, cls="sb", anchor="middle", fill=H2)
    S.text(XR, yb + 54, "runs ≥ 3 bp, SNVs ≤ 2 bp apart", cls="s")
    S.text(XR, yb + 68, "→ drop SNV" + sub("2") + " from every read", cls="sb", fill=AMBER)

    # -- c ---------------------------------------------------------------
    S.panel(XR, 162, "c", "Overlapping-alignment filter")
    yc = 196
    S.read(470, 604, yc, color=H1, w=4.5)
    S.text(464, yc + 3, "A" + sub("1"), cls="sb", anchor="end", fill=H1)
    S.read(562, 756, yc + 20, color=H1, w=4.5)
    S.text(556, yc + 23, "A" + sub("2"), cls="sb", anchor="end", fill=H1)
    S.rect(562, yc - 8, 42, 36, fill=AMBERL, r=2, op=0.85)
    S.text(583, yc + 44, "overlap", cls="s", anchor="middle", fill=AMBER)
    S.text(XR, yc + 66, "overlap / combined span ≥ 0.2", cls="s")
    S.text(XR, yc + 80, "→ discard the shorter alignment A" + sub("1"),
           cls="sb", fill=AMBER)

    S.rule(XL, 334, W - XL)

    # -- e  copy-number-aware filter: interval detection ---------------------
    S.panel(XL, 358, "e", "Copy-number-aware filter: interval detection")
    x0, x1, yb = 60, 436, 448
    n, dx = 56, (x1 - x0) / 56.0
    rng = random.Random(11)
    front = [rng.choice([0, 1, 1]) for _ in range(n)]
    back = [rng.choice([0, 1, 1]) for _ in range(n)]
    for i in range(15, 40):
        front[i] = max(front[i], 1); back[i] = max(back[i], 1)
    front[14] = 9
    for i in (20, 26, 31):
        front[i] = 3
    back[39], back[40], back[41] = 6, 8, 5
    u = 5.6
    S.rect(x0 + 13.4 * dx, yb - 62, 29 * dx, 110, fill=AMBERL, r=2, op=0.5)
    for i in range(n):
        x = x0 + i * dx
        if front[i]: S.rect(x - 2.2, yb - u * front[i], 4.4, u * front[i], fill=H1, r=0.5)
        if back[i]: S.rect(x - 2.2, yb, 4.4, u * back[i], fill=H2, r=0.5)
    S.line(x0 - 6, yb, x1 + 6, yb, stroke=INK, w=1)
    S.text(XL, yb - 58, "alignment starts", cls="sb", fill=H1)
    S.text(XL, yb - 47, "(front-clipped)", cls="s", fill=H1)
    S.text(XL, yb + 30, "alignment ends", cls="sb", fill=H2)
    S.text(XL, yb + 41, "(back-clipped)", cls="s", fill=H2)
    S.text(x0 + 14 * dx + 7, yb - 50, "step: ≥ 5 front-clips", cls="sb", fill=AMBER)
    S.text(x0 + 27 * dx, yb - 38, "ramps: front-clips &gt; back-clips", cls="sb", anchor="middle", fill=AMBER)
    for i in (20, 26, 31):
        S.line(x0 + i * dx, yb - 30, x0 + i * dx, yb - 23, stroke=AMBER, w=0.9, arrow="arra")
    S.text(x0 + 42 * dx + 4, yb + 34, "pull-down closes", cls="sb", fill=AMBER)
    S.text(x0 + 26 * dx, yb + 60, "candidate interval, extended while excess c &gt; 30; abandoned beyond 200 kb", cls="s",
           anchor="middle", fill=AMBER)
    S.text(x1, yb + 76, "genomic position →", cls="s", anchor="end")
    # state diagram of the scanner
    sx0 = 466
    def state(x, y, w, lab, fill, tc):
        S.rect(x, y, w, 20, fill=fill, r=10)
        S.text(x + w / 2, y + 14, lab, cls="sb", anchor="middle", fill=tc)
    state(sx0, 392, 64, "scanning", VLGREY, INK)
    state(sx0 + 130, 372, 50, "step", H1L, H1)
    state(sx0 + 130, 412, 50, "ramp", AMBERL, AMBER)
    state(sx0 + 228, 392, 60, "interval", GREENL, GREEN)
    S.path(f"M{sx0+64},399 C{sx0+100},399 {sx0+100},382 {sx0+128},382", stroke=GREY, w=1, arrow="arr")
    S.path(f"M{sx0+64},405 C{sx0+100},405 {sx0+100},422 {sx0+128},422", stroke=GREY, w=1, arrow="arr")
    S.text(sx0 + 96, 368, "≥ 5 front-clips", cls="s", anchor="middle")
    S.text(sx0 + 96, 442, "front &gt; back", cls="s", anchor="middle")
    S.path(f"M{sx0+148},372 C{sx0+142},352 {sx0+168},352 {sx0+162},372", stroke=GREY, w=1, arrow="arr")
    S.path(f"M{sx0+148},432 C{sx0+142},452 {sx0+168},452 {sx0+162},432", stroke=GREY, w=1, arrow="arr")
    S.text(sx0 + 155, 346, "extend while c &gt; 30", cls="s", anchor="middle")
    S.text(sx0 + 155, 466, "extend while c &gt; 30", cls="s", anchor="middle")
    S.path(f"M{sx0+180},382 L{sx0+226},398", stroke=GREY, w=1, arrow="arr")
    S.path(f"M{sx0+180},422 L{sx0+226},406", stroke=GREY, w=1, arrow="arr")
    S.text(sx0 + 203, 370, "≥ n/2 back-clips", cls="s", anchor="middle")
    S.text(sx0 + 203, 444, "≥ c/4 back-clips", cls="s", anchor="middle")

    S.rule(XL, 520, W - XL)

    # -- f  copy-number-aware filter: mismatch load ---------------------------
    S.panel(XL, 544, "f", "Copy-number-aware filter: site removal")
    Rm = "R" + sub("m")
    S.text(XL + 6, 578, "MR  =", cls="eq", fill=INK)
    S.frac(170, 574, "mean " + Rm + " (ALT)",
           "mean " + Rm + " (REF) + mean " + Rm + " (ALT)", cls="s", width=156)
    S.text(262, 578, "≥ 0.7  →  remove the site from every read", cls="tb", fill=AMBER)
    S.text(XL, 598, Rm + " = alternate alleles a read carries at other sites inside the interval", cls="s")
    scenes = [(XL, "true heterozygous site", "MR = 0.52", "kept", GREEN,
               [(0, [0, 0, 1, 0, 0]), (0, [0, 0, 0, 0, 1]), (0, [0, 1, 0, 0, 0]),
                (1, [0, 0, 0, 1, 0]), (1, [1, 0, 0, 0, 0]), (1, [0, 0, 1, 0, 0])]),
              (400, "paralogue-specific difference", "MR = 0.87", "removed", AMBER,
               [(0, [0, 0, 1, 0, 0]), (0, [0, 0, 0, 0, 0]), (0, [0, 1, 0, 0, 0]),
                (1, [1, 1, 0, 1, 1]), (1, [1, 0, 1, 1, 1]), (1, [0, 1, 1, 1, 1])])]
    for bx, title, mr, verdict, col, reads in scenes:
        S.text(bx, 622, title, cls="sb", fill=INK)
        for i, (alt, mm) in enumerate(reads):
            y = 638 + i * 15
            c = H2 if alt else H1
            S.text(bx + 22, y + 3, "ALT" if alt else "REF", cls="s", anchor="end", fill=c)
            S.read(bx + 28, bx + 250, y, color=LGREY, w=4)
            S.node(bx + 139, y, "", c, r=5)
            for j, m in enumerate(mm):
                xx = bx + 42 + j * 44
                if abs(xx - (bx + 139)) < 10: continue
                S.line(xx, y - 5, xx, y + 5, stroke=H2 if m else LGREY, w=1.4 if m else 1)
        S.text(bx + 258, 664, mr, cls="tb", fill=col)
        S.text(bx + 258, 678, verdict, cls="sb", fill=col)
    S.text(XL, 736, "grey ticks, reference allele", cls="s")
    S.text(XL + 146, 736, "red ticks, alternate allele at another heterozygous site",
           cls="s", fill=H2)

    # -- pipeline strip ---------------------------------------------------
    S.rule(XL, 752, W - XL)
    S.panel(XL, 772, "g", "Order of operations")
    steps = [("extract", GREENL, GREEN), ("b  homopolymer", VLGREY, INK),
             ("c  overlap", VLGREY, INK), ("d  repeat flag", AMBERL, AMBER),
             ("e–f  copy number", VLGREY, INK), ("graph", GREENL, GREEN)]
    x = 168
    for i, (lab, fill, tc) in enumerate(steps):
        w = S.chip(x, 762, lab, fill=fill, tc=tc)
        if i < len(steps) - 1:
            S.line(x + w + 3, 770.5, x + w + 11, 770.5, stroke=LGREY, w=1, arrow="arr")
        x += w + 14

    S.save("suppfig1_observations.svg")


# ============================================================================
# S2  Pairwise support, weighted voting, phasing entropy and block formation
# ============================================================================
def fig_s2():
    S = SVG(W, 700, "Pairwise allele support, weighted voting and phasing entropy")
    XL, XR = 16, 412
    S.line(392, 18, 392, 684, stroke=LGREY, w=0.8)
    S.rule(XL, 236, W - XL)
    S.rule(XL, 466, W - XL)

    # -- a  allele-pair support ---------------------------------------------
    S.panel(XL, 24, "a", "Allele-pair support between u and v")
    ux, vx = 92, 196
    S.text(ux, 52, "u", cls="mb", anchor="middle", fill=INK)
    S.text(vx, 52, "v", cls="mb", anchor="middle", fill=INK)
    stack = [(9,  "r", "r", H1,   "w" + sub("rr") + " = 9",   None),
             (7,  "a", "a", H2,   "w" + sub("aa") + " = 7",   None),
             (1,  "r", "a", GREY, "w" + sub("ra") + " = 1",   None),
             (1,  "a", "r", GREY, "w" + sub("ar") + " = 0.1", "Q &lt; 12")]
    for k, (n, au, av, col, wlab, note) in enumerate(stack):
        y = 70 + k * 27
        S.text(66, y + 3, f"× {n}", cls="sb", anchor="end", fill=GREY)
        bar = H1E if col == H1 else (H2E if col == H2 else LGREY)
        S.read(72, 216, y, color=bar, w=6)
        S.node(ux, y, au, H1 if au == "r" else H2, r=8)
        if note:                                       # low-quality base: faded glyph
            S.node(vx, y, av, LGREY, r=8, filled=False, sw=1.4)
            S.text(224, y + 3, note, cls="s", fill=AMBER)
        else:
            S.node(vx, y, av, H1 if av == "r" else H2, r=8)
        S.text(272 if note else 230, y + 3, wlab, cls="sb", fill=col)
    S.text(230, 166, "read adds 1 (both bases ≥ Q12) or 0.1", cls="s")
    # P, Q and s
    bx, sc = 84, 15.5
    for k, (lab, val, col) in enumerate([("P = w" + sub("rr") + " + w" + sub("aa"), 16, H1),
                                          ("Q = w" + sub("ra") + " + w" + sub("ar"), 1.1, GREY)]):
        y = 178 + k * 22
        S.text(bx - 6, y + 10, lab, cls="s", anchor="end")
        S.rect(bx, y, val * sc, 13, fill=col, r=1)
        S.text(bx + val * sc + 5, y + 10, f"{val:g}", cls="tb", fill=col)
    S.text(XL, 228, "s = min(P, Q) / max(P, Q) = 0.07", cls="tb", fill=INK)

    # -- b  vote rule ----------------------------------------------------------
    S.panel(XR, 24, "b", "Vote rule for the pair (u, v)")
    ax0, ax1, ay = 446, 746, 92
    def sx(v): return ax0 + (ax1 - ax0) * v
    S.rect(sx(0), ay - 9, sx(0.1) - sx(0), 18, fill=GREENL, r=1)
    S.rect(sx(0.1), ay - 9, sx(0.7) - sx(0.1), 18, fill="#ffffff", stroke=LGREY, sw=0.8, r=0)
    S.rect(sx(0.7), ay - 9, sx(1) - sx(0.7), 18, fill=VLGREY, r=1)
    S.line(sx(0), ay + 9, sx(1), ay + 9, stroke=INK, w=1, cap="butt")
    for v in (0, 0.1, 0.3, 0.7, 1):
        S.line(sx(v), ay + 9, sx(v), ay + 13, stroke=INK, w=1)
        S.text(sx(v), ay + 24, f"{v:g}", cls="s", anchor="middle")
    S.text(sx(0.5), ay + 38, "pair ambiguity s", cls="s", anchor="middle")
    S.text(sx(0.05), ay - 16, "weight 20", cls="sb", anchor="middle", fill=GREEN)
    S.text(sx(0.4), ay + 4, "weight 1", cls="sb", anchor="middle", fill=INK)
    S.text(sx(0.85), ay + 4, "no vote", cls="sb", anchor="middle", fill=GREY)
    S.line(sx(0.3), ay - 9, sx(0.3), ay + 9, stroke=AMBER, w=1.2, dash="2.5,2")
    S.text(sx(0.3), ay - 14, "SNV–5mC: 0.3", cls="s", anchor="middle", fill=AMBER)
    # overrides
    S.node(XR + 8, 150, "", GREEN, r=4)
    S.text(XR + 18, 153, "one pairing &lt; 1 unit, the other ≥ 1 → weight 20, any s", cls="s")
    S.node(XR + 8, 170, "", AMBER, r=4)
    S.text(XR + 18, 173, "voter u is a tandem-repeat indel → weight 0.1", cls="s")
    # vote direction
    for k, (x0, cross, lab) in enumerate([(XR + 20, False, "P → v" + sup("r") + " joins hap(u" + sup("r") + ")"),
                                           (XR + 190, True, "Q → v" + sup("r") + " joins hap(u" + sup("a") + ")")]):
        y1, y2 = 200, 224
        if cross:
            S.line(x0 + 6, y2 - 4, x0 + 44, y1 + 4, stroke=H1E, w=4)
        else:
            S.line(x0 + 6, y1, x0 + 44, y1, stroke=H1E, w=4)
        S.line(x0 + 6, y1 + (0 if cross else 0), x0 + 44, y2 if not cross else y2, stroke=LGREY, w=1) if False else None
        S.node(x0, y1, "r", H1, r=7); S.node(x0, y2, "a", H2, r=7)
        S.node(x0 + 50, y1, "r", H1, r=7); S.node(x0 + 50, y2, "a", H2, r=7)
        S.text(x0 + 64, y1 + 12, lab, cls="s")

    # -- c  multi-neighbour votes ----------------------------------------------
    S.panel(XL, 254, "c", "Weighted votes from up to k = 35 upstream variants")
    xs = [60, 118, 176, 234, 292, 350]
    yt, yb = 336, 404
    hp = [1, 2, 1, 1, 2, None]
    for x, h in zip(xs, hp):
        S.line(x, 322, x, 418, stroke=LGREY, w=0.6, dash="2,3")
        if h is None:
            S.node(x, yt, "r", GREY, r=10, filled=False)
            S.node(x, yb, "a", GREY, r=10, filled=False)
        else:
            S.node(x, yt, "r", H1 if h == 1 else H2, r=10)
            S.node(x, yb, "a", H2 if h == 1 else H1, r=10)
    for i, hap, w in [(0, 1, 20), (1, 1, 1), (2, 1, 1), (4, 1, 0.1), (3, 2, 1)]:
        x, xv = xs[i], xs[5]
        c = H1 if hap == 1 else H2
        yy = yt if hap == 1 else yb
        span = abs(xv - x)
        arc = (yt - 16 - 0.20 * span) if hap == 1 else (yb + 14 + 0.10 * span)
        S.path(f"M{x+10},{yy} C{(x+xv)/2},{arc} {(x+xv)/2},{arc} {xv-10},{yy}",
               stroke=c, w=0.9 + 1.7 * math.log10(w * 10 + 1), op=0.8)
        S.halo_text((x + xv) / 2, arc + (5 if hap == 1 else 11), f"{w:g}",
                    cls="sb", anchor="middle", fill=c, hw=18)
    for x, lab in zip(xs, ["v" + sub(MINUS + "5"), "v" + sub(MINUS + "4"), "v" + sub(MINUS + "3"),
                           "v" + sub(MINUS + "2"), "v" + sub(MINUS + "1"), "v"]):
        S.halo_text(x, 373, lab, cls="m", anchor="middle", fill=INK, hw=22)
    S.text(XL, yt + 3, "hap 1", cls="s", fill=H1)
    S.text(XL, yb + 3, "hap 2", cls="s", fill=H2)
    # vote totals as bars
    for k, (lab, val, col) in enumerate([("h" + sub("1") + "(v)", 22.1, H1), ("h" + sub("2") + "(v)", 1, H2)]):
        y = 428 + k * 16
        S.text(XL + 30, y + 10, lab, cls="s", anchor="end")
        S.rect(XL + 36, y, val * 7.4, 11, fill=col, r=1)
        S.text(XL + 36 + val * 7.4 + 5, y + 9, f"{val:g}", cls="tb", fill=col)
    S.text(XL + 236, 458, "→ v joins haplotype 1", cls="sb", fill=H1)

    # -- d  single-read guard ---------------------------------------------------
    S.panel(XR, 254, "d", "Single-read guard")
    ax0, ax1, ay = XR + 60, XR + 290, 288
    supports = [0.4, 0.6, 0.8, 1.0, 2.6, 4.1, 6.0, 9.4]
    def gx(v): return ax0 + (ax1 - ax0) * v / 10.0
    S.rect(ax0, ay - 6, gx(1) - ax0, len(supports) * 12 + 6, fill=AMBERL, r=1)
    for i, p in enumerate(supports):
        y = ay + i * 12
        c = AMBER if p <= 1 else H1
        S.line(ax0, y, gx(p), y, stroke=c, w=1.2)
        S.circle(gx(p), y, 2.6, fill=c, stroke=c, sw=0)
    yax = ay + len(supports) * 12
    S.line(ax0, yax, ax1, yax, stroke=INK, w=1)
    for v in (0, 1, 5, 10):
        S.line(gx(v), yax, gx(v), yax + 4, stroke=INK, w=1)
        S.text(gx(v), yax + 14, str(v), cls="s", anchor="middle")
    S.text(ax1 + 6, yax + 4, "P + Q", cls="s")
    S.text(XR + 54, ay + 48, "votes to v", cls="s", anchor="end")
    S.text(gx(1) + 4, ay - 12, "4 votes rest on one read (P + Q ≤ 1)", cls="sb", fill=AMBER)
    S.callout(XR, 418, 352, 34, fill=AMBERL, accent=AMBER)
    S.text(XR + 10, 432, "&gt; 3 such votes → recompute h" + sub("1") + ", h" + sub("2"), cls="tb", fill=INK)
    S.text(XR + 10, 446, "from votes with s &lt; 0.2, weight ≥ 1, non-indel voter only", cls="s")

    # -- e  phasing entropy ----------------------------------------------------
    S.panel(XL, 484, "e", "Phasing entropy  PE = − Σ p" + sub("i") + " log" + sub("2") + " p" + sub("i"))
    px0, px1, py0, py1 = 58, 212, 660, 522
    def ex(p): return px0 + (px1 - px0) * p
    def ey(v): return py0 - (py0 - py1) * v
    lo, hi = 0.243, 0.757                       # H(p) >= 0.8
    S.rect(ex(lo), py1, ex(hi) - ex(lo), py0 - py1, fill=AMBERL, r=0, op=0.7)
    pts = []
    for i in range(0, 101):
        p = i / 100
        H = 0 if p in (0, 1) else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        pts.append(f"{ex(p):.1f},{ey(H):.1f}")
    S.path("M" + " L".join(pts), stroke=INK, w=1.4)
    S.line(px0, ey(0.8), px1, ey(0.8), stroke=AMBER, w=1, dash="3,2.5")
    S.text(px1 + 4, ey(0.8) + 3, "0.8", cls="sb", fill=AMBER)
    S.line(px0, py0, px1, py0, stroke=INK, w=1); S.line(px0, py0, px0, py1, stroke=INK, w=1)
    for p in (0, 0.5, 1):
        S.text(ex(p), py0 + 13, f"{p:g}", cls="s", anchor="middle")
    for v in (0, 1):
        S.text(px0 - 5, ey(v) + 3, f"{v}", cls="s", anchor="end")
    S.text((px0 + px1) / 2, py0 + 26, "p" + sub("1") + " = h" + sub("1") + " / (h" + sub("1") + " + h" + sub("2") + ")", cls="s", anchor="middle")
    S.text(px0 - 14, (py0 + py1) / 2, "PE", cls="s", anchor="middle", rot=-90)
    S.text(ex(0.5), py1 - 8, "GNN window (Suppl. Fig. 4)", cls="s", anchor="middle", fill=AMBER)
    for a_, b_ in ((22.1, 1), (3, 1), (4, 3), (5, 5)):
        p = a_ / (a_ + b_)
        H = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        S.circle(ex(p), ey(H), 3.2, fill=(AMBER if H >= 0.8 else INK), stroke="#fff", sw=1)
    S.text(292, 522, "h" + sub("1") + " : h" + sub("2"), cls="s", anchor="end")
    S.text(384, 522, "PE", cls="s", anchor="end")
    for i, (lab, a, b) in enumerate([("22.1 : 1", 22.1, 1), ("3 : 1", 3, 1), ("4 : 3", 4, 3), ("5 : 5", 5, 5)]):
        y = 534 + i * 26
        tot = a + b
        p1, p2 = a / tot, b / tot
        pe = -(p1 * math.log2(p1) + p2 * math.log2(p2))
        if pe >= 0.8:
            S.rect(250, y - 5, 138, 22, fill=AMBERL, r=2, op=0.7)
        S.text(292, y + 10, lab, cls="s", anchor="end")
        S.rect(298, y, 52 * p1, 12, fill=H1, r=1)
        S.rect(298 + 52 * p1, y, 52 * p2, 12, fill=H2, r=1)
        S.text(384, y + 10, f"{pe:.2f}", cls="sb", anchor="end", fill=AMBER if pe >= 0.8 else INK)

    # -- f  block formation -----------------------------------------------------
    S.panel(XR, 484, "f", "Block formation")
    cols = [436 + i * 26 for i in range(5)] + [566] + [622 + i * 26 for i in range(4)] + [738]
    yt, yb = 548, 586
    kinds = ["b"] * 5 + ["skip"] + ["tie", "b", "b", "b"] + ["single"]
    for i, (x, k) in enumerate(zip(cols, kinds)):
        nxt = cols[i + 1] if i + 1 < len(cols) else None
        if (k == "b" and i + 1 < len(cols) and kinds[i + 1] == "b") or k == "tie":
            S.line(x, yt, nxt, yt, stroke=H1E, w=5, cap="butt")
            S.line(x, yb, nxt, yb, stroke=H2E, w=5, cap="butt")
    for x, k in zip(cols, kinds):
        if k == "b":
            S.node(x, yt, "", H1, r=6); S.node(x, yb, "", H2, r=6)
        elif k == "tie":
            S.node(x, yt, "", AMBER, r=6, filled=False); S.node(x, yb, "", AMBER, r=6, filled=False)
        else:
            S.node(x, yt, "", GREY, r=6, filled=False); S.node(x, yb, "", GREY, r=6, filled=False)
    # the > 300 kb gap
    S.line(574, (yt + yb) / 2, 614, (yt + yb) / 2, stroke=GREY, w=1, dash="2,3")
    S.text(594, (yt + yb) / 2 + 13, "&gt; 300 kb", cls="s", anchor="middle", fill=GREY)
    S.text(566, yb + 22, "skipped", cls="s", anchor="middle", fill=GREY)
    S.text(622, yt - 14, "tie", cls="sb", anchor="middle", fill=AMBER)
    S.text(738, yt - 14, "singleton", cls="s", anchor="middle", fill=GREY)
    S.text(738, yb + 22, "dropped", cls="s", anchor="middle", fill=GREY)
    for x1, x2, lab in [(cols[0], cols[4], "PS 1"), (cols[6], cols[9], "PS 2")]:
        S.line(x1 - 8, yb + 14, x2 + 8, yb + 14, stroke=INK, w=1.6, cap="butt")
        S.text((x1 + x2) / 2, yb + 27, lab, cls="sb", anchor="middle", fill=INK)
    S.text(XR + 6, yt + 3, "hap 1", cls="s", anchor="end", fill=H1)
    S.text(XR + 6, yb + 3, "hap 2", cls="s", anchor="end", fill=H2)
    S.text(XR, 646, "PS = position of the first variant of the block", cls="s")

    S.save("suppfig2_voting.svg")


# ============================================================================
# S3  Read-based correction
# ============================================================================
def fig_s3():
    S = SVG(W, 426, "Read-based correction")
    XL = 16

    # -- a ---------------------------------------------------------------
    S.panel(XL, 24, "a", "Step 1: read assignment to haplotypes")
    xs = [110 + i * 62 for i in range(6)]
    for i, x in enumerate(xs):
        S.text(x, 52, "v" + sub(str(i + 1)), cls="m", anchor="middle", fill=INK)
    reads = [([1, 1, 1, 1, None, 1], "hap 1", "5/5", H1),
             ([2, 2, None, 2, 2, 2], "hap 2", "5/5", H2),
             ([1, 1, 2, 1, 1, None], "hap 1", "4/5 = 0.80", H1),
             ([1, 2, 2, 1, None, None], "untagged", "2/4 = 0.50", GREY),
             ([None, None, 2, None, None, None], "untagged", "&lt; 2 alleles", GREY)]
    for i, (al, lab, frac, c) in enumerate(reads):
        y = 74 + i * 26
        S.text(XL + 44, y + 3, f"read {i+1}", cls="s", anchor="end")
        S.read(XL + 52, 500, y, color=LGREY if c == GREY else (H1L if c == H1 else H2L), w=5)
        for x, a in zip(xs, al):
            if a is None: continue
            S.node(x, y, "r" if a == 1 else "a", H1 if a == 1 else H2, r=8)
        S.text(512, y + 3, lab, cls="sb", fill=c)
        S.text(568, y + 3, frac, cls="s")
    n1, n2 = "n" + sub("1"), "n" + sub("2")
    S.callout(XL, 208, 660, 42, fill=VLGREY, accent=INK)
    S.text(XL + 12, 226, "tagged if  max(" + n1 + "," + n2 + ") / (" + n1 + " + " + n2
           + ")  &gt; 0.65   and   weighted evidence &gt; 1", cls="tb", fill=INK)
    S.text(XL + 12, 242, "allele weights: SNV 1, SV 1, indel 0.1, 5mC 0   "
           "(so ≥ 2 SNV/SV alleles are needed)", cls="s")

    S.rule(XL, 264, W - XL)

    # -- b ---------------------------------------------------------------
    S.panel(XL, 288, "b", "Step 2: phase re-derivation from tagged reads")
    # evidence at the variant from the tagged reads (read, its haplotype, its allele)
    cases = [(XL,  "v" + sub("3"), [("read 1", 1, "r"), ("read 2", 2, "a"), ("read 3", 1, "a")],
              2, 1, AMBER, "unphased, GT 0/1"),
             (396, "v" + sub("1"), [("read 1", 1, "r"), ("read 2", 2, "a"), ("read 3", 1, "r")],
              3, 0, H1, "phased, GT 0|1")]
    for bx, v, reads, a1, a2, col, verdict in cases:
        S.text(bx, 316, "variant " + v, cls="tb", fill=INK)
        for k, (lab, hap, al) in enumerate(reads):
            y = 336 + k * 20
            hc = H1 if hap == 1 else H2
            S.text(bx + 40, y + 3, lab, cls="s", anchor="end")
            S.read(bx + 46, bx + 150, y, color=(H1E if hap == 1 else H2E), w=5)
            S.node(bx + 98, y, al, H1 if al == "r" else H2, r=7)
            S.text(bx + 156, y + 3, f"hap {hap}", cls="s", fill=hc)
            consistent = (hap == 1 and al == "r") or (hap == 2 and al == "a")
            S.text(bx + 196, y + 3, "consistent" if consistent else "conflicting",
                   cls="sb", fill=(GREEN if consistent else H2))
        # rho bar against the 0.75 threshold
        rho = max(a1, a2) / (a1 + a2)
        rx, by = bx + 262, 336
        S.text(rx, by + 3, "n" + sub("1") + " = " + str(a1) + ",  n" + sub("2") + " = " + str(a2), cls="s")
        S.text(rx, by + 24, "ρ = max / sum", cls="s")
        S.rect(rx, by + 32, 84, 9, fill=VLGREY, stroke=LGREY, sw=0.6, r=1)
        S.rect(rx, by + 32, 84 * rho, 9, fill=col, r=1)
        S.line(rx + 84 * 0.75, by + 28, rx + 84 * 0.75, by + 45, stroke=INK, w=1, dash="2,2")
        S.text(rx + 84 * 0.75, by + 55, "0.75", cls="s", anchor="middle")
        S.text(rx + 90, by + 40, f"{rho:.2f}", cls="tb", fill=col)
        S.text(rx, by + 72, "→ " + verdict, cls="sb", fill=col)

    S.save("suppfig3_read_correction.svg")


# ============================================================================
# S4  GNN module overview
# ============================================================================
def fig_s4():
    S = SVG(W, 356, "Overview of the graph neural network correction module")
    AX, BX, CX, DX = 16, 186, 414, 586

    def stage_arrow(x, y=186):
        S.path(f"M{x},{y-7} L{x+9},{y} L{x},{y+7}", stroke=LGREY, w=1.6)

    stage_arrow(174); stage_arrow(402); stage_arrow(574)

    # ---------------------------------------------------------------- a ----
    S.panel(AX, 24, "a", "Initial phasing")
    S.text(AX, 50, "long reads", cls="sb", fill=INK)
    spans = [(22, 150), (34, 166), (26, 158), (40, 170), (22, 140)]
    for i, (rx0, rx1) in enumerate(spans):
        y = 62 + i * 11
        S.read(rx0, rx1, y, color=LGREY, w=4.5)
        for j, px in enumerate((52, 90, 128)):
            if rx0 - 4 <= px <= rx1 + 4:
                c = H1 if (i + j) % 3 else H2
                S.rect(px - 2, y - 4, 4, 8, fill=c, r=0.5)
    S.line(93, 122, 93, 132, stroke=GREY, w=1, arrow="arr")
    S.text(93, 143, "variant calling", cls="s", anchor="middle")
    S.rect(36, 150, 114, 21, fill=H1L, stroke=H1, sw=0.9, r=4)
    S.text(93, 164, "LongPhase", cls="tb", anchor="middle", fill=H1)
    S.line(93, 173, 93, 185, stroke=GREY, w=1, arrow="arr")

    xs = [30, 61, 92, 123, 154]
    yt, yb = 204, 226
    S.rect(xs[2] - 11, yt - 12, 22, (yb - yt) + 24, fill=AMBERL, r=3)
    for i, x in enumerate(xs):
        if i < 4:
            S.line(x + 8, yt, xs[i + 1] - 8, yt, stroke=H1, w=1.4)
            S.line(x + 8, yb, xs[i + 1] - 8, yb, stroke=H2, w=1.4)
    for x in xs:
        S.node(x, yt, "", H1, r=7)
        S.node(x, yb, "", H2, r=7)
    S.text(AX, 250, "initial phase assignment", cls="s")
    S.line(93, 258, 93, 270, stroke=GREY, w=1, arrow="arr")

    wx0, wn = 24, 41
    wdx = (168 - wx0) / (wn - 1.0)
    S.rect(wx0 + 20 * wdx - 4, 279, 8, 26, fill=AMBER, r=2, op=0.16)
    for r, c in ((288, H1), (299, H2)):
        for k in range(wn):
            S.circle(wx0 + k * wdx, r, 1.5, fill=AMBER if k == 20 else c,
                     stroke="none", sw=0)
    S.text(wx0, 318, "\u221220", cls="s", anchor="middle")
    S.text(168, 318, "+20", cls="s", anchor="middle")
    S.text(wx0 + 20 * wdx, 318, "PE \u2265 0.8", cls="sb", anchor="middle", fill=AMBER)
    S.text(AX, 336, "variant window around the trigger", cls="s")

    # ---------------------------------------------------------------- b ----
    S.panel(BX, 24, "b", "Graph representation")
    S.text(BX, 50, "node features", cls="sb", fill=INK)
    S.chip(BX + 76, 39, "31 per allele node", fill=VLGREY)
    groups = [("phasing evidence", 16, AMBER), ("genomic context", 6, GREEN),
              ("graph structure", 5, H1), ("variant class", 4, GREY)]
    for gi, (name, k, col) in enumerate(groups):
        y = 60 + gi * 16
        S.text(BX + 2, y + 7, name, cls="s")
        for j in range(k):
            S.rect(BX + 90 + j * 7, y, 5, 9, fill=col, r=0.8,
                   op=0.35 + 0.65 * (j + 1) / k)
        S.text(BX + 208, y + 7, str(k), cls="sb", fill=col)

    gy1, gy2 = 168, 212
    gxs = [BX + 12 + i * 18.6 for i in range(12)]
    grng = random.Random(3)
    for i in range(12):
        for j in range(i + 1, min(12, i + 4)):
            if grng.random() < 0.7:
                xi, xj = gxs[i], gxs[j]
                S.path(f"M{xi+4},{gy1-4} Q{(xi+xj)/2},{gy1-14-(j-i)*5} {xj-4},{gy1-4}",
                       stroke=H1, w=0.7, op=0.45)
                S.path(f"M{xi+4},{gy2+4} Q{(xi+xj)/2},{gy2+14+(j-i)*5} {xj-4},{gy2+4}",
                       stroke=H2, w=0.7, op=0.45)
    S.line(gxs[4] + 4, gy1 + 4, gxs[6] - 4, gy2 - 4, stroke=GREY, w=0.8, dash="2.5,2")
    for i, x in enumerate(gxs):
        cen = (i == 5)
        S.node(x, gy1, "", AMBER if cen else H1, r=5.5)
        S.node(x, gy2, "", AMBER if cen else H2, r=5.5)
    S.text(BX, 246, "allele graph of the window", cls="s")
    S.text(BX + 212, 246, "amber, trigger variant", cls="s", anchor="end", fill=AMBER)

    S.text(BX, 272, "edge features", cls="sb", fill=INK)
    S.chip(BX + 72, 261, "6 per edge", fill=VLGREY)
    # one glyph per feature group: what the weight is built from, how the
    # separation is measured, and whether the pair straddles a phase set
    g1, g2, g3 = BX + 30, BX + 104, BX + 180

    # vote weight, support -- reads carrying both alleles pool into one edge
    for k, (rx0, rx1) in enumerate(((-28, 24), (-24, 28), (-26, 22))):
        ry = 286 + k * 5
        S.read(g1 + rx0, g1 + rx1, ry, color=LGREY, w=2.6)
        for dx in (-20, 20):
            S.circle(g1 + dx, ry, 1.7, fill=H1, stroke=H1, sw=0)
    S.line(g1, 300, g1, 309, stroke=LGREY, w=0.8, arrow="arr")
    S.line(g1 - 15, 316, g1 + 15, 316, stroke=H1, w=4.2)
    S.node(g1 - 20, 316, "", H1, r=5)
    S.node(g1 + 20, 316, "", H1, r=5)

    # genomic distance -- dimension line between the two variant positions
    S.line(g2 - 17, 296, g2 + 17, 296, stroke=H1, w=1.6)
    S.node(g2 - 22, 296, "", H1, r=5)
    S.node(g2 + 22, 296, "", H1, r=5)
    for dx in (-22, 22):
        S.line(g2 + dx, 303, g2 + dx, 317, stroke=LGREY, w=0.8, cap="butt")
    for dx in (-21, 21):
        S.line(g2, 312, g2 + dx, 312, stroke=GREY, w=0.8, arrow="arr")

    # phase-set relation -- the pair straddles a phase-set boundary
    S.text(g3 - 18, 286, "PS i", cls="s", anchor="middle")
    S.text(g3 + 18, 286, "PS j", cls="s", anchor="middle")
    S.line(g3 - 13, 302, g3 + 13, 302, stroke=H1, w=1.6)
    S.node(g3 - 18, 302, "", H1, r=5)
    S.node(g3 + 18, 302, "", H1, r=5)
    S.line(g3, 292, g3, 316, stroke=GREY, w=1, dash="2.5,2")

    for gx, l1, l2 in ((g1, "vote weight,", "support"), (g2, "genomic", "distance"),
                       (g3, "phase-set", "relation")):
        S.text(gx, 332, l1, cls="s", anchor="middle")
        S.text(gx, 342, l2, cls="s", anchor="middle")

    # ---------------------------------------------------------------- c ----
    S.panel(CX, 24, "c", "Graph neural network")
    for k in (8, 4):
        S.rect(CX + k, 50 - k, 152, 228, fill="#ffffff", stroke=LGREY, sw=0.8, r=4)
    S.rect(CX, 50, 152, 228, fill="#ffffff", stroke=INK, sw=1, r=4)
    S.text(CX + 10, 66, "layer \u2113", cls="sb", fill=INK)
    S.text(CX + 142, 66, "\u00d7 4", cls="sb", anchor="end", fill=INK)
    S.line(CX + 76, 38, CX + 76, 48, stroke=GREY, w=1, arrow="arr")

    lcx, gcx, icy = CX + 42, CX + 110, 100
    ring = [(math.cos(math.radians(d)) * 15, math.sin(math.radians(d)) * 15)
            for d in (90, 162, 234, 306, 18)]
    for cx_, coll in ((lcx, TEALL), (gcx, PURPL)):
        S.circle(cx_, icy, 23, fill=coll, stroke="none", sw=0)
    for dx, dy in ring:
        S.line(lcx + dx * 0.74, icy - dy * 0.74, lcx + dx * 0.34, icy - dy * 0.34,
               stroke=TEAL, w=0.9, arrow="arr")
        S.circle(lcx + dx, icy - dy, 3.2, fill="#ffffff", stroke=TEAL, sw=1)
    S.circle(lcx, icy, 4.4, fill=TEAL, stroke=TEAL, sw=0)
    for i in range(5):
        for j in range(i + 1, 5):
            S.line(gcx + ring[i][0], icy - ring[i][1],
                   gcx + ring[j][0], icy - ring[j][1], stroke=PURP, w=0.6)
    for dx, dy in ring:
        S.circle(gcx + dx, icy - dy, 3.2, fill=PURP, stroke=PURP, sw=0)
    S.text(lcx, icy + 36, "local", cls="sb", anchor="middle", fill=TEAL)
    S.text(lcx, icy + 47, "message passing", cls="s", anchor="middle")
    S.text(gcx, icy + 36, "global", cls="sb", anchor="middle", fill=PURP)
    S.text(gcx, icy + 47, "self-attention", cls="s", anchor="middle")

    fx, fy = CX + 76, 182
    S.path(f"M{lcx},{icy+52} L{lcx},{fy} L{fx-9},{fy}", stroke=TEAL, w=1, arrow="arr")
    S.path(f"M{gcx},{icy+52} L{gcx},{fy} L{fx+9},{fy}", stroke=PURP, w=1, arrow="arr")
    S.path(f"M{CX+12},80 L{CX+12},{fy} L{fx-9},{fy}", stroke=LGREY, w=0.9,
           dash="2.5,2", arrow="arr")
    S.circle(fx, fy, 7, fill="#ffffff", stroke=INK, sw=1)
    S.text(fx, fy + 3.4, "+", cls="tb", anchor="middle", fill=INK)
    S.text(fx, fy - 16, "fusion", cls="sb", anchor="middle", fill=INK)

    S.line(fx, fy + 7, fx, 204, stroke=GREY, w=1, arrow="arr")
    S.rect(CX + 32, 206, 88, 21, fill=VLGREY, stroke=LGREY, sw=0.9, r=3)
    S.text(fx, 220, "feed-forward", cls="tb", anchor="middle", fill=INK)
    S.line(fx, 227, fx, 238, stroke=GREY, w=1, arrow="arr")
    S.path(f"M{CX+140},{fy+14} L{CX+140},246 L{fx+9},246", stroke=LGREY, w=0.9,
           dash="2.5,2", arrow="arr")
    S.circle(fx, 246, 7, fill="#ffffff", stroke=INK, sw=1)
    S.text(fx, 249.4, "+", cls="tb", anchor="middle", fill=INK)
    S.line(fx, 253, fx, 288, stroke=GREY, w=1, arrow="arr")
    S.rect(CX + 20, 290, 112, 20, fill=AMBERL, stroke=AMBER, sw=0.9, r=3)
    S.text(fx, 303, "P(misphased)", cls="tb", anchor="middle", fill=INK)
    S.text(CX, 328, "classifier head; the two allele", cls="s")
    S.text(CX, 340, "nodes of a variant are averaged", cls="s")


    # ---------------------------------------------------------------- d ----
    S.panel(DX, 24, "d", "Refined phasing")
    ox0, on = DX + 32, 41
    odx = (758 - ox0) / (on - 1.0)
    S.text(DX, 50, "original window", cls="sb", fill=INK)
    S.rect(ox0 + 20 * odx - 4, 57, 8, 26, fill=AMBER, r=2, op=0.16)
    for r, c in ((64, H1), (75, H2)):
        for k in range(on):
            S.circle(ox0 + k * odx, r, 1.6, fill=AMBER if k == 20 else c,
                     stroke="none", sw=0)
    S.text(DX + 84, 100, "+", cls="pl", anchor="middle", fill=GREY)

    S.text(DX, 122, "predicted error probability", cls="sb", fill=INK)
    base, hmax = 162, 30
    S.rect(ox0 + 20 * odx - 4, base - hmax, 8, hmax, fill=AMBER, r=2, op=0.16)
    prng = random.Random(21)
    probs = [min(0.27, 0.02 + prng.random() * 0.22) for _ in range(on)]
    probs[20], probs[19], probs[21] = 0.62, 0.21, 0.24
    for k, pr in enumerate(probs):
        h = hmax * pr
        S.rect(ox0 + k * odx - 1.3, base - h, 2.6, h,
               fill=AMBER if pr >= 0.30 else GREY, r=0.4)
    S.line(ox0 - 4, base, 760, base, stroke=INK, w=0.9)
    thr = base - hmax * 0.30
    S.line(ox0 - 4, thr, 760, thr, stroke=AMBER, w=0.9, dash="2.5,2")
    S.text(760, thr - 5, "cutoff", cls="sb", anchor="end", fill=AMBER)
    S.text(DX + 84, 188, "=", cls="pl", anchor="middle", fill=GREY)

    S.text(DX, 210, "updated window", cls="sb", fill=INK)
    ry1, ry2 = 228, 239
    for bx in (ox0 - 5, ox0 + 20.8 * odx):
        S.rect(bx, ry1 - 8, 19.4 * odx, 27, fill="none", stroke=GREY, sw=0.8,
               dash="3,2.5", r=3)
    for r, c in ((ry1, H1), (ry2, H2)):
        for k in range(on):
            if k == 20:
                S.circle(ox0 + k * odx, r, 2.2, fill="#ffffff", stroke=GREY, sw=1)
            else:
                S.circle(ox0 + k * odx, r, 1.6, fill=c, stroke="none", sw=0)
    S.line(ox0 + 20 * odx, 250, ox0 + 20 * odx, 258, stroke=GREY, w=0.8)
    S.text(ox0 + 20 * odx, 268, "unphased", cls="sb", anchor="middle", fill=GREY)
    S.text(ox0 + 9 * odx, 284, "PS 1001", cls="s", anchor="middle")
    S.text(ox0 + 31 * odx, 284, "PS 1436", cls="s", anchor="middle")
    S.callout(DX, 296, 174, 34, fill=VLGREY, accent=AMBER)
    S.text(DX + 10, 310, "GT 0/1, PS dropped", cls="tb", fill=INK)
    S.text(DX + 10, 323, "genotype preserved, block split", cls="s")

    S.save("suppfig4_gnn_overview.svg")


# ============================================================================
# S5  GNN window construction
# ============================================================================
def fig_s5():
    S = SVG(W, 840, "Window construction and phase-set update")
    XL = 16

    # -- a ---------------------------------------------------------------
    S.panel(XL, 24, "a", "Window around a trigger variant (PE ≥ 0.8)")
    n, x0, dx = 13, 76, 52
    yt, yb = 132, 196
    center = 6
    S.rect(x0 + (center - 2.6) * dx, 84, 5.2 * dx, 156, fill="none",
           stroke=AMBER, sw=1, dash="3,2.5", r=3)
    S.rect(x0 + center * dx - 15, 90, 30, 144, fill=AMBERL, r=2, op=0.7)
    rng = random.Random(7)
    for i in range(n):
        for j in range(i + 1, min(n, i + 4)):
            if rng.random() < 0.72:
                xi, xj = x0 + i * dx, x0 + j * dx
                S.path(f"M{xi+6},{yt-6} Q{(xi+xj)/2},{yt-26-(j-i)*7} {xj-6},{yt-6}",
                       stroke=H1, w=0.8, op=0.45)
                S.path(f"M{xi+6},{yb+6} Q{(xi+xj)/2},{yb+26+(j-i)*7} {xj-6},{yb+6}",
                       stroke=H2, w=0.8, op=0.45)
    for i in range(n):
        x = x0 + i * dx
        S.node(x, yt, "r", H1, r=9)
        S.node(x, yb, "a", H2, r=9)
        if i == center:
            lab = "c"
        elif i == 0:
            lab = MINUS + "20"
        elif i == n - 1:
            lab = "+20"
        elif abs(i - center) <= 2:
            lab = ("+" if i > center else MINUS) + str(abs(i - center))
        else:
            lab = ""
        if lab:
            S.text(x, 80, lab, cls="s", anchor="middle", fill=AMBER if i == center else GREY)
    S.line(x0 + 5 * dx + 7, yt + 6, x0 + 7 * dx - 7, yb - 6, stroke=GREY, w=1, dash="2.5,2")
    S.text(x0 - 22, yt + 3, "…", cls="t", anchor="middle")
    S.text(x0 + n * dx - 30, yt + 3, "…", cls="t", anchor="middle")
    S.text(x0 + center * dx, 254, "centre zone, predictions kept",
           cls="sb", anchor="middle", fill=AMBER)
    kx = XL
    for c, lab, dash in [(H1, "hap-1 allele edges", None), (H2, "hap-2 allele edges", None),
                         (GREY, "cross-haplotype edge", "2.5,2")]:
        S.line(kx, 278, kx + 16, 278, stroke=c, w=1.4, dash=dash)
        S.text(kx + 21, 281, lab, cls="s")
        kx += 26 + 5.4 * len(lab)
    S.text(kx + 4, 281, "≤ 41 variants, ≤ 82 allele nodes", cls="s", fill=INK)

    S.rule(XL, 300, W - XL)

    # -- b ---------------------------------------------------------------
    S.panel(XL, 324, "b", "Bridge-vertex feature")
    cy = 362
    left = [(XL + 30, cy - 14), (XL + 30, cy + 14), (XL + 62, cy)]
    right = [(XL + 160, cy - 14), (XL + 160, cy + 14), (XL + 128, cy)]
    mid = (XL + 95, cy)
    for tri in (left, right):
        for i in range(3):
            S.line(*tri[i], *tri[(i + 1) % 3], stroke=LGREY, w=1.2)
    S.line(*left[2], *mid, stroke=AMBER, w=1.2)
    S.line(*mid, *right[2], stroke=AMBER, w=1.2)
    for px, py in left + right:
        S.circle(px, py, 5.5, fill="#fff", stroke=GREY, sw=1.2)
    S.circle(mid[0], mid[1], 5.5, fill=AMBER, stroke=AMBER, sw=0)
    S.text(XL + 190, cy - 4, "removing this variant disconnects the window",
           cls="s")
    S.text(XL + 190, cy + 10, "→ is_bridge = 1", cls="sb", fill=AMBER)

    # -- c ---------------------------------------------------------------
    S.panel(452, 324, "c", "Centre-zone mask")
    cx0, cx1, cy0 = 480, 700, 356
    S.rect(cx0 + (cx1 - cx0) * 0.25, cy0 - 8, (cx1 - cx0) * 0.5, 16, fill=AMBERL, r=2)
    S.line(cx0, cy0, cx1, cy0, stroke=INK, w=1)
    for f, lab in ((0, MINUS + "1"), (0.25, MINUS + "0.5"), (0.5, "c"), (0.75, "+0.5"), (1, "+1")):
        xx = cx0 + (cx1 - cx0) * f
        S.line(xx, cy0 - 4, xx, cy0 + 4, stroke=INK, w=1)
        S.text(xx, cy0 + 17, lab, cls="s", anchor="middle", fill=(AMBER if lab == "c" else GREY))
    S.node(cx0 + (cx1 - cx0) * 0.5, cy0, "", AMBER, r=4)
    S.text(cx0 + (cx1 - cx0) * 0.5, cy0 - 14, "predictions kept", cls="sb", anchor="middle", fill=AMBER)
    S.text(cx1 + 8, cy0 + 3, "r", cls="m", fill=INK)
    S.text(466, 392, "r = |pos − pos" + sub("c") + "| / max offset;  kept if r ≤ min(1, 10 / round(20 · r" + sub("max") + ")) = 0.5",
           cls="s")

    # -- d ---------------------------------------------------------------
    S.rule(XL, 410, W - XL)
    S.panel(XL, 434, "d", "Exported phasing graph (DOT)")
    S.rect(XL, 442, 400, 24, fill=VLGREY, r=2)
    S.text(XL + 10, 458, "1001.1 -&gt; 1543.1 [label=16.0]     1001.2 -&gt; 1543.2 [label=1.1]", cls="code")
    S.text(436, 458, "position.allele → position.allele,  label = vote weight cast at the source", cls="s")

    S.rule(XL, 486, W - XL)

    # -- e  before correction ---------------------------------------------
    xs = [66 + i * 58 for i in range(10)]
    flagged = 5
    S.panel(XL, 510, "e", "Before correction: one phase set")
    yt, yb = 564, 610
    for i, x in enumerate(xs):
        if i < 9:
            S.line(x, yt, xs[i + 1], yt, stroke=H1E, w=5, cap="butt")
            S.line(x, yb, xs[i + 1], yb, stroke=H2E, w=5, cap="butt")
        if i in (3, 7):
            S.path(f"M{x+6},{yt-7} Q{(x+xs[i+2])/2},{yt-32} {xs[i+2]-6},{yt-7}",
                   stroke=H1, w=0.9, op=0.55)
    for i, x in enumerate(xs):
        S.node(x, yt, "r", H1, r=9)
        S.node(x, yb, "a", H2, r=9)
    S.rect(xs[flagged] - 16, yt - 18, 32, (yb - yt) + 36, fill="none",
           stroke=AMBER, sw=1.4, r=3)
    S.text(xs[flagged], yb + 36, "P(error) = 0.62 ≥ 0.30", cls="sb",
           anchor="middle", fill=AMBER)
    S.text(XL, yb + 36, "PS 1001, GT 0|1 / 1|0", cls="s")

    S.rule(XL, 672, W - XL)

    # -- f  after correction ------------------------------------------------
    S.panel(XL, 696, "f", "After correction: variant unphased, phase set split")
    yt2, yb2 = 748, 790
    S.rect(xs[0] - 18, yt2 - 18, xs[4] - xs[0] + 36, (yb2 - yt2) + 36, fill="none",
           stroke=H1, sw=0.9, dash="3,2.5", r=3)
    S.rect(xs[6] - 18, yt2 - 18, xs[9] - xs[6] + 36, (yb2 - yt2) + 36, fill="none",
           stroke=H1, sw=0.9, dash="3,2.5", r=3)
    for i, x in enumerate(xs):
        if i < 9 and flagged not in (i, i + 1):
            S.line(x, yt2, xs[i + 1], yt2, stroke=H1E, w=5, cap="butt")
            S.line(x, yb2, xs[i + 1], yb2, stroke=H2E, w=5, cap="butt")
    S.path(f"M{xs[3]+6},{yt2-7} Q{(xs[3]+xs[5])/2},{yt2-30} {xs[5]-6},{yt2-7}",
           stroke=LGREY, w=0.9, dash="2.5,2")
    for i, x in enumerate(xs):
        if i == flagged:
            S.node(x, yt2, "r", GREY, r=9, filled=False)
            S.node(x, yb2, "a", GREY, r=9, filled=False)
        else:
            S.node(x, yt2, "r", H1, r=9)
            S.node(x, yb2, "a", H2, r=9)
    S.text(xs[flagged], yt2 - 28, "GT 0/1, PS removed", cls="sb", anchor="middle", fill=GREY)
    S.text((xs[0] + xs[4]) / 2, yb2 + 32, "PS 1001, largest component", cls="s",
           anchor="middle")
    S.text((xs[6] + xs[9]) / 2, yb2 + 32, "PS 1436, position of the first variant",
           cls="s", anchor="middle")
    S.line(646, yt2 - 8, 662, yt2 - 8, stroke=LGREY, w=1.2, dash="2.5,2")
    S.text(667, yt2 - 5, "edge no longer counted", cls="s")
    S.text(646, yt2 + 14, "genotypes are never flipped", cls="sb", fill=INK)

    S.save("suppfig5_gnn_window.svg")


# ============================================================================
# S6  GNN architecture
# ============================================================================
def fig_s6():
    S = SVG(W, 440, "Graph neural network architecture")

    def box(x, y, w, h, label, sub_=None, fill=VLGREY, stroke=LGREY, tc=INK):
        S.rect(x, y, w, h, fill=fill, stroke=stroke, sw=0.9, r=3)
        S.text(x + w / 2, y + h / 2 + (3.5 if not sub_ else -1.5), label, cls="tb",
               anchor="middle", fill=tc)
        if sub_:
            S.text(x + w / 2, y + h / 2 + 11, sub_, cls="s", anchor="middle")

    box(16, 44, 150, 32, "node features", "N × 31", fill="#fff", stroke=INK)
    box(16, 88, 150, 32, "edge features", "N × N × 6", fill="#fff", stroke=INK)
    box(16, 132, 150, 32, "adjacency", "undirected + self-loops", fill="#fff", stroke=INK)
    box(196, 44, 140, 32, "BatchNorm", "frozen, per-feature")
    box(196, 88, 140, 32, "Linear 31 → 128", "GELU")
    S.line(166, 60, 194, 60, stroke=GREY, arrow="arr")
    S.line(266, 76, 266, 86, stroke=GREY, arrow="arr")

    lx, ly, lw, lh = 366, 26, 398, 284
    S.rect(lx, ly, lw, lh, fill="none", stroke=INK, sw=1, r=4, dash="4,3")
    S.text(lx + 12, ly + 17, "GPS layer × 4", cls="h")
    S.text(lx + lw - 12, ly + lh - 10, "hidden 128, 4 heads", cls="s", anchor="end")
    box(lx + 16, ly + 28, 176, 34, "local  GATv2",
        "attention over x" + sub("i") + ", x" + sub("j") + ", e" + sub("ij"),
        fill=TEALL, stroke=TEAL)
    S.text(lx + 104, ly + 75, "softmax over incoming edges of i", cls="s", anchor="middle")
    S.text(lx + 104, ly + 87, "edge encoder 6 → 128 per layer", cls="s", anchor="middle")
    box(lx + 206, ly + 28, 176, 34, "global  self-attention",
        "softmax(QK" + sup("T") + "/√d) V over N nodes", fill=PURPL, stroke=PURP)
    S.text(lx + 294, ly + 75, "Q, K, V, O projections 128 → 128", cls="s", anchor="middle")
    S.text(lx + 294, ly + 87, "window-wide context", cls="s", anchor="middle")
    box(lx + 110, ly + 104, 180, 30, "x + local + global", fill="#fff", stroke=INK)
    S.line(lx + 104, ly + 95, lx + 158, ly + 103, stroke=GREY, arrow="arr")
    S.line(lx + 294, ly + 95, lx + 242, ly + 103, stroke=GREY, arrow="arr")
    box(lx + 110, ly + 150, 180, 26, "LayerNorm")
    box(lx + 110, ly + 192, 180, 30, "FFN 128 → 256 → 128", "GELU, residual")
    box(lx + 110, ly + 238, 180, 26, "LayerNorm")
    for y1, y2 in [(ly + 134, ly + 148), (ly + 176, ly + 190), (ly + 222, ly + 236)]:
        S.line(lx + 200, y1, lx + 200, y2, stroke=GREY, arrow="arr")
    S.path(f"M336,104 L352,104 L352,60 L{lx+12},60", stroke=GREY, w=1, arrow="arr")
    S.path(f"M352,60 L352,49 L{lx+294},49 L{lx+294},{ly+26}", stroke=GREY, w=1, arrow="arr")

    box(366, 344, 190, 32,
        "concat [ h" + sub("i") + " | Σw" + sub("ij") + " | max w" + sub("ij") + " ]",
        "130 features", fill="#fff", stroke=INK)
    box(586, 344, 178, 32, "Linear 130 → 128 → 2", "GELU, softmax")
    box(586, 392, 178, 30, "P(misphased)", "mean of the two allele nodes",
        fill=AMBERL, stroke=AMBER, tc=INK)
    S.line(lx + 200, ly + lh, lx + 200, 342, stroke=GREY, arrow="arr")
    S.line(556, 360, 584, 360, stroke=GREY, arrow="arr")
    S.line(675, 376, 675, 390, stroke=GREY, arrow="arr")
    S.path("M166,104 L184,104 L184,328 L366,328 L366,342", stroke=GREY, w=0.9,
           dash="2.5,2", arrow="arr")
    S.text(192, 324, "raw edge weights", cls="s")

    S.table(16, 344, [136, 194],
            [("parameters", "687,358, compiled into the binary"),
             ("attention cost", "dense O(N²), N ≤ 82 (cap 256)"),
             ("numerics", "exact GELU, LayerNorm ε = 10" + sup("−5")),
             ("isolated nodes", "attend uniformly to all nodes")],
            rowh=16)

    S.save("suppfig6_gnn_architecture.svg")


# ============================================================================
# S7  modcall
# ============================================================================
def fig_s7():
    S = SVG(W, 566, "Allele-specific methylation calling with modcall")
    XL, XR = 16, 424
    S.line(406, 18, 406, 550, stroke=LGREY, w=0.8)
    RW = 340   # right column width

    def cpg_mark(cx, cy, state, r=4.4):
        """state: 'm' methylated, 'u' unmethylated, 'a' ambiguous."""
        if state == "m":
            S.circle(cx, cy, r, fill=INK, stroke=INK, sw=0)
        elif state == "u":
            S.circle(cx, cy, r, fill="#ffffff", stroke=INK, sw=1.1)
        else:
            S.circle(cx, cy, r, fill=LGREY, stroke=GREY, sw=0.9)

    # -- a  read-level ML parsing ---------------------------------------
    S.panel(XL, 24, "a", "Per-read CpG state from the MM / ML tags")
    sites = [78, 132, 186, 262, 330]
    stat  = ["Homo", "Hetero", "Hetero", "Homo", "Hetero"]
    S.rect(52, 38, 330, 11, fill=HEADF, r=1)
    for x, st in zip(sites, stat):
        S.text(x, 34, st, cls="s", anchor="middle",
               fill=(INK if st == "Hetero" else GREY))
        S.text(x, 47, "CpG", cls="n", anchor="middle", fill=GREY)
    # forward-strand reads
    fwd = [(56, 300, {78: "m", 132: "m", 186: "m", 330: "u"}),
           (96, 378, {132: "m", 186: "m", 330: "u"}),
           (56, 340, {78: "m", 132: "u", 186: "u"}),
           (56, 230, {78: "m", 132: "u", 186: "a"})]
    rev = [(66, 372, {78: "m", 262: "m", 330: "m"}),
           (120, 382, {186: "a", 262: "m", 330: "m"}),
           (56, 320, {78: "m", 186: "m", 262: "m"})]
    y = 62
    S.text(XL, y + 22, "forward", cls="s", rot=-90)
    for x1, x2, marks in fwd:
        S.line(x1, y, x2, y, stroke=LGREY, w=1.1, arrow="arr")
        for px, st in marks.items():
            if x1 <= px <= x2: cpg_mark(px, y, st)
        y += 15
    y += 7
    S.text(XL, y + 18, "reverse", cls="s", rot=-90)
    for x1, x2, marks in rev:
        S.line(x2, y, x1, y, stroke=LGREY, w=1.1, arrow="arr")
        for px, st in marks.items():
            if x1 <= px <= x2: cpg_mark(px, y, st)
        y += 15
    # threshold scale
    ys = y + 16
    x0, x1s = 62, 372
    for f0, wf, col in [(0.0, 0.2, "#ffffff"), (0.2, 0.6, VLGREY), (0.8, 0.2, INK)]:
        S.rect(x0 + f0 * (x1s - x0), ys, wf * (x1s - x0), 11, fill=col,
               stroke=LGREY, sw=0.7, r=1)
    for p2, lab in [(0, "0"), (0.2, "0.2"), (0.8, "0.8"), (1, "1")]:
        xx = x0 + p2 * (x1s - x0)
        S.text(xx, ys + 22, lab, cls="s", anchor="middle")
    for f0, wf, lab in [(0.0, 0.2, "unmethylated"), (0.2, 0.6, "ambiguous"),
                        (0.8, 0.2, "methylated")]:
        S.text(x0 + (f0 + wf / 2) * (x1s - x0), ys + 34, lab, cls="s",
               anchor="middle")
    S.text(XL, ys + 9, "ML / 255", cls="s")

    # -- b  CpG merging --------------------------------------------------
    yb0 = 246
    S.panel(XL, yb0, "b", "Strand pooling and merging of consecutive CpGs")
    yb = yb0 + 22
    for col_x, hdr in [(58, "two CpG coordinates"), (250, "one merged locus")]:
        S.text(col_x + 58, yb, hdr, cls="s", anchor="middle", fill=GREY)
    # left: two coordinates, forward reads carry C, reverse carry G
    for k, (lx, pair) in enumerate([(58, [(96, 116)]), (250, [(306, 306)])]):
        for (ca, cb) in pair:
            S.rect(lx, yb + 8, 116, 11, fill=HEADF, r=1)
            S.text(ca, yb + 17, "C", cls="n", anchor="middle", fill=INK)
            if cb != ca:
                S.text(cb, yb + 17, "G", cls="n", anchor="middle", fill=GREY)
        yy = yb + 28
        for j in range(6):
            fwdr = j < 3
            st = "m" if j < 3 else "u"
            S.line(lx, yy, lx + 116, yy, stroke=LGREY, w=1.1)
            if k == 0:
                cpg_mark(ca if fwdr else cb, yy, st)
            else:
                cpg_mark(306, yy, st)
            yy += 12
    S.path(f"M188,{yb+58} L240,{yb+58}", stroke=INK, w=1.2, arrow="arrd")
    

    # -- c  site genotype ------------------------------------------------
    yc0 = 412
    S.panel(XL, yc0, "c", "Site genotype")
    S.callout(XL, yc0 + 12, 374, 30, fill=VLGREY, accent=INK)
    S.text(XL + 10, yc0 + 26, "heterozygous if  min(M,U) / max(M,U) &#8805; 0.6"
           "   and   A / (M+U+A) &#8804; 0.2", cls="tb", fill=INK)
    S.text(XL + 10, yc0 + 38, "otherwise homozygous methylated or unmethylated, and "
           "excluded from phasing", cls="s")
    for i, (m, u, a, gt, col) in enumerate([(14, 12, 2, "0/1", GREEN),
                                            (25, 2, 1, "1/1", GREY),
                                            (9, 8, 11, "excluded", GREY)]):
        yy = yc0 + 52 + i * 22
        tot, bw = m + u + a, 190
        S.rect(XL + 96, yy, bw * m / tot, 13, fill=INK, r=1)
        S.rect(XL + 96 + bw * m / tot, yy, bw * u / tot, 13, fill="#ffffff",
               stroke=LGREY, sw=0.7, r=1)
        S.rect(XL + 96 + bw * (m + u) / tot, yy, bw * a / tot, 13, fill=LGREY, r=1)
        S.text(XL + 90, yy + 10, f"M {m}   U {u}   A {a}", cls="s", anchor="end")
        S.text(XL + 296, yy + 10, gt, cls="tb", fill=col)
    kx = XL
    for c, sk, lab in [(INK, INK, "methylated"), ("#ffffff", LGREY, "unmethylated"),
                       (LGREY, LGREY, "ambiguous")]:
        S.rect(kx, yc0 + 124, 10, 10, fill=c, stroke=sk, sw=0.7, r=1)
        S.text(kx + 14, yc0 + 133, lab, cls="s")
        kx += 22 + 5.4 * len(lab)

    # -- d  the four edge types ------------------------------------------
    S.panel(XR, 24, "d", "Read support between two loci")
    pairs = [("MM", "m", "m", 8), ("UU", "u", "u", 10),
             ("MU", "m", "u", 2), ("UM", "u", "m", 1)]
    for k, (lab, s1, s2, n) in enumerate(pairs):
        col_i, row_i = k % 2, k // 2
        ex = XR + col_i * 168
        ey = 52 + row_i * 40
        S.text(ex, ey + 4, lab, cls="sb", fill=GREY)
        cpg_mark(ex + 34, ey, s1, r=6)
        cpg_mark(ex + 88, ey, s2, r=6)
        S.line(ex + 41, ey, ex + 81, ey, stroke=LGREY, w=1.4)
        S.text(ex + 116, ey + 4, str(n), cls="tb", anchor="end", fill=INK)
        S.text(ex + 121, ey + 4, "read" if n == 1 else "reads", cls="s")
    S.rule(XR, 140, XR + RW)
    S.text(XR, 158, "P = MM + UU = 18", cls="tb", fill=INK)
    S.text(XR + 132, 158, "Q = MU + UM = 3", cls="tb", fill=INK)
    S.text(XR, 182, "linkage  =", cls="eq", fill=INK)
    S.frac(XR + 108, 178, "max(P, Q)", "P + Q", cls="s", width=64)
    S.text(XR + 150, 182, "= 0.86", cls="tb", fill=INK)
    S.text(XR + 196, 182, "&lt; 0.9  rejected", cls="tb", fill=AMBER)
    

    # -- e  linking modes -------------------------------------------------
    S.panel(XR, 246, "e", "Co-segregation with a neighbouring marker")
    modes = [("SNV-anchored", GREEN, "strong anchor",
              "SNV among the next 20 variants"),
             ("methylation-only", GREEN, "strong anchor",
              "no informative SNV in range"),
             ("iterative expansion", AMBER, "weak, admitted",
              "against an accepted CpG, &#8805; 6 reads, 2 rounds")]
    for k, (title, col, verdict, note) in enumerate(modes):
        yk = 272 + k * 62
        S.text(XR, yk, title, cls="sb", fill=INK)
        ax, bx = XR + 30, XR + 110
        yt2 = yk + 26
        if k == 0:
            S.node(ax, yt2, "R", H1, r=8)
            S.text(ax, yk + 46, "SNV", cls="s", anchor="middle")
        else:
            cpg_mark(ax, yt2, "m", r=7)
            S.text(ax, yk + 46, "CpG", cls="s", anchor="middle")
        cpg_mark(bx, yt2, "m", r=7)
        S.text(bx, yk + 46, "CpG", cls="s", anchor="middle")
        S.line(ax + 9, yt2, bx - 9, yt2, stroke=col, w=2.2)
        S.text(bx + 22, yt2 + 4, verdict, cls="sb",
               fill=(col if col != LGREY else GREY))
        S.text(bx + 22, yt2 + 16, note, cls="s")
    S.callout(XR, 458, RW, 30, fill=AMBERL, accent=AMBER)
    S.text(XR + 10, 472, "a pair is considered only while spanning reads &gt; max(6, "
           "(n" + sub("1") + " + n" + sub("2") + ") / 4)", cls="tb", fill=INK)
    S.text(XR + 10, 483, "falling to that bound ends the neighbour scan for the site",
           cls="s")

    # -- f  output --------------------------------------------------------
    S.panel(XR, 512, "f", "Output record")
    S.rect(XR, 522, RW, 30, fill=VLGREY, r=2)
    S.text(XR + 8, 535, "chr1 10469 . N . . PASS RS=P;MR=read3,read7;NR=read1,read4",
           cls="code")
    S.text(XR + 8, 547, "GT:MD:UD:DP   0/1:14:12:28", cls="code")

    S.save("suppfig7_modcall.svg")


# ============================================================================
# S8  Evaluation metrics
# ============================================================================
def fig_s8():
    S = SVG(W, 372, "Phasing evaluation metrics")
    XL = 16

    # -- a ---------------------------------------------------------------
    S.panel(XL, 24, "a", "Switch errors, flips and Hamming distance within one block")
    xs = [160 + i * 58 for i in range(10)]
    truth = [0] * 10
    query = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]
    S.text(146, 56, "position", cls="s", anchor="end")
    for i, x in enumerate(xs):
        S.text(x, 56, str(i + 1), cls="s", anchor="middle")
    for lab, hap, y in [("truth h" + sub("0"), truth, 80),
                        ("query h" + sub("0"), query, 116)]:
        S.text(146, y + 3, lab, cls="sb", anchor="end", fill=INK)
        for x, a in zip(xs, hap):
            S.node(x, y, str(a), H1 if a == 0 else H2, r=10)
    sw = ["0" if query[i] == query[i + 1] else "1" for i in range(9)]
    S.text(146, 158, "switch encoding", cls="sb", anchor="end", fill=INK)
    for i in range(9):
        x = (xs[i] + xs[i + 1]) / 2
        on = sw[i] == "1"
        S.text(x, 158, sw[i], cls="tb", anchor="middle", fill=H2 if on else LGREY)
        if on:
            S.line(x, 130, x, 148, stroke=H2, w=1, dash="2.5,2")
    xf1, xf2 = (xs[6] + xs[7]) / 2, (xs[7] + xs[8]) / 2
    S.path(f"M{xf1},168 L{xf1},175 L{xf2},175 L{xf2},168", stroke=H2, w=1)
    S.text((xf1 + xf2) / 2, 188, "flip", cls="sb", anchor="middle", fill=H2)
    for i in (2, 8):
        S.text((xs[i] + xs[i + 1]) / 2, 176, "isolated", cls="s", anchor="middle", fill=H2)

    S.table(XL, 204, [118, 60, 132, 106],
            [("switch errors", "4", "isolated switches", "2"),
             ("flips", "1", "Hamming distance", "min(5, 5) = 5 of 10")],
            rowh=16, cell_cls=("tb", "t", "tb", "t"))

    S.rule(XL, 250, W - XL)

    # -- b ---------------------------------------------------------------
    S.panel(XL, 274, "b", "Block statistics")
    bx, by = XL + 68, 300
    sc = 0.90
    S.text(bx - 8, by + 3, "truth blocks", cls="s", anchor="end")
    S.text(bx - 8, by + 21, "query blocks", cls="s", anchor="end")
    S.text(bx - 8, by + 39, "compared", cls="s", anchor="end")
    for x, w in [(0, 120), (132, 92), (236, 24), (272, 108)]:
        S.rect(bx + x * sc, by - 4, w * sc, 9, fill=H1, r=1)
    for x, w in [(0, 64), (72, 140), (222, 38), (270, 106)]:
        S.rect(bx + x * sc, by + 14, w * sc, 9, fill=H2, r=1)
    for x, w in [(0, 64), (72, 48), (132, 80), (272, 104)]:
        S.rect(bx + x * sc, by + 32, w * sc, 9, fill=INK, r=1)
    S.rect(bx + 236 * sc, by + 32, 24 * sc, 9, fill="none", stroke=LGREY, sw=0.8, r=1)
    S.text(bx + 248 * sc, by + 56, "singleton, ignored", cls="s", anchor="middle", fill=GREY)

    S.table(462, 288, [122, 180],
            [("phased fraction", "phased truth het / all truth het"),
             ("block N50", "span at 50% cumulative block span"),
             ("switch error rate", "switch errors / assessed pairs × 100")],
            rowh=16)
    S.text(462, 356, "longphase compare; cross-tool comparisons use --only-snvs", cls="s")

    S.save("suppfig8_metrics.svg")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for f in (fig_s1, fig_s2, fig_s3, fig_s4, fig_s5, fig_s6, fig_s7, fig_s8):
        f()
