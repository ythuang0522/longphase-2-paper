"""Draft: Supplementary Fig. 11 (weighted phasing graph + multi-neighbour voting)."""
from common import *


def anode(F, x, y, lab, color=INK, r=1.35, faded=False, dashed=False, fill="white", size=5):
    F.ax.add_patch(Circle((x, y), r, fc=fill, ec=color, lw=0.7, zorder=5,
                          ls=(0, (1.2, 0.8)) if dashed else "-", alpha=0.4 if faded else 1))
    F.t(x, y + 0.05, lab, size=size, color=color, ha="center", weight="bold", zorder=6,
        alpha=0.4 if faded else 1)


F = Fig(160, 129)

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
# c: vote rule
F.letter(1, 60, "c", "Vote weight")
ax0, ax1, ay = 4, 70, 70
sx = lambda v: ax0 + (ax1 - ax0) * v
F.rect(sx(0), ay - 2.5, sx(0.1) - sx(0), 5, fc=GREENL, ec=INK, lw=0.4, z=1)
F.rect(sx(0.1), ay - 2.5, sx(0.7) - sx(0.1), 5, fc=VLGREY, ec=INK, lw=0.4, z=1)
F.rect(sx(0.7), ay - 2.5, sx(1) - sx(0.7), 5, fc="white", ec=INK, lw=0.4, z=1)
F.t(sx(0.0), ay - 4.6, "weight 20", size=5, ha="left", weight="bold", color=GREEN)
F.t(sx(0.4), ay, "weight 1", size=5, ha="center")
F.t(sx(0.85), ay, "no vote", size=5, ha="center", color=GREY)
F.line(sx(0.3), ay - 3.5, sx(0.3), ay + 3.5, color=AMBER, lw=0.7, ls=(0, (1.5, 1.0)), z=3)
F.t(sx(0.3), ay - 4.6, "SNV–5mC", size=4.8, ha="center", color=AMBER)
for v, lab in [(0, "0"), (0.1, "0.1"), (0.7, r"$\tau$"), (1, "1")]:
    F.t(sx(v), ay + 4.6, lab, size=5, color=GREY, ha="center")
F.t((ax0 + ax1) / 2, ay + 8.2, "pair ambiguity $s$", size=5, color=GREY, ha="center")
F.t(ax0, ay + 12.5, "an indel in a tandem repeat votes with weight 0.1", size=4.8, color=INK)

# d: weighted votes
DX = 80
F.line(DX - 3, 56, DX - 3, 126, color=LGREY, lw=0.4)
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

# e: single-read guard
F.line(1, 89, 75, 89, color=LGREY, lw=0.4)
F.letter(1, 95, "e", "Single-read guard")
bx0, bw1 = 22, 50
vals = [(0.4, True), (0.6, True), (0.8, True), (0.9, True), (3.0, False), (5.5, False), (8.5, False)]
for i, (v, weak) in enumerate(vals):
    y = 100 + i * 2.8
    F.rect(bx0, y - 0.8, bw1 * v / 10, 1.6, fc=AMBER if weak else INK, z=2, ec="none")
    if weak:
        F.cross(bx0 + bw1 * v / 10 + 2.2, y, s=0.6, color=GREY)
F.line(bx0 + bw1 * 0.1, 98.6, bx0 + bw1 * 0.1, 119.5, color=GREY, lw=0.4, ls=(0, (1.2, 1.0)))
F.t(bx0 + bw1 * 0.1, 121.6, "1 read", size=4.8, color=GREY, ha="center")
F.t(bx0 + bw1, 121.6, "support", size=4.8, color=GREY, ha="right")
F.t(3, 104.2, "4 votes with", size=4.8, color=AMBER)
F.t(3, 107.0, "support of 1 read:", size=4.8, color=AMBER)
F.t(3, 109.8, "not counted", size=4.8, color=AMBER)
F.t(3, 116.0, "stronger votes:", size=4.8, color=INK)
F.t(3, 118.8, "counted", size=4.8, color=INK)

# f: blocks
F.line(DX - 1, 102, 159, 102, color=LGREY, lw=0.4)
F.letter(DX, 108, "f", "Phase blocks")
bxs = [DX + 4 + i * 8 for i in range(9)]
yb1, yb2 = 116, 122
F.line(bxs[0], yb1, bxs[4], yb1, color=H1E, lw=1.3); F.line(bxs[0], yb2, bxs[4], yb2, color=H2E, lw=1.3)
F.line(bxs[5], yb1, bxs[8], yb1, color=H1E, lw=1.3); F.line(bxs[5], yb2, bxs[8], yb2, color=H2E, lw=1.3)
for i, x in enumerate(bxs):
    if i == 2:
        F.node(x, yb1, "white", GREY, r=1.0); F.node(x, yb2, "white", GREY, r=1.0)
        continue
    F.node(x, yb1, H1, AMBER if i == 5 else H1, r=1.0, lw=1.0 if i == 5 else 0.7)
    F.node(x, yb2, H2, AMBER if i == 5 else H2, r=1.0, lw=1.0 if i == 5 else 0.7)
F.t(bxs[2], 125.6, "tie in block: unphased", size=4.8, color=GREY, ha="center")
F.t(bxs[5] + 1, 125.6, "tie beyond last edge: new block", size=4.8, color=AMBER, ha="left")
F.t((bxs[0] + bxs[4]) / 2, 111.6, "PS 1", size=5, ha="center", weight="bold")
F.t((bxs[5] + bxs[8]) / 2, 111.6, "PS 2", size=5, ha="center", weight="bold")
F.save("draft_11")
