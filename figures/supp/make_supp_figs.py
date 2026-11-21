#!/usr/bin/env python3
"""Generate four supplementary method figures (SVG) for the LongPhase 2 manuscript.

fig_s1 (suppfig1_observations), fig_s2 (suppfig2_voting), fig_s3 (suppfig3_read_correction) and
fig_s7 (suppfig7_modcall) were replaced on 2026-11-16 by make_supp_schematics.py, which writes those
four PDFs directly.

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
def fig_s4():
    S = SVG(W, 356, "Overview of the graph neural network unphasing module")
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
    S.text(93, 164, "LongPhase 2", cls="tb", anchor="middle", fill=H1)
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
    S.text(fx, 303, "onset score", cls="tb", anchor="middle", fill=INK)
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

    S.text(DX, 122, "onset score", cls="sb", fill=INK)
    base, hmax = 162, 30
    S.rect(ox0 + 20 * odx - 4, base - hmax, 8, hmax, fill=AMBER, r=2, op=0.16)
    prng = random.Random(21)
    probs = [min(0.27, 0.02 + prng.random() * 0.22) for _ in range(on)]
    probs[20], probs[19], probs[21] = 0.62, 0.21, 0.24
    for k, pr in enumerate(probs):
        h = hmax * pr
        S.rect(ox0 + k * odx - 1.3, base - h, 2.6, h,
               fill=AMBER if pr >= 0.35 else GREY, r=0.4)
    S.line(ox0 - 4, base, 760, base, stroke=INK, w=0.9)
    thr = base - hmax * 0.35
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
    S = SVG(W, 408, "Window construction for the graph neural network")
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
    S.text(466, 392, "r = (pos − pos" + sub("c") + ") / max |offset|; |r| ≤ 0.5",
           cls="s")

    # Panels d-f (DOT format, phase set before and after unphasing) were removed on
    # 2026-11-16 (author, option A): Supplementary Fig. 13d shows the same step.

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
    box(586, 392, 178, 30, "onset score", "mean of the two allele nodes",
        fill=AMBERL, stroke=AMBER, tc=INK)
    S.line(lx + 200, ly + lh, lx + 200, 342, stroke=GREY, arrow="arr")
    S.line(556, 360, 584, 360, stroke=GREY, arrow="arr")
    S.line(675, 376, 675, 390, stroke=GREY, arrow="arr")
    S.path("M166,104 L184,104 L184,328 L366,328 L366,342", stroke=GREY, w=0.9,
           dash="2.5,2", arrow="arr")
    S.text(192, 324, "σ(w) of incoming edges", cls="s")

    S.table(16, 344, [136, 194],
            [("stored values", "687,358"),
             ("attention cost", "dense O(N²), N ≤ 82 allele nodes"),
             ("numerics", "erf-based GELU, LayerNorm ε = 10" + sup("−5"))],
            rowh=16)

    S.save("suppfig6_gnn_architecture.svg")


# ============================================================================
# S7  modcall
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
    for f in (fig_s4, fig_s5, fig_s6, fig_s8):
        f()
