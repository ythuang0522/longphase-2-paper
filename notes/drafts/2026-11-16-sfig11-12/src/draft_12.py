"""Draft: Supplementary Fig. 12 (read-based correction + phasing entropy)."""
from common import *


def anode(F, x, y, lab, color=INK, r=1.25, size=4.8):
    F.ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=0.7, zorder=5))
    F.t(x, y + 0.05, lab, size=size, color=color, ha="center", weight="bold", zorder=6)


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
        anode(F, vx[i], y, al[i], color=HC[al[i]])
    F.t(96, y, frac, size=5, color=GREY)
    F.t(118, y, out, size=5, color=H1 if hap == "1" else H2 if hap == "2" else GREY,
        weight="normal" if hap == "-" else "bold")
F.t(96, 10.5, "majority fraction", size=4.8, color=GREY)
F.t(3, 37.5, r"A read is assigned when its majority fraction exceeds $\theta_{\mathrm{read}}$ and its evidence is sufficient;"
    " indels have a lower weight and 5mC is not used.", size=4.8, color=GREY)

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
        anode(F, ex + 9, y, a, color=HC[a], r=1.15)
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

F.save("draft_12")
