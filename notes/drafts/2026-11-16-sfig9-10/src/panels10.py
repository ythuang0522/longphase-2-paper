"""Panels for the Supplementary Fig. 10 drafts (10A and 10B)."""
from common import *


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


def tr_indel(F, x0, y0):
    """Indel in a tandem repeat: kept, votes with a lower weight."""
    seq = "GCACACACACAT"
    for i, b in enumerate(seq):
        F.t(x0 + 2 + i * 2.6, y0 + 4, b, size=5.5, ha="center", color=INK)
    F.rect(x0 + 2 + 0.6 * 2.6, y0 + 2.2, 2.6 * 10, 3.6, fc=AMBERL, z=0)
    F.vbox(x0 + 2 + 5.5 * 2.6, y0 + 10, "+CA", 2, w=5.0, h=2.6, size=4.8, dashed=True)
    F.t(x0 + 2, y0 + 15.5, "kept in the graph; its votes have a lower weight", size=5, color=INK)


def hp_snv(F, x0, y0):
    """Nanopore homopolymer SNV filter."""
    seq = "GTAAAAACAAAATG"
    for i, b in enumerate(seq):
        F.t(x0 + 2 + i * 2.4, y0 + 4, b, size=5.5, ha="center", color=INK)
    F.rect(x0 + 2 + 1.6 * 2.4, y0 + 2.2, 2.4 * 5, 3.6, fc=AMBERL, z=0)
    F.rect(x0 + 2 + 7.6 * 2.4, y0 + 2.2, 2.4 * 4, 3.6, fc=AMBERL, z=0)
    for k, (i, lab) in enumerate([(6, "SNV 1"), (7, "SNV 2")]):
        xx = x0 + 2 + i * 2.4
        F.line(xx, y0 + 6.3, xx, y0 + 8.0, color=INK, lw=0.6)
        F.t(xx + (-0.6 if k == 0 else 0.6), y0 + 9.8, lab, size=5, ha="right" if k == 0 else "left")
    F.cross(x0 + 2 + 7 * 2.4 + 4.2, y0 + 12.4, s=0.7)
    F.t(x0 + 2 + 7 * 2.4 + 5.4, y0 + 12.4, "removed", size=5, color=H2)
    F.t(x0 + 2, y0 + 16.5, "two close SNVs in homopolymers: the downstream SNV is removed", size=5, color=INK)
