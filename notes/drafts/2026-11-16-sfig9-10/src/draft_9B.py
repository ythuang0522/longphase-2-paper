"""Draft 9B: modcall shown on one worked region, with a status grid per CpG."""
from common import *

F = Fig(160, 76)
TOP = 5
F.letter(1, TOP, "a", "Allele-specific 5mC calling in one region")

S1, S2 = 12, 100
C = {1: 24, 2: 36, 3: 48, 4: 62, 5: 82, 6: 85}
RY = 13
F.line(5, RY, 105, RY, color=INK, lw=0.9)
for x in [S1, S2]:
    F.line(x, RY - 1.1, x, RY + 1.1, color=INK, lw=0.7)
    F.t(x, RY - 2.6, "SNV", size=5, color=GREY, ha="center")
for k, x in C.items():
    F.line(x, RY - 1.1, x, RY + 1.1, color=INK, lw=0.7)
    F.t(x + (-0.8 if k == 5 else 0.8 if k == 6 else 0), RY - 2.6, f"{k}", size=5, color=GREY, ha="center")
F.t(30, RY - 2.6, "", size=5)
F.t(4, RY - 2.6, "CpG", size=5, color=GREY, ha="right") if False else None

# reads: (hap, x1, x2, {site: state})
reads = [
    (1, 6, 52, {1: "m", 2: "m", 3: "m"}),
    (2, 7, 56, {1: "u", 2: "m", 3: "m"}),
    (1, 5, 41, {1: "m", 2: "m"}),
    (2, 9, 50, {1: "u", 2: "m", 3: "u"}),
    (1, 18, 66, {1: "m", 2: "a", 3: "u", 4: "m"}),
    (2, 30, 54, {2: "m", 3: "u"}),
    (1, 56, 88, {4: "m", 5: "m", 6: "m"}),
    (2, 54, 90, {4: "u", 5: "u", 6: "u"}),
    (1, 72, 104, {5: "m", 6: "m"}),
    (2, 74, 105, {5: "u", 6: "a"}),
    (1, 78, 103, {5: "m", 6: "m"}),
]
for i, (h, x1, x2, st) in enumerate(reads):
    y = 17.5 + i * 2.75
    F.read(x1, x2, y, w=0.9)
    if x1 <= S1 <= x2:
        F.snv(S1, y, "A" if h == 1 else "G", h, r=1.05, size=4.5)
    if x1 <= S2 <= x2:
        F.snv(S2, y, "T" if h == 1 else "C", h, r=1.05, size=4.5)
    for k, s in st.items():
        F.meth(C[k], y, s, r=0.72)

# status grid -----------------------------------------------------------
gy0 = 50.5
rows = ["candidate", "SNV link", "CpG link", "neighbours"]
status = {  # per CpG: one symbol per row; '' = not tested
    1: ["y", "y", "", "y"],
    2: ["n", "", "", ""],
    3: ["y", "n", "n", ""],
    4: ["y", "n", "y", "y"],
    5: ["y", "y", "", "y"],
    6: ["y", "y", "", "y"],
}
for r, lab in enumerate(rows):
    y = gy0 + r * 4.2
    F.rect(5, y - 2.1, 100, 4.2, fc=VLGREY if r % 2 == 0 else "white", z=0)
    F.t(6, y, lab, size=5, color=GREY)
    for k, sym in status.items():
        if sym[r] == "y":
            F.tick(C[k] if k < 5 else (C[k] - 0.6 if k == 5 else C[k] + 0.6), y, s=0.7)
        elif sym[r] == "n":
            F.cross(C[k], y, s=0.6, color=H2)
        else:
            F.t(C[k] if k < 5 else (C[k] - 0.6 if k == 5 else C[k] + 0.6), y, "–", size=5, color=LGREY, ha="center")
# merged loci
my = gy0 + 4 * 4.2 + 0.8
F.t(6, my + 0.6, "locus", size=5, color=GREY)
for x0, x1, lab in [(C[1], C[1], ""), (C[4], C[4], ""), (C[5], C[6], "")]:
    if x0 == x1:
        F.lollipop(x0, my + 2.2, "m", 1, stem=1.4, r=0.7)
    else:
        F.line(x0, my - 0.6, x0, my + 0.2, color=GREY, lw=0.5)
        F.line(x1, my - 0.6, x1, my + 0.2, color=GREY, lw=0.5)
        F.line(x0, my + 0.2, x1, my + 0.2, color=GREY, lw=0.5)
        F.lollipop((x0 + x1) / 2, my + 2.2, "m", 1, stem=1.4, r=0.7)
F.t(C[6] + 2.5, my + 1.2, "2 CpGs merged", size=5, color=GREY)

# ---------------------------------------------------------------- b ------
BX = 112
F.line(BX - 2.5, 3, BX - 2.5, 72, color=LGREY, lw=0.4)
F.letter(BX, TOP, "b", "Criteria")
F.t(BX + 1, 12, "Candidate", size=6, weight="bold")
F.t(BX + 1, 16.5, r"$\min(M,U)\,/\,\max(M,U) \geq \alpha$", size=5.5)
F.t(BX + 1, 20.5, r"$A\,/\,(M+U+A) \leq \beta$", size=5.5)
F.t(BX + 1, 27.5, "Linkage (SNV and CpG 1)", size=6, weight="bold")
gx, gy, cw, ch = BX + 9, 33, 6.5, 4.2
F.meth(gx + cw / 2, gy - 1.2, "m", r=0.75)
F.meth(gx + 1.5 * cw, gy - 1.2, "u", r=0.75)
F.snv(gx - 2.4, gy + ch / 2 + 0.3, "A", 1, r=1.2, size=5)
F.snv(gx - 2.4, gy + 1.5 * ch + 0.3, "G", 2, r=1.2, size=5)
for r_ in range(2):
    for c_ in range(2):
        diag = r_ == c_
        cnt = [[2, 0], [0, 2]][r_][c_]
        F.rect(gx + c_ * cw, gy + 0.3 + r_ * ch, cw, ch, fc=GREENL if diag else "white", ec=LGREY, lw=0.5, z=1)
        F.t(gx + (c_ + 0.5) * cw, gy + 0.3 + (r_ + 0.5) * ch, str(cnt), size=6, ha="center",
            weight="bold" if diag else "normal", color=INK if diag else GREY)
F.t(BX + 1, 47, r"$\frac{\max(RR+AA,\,RA+AR)}{RR+AA+RA+AR} \geq \gamma$", size=6)
F.t(BX + 1, 54, "Stages", size=6, weight="bold")
for i, s in enumerate(["1  test against an SNV", "2  test against accepted CpGs", "3  keep if linked to both",
                       "    neighbouring accepted sites"]):
    F.t(BX + 1, 58.5 + i * 3.6, s, size=5)

# key
ky = 73.5
F.meth(6, ky, "m"); F.t(7.6, ky, "methylated", size=5)
F.meth(24, ky, "u"); F.t(25.6, ky, "unmethylated", size=5)
F.meth(44, ky, "a"); F.t(45.6, ky, "ambiguous", size=5)
F.snv(62, ky, "A", 1, r=1.05, size=4.5); F.snv(65, ky, "G", 2, r=1.05, size=4.5); F.t(67, ky, "SNV alleles", size=5)
F.tick(84, ky, s=0.7); F.t(85.6, ky, "passed", size=5)
F.cross(96, ky, s=0.6); F.t(97.6, ky, "failed", size=5)

F.save("draft_9B")
