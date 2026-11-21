#!/usr/bin/env python3
"""Supplementary Figs. 9 (modcall), 10 (allele observations and the copy-number-aware filter),
11 (weighted phasing graph and multi-neighbour voting) and 12 (read-based correction and phasing entropy).

Figs. 11 and 12 replace fig_s2() and fig_s3() of make_supp_figs.py (author decision 2026-11-16, option A,
drafts in notes/drafts/2026-11-16-sfig11-12/).

Replaces fig_s7() and fig_s1() of make_supp_figs.py (author decision 2026-11-16, options 9A and 10A,
drafts in notes/drafts/2026-11-16-sfig9-10/). Matplotlib, millimetre coordinates with y down,
160 mm wide (\\textwidth), Arial 5-8 pt, the glyphs of Fig. 1. The example counts are illustrations.

Run from figures/supp/:  python3 make_supp_schematics.py   (writes the two PDFs directly)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, FancyArrowPatch, Polygon
import numpy as np

plt.rcParams.update({
    "font.family": "Arial", "pdf.fonttype": 42, "svg.fonttype": "none",
    "mathtext.fontset": "custom", "mathtext.rm": "Arial", "mathtext.it": "Arial:italic",
    "mathtext.bf": "Arial:bold",
})

H1, H1L, H1E = "#1687C9", "#DCEAF6", "#6CC8EE"
H2, H2L, H2E = "#DC2B23", "#FAE3DD", "#F0766C"
INK, GREY, LGREY, VLGREY = "#16233D", "#6E7C8C", "#C7D1DB", "#F1F4F7"
AMBER, AMBERL = "#B8860B", "#FBF0D5"
GREEN, GREENL = "#1F7A4D", "#E4F1EA"
HAP = {1: H1, 2: H2, 0: GREY}
PT = 72 / 25.4  # points per mm


class Fig:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.set_aspect("equal"); ax.axis("off")
        self.ax = ax

    # text -----------------------------------------------------------------
    def t(self, x, y, s, size=6, color=INK, ha="left", va="center", weight="normal", style="normal", **kw):
        return self.ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
                            fontweight=weight, fontstyle=style, **kw)

    def letter(self, x, y, L, title=None):
        self.t(x, y, L, size=8, weight="bold", va="baseline")
        if title:
            self.t(x + 3.6, y, title, size=7, weight="bold", va="baseline")

    # lines ----------------------------------------------------------------
    def line(self, x1, y1, x2, y2, color=GREY, lw=0.5, ls="-", z=1, cap="butt"):
        self.ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=z,
                     solid_capstyle=cap, dash_capstyle=cap)

    def read(self, x1, x2, y, color=LGREY, w=1.1, z=1):
        self.ax.plot([x1, x2], [y, y], color=color, lw=w * PT, solid_capstyle="round", zorder=z)

    def arrow(self, x1, y1, x2, y2, color=GREY, lw=0.6, head=2.2, z=2, rad=0.0):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=f"-|>,head_length={head*0.5},head_width={head*0.3}",
                            mutation_scale=4, color=color, lw=lw, zorder=z,
                            connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0)
        self.ax.add_patch(a)

    def arc(self, x1, x2, y, h, color=GREEN, lw=0.9, ls="-", z=2):
        xs = np.linspace(x1, x2, 40)
        ys = y - h * np.sin(np.linspace(0, np.pi, 40))
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")

    # shapes ---------------------------------------------------------------
    def rect(self, x, y, w, h, fc=VLGREY, ec="none", lw=0.5, z=0, r=0.0):
        if r:
            p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                               fc=fc, ec=ec, lw=lw, zorder=z)
        else:
            p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z)
        self.ax.add_patch(p)

    def snv(self, x, y, base, hap, r=1.45, size=5.5, faded=False):
        c = HAP[hap]
        self.ax.add_patch(Circle((x, y), r, fc="white", ec=c, lw=0.8, zorder=4, alpha=0.35 if faded else 1))
        self.t(x, y + 0.05, base, size=size, color=c, ha="center", weight="bold", zorder=5)

    def vbox(self, x, y, label, hap, w=4.0, h=2.6, size=5, dashed=False):
        c = HAP[hap]
        self.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.5",
                                         fc="white", ec=c, lw=0.8, zorder=4, ls="--" if dashed else "-"))
        self.t(x, y + 0.05, label, size=size, color=c, ha="center", weight="bold", zorder=5)

    def meth(self, x, y, state, r=0.85, z=4):
        if state == "m":
            self.ax.add_patch(Circle((x, y), r, fc=INK, ec=INK, lw=0.5, zorder=z))
        elif state == "u":
            self.ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=0.6, zorder=z))
        else:
            self.ax.add_patch(Circle((x, y), r, fc=LGREY, ec=GREY, lw=0.5, zorder=z))

    def lollipop(self, x, y, state, hap, stem=1.8, r=0.9):
        self.line(x, y, x, y - stem, color=INK, lw=0.6, z=4)
        self.meth(x, y - stem, state, r=r, z=5)

    def node(self, x, y, fc, ec, r=1.1, lw=0.7, z=4):
        self.ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=z))

    def cross(self, x, y, s=0.9, color=H2, lw=0.8, z=6):
        self.line(x - s, y - s, x + s, y + s, color=color, lw=lw, z=z, cap="round")
        self.line(x - s, y + s, x + s, y - s, color=color, lw=lw, z=z, cap="round")

    def tick(self, x, y, s=0.9, color=GREEN, lw=0.8, z=6):
        self.ax.plot([x - s, x - s * 0.25, x + s], [y, y + s * 0.7, y - s * 0.8], color=color, lw=lw,
                     zorder=z, solid_capstyle="round", solid_joinstyle="round")

    def zigzag(self, x, y, n=3, w=0.7, h=0.6, color=AMBER, lw=0.6, direction=1):
        xs = [x + direction * i * w / 2 for i in range(2 * n + 1)]
        ys = [y + (h if i % 2 else -h) * 0.5 if i else y for i in range(2 * n + 1)]
        self.ax.plot(xs, ys, color=color, lw=lw, zorder=3, solid_joinstyle="round")

    def save(self, path):
        self.fig.savefig(path + ".pdf")
        plt.close(self.fig)




def align_select(F, x0, y0, w):
    """Overlapping-alignment filter: the shorter of two overlapping alignments is discarded."""
    ry = y0 + 6
    F.line(x0 + 1, ry, x0 + w - 1, ry, color=INK, lw=0.9)
    F.t(x0 + 1, ry - 2.2, "reference", size=5, color=GREY)
    a2 = (x0 + 0.30 * w, x0 + 0.95 * w)
    a1 = (x0 + 0.08 * w, x0 + 0.46 * w)
    ov = (a2[0], a1[1])
    F.rect(ov[0], ry + 3.9, ov[1] - ov[0], 6.2, fc=AMBERL, z=0)
    F.read(*a2, ry + 9, color=GREY, w=1.1)
    F.read(*a1, ry + 5, color=LGREY, w=1.1)
    F.t(a2[1], ry + 11.6, "alignment 2", size=5, color=GREY, ha="right")
    F.t(a1[0], ry + 2.6, "alignment 1 (shorter)", size=5, color=GREY)
    F.cross((a1[0] + ov[0]) / 2, ry + 5, s=0.75)
    F.t((ov[0] + ov[1]) / 2, ry + 11.8, "overlap", size=5, color=AMBER, ha="center")
    F.t(x0 + 1, ry + 18.5, r"overlap / combined span $\geq$ 0.2:", size=5, color=INK)
    F.t(x0 + 1, ry + 21.8, "the shorter alignment is discarded", size=5, color=INK)


def allele_extract(F, x0, y0, w, sources=True):
    """One read across the four variant classes, with the source of each allele."""
    ry = y0 + 6
    cols = [x0 + w * f for f in (0.10, 0.33, 0.60, 0.88)]
    names = ["SNV", "indel", "SV", "5mC"]
    F.line(x0 + 1, ry, x0 + w - 1, ry, color=INK, lw=0.9)
    for x, n in zip(cols, names):
        F.line(x, ry - 1.1, x, ry + 1.1, color=INK, lw=0.7)
        F.t(x, ry - 2.6, n, size=5, color=GREY, ha="center")
    # read 1: spans all four sites, deletion gap at the SV
    y1 = ry + 6
    svw = 0.12 * w
    F.read(x0 + 2, cols[2] - svw / 2, y1)
    F.read(cols[2] + svw / 2, x0 + w - 2, y1)
    F.line(cols[2] - svw / 2, y1, cols[2] + svw / 2, y1, color=GREY, lw=0.6, ls=(0, (1.2, 1.0)))
    F.snv(cols[0], y1, "G", 2, r=1.3, size=5)
    F.vbox(cols[1], y1, "+CA", 2, w=5.0, h=2.6, size=4.8)
    F.vbox(cols[2], y1, "DEL", 2, w=5.2, h=2.6, size=4.8)
    F.lollipop(cols[3], y1, "m", 2, stem=1.6, r=0.85)
    # read 2: ends at the SV, clipped tail continues as a supplementary alignment
    y2 = ry + 11
    F.read(x0 + 0.40 * w, cols[2] - 0.2, y2)
    F.zigzag(cols[2] - 0.2, y2, n=3, direction=1)
    F.vbox(cols[2] - 3.6, y2, "DEL", 2, w=5.2, h=2.6, size=4.8, dashed=True) if False else None
    F.t(cols[2] + 3.6, y2, "split", size=5, color=AMBER)
    if sources:
        srcs = [("aligned base", "with its Phred quality"),
                ("CIGAR insertion or", "deletion after the site"),
                ("CIGAR, split alignment", "or caller read list"),
                ("modcall read", "lists")]
        for x, (l1, l2) in zip(cols, srcs):
            F.t(x, ry + 17.0, l1, size=5, color=INK, ha="center")
            F.t(x, ry + 20.0, l2, size=5, color=INK, ha="center")


def clip_profile(F, x0, y0, w, h=26, detail=False):
    """Per-position counts of front-clipped (up) and back-clipped (down) alignments define an interval."""
    rng = np.random.default_rng(3)
    n = 46
    bw = w / n
    base = y0 + h * 0.55
    lo, hi = int(n * 0.30), int(n * 0.74)
    F.rect(x0 + lo * bw - 0.4, y0 + 1.5, (hi - lo + 1) * bw + 0.8, h - 1.5, fc=AMBERL, z=0)
    for i in range(n):
        up = int(rng.random() < 0.22)
        dn = int(rng.random() < 0.22)
        if i == lo:
            up = 9
        if detail and i in (lo + 5, lo + 11):
            up = 4
        if i in (hi - 1, hi):
            dn = 7 if i == hi else 5
        x = x0 + i * bw + 0.15 * bw
        if up:
            F.rect(x, base - up * 1.05, 0.7 * bw, up * 1.05, fc=INK, z=2)
        if dn:
            F.rect(x, base, 0.7 * bw, dn * 1.05, fc=GREY, z=2)
    F.line(x0, base, x0 + w, base, color=INK, lw=0.5, z=3)
    F.t(x0 + 0.5, y0 + 3.0, "front-clipped", size=5, color=INK)
    F.t(x0 + 0.5, base + 6.0, "back-clipped", size=5, color=GREY)
    F.t(x0 + (lo + hi) / 2 * bw, y0 + h + 1.8, "candidate interval", size=5, color=AMBER, ha="center")
    if detail:
        F.t(x0 + lo * bw + 1.2, base - 10.2, "opens: front-clip cluster", size=5, color=INK)
        F.t(x0 + hi * bw - 1.0, base + 9.4, "closes: back-clip cluster", size=5, color=INK, ha="right")


def mr_examples(F, x0, y0, w, show_formula=True):
    """Two sites inside an interval: true heterozygous (kept) and paralogous (removed)."""
    if show_formula:
        F.t(x0 + 1, y0 + 2, r"$\mathrm{MR} = \overline{R}_{\mathrm{ALT}} \,/\, (\overline{R}_{\mathrm{REF}} + \overline{R}_{\mathrm{ALT}})$",
            size=6)
        F.t(x0 + 1, y0 + 6.2, "mean number of other alternate alleles per read, in the REF and the ALT reads", size=5, color=GREY)
    half = w / 2
    examples = [
        ("true heterozygous site", [[1, 0, 1], [1, 0, 1]], "MR = 0.50, kept", GREEN),
        ("reads from a paralogue", [[0, 1, 0], [3, 3, 2]], "MR = 0.89, removed", H2),
    ]
    others = [0.12, 0.30, 0.68, 0.86]
    for e, (title, loads, verdict, col) in enumerate(examples):
        ex = x0 + e * half
        ey = y0 + 11
        F.t(ex + 1, ey, title, size=5.5, weight="bold")
        rw = half - 6
        k = 0
        for g, allele in enumerate(["REF", "ALT"]):
            for j in range(3):
                y = ey + 3.6 + k * 2.6
                F.read(ex + 7, ex + 2 + rw, y, w=0.85)
                vx = ex + 4.5 + rw * 0.5
                if j == 1:
                    F.t(ex + 1, y, allele, size=5, color=GREY)
                if allele == "REF":
                    F.ax.add_patch(Circle((vx, y), 0.75, fc="white", ec=INK, lw=0.6, zorder=4))
                else:
                    F.ax.add_patch(Circle((vx, y), 0.75, fc=INK, ec=INK, lw=0.6, zorder=4))
                for m in range(loads[g][j]):
                    tx = ex + 7 + (rw - 5) * others[(m + j) % 4]
                    F.line(tx, y - 0.8, tx, y + 0.8, color=AMBER, lw=0.8, z=4)
                k += 1
        F.t(ex + 4.5 + rw * 0.5, ey + 3.6 + 6 * 2.6 + 0.6, verdict, size=5.5, color=col, ha="center", weight="bold")
    return y0 + 11 + 3.6 + 6 * 2.6 + 2



def fig9():
    F = Fig(160, 66)
    TOP = 5

    # ---------------------------------------------------------------- a ------
    F.letter(1, TOP, "a", "Read classification")
    xs = [9, 20, 31]
    F.line(4, 12, 37, 12, color=INK, lw=0.9)
    for x in xs:
        F.line(x, 10.8, x, 13.2, color=INK, lw=0.7)
        F.t(x, 9.2, "CpG", size=5, color=GREY, ha="center")
    reads = [  # (x1, x2, strand, states at xs or None)
        (4, 36, +1, ["m", "m", "m"]),
        (6, 35, +1, ["u", "a", "u"]),
        (5, 34, +1, ["u", "u", "a"]),
        (4, 25, -1, ["m", "m", None]),
        (13, 37, -1, [None, "u", "u"]),
    ]
    for i, (x1, x2, s, st) in enumerate(reads):
        y = 16 + i * 3.2
        F.read(x1, x2, y)
        tip = x2 + 0.9 if s > 0 else x1 - 0.9
        base = x2 - 0.3 if s > 0 else x1 + 0.3
        F.ax.add_patch(Polygon([(base, y - 0.75), (base, y + 0.75), (tip, y)], fc=LGREY, ec="none", zorder=1))
        for x, k in zip(xs, st):
            if k:
                F.meth(x, y, k)
    F.t(2.2, 19.2, "forward", size=5, color=GREY, ha="center", rotation=90)
    F.t(2.2, 27.2, "reverse", size=5, color=GREY, ha="center", rotation=90)
    # probability scale
    y0, x0, x1 = 39, 6, 36
    sx = lambda v: x0 + (x1 - x0) * v
    F.rect(sx(0), y0, sx(0.2) - sx(0), 2.2, fc="white", ec=INK, lw=0.5, z=2)
    F.rect(sx(0.2), y0, sx(0.8) - sx(0.2), 2.2, fc=LGREY, ec=INK, lw=0.5, z=2)
    F.rect(sx(0.8), y0, sx(1) - sx(0.8), 2.2, fc=INK, ec=INK, lw=0.5, z=2)
    for v, lab in [(0, "0"), (0.2, "0.2"), (0.8, "0.8"), (1, "1")]:
        F.t(sx(v), y0 + 3.6, lab, size=5, color=GREY, ha="center")
    F.t((x0 + x1) / 2, y0 - 1.6, "5mC probability", size=5, color=GREY, ha="center")
    F.t(sx(0.1), y0 + 6.3, "unmeth.", size=5, ha="center")
    F.t(sx(0.5), y0 + 6.3, "ambiguous", size=5, ha="center")
    F.t(sx(0.9), y0 + 6.3, "meth.", size=5, ha="center")

    # ---------------------------------------------------------------- b ------
    BX = 41
    F.letter(BX, TOP, "b", "Candidate selection")
    rows = [("14", "12", "2", True, "balanced"),
            ("25", "2", "1", False, "unbalanced"),
            ("9", "8", "11", False, "ambiguous")]
    bx0, bw = BX + 2, 26
    for i, (m, u, a, ok, why) in enumerate(rows):
        y = 12 + i * 8.5
        m, u, a = int(m), int(u), int(a)
        n = m + u + a
        w = lambda k: bw * k / n
        F.rect(bx0, y, w(m), 2.6, fc=INK, ec=INK, lw=0.4, z=2)
        F.rect(bx0 + w(m), y, w(u), 2.6, fc="white", ec=INK, lw=0.4, z=2)
        F.rect(bx0 + w(m) + w(u), y, w(a), 2.6, fc=LGREY, ec=INK, lw=0.4, z=2)
        F.t(bx0, y + 4.4, f"M {m}  U {u}  A {a}", size=5, color=GREY)
        F.t(bx0 + bw, y + 4.4, why, size=5, color=GREEN if ok else GREY, ha="right")
        if ok:
            F.tick(bx0 + bw + 3, y + 1.3)
        else:
            F.cross(bx0 + bw + 3, y + 1.3, s=0.75, color=GREY)
    F.t(BX + 2, 40, r"$\min(M,U)\,/\,\max(M,U) \geq \alpha$", size=5.5)
    F.t(BX + 2, 44, r"$A\,/\,(M+U+A) \leq \beta$", size=5.5)

    # ---------------------------------------------------------------- c ------
    CX = 79
    F.letter(CX, TOP, "c", "Linkage test")
    # 2 x 2 table: rows SNV allele, cols CpG state
    gx, gy, cw, ch = CX + 9, 12.5, 6.5, 4.2
    F.t(gx + cw, gy - 2.6, "CpG", size=5, color=GREY, ha="center")
    F.meth(gx + cw / 2, gy - 0.9, "m", r=0.75)
    F.meth(gx + 1.5 * cw, gy - 0.9, "u", r=0.75)
    F.t(gx - 6.5, gy + ch, "SNV", size=5, color=GREY, ha="center", rotation=90)
    F.snv(gx - 2.2, gy + ch / 2, "A", 1, r=1.2, size=5)
    F.snv(gx - 2.2, gy + 1.5 * ch, "G", 2, r=1.2, size=5)
    cells = [[9, 0], [1, 8]]
    for r_ in range(2):
        for c_ in range(2):
            diag = (r_ == c_)
            F.rect(gx + c_ * cw, gy + 0.6 + r_ * ch, cw, ch, fc=GREENL if diag else "white", ec=LGREY, lw=0.5, z=1)
            F.t(gx + (c_ + 0.5) * cw, gy + 0.6 + (r_ + 0.5) * ch, str(cells[r_][c_]), size=6,
                ha="center", weight="bold" if diag else "normal", color=INK if diag else GREY)
    F.t(gx + 2 * cw + 2.5, gy + 3.2, r"$\frac{\max(RR+AA,\,RA+AR)}{RR+AA+RA+AR}$", size=6)
    F.t(gx + 2 * cw + 2.5, gy + 7.6, r"$= 17/18 \geq \gamma$", size=5.5)
    F.t(gx + 2 * cw + 2.5, gy + 10.6, "linked", size=5.5, color=GREEN, weight="bold")
    # three stages
    sy = [33, 42.5, 52]
    labels = ["1  SNV anchor", "2  expansion", "3  neighbour filter"]
    px = [CX + 4, CX + 12, CX + 20, CX + 28, CX + 36]
    for k, y in enumerate(sy):
        F.t(CX + 1, y - 5.6, labels[k], size=5, color=GREY)
        F.line(px[0], y, px[-1], y, color=LGREY, lw=0.4, z=0)
    # stage 1: SNV links CpG 1 and CpG 2; CpG 3 not linked
    y = sy[0]
    F.arc(px[0], px[1], y, 1.6); F.arc(px[0], px[2], y, 3.0)
    F.snv(px[0], y, "G", 2, r=1.15, size=5)
    for x, st in zip(px[1:], ["acc", "acc", "cand", "cand"]):
        F.node(x, y, INK if st == "acc" else "white", INK if st == "acc" else GREY, r=0.9)
    F.t(px[-1] + 2, y, "beyond SNV range", size=4.8, color=GREY) if False else None
    # stage 2: unlinked candidates tested against accepted CpGs
    y = sy[1]
    F.arc(px[2], px[3], y, 2.2); F.arc(px[3], px[4], y, 2.2)
    F.snv(px[0], y, "G", 2, r=1.15, size=5)
    for x in px[1:]:
        F.node(x, y, INK, INK, r=0.9)
    # stage 3: an accepted CpG is kept only if linked to both neighbours
    y = sy[2]
    F.snv(px[0], y, "G", 2, r=1.15, size=5)
    F.arc(px[1], px[2], y, 2.2); F.arc(px[2], px[3], y, 2.2)
    F.arc(px[3], px[4], y, 2.2, color=GREY, ls=(0, (1.5, 1.2)), lw=0.7)
    for x in px[1:]:
        F.node(x, y, INK, INK, r=0.9)
    F.tick(px[2], y + 3.0, s=0.7)
    F.cross(px[3], y + 3.0, s=0.65)

    # ---------------------------------------------------------------- d ------
    DX = 124
    F.letter(DX, TOP, "d", "Merging and output")
    # forward-strand calls at the C and reverse-strand calls at the G form one locus
    XC, XG = DX + 11, DX + 15
    F.t(XC, 12, "C", size=6, ha="center", weight="bold", color=INK)
    F.t(XG, 12, "G", size=6, ha="center", weight="bold", color=INK)
    F.rect(XC - 2, 9.9, XG - XC + 4, 4.2, fc="none", ec=LGREY, lw=0.5, z=0, r=0.6)
    F.t(XG + 3.5, 12, "one CpG", size=5, color=GREY)
    for j, (strand, st) in enumerate([(+1, "m"), (-1, "m"), (+1, "u"), (-1, "u")]):
        y = 16.8 + j * 2.7
        x1, x2 = (DX + 3, DX + 20) if strand > 0 else (DX + 5, DX + 23)
        F.read(x1, x2, y, w=0.9)
        tip = x2 + 0.8 if strand > 0 else x1 - 0.8
        base = x2 - 0.3 if strand > 0 else x1 + 0.3
        F.ax.add_patch(Polygon([(base, y - 0.65), (base, y + 0.65), (tip, y)], fc=LGREY, ec="none", zorder=1))
        F.meth(XC if strand > 0 else XG, y, st, r=0.7)
        F.t(DX + 25, y, "forward" if strand > 0 else "reverse", size=4.8, color=GREY)
    F.arrow(DX + 11, 28.5, DX + 11, 32.5)
    F.t(DX + 13, 30.5, "one locus", size=5, color=GREY)
    # read groups
    F.t(DX + 1.5, 36.2, "M reads", size=5, color=GREY)
    F.t(DX + 1.5, 40.2, "U reads", size=5, color=GREY)
    for k in range(4):
        F.meth(DX + 12 + k * 2.4, 36.2, "m", r=0.75)
        F.meth(DX + 12 + k * 2.4, 40.2, "u", r=0.75)
    F.arrow(DX + 11, 43.2, DX + 11, 47.2)
    F.t(DX + 13, 45.2, "phasing graph", size=5, color=GREY)
    # haplotype lines with lollipops (as in Fig. 1)
    for y, col, st in [(52.5, H1E, "m"), (58.5, H2E, "u")]:
        F.line(DX + 2, y, DX + 33, y, color=col, lw=1.4, z=1)
    F.snv(DX + 6, 52.5, "A", 1, r=1.2, size=5); F.snv(DX + 6, 58.5, "G", 2, r=1.2, size=5)
    F.lollipop(DX + 17, 52.5, "m", 1); F.lollipop(DX + 17, 58.5, "u", 2)
    F.snv(DX + 28, 52.5, "T", 1, r=1.2, size=5); F.snv(DX + 28, 58.5, "C", 2, r=1.2, size=5)

    # column rules
    for x in [39.5, 77.5, 122]:
        F.line(x, 3, x, 62, color=LGREY, lw=0.4)

    # key ------------------------------------------------------------------
    ky = 63.8
    F.meth(4, ky, "m"); F.t(5.6, ky, "methylated", size=5)
    F.meth(22, ky, "u"); F.t(23.6, ky, "unmethylated", size=5)
    F.meth(42, ky, "a"); F.t(43.6, ky, "ambiguous", size=5)
    F.node(80, ky, INK, INK, r=0.9); F.t(81.6, ky, "accepted CpG", size=5)
    F.node(100, ky, "white", GREY, r=0.9); F.t(101.6, ky, "candidate", size=5)
    F.line(116, ky, 120, ky, color=GREEN, lw=0.9); F.t(121, ky, "linked", size=5)
    F.line(131, ky, 135, ky, color=GREY, lw=0.7, ls=(0, (1.5, 1.2))); F.t(136, ky, "not linked", size=5)

    F.save("suppfig7_modcall")


def fig10():
    F = Fig(160, 84)
    F.letter(1, 5, "a", "Alignment selection")
    align_select(F, 0, 7, 50)
    F.line(53, 3, 53, 34, color=LGREY, lw=0.4)
    F.letter(56, 5, "b", "Allele extraction")
    allele_extract(F, 56, 7, 104)
    F.line(1, 37, 159, 37, color=LGREY, lw=0.4)
    F.letter(1, 43, "c", "Copy-number-aware filter")
    clip_profile(F, 2, 47, 66, h=30)
    mr_examples(F, 74, 45, 86)
    F.save("suppfig1_observations")


def anode(F, x, y, lab, color=INK, r=1.35, faded=False, dashed=False, fill="white", size=5):
    F.ax.add_patch(Circle((x, y), r, fc=fill, ec=color, lw=0.7, zorder=5,
                          ls=(0, (1.2, 0.8)) if dashed else "-", alpha=0.4 if faded else 1))
    F.t(x, y + 0.05, lab, size=size, color=color, ha="center", weight="bold", zorder=6,
        alpha=0.4 if faded else 1)


def anode12(F, x, y, lab, color=INK, r=1.25, size=4.8):
    anode(F, x, y, lab, color=color, r=r, size=size)


def fig11():
    F = Fig(160, 145)
    # ======================================================== row 1: graph ===
    F.t(1, 2.2, "Weighted phasing graph", size=6, color=GREY, weight="bold")
    F.letter(1, 8, "a", "Graph construction")
    # reads
    xs = [6, 14, 22, 30, 38]
    RY = 15
    F.line(3, RY, 41, RY, color=INK, lw=0.9)
    for i, x in enumerate(xs):
        F.line(x, RY - 1.0, x, RY + 1.0, color=INK, lw=0.7)
        F.t(x, RY - 2.5, f"$v_{i+1}$", size=5.5, color=GREY, ha="center")
    reads = [  # (start idx, alleles, low-quality idx)
        (0, "rrara", None),
        (0, "aara", None),
        (1, "arar", 4),
    ]
    for j, (s0, al, lq) in enumerate(reads):
        y = RY + 5 + j * 4.2
        F.read(xs[s0] - 2.5, xs[s0 + len(al) - 1] + 2.5, y)
        F.t(1.5, y, f"read {j+1}", size=4.8, color=GREY, ha="left") if False else None
        for k, a in enumerate(al):
            anode(F, xs[s0 + k], y, a, r=1.2, dashed=(lq == s0 + k), size=4.8)
    F.t(3, RY + 18.5, "dashed: base quality below threshold", size=4.8, color=GREY)
    F.arrow(43, 24, 48, 24)
    # graph
    gx = [53, 62, 71, 80, 89]
    yr, ya = 20, 31
    edges = {}
    for s0, al, lq in reads:
        for i in range(len(al)):
            for d in (1, 2):  # k = 2 in this example
                j = i + d
                if j >= len(al):
                    continue
                key = (s0 + i, al[i], s0 + j, al[j])
                full = lq not in (s0 + i, s0 + j)
                edges[key] = edges.get(key, 0) + (1.0 if full else 0.1)
    for (i, ai, j, aj), w in edges.items():
        x1, y1 = gx[i], yr if ai == "r" else ya
        x2, y2 = gx[j], yr if aj == "r" else ya
        ls = (0, (1.2, 1.0)) if w < 0.5 else "-"
        lw = 0.5 + 0.6 * w if w >= 0.5 else 0.5
        if y1 == y2 and j - i == 2:
            F.arc(x1, x2, y1, (3.2 if y1 == yr else -3.2), color=GREY, lw=lw, ls=ls, z=2)
        else:
            F.line(x1, y1, x2, y2, color=GREY, lw=lw, ls=ls, z=2, cap="round")
    for i, x in enumerate(gx):
        anode(F, x, yr, "r")
        anode(F, x, ya, "a")
        F.t(x, 13.8, f"$v_{i+1}$", size=5.5, color=GREY, ha="center")
    # skipped variant beyond the maximum distance
    F.t(93.5, (yr + ya) / 2, "//", size=6, color=GREY, ha="center")
    anode(F, 98.5, yr, "r", color=GREY, faded=True)
    anode(F, 98.5, ya, "a", color=GREY, faded=True)
    F.t(98.5, 13.8, "skipped", size=4.8, color=GREY, ha="center")
    F.t(93.5, 37.5, "> maximum distance", size=4.8, color=GREY, ha="center")
    F.t(51, 42, r"edges to the alleles of the next $k$ variants ($k$ = 2 here)", size=4.8, color=GREY)
    F.line(51, 46.2, 55, 46.2, color=GREY, lw=1.4); F.t(56, 46.2, "full weight, summed over reads", size=4.8, color=GREY)
    F.line(82, 46.2, 86, 46.2, color=GREY, lw=0.5, ls=(0, (1.2, 1.0))); F.t(87, 46.2, "reduced weight", size=4.8, color=GREY)

    # b: pair support
    BX = 108
    F.line(BX - 3, 5, BX - 3, 48, color=LGREY, lw=0.4)
    F.letter(BX, 8, "b", "Pair support and ambiguity")
    gx0, gy0, cw, ch = BX + 10, 17, 8, 4.6
    F.t(gx0 + cw, gy0 - 3.4, "$v$", size=5.5, color=GREY, ha="center")
    F.t(BX + 3.2, gy0 + ch, "$u$", size=5.5, color=GREY, ha="center")
    anode(F, gx0 + cw / 2, gy0 - 1.3, "r", r=1.1, size=4.6)
    anode(F, gx0 + 1.5 * cw, gy0 - 1.3, "a", r=1.1, size=4.6)
    anode(F, gx0 - 2.4, gy0 + 0.6 + ch / 2, "r", r=1.1, size=4.6)
    anode(F, gx0 - 2.4, gy0 + 0.6 + 1.5 * ch, "a", r=1.1, size=4.6)
    cells = [["$w_{rr}$ = 9", "$w_{ra}$ = 1"], ["$w_{ar}$ = 0.1", "$w_{aa}$ = 7"]]
    for r_ in range(2):
        for c_ in range(2):
            diag = r_ == c_
            F.rect(gx0 + c_ * cw, gy0 + 0.6 + r_ * ch, cw, ch, fc=GREENL if diag else "white", ec=LGREY, lw=0.5, z=1)
            F.t(gx0 + (c_ + 0.5) * cw, gy0 + 0.6 + (r_ + 0.5) * ch, cells[r_][c_], size=4.8, ha="center",
                color=INK if diag else GREY)
    F.t(BX + 1, 33, r"$P = w_{rr} + w_{aa} = 16$", size=5.5)
    F.t(BX + 1, 37, r"$Q = w_{ra} + w_{ar} = 1.1$", size=5.5)
    F.t(BX + 1, 41.5, r"$s = \min(P,Q)\,/\,\max(P,Q) = 0.07$", size=5.5)

    F.line(1, 50, 159, 50, color=LGREY, lw=0.4)

    # ======================================================= row 2: voting ===
    F.t(1, 54, "Multi-neighbour voting", size=6, color=GREY, weight="bold")
    # c: vote weight against pair ambiguity, one line per pair type
    F.letter(1, 60, "c", "Vote weight")
    ax0, ax1 = 16, 70
    sx = lambda v: ax0 + (ax1 - ax0) * v
    levels = {"none": 79, 0.1: 75, 1: 70.5, 20: 64.8}   # categorical y positions
    for lab, y in [("no vote", levels["none"]), ("0.1", levels[0.1]), ("1", levels[1]), ("20", levels[20])]:
        F.t(ax0 - 1.5, y, lab, size=5, color=GREY, ha="right")
        F.line(ax0, y, ax1, y, color=VLGREY, lw=0.4, z=0)
    F.line(ax0, 62.5, ax0, 81, color=INK, lw=0.5)
    F.line(ax0, 81, ax1, 81, color=INK, lw=0.5)
    for v, lab in [(0, "0"), (0.1, "0.1"), (0.3, "0.3"), (0.7, r"$\tau$"), (1, "1")]:
        F.line(sx(v), 81, sx(v), 81.8, color=INK, lw=0.5)
        F.t(sx(v), 83.4, lab, size=5, color=GREY, ha="center")
    F.t((ax0 + ax1) / 2, 86.4, "pair ambiguity $s$", size=5, color=GREY, ha="center")
    F.t(3.5, 72, "vote weight", size=5, color=GREY, ha="center", rotation=90)

    def step(segs, color, lw, ls="-", dy=0.0):
        pts = []
        for x0, x1, lev in segs:
            y = levels[lev] + dy
            pts += [(sx(x0), y), (sx(x1), y)]
        F.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, ls=ls, zorder=3,
                  solid_joinstyle="miter", solid_capstyle="butt")
    step([(0, 0.1, 20), (0.1, 0.7, 1), (0.7, 1, "none")], INK, 1.1)
    step([(0, 0.1, 20), (0.1, 0.3, 1), (0.3, 1, "none")], AMBER, 0.9, ls=(0, (2.2, 1.2)), dy=0.9)
    step([(0, 0.7, 0.1), (0.7, 1, "none")], GREY, 0.9, dy=0.0)
    # key
    kx = 47
    F.line(kx, 61.0, kx + 4, 61.0, color=INK, lw=1.1); F.t(kx + 5, 61.0, "most pairs", size=4.8)
    F.line(kx, 64.0, kx + 4, 64.0, color=AMBER, lw=0.9, ls=(0, (2.2, 1.2))); F.t(kx + 5, 64.0, "SNV–5mC", size=4.8)
    F.line(kx, 67.0, kx + 4, 67.0, color=GREY, lw=0.9); F.t(kx + 5, 67.0, "repeat indel voter", size=4.8)

    # d: weighted votes
    DX = 80
    F.line(DX - 3, 56, DX - 3, 142, color=LGREY, lw=0.4)
    F.letter(DX, 60, "d", "Votes from up to $k$ upstream variants")
    ux = [DX + 6 + i * 11 for i in range(6)]  # 5 upstream + v
    y1, y2 = 70, 77
    F.line(DX + 2, y1, ux[4] + 3, y1, color=H1E, lw=1.3, z=1)
    F.line(DX + 2, y2, ux[4] + 3, y2, color=H2E, lw=1.3, z=1)
    ups = ["ra", "ar", "ra", "ra", "ar"]  # allele on hap1, hap2
    for i in range(5):
        anode(F, ux[i], y1, ups[i][0], color=H1)
        anode(F, ux[i], y2, ups[i][1], color=H2)
        F.t(ux[i], 64.8, f"$u_{i+1}$", size=5.5, color=GREY, ha="center")
    anode(F, ux[5], y1, "r", color=GREY)
    anode(F, ux[5], y2, "a", color=GREY)
    F.t(ux[5], 64.8, "$v$", size=5.5, color=INK, ha="center")
    votes = [(0, 20, 1), (1, 1, 1), (2, 1, 1), (3, 0.1, 1), (4, 1, 2)]  # upstream idx, weight, hap of v's r
    base = y2 + 2.4
    for i, w, h in votes:
        col = H1 if h == 1 else H2
        depth = 1.6 + 1.25 * (4 - i)
        F.arc(ux[i], ux[5], base, -depth, color=col, lw=0.35 + 0.07 * w, z=2)
        F.t(ux[i] - 1.0, base + 1.5, f"{w:g}", size=4.8, color=col, ha="right")
    # totals
    F.t(DX + 1, 94.5, "$h_1$", size=5.5, color=H1)
    F.t(DX + 1, 98.5, "$h_2$", size=5.5, color=H2)
    F.rect(DX + 6, 93.4, 44, 2.2, fc=H1, z=1); F.t(DX + 51.5, 94.5, "22.1", size=5)
    F.rect(DX + 6, 97.4, 2.0, 2.2, fc=H2, z=1); F.t(DX + 9.5, 98.5, "1", size=5)
    F.t(DX + 58, 96.5, "$v$: $r$ on haplotype 1", size=5, color=INK)

    # e: single-read guard (author, option A): one long read makes many weight-20 votes
    O = 90  # vertical offset of the panel
    F.line(1, 89, 75, 89, color=LGREY, lw=0.4)
    F.letter(1, O + 5, "e", "Single-read guard")
    ex = [6 + i * 9 for i in range(7)]          # u1..u6, v
    e1, e2 = O + 13, O + 18
    F.line(3, e1, ex[5] + 2.5, e1, color=H1E, lw=1.2); F.line(3, e2, ex[5] + 2.5, e2, color=H2E, lw=1.2)
    for i, al in enumerate("rarrar"):
        anode(F, ex[i], e1, al, color=H1, r=1.2, size=4.6)
        anode(F, ex[i], e2, "a" if al == "r" else "r", color=H2, r=1.2, size=4.6)
        F.t(ex[i], O + 8.6, f"$u_{i+1}$", size=5, color=GREY, ha="center")
    anode(F, ex[6], e1, "r", color=GREY, r=1.2, size=4.6); anode(F, ex[6], e2, "a", color=GREY, r=1.2, size=4.6)
    F.t(ex[6], O + 8.6, "$v$", size=5, color=INK, ha="center")
    F.read(ex[2] - 2, ex[6] + 2, O + 22.3, color=AMBERL, w=1.0)
    F.t(ex[2] - 2.5, O + 22.3, "one read", size=4.8, color=AMBER, ha="right")
    eb = O + 24.6
    for i, d in [(0, 4.6), (1, 4.0)]:
        F.arc(ex[i], ex[6], eb, -d, color=H1, lw=1.2, z=2)
    for i, d in [(2, 3.2), (3, 2.5), (4, 1.8), (5, 1.2)]:
        F.arc(ex[i], ex[6], eb, -d, color=H2, lw=0.8, ls=(0, (1.6, 1.0)), z=2)
    F.t(2, O + 33.5, "2 votes, 12 reads each", size=4.8, color=H1)
    F.t(40, O + 33.5, "4 votes, 1 read each", size=4.8, color=H2)
    F.t(2, O + 36.3, "weight 20 each", size=4.8, color=GREY)
    F.t(40, O + 36.3, "weight 20 each", size=4.8, color=GREY)

    def tally(x0, y, h1, h2, label, verdict, vcol, scale=0.32):
        F.t(x0, y - 3.0, label, size=5, color=GREY)
        F.t(x0, y, "$h_1$", size=5, color=H1)
        F.t(x0, y + 3.0, "$h_2$", size=5, color=H2)
        if h1:
            F.rect(x0 + 4, y - 0.9, h1 * scale, 1.8, fc=H1, z=1)
        F.t(x0 + 5 + h1 * scale, y, f"{h1:g}", size=4.8)
        if h2:
            F.rect(x0 + 4, y + 2.1, h2 * scale, 1.8, fc=H2, z=1)
        F.t(x0 + 5 + h2 * scale, y + 3.0, f"{h2:g}", size=4.8)
        F.t(x0 + 4, y + 6.4, verdict, size=5, color=vcol, weight="bold")

    tally(2, O + 45, 40, 80, "all votes", "$v$ follows the one read", H2)
    tally(40, O + 45, 40, 0, "with the guard", "$v$ follows the 12-read votes", H1)

    # f: blocks
    F.line(DX - 1, 110, 159, 110, color=LGREY, lw=0.4)
    F.letter(DX, 116, "f", "Phase blocks")
    bxs = [DX + 4 + i * 8 for i in range(9)]
    yb1, yb2 = 124, 130
    F.line(bxs[0], yb1, bxs[4], yb1, color=H1E, lw=1.3); F.line(bxs[0], yb2, bxs[4], yb2, color=H2E, lw=1.3)
    F.line(bxs[5], yb1, bxs[8], yb1, color=H1E, lw=1.3); F.line(bxs[5], yb2, bxs[8], yb2, color=H2E, lw=1.3)
    for i, x in enumerate(bxs):
        if i == 2:
            F.node(x, yb1, "white", GREY, r=1.0); F.node(x, yb2, "white", GREY, r=1.0)
            continue
        F.node(x, yb1, H1, AMBER if i == 5 else H1, r=1.0, lw=1.0 if i == 5 else 0.7)
        F.node(x, yb2, H2, AMBER if i == 5 else H2, r=1.0, lw=1.0 if i == 5 else 0.7)
    F.t(bxs[2], 133.6, "tie in block: unphased", size=4.8, color=GREY, ha="center")
    F.t(bxs[5] + 1, 133.6, "tie beyond last edge: new block", size=4.8, color=AMBER, ha="left")
    F.t((bxs[0] + bxs[4]) / 2, 119.6, "PS 1", size=5, ha="center", weight="bold")
    F.t((bxs[5] + bxs[8]) / 2, 119.6, "PS 2", size=5, ha="center", weight="bold")
    F.save("suppfig2_voting")


def fig12():
    F = Fig(160, 86)
    HC = {"r": H1, "a": H2}   # here haplotype 1 carries r at every variant

    # ---------------------------------------------------------------- a ------
    F.letter(1, 5, "a", "Read assignment to haplotypes")
    vx = [24 + i * 11 for i in range(6)]
    for i, x in enumerate(vx):
        F.t(x, 10.5, f"$v_{i+1}$", size=5.5, color=GREY, ha="center")
    reads = [
        ("rrrr-r", "1", "5 / 5", "haplotype 1"),
        ("aa-aaa", "2", "5 / 5", "haplotype 2"),
        ("rrar-r", "1", "4 / 5 = 0.80", "haplotype 1"),
        ("rаar--".replace("а", "a"), "-", "2 / 4 = 0.50", "not assigned"),
        ("--a---", "-", "one allele", "not assigned"),
    ]
    for j, (al, hap, frac, out) in enumerate(reads):
        y = 15 + j * 4.0
        idx = [i for i, a in enumerate(al) if a != "-"]
        col = H1E if hap == "1" else H2E if hap == "2" else LGREY
        F.t(3, y, f"read {j+1}", size=4.8, color=GREY)
        F.read(vx[idx[0]] - 3, vx[idx[-1]] + 3, y, color=col, w=0.9)
        for i in idx:
            anode12(F, vx[i], y, al[i], color=HC[al[i]])
        F.t(96, y, frac, size=5, color=GREY)
        F.t(118, y, out, size=5, color=H1 if hap == "1" else H2 if hap == "2" else GREY,
            weight="normal" if hap == "-" else "bold")
    F.t(96, 10.5, "majority fraction", size=4.8, color=GREY)

    F.line(1, 41, 159, 41, color=LGREY, lw=0.4)

    # ---------------------------------------------------------------- b ------
    F.letter(1, 47, "b", "Phase re-derivation from assigned reads")
    examples = [
        ("$v_3$", [("1", "r"), ("2", "a"), ("1", "a")], 2, 1, False),
        ("$v_1$", [("1", "r"), ("2", "a"), ("1", "r")], 3, 0, True),
    ]
    for e, (name, rds, n1, n2, kept) in enumerate(examples):
        ex = 3 + e * 50
        F.t(ex, 53.5, name, size=6, color=INK)
        for j, (h, a) in enumerate(rds):
            y = 58 + j * 3.6
            F.read(ex, ex + 18, y, color=H1E if h == "1" else H2E, w=0.9)
            anode12(F, ex + 9, y, a, color=HC[a], r=1.15)
            F.t(ex + 19.5, y, f"hap {h}", size=4.8, color=H1 if h == "1" else H2)
            ok = (h == "1" and a == "r") or (h == "2" and a == "a")
            F.t(ex + 27, y, "consistent" if ok else "conflicting", size=4.8, color=INK if ok else AMBER)
        rho = max(n1, n2) / (n1 + n2)
        F.t(ex, 72.5, f"$n_1$ = {n1},  $n_2$ = {n2}", size=5, color=GREY)
        bx, bw = ex, 30
        F.rect(bx, 75.5, bw, 2.2, fc=VLGREY, ec=LGREY, lw=0.4, z=1)
        F.rect(bx, 75.5, bw * rho, 2.2, fc=INK if kept else AMBER, z=2)
        F.line(bx + bw * 0.75, 74.5, bx + bw * 0.75, 78.7, color=GREY, lw=0.5, ls=(0, (1.2, 1.0)), z=3)
        F.t(bx + bw * 0.75, 80.6, r"$\theta_{\mathrm{var}}$", size=5, color=GREY, ha="center")
        F.t(bx + bw + 1.5, 76.6, rf"$\rho$ = {rho:.2f}", size=5)
        F.t(ex, 84, "phase kept" if kept else "left unphased", size=5, color=INK if kept else AMBER, weight="bold")

    # ---------------------------------------------------------------- c ------
    CX = 106
    F.line(CX - 3, 44, CX - 3, 85, color=LGREY, lw=0.4)
    F.letter(CX, 47, "c", "Phasing entropy")
    px0, px1, py0, py1 = CX + 8, CX + 50, 79, 54
    X = lambda p: px0 + (px1 - px0) * p
    Y = lambda v: py0 - (py0 - py1) * v
    pe = lambda p: 0.0 if p in (0, 1) else -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    ps = np.linspace(0.0005, 0.9995, 200)
    # shaded PE >= 0.8 (GNN window)
    lo, hi = [p for p in ps if pe(p) >= 0.8][0], [p for p in ps if pe(p) >= 0.8][-1]
    F.rect(X(lo), Y(1.0), X(hi) - X(lo), Y(0) - Y(1.0), fc=AMBERL, z=0)
    F.ax.plot([X(p) for p in ps], [Y(pe(p)) for p in ps], color=INK, lw=0.8, zorder=3)
    F.line(px0, py0, px1, py0, color=INK, lw=0.5); F.line(px0, py0, px0, py1 - 1, color=INK, lw=0.5)
    F.line(px0, Y(0.8), px1, Y(0.8), color=GREY, lw=0.4, ls=(0, (1.2, 1.0)), z=2)
    F.t(px0 - 1, Y(0.8), r"$\theta_{\mathrm{PE}}$", size=5, color=GREY, ha="right")
    for v in (0, 1):
        F.t(px0 - 1, Y(v), str(v), size=5, color=GREY, ha="right")
    for p in (0, 0.5, 1):
        F.t(X(p), py0 + 2.4, f"{p:g}", size=5, color=GREY, ha="center")
    F.t((px0 + px1) / 2, py0 + 5.2, r"$p_1 = h_1 / (h_1 + h_2)$", size=5, color=GREY, ha="center")
    F.t(px0 - 5.5, (py0 + py1) / 2, "PE", size=5, color=GREY, ha="center", rotation=90)
    for h1, h2 in [(22.1, 1), (3, 1), (5, 5)]:
        p = h1 / (h1 + h2)
        F.node(X(p), Y(pe(p)), INK, "white", r=0.8, lw=0.4, z=5)
        if p > 0.9:
            F.t(X(p) - 1.5, Y(pe(p)), f"{h1:g}:{h2:g}", size=4.6, color=INK, ha="right")
        else:
            F.t(X(p) + (1.3 if p > 0.6 else 0), Y(pe(p)) - 2.0, f"{h1:g}:{h2:g}", size=4.6, color=INK,
                ha="left" if p > 0.6 else "center")
    F.t((X(lo) + X(hi)) / 2, Y(0.12), "GNN window", size=4.8, color=AMBER, ha="center")

    F.save("suppfig3_read_correction")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    fig9()
    fig10()
    fig11()
    fig12()
