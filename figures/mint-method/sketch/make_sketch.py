#!/usr/bin/env python3
"""Layout sketch for redrawing the MINT method figure in the dense
NSA / FR-CSU style.  Red letters mark design notes listed below the frame.

Run:  python3 make_sketch.py <media_dir>   (media_dir = ppt/media of mint-method.pptx)
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image

MEDIA = Path(sys.argv[1] if len(sys.argv) > 1 else "media")
OUT = Path(__file__).with_name("mint_layout_sketch.svg")

INK, MUTED = "#1F2933", "#5F6B78"
B = dict(dk="#2F5F86", st="#4F81B0", lo="#EAF2FB", hi="#3F7FC6", fill="#F2F7FC")
O = dict(dk="#9A5310", st="#D9822B", lo="#FDF1E3", hi="#E07B1F", fill="#FEF7EE")
G = dict(dk="#2E6B2A", st="#4E9A46", lo="#EDF7EA", hi="#4A9E3B", fill="#F3FAF1")
RED = "#E03131"
SANS = "Helvetica, Arial, 'Liberation Sans', sans-serif"
SERIF = "'Times New Roman', 'Liberation Serif', serif"
CJK = "'PingFang SC', 'Microsoft YaHei', 'WenQuanYi Zen Hei', sans-serif"
W, H = 1600, 1110
out = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=15, fill=INK, bold=False, italic=False, anchor="start", family=None, halo=False):
    a = ' font-weight="700"' if bold else ""
    a += ' font-style="italic"' if italic else ""
    a += f' text-anchor="{anchor}"' if anchor != "start" else ""
    a += f' font-family="{family}"' if family else ""
    a += ' stroke="#fff" stroke-width="5" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    out.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}"{a}>{esc(s)}</text>')


def MT(x, y, base, sub=None, sup=None, size=17, fill=INK, anchor="start", bold=False):
    """Math-ish label in serif italic: base, optional sub/superscript."""
    w = ' font-weight="700"' if bold else ""
    s = f'<tspan>{esc(base)}</tspan>'
    if sup and sub:
        s += (f'<tspan font-size="{size * .7:.1f}" dy="{-size * .38:.1f}">{esc(sup)}</tspan>'
              f'<tspan font-size="{size * .7:.1f}" dx="{-size * .32:.1f}" dy="{size * .68:.1f}">{esc(sub)}</tspan>')
    elif sub:
        s += f'<tspan font-size="{size * .7:.1f}" dy="{size * .3:.1f}">{esc(sub)}</tspan>'
    elif sup:
        s += f'<tspan font-size="{size * .7:.1f}" dy="{-size * .38:.1f}">{esc(sup)}</tspan>'
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    out.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}" font-family="{SERIF}" '
               f'font-style="italic" fill="{fill}"{w}{an}>{s}</text>')


def R(x, y, w, h, fill="#fff", stroke="#9AA4AE", sw=1.2, rx=8, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    d += f' opacity="{op}"' if op else ""
    out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def P(d, stroke="#5F6B78", sw=1.5, arrow=True, dash=None, fill="none", op=None):
    m = f' marker-end="url(#ah{stroke[1:]})"' if arrow else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    da += f' stroke-opacity="{op}"' if op else ""
    out.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-linejoin="round"{da}{m}/>')


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def cells(x, y, vals, c, pal, rows=None):
    """vals: list (one row) or list of lists; shade = value in [0, 1]."""
    grid = vals if isinstance(vals[0], list) else [vals]
    g = [f'<g stroke="{pal["st"]}" stroke-width="0.8">']
    for r, row in enumerate(grid):
        for i, v in enumerate(row):
            g.append(f'<rect x="{x + i * c:g}" y="{y + r * c:g}" width="{c}" height="{c}" '
                     f'fill="{mix(pal["lo"], pal["hi"], v)}"/>')
    g.append("</g>")
    out.append("".join(g))
    out.append(f'<rect x="{x:g}" y="{y:g}" width="{len(grid[0]) * c}" height="{len(grid) * c}" '
               f'fill="none" stroke="{pal["st"]}" stroke-width="1.3"/>')


def snow(cx, cy, size=18, color="#5D89AA"):
    s = size / 24
    out.append(
        f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({s:.3f})" fill="none" '
        f'stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M10 4l2 1l2 -1M12 2v6.5l3 1.72M17.928 6.268l.134 2.232l1.866 1.232M20.66 7l-5.629 3.25l.01 3.458'
        'M19.928 14.268l-1.866 1.232l-.134 2.232M20.66 17l-5.629 -3.25l-2.99 1.738M14 20l-2 -1l-2 1M12 22v-6.5l-3 -1.72'
        'M6.072 17.732l-.134 -2.232l-1.866 -1.232M3.34 17l5.629 -3.25l-.01 -3.458M4.072 9.732l1.866 -1.232l.134 -2.232'
        'M3.34 7l5.629 3.25l2.99 -1.738"/></g>')


def tag(x, y, letter):
    out.append(f'<g><circle cx="{x}" cy="{y}" r="11" fill="{RED}"/>'
               f'<text x="{x}" y="{y + 5}" font-size="14" font-weight="700" fill="#fff" '
               f'text-anchor="middle">{letter}</text></g>')


def num(x, y, n, color=INK):
    out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#fff" stroke="{color}" stroke-width="1.4"/>'
               f'<text x="{x}" y="{y + 5}" font-size="13" font-weight="700" fill="{color}" '
               f'text-anchor="middle">{n}</text>')


FR = []
for fn in ["image.png", "image2.png", "image3.png", "image4.png"]:
    im = Image.open(MEDIA / fn).convert("RGB").resize((224, 126), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    FR.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())


def frame(k, x, y, w):
    h = w * 9 / 16
    out.append(f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" href="{FR[k % 4]}" '
               f'xlink:href="{FR[k % 4]}" preserveAspectRatio="xMidYMid slice"/>'
               f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="none" stroke="#55606B" stroke-width="0.8"/>')


# ================================================================ frame
R(16, 16, 1568, 756, fill="#FFFFFF", stroke="#9AA4AE", sw=1.4, rx=10, dash="7 5")

# ------------------------------------------------ A: video strip -> groups
MT(44, 70, "V", size=26, bold=True)
T(44, 92, "video", 13, MUTED)
X0, FW = 84, 56
for k in range(12):
    frame(k, X0 + k * 60, 44, FW)
R(X0 + 6 * 60 - 3, 41, 2 * 60 + 2, 37.5, fill="none", stroke=INK, sw=1.8, rx=3, dash="4 3")
groups = [(0, 90, "1"), (2, 250, "2"), (6, 450, "g"), (10, 690, "n")]
for fi, bx, lab in groups:
    xs = X0 + fi * 60
    out.append(f'<path d="M {xs} 76 L {xs + 116} 76 L {bx + 104} 120 L {bx} 120 Z" fill="#CFE0F3" opacity="0.55"/>')
for fi, bx, lab in groups:
    cur = lab == "g"
    R(bx, 120, 104, 36, fill=B["fill"], stroke=INK if cur else B["st"], sw=1.8 if cur else 1.2, rx=5,
      dash="4 3" if cur else None)
    frame(fi, bx + 5, 125, 46)
    frame(fi + 1, bx + 53, 125, 46)
    MT(bx + 52, 177, "G", sub=lab, size=17, anchor="middle")
T(392, 144, "…", 20, MUTED, anchor="middle")
T(622, 144, "…", 20, MUTED, anchor="middle")
T(560, 177, "current group", 13, MUTED, italic=True)
T(442, 104, "Split into two-frame groups", 15, B["dk"], bold=True, anchor="middle", halo=True)
num(330, 99, "1", B["dk"])
for bx in (142, 302, 502, 742):
    P(f"M {bx} 183 V 190", arrow=False, sw=1.3)
P("M 142 190 H 742", arrow=False, sw=1.3)
P("M 360 190 V 200", sw=1.3)
tag(28, 120, "A")

# ------------------------------------------------ B: question
R(828, 40, 228, 72, fill=O["lo"], stroke=O["st"], sw=1.3, rx=8)
R(842, 51, 20, 20, fill="#EE9A35", stroke=O["dk"], sw=1.2, rx=2)
T(870, 67, "Question + options", 15, O["dk"], bold=True)
T(842, 90, "What happened after the person", 13.5, INK, italic=True)
T(842, 106, "raised their hand?", 13.5, INK, italic=True)
MT(1022, 68, "q", size=19, fill=O["dk"], bold=True)
P("M 930 112 V 297", stroke=O["st"], sw=1.5)
tag(816, 40, "B")

# ------------------------------------------------ C: frozen backbone
R(84, 200, 972, 252, fill="#F7F8FA", stroke="#8C96A2", sw=1.3, rx=10, dash="6 4")
snow(112, 220, 18)
T(128, 225, "Frozen Qwen3.5-2B  ·  hybrid block ×2 (layers 9–16)  ·  3× GDN → full attention",
  15, INK, bold=True)
tag(84, 200, "C")

# ---- D: memory branch (GDN)
R(100, 236, 520, 204, fill="#FFFFFF", stroke=B["st"], sw=1.6, rx=10)
for dx, dy in [(0, 0), (8, 0), (0, 8), (8, 8)]:
    R(112 + dx, 252 + dy, 6.5, 6.5, fill=B["hi"], stroke="none", rx=1)
T(134, 264, "Memory Novelty", 17, B["dk"], bold=True)
T(276, 264, "GDN state: predict, then compare", 13.5, MUTED, italic=True)
MT(150, 283, "S", sub="g", sup="−", size=16, fill=B["dk"], anchor="middle")
cells(120, 290, [[.35, .6, .2, .5, .3], [.5, .25, .7, .3, .45], [.2, .55, .35, .6, .25]], 12, B)
MT(150, 342, "k", sub="i", size=16, fill=B["dk"], anchor="middle")
cells(120, 348, [.3, .7, .2, .5, .4], 12, B)
R(206, 312, 66, 24, fill=B["fill"], stroke=B["st"], sw=1.2, rx=12)
T(239, 329, "predict", 13.5, B["dk"], bold=True, anchor="middle")
P("M 180 308 H 192 V 318 H 205", stroke=B["st"], sw=1.3)
P("M 180 354 H 192 V 330 H 205", stroke=B["st"], sw=1.3)
MT(330, 291, "v̂", sub="i", size=16, fill=B["dk"], anchor="middle")
cells(300, 296, [.4, .55, .3, .5, .35], 12, B)
MT(330, 340, "v", sub="i", size=16, fill=B["dk"], anchor="middle")
cells(300, 346, [.4, .9, .3, .15, .35], 12, B)
P("M 272 324 H 286 V 302 H 299", stroke=B["st"], sw=1.3)
R(396, 312, 76, 24, fill=B["fill"], stroke=B["st"], sw=1.2, rx=12)
T(434, 329, "residual", 13.5, B["dk"], bold=True, anchor="middle")
P("M 360 302 H 380 V 318 H 395", stroke=B["st"], sw=1.3)
P("M 360 352 H 380 V 330 H 395", stroke=B["st"], sw=1.3)
P("M 472 324 H 514 A 6 6 0 0 1 520 330 V 469", stroke=B["st"], sw=1.6)
T(530, 356, "normalize,", 13.5, MUTED, italic=True)
T(530, 373, "mean over", 13.5, MUTED, italic=True)
T(530, 390, "heads/layers", 13.5, MUTED, italic=True)
# memory advance lane
P("M 120 306 H 112 A 6 6 0 0 0 106 312 V 404 A 6 6 0 0 0 112 410 H 129", stroke="#6B7580", sw=1.3)
R(130, 392, 150, 38, fill="#F1F3F5", stroke="#8C96A2", sw=1.2, rx=8)
T(205, 408, "native GDN update", 13.5, INK, bold=True, anchor="middle")
T(205, 424, "after the whole group", 12.5, MUTED, italic=True, anchor="middle")
P("M 280 411 H 399", stroke="#6B7580", sw=1.3)
T(340, 404, "advance", 13, MUTED, italic=True, anchor="middle")
MT(430, 384, "S", sub="g+1", sup="−", size=15, fill=B["dk"], anchor="middle")
cells(400, 392, [[.35, .6, .2, .5, .3], [.8, .75, .85, .7, .8], [.2, .55, .35, .6, .25]], 12, B)
tag(612, 244, "D")

# ---- E: relevance branch (full attention)
R(636, 236, 408, 204, fill="#FFFFFF", stroke=O["st"], sw=1.6, rx=10)
out.append(f'<circle cx="657" cy="259" r="7" fill="none" stroke="{O["hi"]}" stroke-width="2"/>'
           f'<circle cx="657" cy="259" r="2.5" fill="{O["hi"]}"/>')
T(672, 264, "Question Relevance", 17, O["dk"], bold=True)
T(672, 283, "full attention · final prompt token", 13.5, MUTED, italic=True)
R(919, 298, 22, 22, fill="#EE9A35", stroke=O["dk"], sw=1.2, rx=2)
T(910, 314, "query", 13, MUTED, italic=True, anchor="end")
rel = [.1, .15, .8, .95, .3, .1, .2, .7, .35, .1, .15, .1]
for i, v in enumerate(rel):
    cx = 690 + i * 15 + 7.5
    P(f"M 930 320 Q {(930 + cx) / 2 + 20} 350 {cx} 391", stroke=O["hi"], sw=0.6 + 2.6 * v, arrow=False,
      op=0.25 + 0.7 * v)
cells(690, 392, rel, 15, O)
MT(882, 405, "a", sub="i", size=16, fill=O["dk"])
P("M 780 407 V 469", stroke=O["st"], sw=1.6)
tag(1036, 244, "E")

# ------------------------------------------------ F: token-level scores and product
nov = [.3, .85, .2, .9, .25, .15, .6, .2, .75, .3, .2, .1]
R(300, 470, 280, 70, fill=B["fill"], stroke=B["st"], sw=1.3, rx=7)
T(316, 490, "Novelty", 15, B["dk"], bold=True)
MT(378, 490, "r̄", sub="i", size=17, fill=B["dk"])
T(420, 490, "(per token)", 13, MUTED, italic=True)
cells(332, 504, nov, 18, B)
R(660, 470, 280, 70, fill=O["fill"], stroke=O["st"], sw=1.3, rx=7)
T(676, 490, "Relevance", 15, O["dk"], bold=True)
MT(756, 490, "a", sub="i", size=17, fill=O["dk"])
T(786, 490, "(per token)", 13, MUTED, italic=True)
cells(692, 504, rel, 18, O)
out.append(f'<circle cx="620" cy="513" r="14" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
           f'<path d="M 614 507 L 626 519 M 626 507 L 614 519" stroke="{INK}" stroke-width="1.7"/>')
P("M 580 513 H 605", stroke=B["st"])
P("M 660 513 H 635", stroke=O["st"])
num(620, 481, "2", G["dk"])
T(632, 568, "multiply per token, before pooling", 13.5, G["dk"], bold=True)
P("M 620 527 V 595", stroke=G["st"], sw=1.6)
tag(648, 478, "F")

# ------------------------------------------------ G: scoring -> selection -> answer
prod = [round(a * b / 0.85, 2) for a, b in zip(nov, rel)]
R(480, 596, 280, 70, fill=G["fill"], stroke=G["st"], sw=1.3, rx=7)
T(496, 616, "Token contributions", 15, G["dk"], bold=True)
MT(662, 616, "a", sub="i", size=16, fill=G["dk"])
MT(680, 616, "r̄", sub="i", size=16, fill=G["dk"])
cells(512, 630, [min(1, p) for p in prod], 18, G)
P("M 760 631 H 789")
R(790, 596, 110, 70, fill=G["fill"], stroke=G["st"], sw=1.3, rx=7)
T(812, 620, "sum in", 15, G["dk"], bold=True)
MT(864, 620, "G", sub="g", size=16, fill=G["dk"])
MT(845, 652, "s", sub="g", size=20, fill=G["dk"], anchor="middle")
num(890, 596, "3", G["dk"])
P("M 900 631 H 925")
R(926, 584, 176, 124, fill="#fff", stroke="#9AA4AE", sw=1.2, rx=8)
T(1014, 604, "normalize per block,", 13.5, INK, anchor="middle")
T(1014, 621, "average the 2 blocks", 13.5, INK, anchor="middle")
hs = [.85, .95, .4, .3, .55, .35, .6, .25]
for i, h in enumerate(hs):
    sel = h > .7
    out.append(f'<rect x="{946 + i * 17}" y="{694 - h * 58:.1f}" width="11" height="{h * 58:.1f}" rx="1.5" '
               f'fill="{G["hi"] if sel else "#C5CDD6"}"/>')
P("M 940 694 H 1088", arrow=False, sw=1, stroke="#8C96A2")
P(f"M 940 {694 - .72 * 58:.1f} H 1088", arrow=False, sw=1, stroke=G["st"], dash="3 3")
P("M 1102 646 H 1125")
R(1126, 584, 204, 124, fill=G["fill"], stroke=G["st"], sw=1.3, rx=8)
T(1158, 606, "Top-K/2 groups", 15, G["dk"], bold=True)
num(1144, 601, "4", G["dk"])
for px, a, lab in [(1138, 0, "2–3 s"), (1236, 2, "4–5 s")]:
    frame(a, px, 620, 44)
    frame(a + 1, px + 46, 620, 44)
    T(px + 45, 662, lab, 13, MUTED, anchor="middle")
T(1228, 690, "original frames + timestamps", 13, MUTED, italic=True, anchor="middle")
P("M 1330 646 H 1355")
R(1356, 584, 204, 124, fill="#F1F3F5", stroke="#8C96A2", sw=1.3, rx=8)
snow(1386, 618, 18)
T(1400, 624, "Frozen Answerer", 16, INK, bold=True)
T(1372, 652, "frames + timestamps", 13.5, MUTED)
T(1372, 672, "+ question  →  answer", 13.5, MUTED)
tag(926, 572, "G")

# ------------------------------------------------ I: legend
R(36, 584, 420, 166, fill="#fff", stroke="#B8C0C9", sw=1.1, rx=8, dash="4 3")
T(52, 608, "Legend", 14, INK, bold=True)
leg = [
    ("cells", B, "memory novelty", 52, 636), ("cells", O, "question relevance", 246, 636),
    ("cells", G, "selection score", 52, 668), ("q", None, "question token q", 246, 668),
    ("cur", None, "current group", 52, 700), ("snow", None, "frozen (no training)", 246, 700),
    ("bar", None, "selected group", 52, 732), ("shade", None, "darker = larger value", 246, 732),
]
for kind, pal, lab, x, y in leg:
    if kind == "cells":
        cells(x, y - 12, [.2, .8], 13, pal)
    elif kind == "q":
        R(x + 6, y - 12, 14, 14, fill="#EE9A35", stroke=O["dk"], sw=1.1, rx=2)
    elif kind == "cur":
        R(x, y - 13, 26, 16, fill="none", stroke=INK, sw=1.6, rx=3, dash="4 3")
    elif kind == "snow":
        snow(x + 13, y - 5, 17)
    elif kind == "bar":
        R(x + 7, y - 15, 11, 18, fill=G["hi"], stroke="none", rx=1.5)
    else:
        cells(x, y - 12, [0, .5, 1], 9, B)
    T(x + 36, y, lab, 13.5, MUTED)
tag(36, 584, "I")

# ------------------------------------------------ H: right visualization panel
R(1080, 32, 488, 532, fill="#FCFCFD", stroke="#9AA4AE", sw=1.2, rx=10, dash="6 4")
T(1324, 60, "Token-aligned Scoring (schematic)", 17, INK, bold=True, anchor="middle")
tag(1080, 32, "H")
import random
rng = random.Random(3)
def pat(hot, base=.1):
    return [min(1, (0.85 + rng.random() * .15) if i in hot else base + rng.random() * .15) for i in range(12)]
N = [pat({2, 3, 4}), pat({1, 5, 6, 9}, .25), pat({0, 1, 2, 3}), pat(set(), .1), pat({6, 7, 8}), pat(set(), .05)]
A = [pat({2, 3, 4}), pat({1, 5, 8}, .25), pat({8, 9, 10, 11}), pat({3, 4, 5, 6}), pat({6, 7, 8, 9}), pat({0}, .05)]
C = [[a * b for a, b in zip(n, r)] for n, r in zip(N, A)]
S = [sum(r) for r in C]
GX, c = 1150, 14
for gi, (ttl, mat, pal, yy, note) in enumerate([
        ("Novelty  r̄", N, B, 92, ("what the memory", "failed to predict")),
        ("Relevance  a", A, O, 210, ("what the question", "attends to")),
        ("Contribution  a·r̄", C, G, 328, None)]):
    T(GX, yy - 8, ttl, 14, pal["dk"], bold=True)
    cells(GX, yy, mat, c, pal)
    for r in range(6):
        T(GX - 8, yy + r * c + 11, f"G{r + 1}", 11.5, MUTED, anchor="end")
    if note:
        T(GX + 12 * c + 18, yy + 36, note[0], 13.5, MUTED, italic=True)
        T(GX + 12 * c + 18, yy + 54, note[1], 13.5, MUTED, italic=True)
T(GX + 12 * c + 18, 320, "group score", 13.5, G["dk"], bold=True)
MT(GX + 12 * c + 106, 320, "s", sub="g", size=16, fill=G["dk"])
top2 = sorted(range(6), key=lambda r: -S[r])[:2]
for r in range(6):
    w = S[r] / max(S) * 120
    sel = r in top2
    out.append(f'<rect x="{GX + 12 * c + 18}" y="{328 + r * c + 2}" width="{w:.1f}" height="{c - 4}" rx="1.5" '
               f'fill="{G["hi"] if sel else "#C5CDD6"}"/>')
    if sel:
        T(GX + 12 * c + 18 + w + 8, 328 + r * c + 12, "✓ selected", 12.5, G["dk"], bold=True)
# match-before-pooling example (G3)
P(f"M {GX - 30} {92 + 2 * c + 7} H {GX - 40} V {470} H {GX - 30}", stroke=RED, sw=1.2, arrow=False, dash="3 3")
T(GX - 26, 452, "G3: novel tokens ≠ relevant tokens", 14, INK, bold=True)
T(GX - 26, 474, "pool first  →  mean(r̄)·mean(a) looks high", 13.5, MUTED)
T(GX - 26, 494, "match first →  Σ aᵢr̄ᵢ stays low, G3 not selected", 13.5, MUTED)
T(GX - 26, 520, "(illustrative pattern — not measured values)", 12.5, MUTED, italic=True)

# ================================================================ notes
NOTES = [
    ("A", "顶部长条放真实视频帧，用浅蓝扇形把相邻两帧展开成组（照搬 NSA 的 Split to Continuous Blocks）；当前组 G_g 用黑色虚线框强调。"),
    ("B", "问题用橙色小方块 q 表示（对应 NSA 的 q_t）。全图橙色只表示“问题 / 相关性”，不要挪作他用。"),
    ("C", "大虚线框 + 雪花 = 冻结的 backbone。标题一行写清模型、层号、block 结构，读者不用看正文。"),
    ("D", "记忆分支把计算画出来：S、k → 预测 v̂ ↔ 真实 v → 残差，全部画成格子；下面一行画“读完整组再更新记忆”。"),
    ("E", "相关性分支：q 到每个 token 的注意力画成粗细 / 深浅不同的弧线，弧越粗 = a_i 越大，格子同色深浅呼应。"),
    ("F", "核心创新放在画面正中：两条 token 级向量 + ⊗，旁边一句话点明“先逐 token 相乘，再汇总”。"),
    ("G", "底部一条流水线：组分数 → 每个 block 归一化后平均 → Top-K/2 → 冻结回答模型。①–④ 与 caption 对应。"),
    ("H", "右侧可视化面板（照搬 NSA 右边的 mask 图）：三张热力图 + 组分数条，用 G3 说明为什么要先对齐再汇总。数值只是示意，图中要标明。"),
    ("I", "图例放在角落，统一解释颜色、方块、雪花、虚线框。全图只用三种主色 + 灰色。"),
    ("✎", "统一规则：圆角框、1.2–1.6 px 线宽、箭头一致；字体二选一：粗体无衬线（像 NSA）或 Times（与正文一致）；公式用 LaTeX 插入。"),
]
T(16, 808, "草图说明（红色字母对应图中位置，这是布局草稿，配色/比例在 PPT 里再调）", 18, INK, bold=True, family=CJK)


from PIL import ImageFont
_CJK = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 62)


def wrap(s, n):
    """Wrap to n px at 15.5 px, never starting a line with closing punctuation."""
    lines, cur = [], ""
    for ch in s:
        if _CJK.getlength(cur + ch) / 4 > n and ch not in "，。；：、）”":
            lines.append(cur)
            cur = ""
        cur += ch
    if cur:
        lines.append(cur)
    return lines


for k, (letter, text) in enumerate(NOTES):
    col, row = k % 2, k // 2
    x, y = 30 + col * 780, 846 + row * 52
    if letter == "✎":
        out.append(f'<circle cx="{x}" cy="{y - 5}" r="11" fill="{INK}"/>'
                   f'<text x="{x}" y="{y}" font-size="13" fill="#fff" text-anchor="middle">✎</text>')
    else:
        tag(x, y - 5, letter)
    for li, line in enumerate(wrap(text, 730)):
        T(x + 20, y + li * 22, line, 15.5, INK, family=CJK)

# ================================================================ assemble
cols = {"#5F6B78", B["st"], O["st"], G["st"], "#6B7580", RED}
markers = "".join(
    f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.4" markerHeight="6.4" '
    f'orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 L2.4,5 Z" fill="{c}"/></marker>' for c in cols)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" '
       f'height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">\n<title>MINT layout sketch</title>\n'
       f'<defs>{markers}</defs>\n<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n' + "\n".join(out) + "\n</svg>\n")
OUT.write_text(svg)
print("wrote", OUT, f"{len(svg) // 1024} KB")
