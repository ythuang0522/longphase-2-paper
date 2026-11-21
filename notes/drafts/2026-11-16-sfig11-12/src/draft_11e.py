"""Panel 11e options: single-read guard."""
from common import *


def anode(F, x, y, lab, color=INK, r=1.2, size=4.6):
    F.ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=0.7, zorder=5))
    F.t(x, y + 0.05, lab, size=size, color=color, ha="center", weight="bold", zorder=6)


def tally(F, x0, y, h1, h2, scale, label, verdict, vcol):
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


# ------------------------------------------------------------- option A --
F = Fig(76, 58)
F.letter(1, 5, "e", "Single-read guard")
ux = [6 + i * 9 for i in range(7)]          # u1..u6, v
y1, y2 = 13, 18
F.line(3, y1, ux[5] + 2.5, y1, color=H1E, lw=1.2); F.line(3, y2, ux[5] + 2.5, y2, color=H2E, lw=1.2)
hap1 = "rarrar"
for i in range(6):
    anode(F, ux[i], y1, hap1[i], color=H1)
    anode(F, ux[i], y2, "a" if hap1[i] == "r" else "r", color=H2)
    F.t(ux[i], 8.6, f"$u_{i+1}$", size=5, color=GREY, ha="center")
anode(F, ux[6], y1, "r", color=GREY); anode(F, ux[6], y2, "a", color=GREY)
F.t(ux[6], 8.6, "$v$", size=5, color=INK, ha="center")
# the one long read
F.read(ux[2] - 2, ux[6] + 2, 22.3, color=AMBERL, w=1.0)
F.t(ux[2] - 2.5, 22.3, "one read", size=4.8, color=AMBER, ha="right")
base = 24.6
# strong votes (many reads, haplotype 1)
for i, d in [(0, 4.6), (1, 4.0)]:
    F.arc(ux[i], ux[6], base, -d, color=H1, lw=1.2, z=2)
# weak votes (one read each, haplotype 2)
for i, d in [(2, 3.2), (3, 2.5), (4, 1.8), (5, 1.2)]:
    F.arc(ux[i], ux[6], base, -d, color=H2, lw=0.8, ls=(0, (1.6, 1.0)), z=2)
F.t(ux[0] - 1, base + 1.3, "12 reads each", size=4.8, color=H1, ha="left") if False else None
F.t(2, 33.5, "2 votes, 12 reads each", size=4.8, color=H1)
F.t(40, 33.5, "4 votes, 1 read each", size=4.8, color=H2)
F.t(2, 36.3, "weight 20 each", size=4.8, color=GREY)
F.t(40, 36.3, "weight 20 each", size=4.8, color=GREY)
tally(F, 2, 45, 40, 80, 0.32, "all votes", "v follows the one read", H2)
tally(F, 40, 45, 40, 0, 0.32, "with the guard", "", INK)
F.t(44, 51.4, "v follows the 12-read votes", size=5, color=H1, weight="bold")
F.save("draft_11e_A")

# ------------------------------------------------------------- option B --
F = Fig(76, 46)
F.letter(1, 5, "e", "Single-read guard")
cols = [3, 16, 30, 44, 58]
heads = ["vote from", "reads", "weight", "$r$ of $v$ on", "counted"]
for x, h in zip(cols, heads):
    F.t(x, 10, h, size=5, color=GREY)
F.line(2, 11.8, 74, 11.8, color=LGREY, lw=0.4)
rows = [("$u_1$", 12, 20, 1), ("$u_2$", 12, 20, 1), ("$u_3$", 1, 20, 2), ("$u_4$", 1, 20, 2),
        ("$u_5$", 1, 20, 2), ("$u_6$", 1, 20, 2)]
for j, (u, n, w, h) in enumerate(rows):
    y = 14.5 + j * 3.2
    weak = n <= 1
    if weak:
        F.rect(2, y - 1.5, 72, 3.0, fc=AMBERL, z=0)
    F.t(cols[0], y, u, size=5)
    F.t(cols[1], y, str(n), size=5)
    F.t(cols[2], y, str(w), size=5)
    F.t(cols[3], y, f"haplotype {h}", size=5, color=H1 if h == 1 else H2)
    if weak:
        F.cross(cols[4] + 1, y, s=0.6, color=GREY)
    else:
        F.tick(cols[4] + 1, y, s=0.6)
F.line(2, 34.0, 74, 34.0, color=LGREY, lw=0.4)
F.t(3, 37, "all votes", size=5, color=GREY); F.t(30, 37, "$h_1$ = 40,  $h_2$ = 80", size=5); F.t(58, 37, "haplotype 2", size=5, color=H2, weight="bold")
F.t(3, 41, "with the guard", size=5, color=GREY); F.t(30, 41, "$h_1$ = 40,  $h_2$ = 0", size=5); F.t(58, 41, "haplotype 1", size=5, color=H1, weight="bold")
F.save("draft_11e_B")
