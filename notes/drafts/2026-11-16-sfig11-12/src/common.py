"""Shared drawing helpers for the Supplementary Fig. 9/10 drafts (mm coordinates, y down)."""
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
        self.fig.savefig(path + ".png", dpi=300)
        self.fig.savefig(path + ".pdf")
        plt.close(self.fig)
