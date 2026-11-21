"""Draft 9A: modcall in four steps, one row, in the order of the Methods."""
from common import *

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
# consecutive CpGs merged into one locus
seq = "CGCG"
for i, b in enumerate(seq):
    F.t(DX + 7 + i * 3.2, 12, b, size=6, ha="center", weight="bold", color=INK)
F.rect(DX + 5.5, 9.9, 3.2 * 4, 4.2, fc="none", ec=LGREY, lw=0.5, z=0, r=0.6)
F.t(DX + 23.5, 12, "2 CpGs", size=5, color=GREY)
for j, (s1, s2) in enumerate([("m", "m"), ("u", "u"), ("m", None), (None, "u")]):
    y = 16.8 + j * 2.7
    x1 = DX + 6.8 if s1 else DX + 12
    x2 = DX + 17.5 if s2 else DX + 10
    F.read(x1 - 1, x2 + 1, y, w=0.9)
    if s1: F.meth(DX + 7.0, y, s1, r=0.7)
    if s2: F.meth(DX + 13.4, y, s2, r=0.7)
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

F.save("draft_9A")
