#!/usr/bin/env python3
"""Generate the MINT method figure (mint_method.svg).

Run:  python3 make_figure.py <media_dir>
<media_dir> holds the assets extracted from the original mint-method.pptx
(ppt/media): image.png .. image4.png are the four video frames and
image2.svg, image4.svg .. image14.svg are dvisvgm (Computer Modern) math.
"""
import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image, ImageFont

MEDIA = Path(sys.argv[1] if len(sys.argv) > 1 else "media")
OUT = Path(__file__).with_name("mint_method.svg")

# ----------------------------------------------------------------- palette
INK, MUTED, RULE = "#1F2933", "#5F6B78", "#8C96A2"
BLUE = dict(dk="#2F5F86", st="#5B87AD", fill="#E6EFF7", cell="#D3E3F0", hi="#7FA7CB")
AMBER = dict(dk="#9A5B17", st="#C98A3F", fill="#FCF1E2", cell="#F6DDB9", hi="#E2A55A")
GREEN = dict(dk="#2F6B4A", st="#5E9A78", fill="#E5F2EA", cell="#CFE6D8", hi="#6DAE88")
GRAY = dict(dk="#3E4954", st="#A6AFB9", fill="#F3F5F7", cell="#E3E7EB")
ICE = "#5D89AA"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

W, H = 1320, 676

# ------------------------------------------------------------ text metrics
_FONTS = {}


def _font(size, bold=False, italic=False):
    key = (size, bold, italic)
    if key not in _FONTS:
        name = "Bold" if bold else ("Italic" if italic else "Regular")
        _FONTS[key] = ImageFont.truetype(
            f"/usr/share/fonts/truetype/liberation/LiberationSans-{name}.ttf", size * 4)
    return _FONTS[key]


def tw(s, size, bold=False, italic=False):
    return _font(size, bold, italic).getlength(s) / 4


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


out = []


def T(x, y, s, size=17, fill=INK, bold=False, italic=False, anchor="start"):
    a = f' font-weight="700"' if bold else ""
    a += ' font-style="italic"' if italic else ""
    a += f' text-anchor="{anchor}"' if anchor != "start" else ""
    out.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}"{a}>{esc(s)}</text>')


# -------------------------------------------------------------------- math
MATH = {  # name -> source file
    "K/2": "image2.svg", "Sg-": "image4.svg", "ki": "image5.svg", "vhat": "image6.svg",
    "vi": "image7.svg", "rbar": "image8.svg", "ai": "image9.svg", "airbar": "image11.svg",
    "Gg": "image12.svg", "sg": "image14.svg",
}
math_defs, math_info = [], {}
for n, (name, fn) in enumerate(MATH.items()):
    src = (MEDIA / fn).read_text()
    vb = [float(v) for v in re.search(r"viewBox='([^']+)'", src).group(1).split()]
    base = float(re.search(r"data-y='([\d.]+)' id='math-baseline'", src).group(1))
    pre = f"m{n}-"
    for pid, d in re.findall(r"<path id='([^']+)' d='([^']+)'/>", src):
        math_defs.append(f'<path id="{pre}{pid}" d="{d}"/>')
    uses = []
    for body in re.findall(r"<use ([^>]+)/>", src):
        x = re.search(r"x='([-\d.]+)'", body).group(1)
        y = re.search(r"y='([-\d.]+)'", body).group(1)
        ref = re.search(r"href='#([^']+)'", body).group(1)
        uses.append(f'<use x="{x}" y="{y}" xlink:href="#{pre}{ref}"/>')
    rects = re.findall(r"<rect [^>]+/>", src)
    math_info[name] = dict(vb=vb, base=base, body="".join(uses + rects))


def M(name, x, y, s=1.8, fill=INK, anchor="start"):
    """Place TeX math so its baseline sits on y. Returns advance width."""
    info = math_info[name]
    w = (info["vb"][0] + info["vb"][2]) * s
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    out.append(f'<g transform="translate({x:.2f} {y - info["base"] * s:.2f}) scale({s})" '
               f'fill="{fill}">{info["body"]}</g>')
    return w


def TM(x, y, parts, size=17, anchor="start", gap=4):
    """Mixed run: parts = [("t", text, opts) | ("m", name, opts)]."""
    widths = []
    for kind, val, o in parts:
        if kind == "t":
            widths.append(tw(val, size, o.get("bold"), o.get("italic")))
        else:
            info = math_info[val]
            widths.append((info["vb"][0] + info["vb"][2]) * o.get("s", 1.8))
    total = sum(widths) + gap * (len(parts) - 1)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    for (kind, val, o), w in zip(parts, widths):
        if kind == "t":
            T(x, y, val, size, **o)
        else:
            M(val, x, y, **o)
        x += w + gap


# ------------------------------------------------------------------ shapes
def box(x, y, w, h, fill="#fff", stroke=RULE, sw=1.2, rx=7, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{extra}/>')


def path(d, stroke=RULE, sw=1.4, arrow=True, dash=None, fill="none"):
    m = f' marker-end="url(#ah-{stroke[1:]})"' if arrow else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-linejoin="round"{da}{m}/>')


def cells(x, y, n, c, pal, rows=1, hi=None, hi_fill=None, fills=None):
    """A row (or matrix) of token cells with hairline separators."""
    g = [f'<g stroke="{pal["st"]}" stroke-width="0.9">']
    for r in range(rows):
        for i in range(n):
            f = pal["cell"]
            if fills:
                f = fills[r][i]
            if hi is not None and i == hi:
                f = hi_fill or pal["hi"]
            g.append(f'<rect x="{x + i * c:g}" y="{y + r * c:g}" width="{c}" height="{c}" fill="{f}"/>')
    g.append("</g>")
    out.append("".join(g))
    out.append(f'<rect x="{x:g}" y="{y:g}" width="{n * c}" height="{rows * c}" rx="1.5" '
               f'fill="none" stroke="{pal["st"]}" stroke-width="1.2"/>')


def snow(cx, cy, size=20, color=ICE):
    s = size / 24
    out.append(
        f'<g transform="translate({cx - size / 2:.2f} {cy - size / 2:.2f}) scale({s:.4f})" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M10 4l2 1l2 -1M12 2v6.5l3 1.72M17.928 6.268l.134 2.232l1.866 1.232'
        'M20.66 7l-5.629 3.25l.01 3.458M19.928 14.268l-1.866 1.232l-.134 2.232'
        'M20.66 17l-5.629 -3.25l-2.99 1.738M14 20l-2 -1l-2 1M12 22v-6.5l-3 -1.72'
        'M6.072 17.732l-.134 -2.232l-1.866 -1.232M3.34 17l5.629 -3.25l-.01 -3.458'
        'M4.072 9.732l1.866 -1.232l.134 -2.232M3.34 7l5.629 3.25l2.99 -1.738"/></g>')


# ------------------------------------------------------------------ frames
FRAMES = []
for fn in ["image.png", "image2.png", "image3.png", "image4.png"]:
    im = Image.open(MEDIA / fn).convert("RGB")
    im = im.resize((256, 144), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    FRAMES.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
_clip = [0]


def frame(k, x, y, w):
    h = w * 9 / 16
    _clip[0] += 1
    cid = f"fc{_clip[0]}"
    out.append(f'<clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="3"/></clipPath>'
               f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" href="{FRAMES[k]}" '
               f'xlink:href="{FRAMES[k]}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>'
               f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="3" fill="none" '
               f'stroke="#6B7580" stroke-opacity="0.35" stroke-width="0.8"/>')
    return h


def panel_title(x, y, tag, text):
    T(x, y, tag, 21, bold=True)
    T(x + tw(tag, 21, bold=True) + 8, y, text, 21, bold=True)


# =============================================================== PANEL (a)
panel_title(20, 30, "(a)", "Selection with a pretrained hybrid backbone")

# ---- inputs
T(20, 64, "Candidate video", 17, bold=True)
for gi, gx in enumerate([20, 144]):
    box(gx, 74, 116, 37.25, fill=GRAY["fill"], stroke="#C4CBD3", sw=1, rx=6)
    frame(2 * gi, gx + 4, 78, 52)
    frame(2 * gi + 1, gx + 60, 78, 52)
T(272, 99, "…", 19, fill=MUTED)
T(140, 132, "two-frame groups", 16, fill=MUTED, anchor="middle")

T(20, 166, "Question + options", 17, bold=True)
box(20, 176, 246, 58, fill=AMBER["fill"], stroke=AMBER["st"], sw=1.1, rx=8)
T(34, 200, "What happened after the", 17, italic=True)
T(34, 222, "person raised their hand?", 17, italic=True)

path("M 290 92.6 H 292 A 6 6 0 0 1 298 98.6 V 135 A 6 6 0 0 0 304 141", arrow=False)
path("M 266 205 H 292 A 6 6 0 0 0 298 199 V 147 A 6 6 0 0 1 304 141", arrow=False)
path("M 298 141 H 318")

# ---- frozen backbone
box(318, 44, 424, 218, fill="#F7F8FA", stroke="#B8C0C9", sw=1.2, rx=10)
T(334, 72, "Qwen3.5-2B", 19, bold=True)
snow(718, 66, 20)
T(334, 94, "Hybrid block ×2  ·  layers 9–16", 16, fill=MUTED)
box(340, 102, 392, 64, fill="#FFFFFF", stroke="#CDD3DA", sw=1, rx=8)  # stacked copy
box(334, 108, 392, 64, fill="#FFFFFF", stroke="#B8C0C9", sw=1.1, rx=8)
for i, gx in enumerate([348, 426, 504]):
    box(gx, 122, 62, 36, fill=BLUE["fill"], stroke=BLUE["st"], sw=1.2, rx=6)
    T(gx + 31, 146, "GDN", 17, fill=BLUE["dk"], bold=True, anchor="middle")
    if i < 2:
        path(f"M {gx + 63} 140 H {gx + 77}", stroke=BLUE["st"], sw=1.2)
box(586, 122, 128, 36, fill=AMBER["fill"], stroke=AMBER["st"], sw=1.2, rx=6)
T(650, 146, "Full attention", 16, fill=AMBER["dk"], bold=True, anchor="middle")
path("M 567 140 H 585", stroke=RULE, sw=1.2)
# taps
path("M 352 162 V 166 H 562 V 162", stroke=BLUE["st"], sw=1.2, arrow=False)
path("M 457 166 V 192", stroke=BLUE["st"], sw=1.3)
path("M 650 158 V 192", stroke=AMBER["st"], sw=1.3)
T(457, 211, "Memory novelty", 17, fill=BLUE["dk"], bold=True, anchor="middle")
T(650, 211, "Question relevance", 17, fill=AMBER["dk"], bold=True, anchor="middle")
# outputs to scoring
path("M 650 217 V 226 A 6 6 0 0 0 656 232 H 790", stroke=AMBER["st"], sw=1.5)
path("M 457 217 V 240 A 6 6 0 0 0 463 246 H 790", stroke=BLUE["st"], sw=1.5)

# ---- token-aligned scoring (zoom source for panel b)
box(790, 168, 124, 94, fill=GREEN["fill"], stroke=GREEN["st"], sw=1.3, rx=8)
T(852, 199, "Token-aligned", 17, fill=GREEN["dk"], bold=True, anchor="middle")
T(852, 219, "scoring", 17, fill=GREEN["dk"], bold=True, anchor="middle")
T(852, 247, "see (b)", 15, fill=MUTED, italic=True, anchor="middle")
path("M 914 215 H 931")

# ---- normalize + aggregate, with schematic group-score bars
box(932, 96, 158, 166, fill="#FFFFFF", stroke="#B8C0C9", sw=1.2, rx=8)
T(1011, 120, "Normalize per block;", 16, anchor="middle")
T(1011, 140, "average blocks", 16, anchor="middle")
heights = [0.84, 0.93, 0.42, 0.30, 0.55, 0.36, 0.62, 0.26]
bx0, base_y, hmax, bw, bg = 959, 234, 76, 9.5, 4.4
cut = base_y - 0.72 * hmax
for i, h in enumerate(heights):
    sel = h > 0.72
    out.append(f'<rect x="{bx0 + i * (bw + bg):.1f}" y="{base_y - h * hmax:.1f}" width="{bw}" '
               f'height="{h * hmax:.1f}" rx="1.5" fill="{GREEN["hi"] if sel else "#C5CDD6"}"/>')
path(f"M 952 {base_y} H 1070", stroke="#8C96A2", sw=1, arrow=False)
path(f"M 952 {cut:.1f} H 1070", stroke=GREEN["st"], sw=1, arrow=False, dash="3 3")
T(1011, 253, "group scores", 15, fill=MUTED, italic=True, anchor="middle")
path("M 1090 179 H 1094 A 6 6 0 0 0 1100 173 V 99 A 6 6 0 0 1 1106 93 H 1111")

# ---- top-K/2 selection and frozen answerer
box(1112, 44, 194, 98, fill=GREEN["fill"], stroke=GREEN["st"], sw=1.3, rx=8)
TM(1209, 70, [("t", "Top-", {"bold": True, "fill": GREEN["dk"]}),
              ("m", "K/2", {"fill": GREEN["dk"], "s": 1.75}),
              ("t", "\u00a0frame pairs", {"bold": True, "fill": GREEN["dk"]})], gap=0, anchor="middle")
for px, (a, b), lab in [(1122, (0, 1), "2–3 s"), (1213, (2, 3), "4–5 s")]:
    frame(a, px, 84, 42)
    frame(b, px + 44, 84, 42)
    T(px + 43, 129, lab, 15, fill=MUTED, anchor="middle")
path("M 1150 142 V 197")
T(1162, 166, "original frames", 15, fill=MUTED)
T(1162, 184, "+ timestamps", 15, fill=MUTED)
box(1112, 198, 194, 64, fill=GRAY["fill"], stroke="#B8C0C9", sw=1.2, rx=8)
T(1209, 225, "Answerer", 18, bold=True, anchor="middle")
snow(1266, 219, 17)
T(1209, 248, "+ question", 15, fill=MUTED, anchor="middle")

# =============================================================== PANEL (b)
PB = 290
# zoom wedge from the scoring box to panel (b)
out.append(f'<path d="M 790 262 L 700 {PB} L 1004 {PB} L 914 262 Z" fill="{GREEN["fill"]}" opacity="0.7"/>')
path(f"M 790 262 L 700 {PB}", stroke=GREEN["st"], sw=1, arrow=False, dash="3 3")
path(f"M 914 262 L 1004 {PB}", stroke=GREEN["st"], sw=1, arrow=False, dash="3 3")
box(12, PB, 1296, 376, fill="#FBFCFD", stroke="#CBD2D9", sw=1.1, rx=12)
path(f"M 700 {PB} H 1004", stroke=GREEN["st"], sw=1.4, arrow=False)
panel_title(28, PB + 32, "(b)", "Memory-informed scoring within each hybrid block")

C = 18  # token-cell size
# ---- memory & key
TM(36, 362, [("t", "Pre-group memory", {"bold": True}), ("m", "Sg-", {"fill": BLUE["dk"]})])
cells(36, 376, 6, C, BLUE, rows=4)
TM(36, 490, [("t", "Key", {}), ("m", "ki", {"fill": BLUE["dk"]})])
cells(36, 500, 6, C, BLUE)
box(196, 400, 132, 52, fill=BLUE["fill"], stroke=BLUE["st"], sw=1.2, rx=7)
T(262, 431, "Predict value", 17, fill=BLUE["dk"], bold=True, anchor="middle")
path("M 144 413 H 195", stroke=BLUE["st"])
path("M 144 509 H 164 A 6 6 0 0 0 170 503 V 446 A 6 6 0 0 1 176 440 H 195", stroke=BLUE["st"])

# ---- prediction vs. value -> normalized residual
TM(372, 404, [("t", "Prediction", {}), ("m", "vhat", {"fill": BLUE["dk"]})])
cells(372, 417, 6, C, BLUE)
path("M 328 426 H 371", stroke=BLUE["st"])
TM(372, 490, [("t", "Value", {}), ("m", "vi", {"fill": BLUE["dk"]})])
cells(372, 500, 6, C, BLUE)
box(526, 424, 138, 70, fill=BLUE["fill"], stroke=BLUE["st"], sw=1.2, rx=7)
T(595, 454, "Normalized", 17, fill=BLUE["dk"], bold=True, anchor="middle")
T(595, 474, "residual", 17, fill=BLUE["dk"], bold=True, anchor="middle")
path("M 480 426 H 496 A 6 6 0 0 1 502 432 V 440 A 6 6 0 0 0 508 446 H 525", stroke=BLUE["st"])
path("M 480 509 H 496 A 6 6 0 0 0 502 503 V 478 A 6 6 0 0 1 508 472 H 525", stroke=BLUE["st"])

# ---- novelty & relevance, token-aligned
NX, HI = 806, 3
TM(NX, 444, [("t", "Novelty", {"bold": True, "fill": BLUE["dk"]}), ("m", "rbar", {"fill": BLUE["dk"]})])
cells(NX, 452, 6, C, BLUE, hi=HI)
path(f"M 664 461 H {NX - 1}", stroke=BLUE["st"])
T(735, 452, "head / layer mean", 15, fill=MUTED, italic=True, anchor="middle")

TM(NX, 582, [("t", "Relevance", {"bold": True, "fill": AMBER["dk"]}), ("m", "ai", {"fill": AMBER["dk"]})])
cells(NX, 542, 6, C, AMBER, hi=HI)
box(600, 534, 178, 34, fill=AMBER["fill"], stroke=AMBER["st"], sw=1.2, rx=7)
T(689, 556, "Final-prompt attention", 16, fill=AMBER["dk"], bold=True, anchor="middle")
path(f"M 778 551 H {NX - 1}", stroke=AMBER["st"])

hx = NX + HI * C + C / 2
path(f"M {hx} 472 V 540", stroke="#7D8894", sw=1.1, arrow=False, dash="2.5 3")
T(hx - 12, 499, "match tokens", 15, fill=MUTED, italic=True, anchor="end")
T(hx - 12, 517, "before pooling", 15, fill=MUTED, italic=True, anchor="end")

# ---- product, contributions, group sum
OX, OY = 958, 506
path(f"M {NX + 6 * C} 461 H {OX - 6} A 6 6 0 0 1 {OX} 467 V {OY - 14}", stroke=BLUE["st"])
path(f"M {NX + 6 * C} 551 H {OX - 6} A 6 6 0 0 0 {OX} 545 V {OY + 14}", stroke=AMBER["st"])
out.append(f'<circle cx="{OX}" cy="{OY}" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="1.3"/>')
path(f"M {OX - 5.5} {OY - 5.5} L {OX + 5.5} {OY + 5.5} M {OX + 5.5} {OY - 5.5} L {OX - 5.5} {OY + 5.5}",
     stroke=INK, sw=1.5, arrow=False)
path(f"M {OX + 13} {OY} H 1001")
T(1056, 485, "Token contributions", 16, anchor="middle")
cells(1002, OY - 9, 6, C, GREEN, hi=HI)
M("airbar", 1056, 537, anchor="middle", fill=GREEN["dk"])
path(f"M 1110 {OY} H 1137")
box(1138, 476, 158, 60, fill=GREEN["fill"], stroke=GREEN["st"], sw=1.3, rx=8)
T(1217, 501, "Sum within", 17, fill=GREEN["dk"], bold=True, anchor="middle")
TM(1217, 523, [("t", "group", {"bold": True, "fill": GREEN["dk"]}), ("m", "Gg", {"fill": GREEN["dk"]})],
   anchor="middle")
T(1217, 566, "Per-block group score", 16, fill=MUTED, anchor="middle")
M("sg", 1217, 598, s=1.85, anchor="middle")

# ---- native memory update (advance after reading the whole group)
path("M 36 395 H 30 A 6 6 0 0 0 24 401 V 613 A 6 6 0 0 0 30 619 H 195", stroke=GRAY["dk"], sw=1.3)
TM(300, 578, [("t", "Current group", {}), ("m", "Gg", {"fill": INK})], anchor="middle")
path("M 300 584 V 599", stroke=GRAY["dk"], sw=1.3)
box(196, 600, 208, 38, fill=GRAY["fill"], stroke="#9EA8B3", sw=1.2, rx=7)
T(300, 625, "Native memory update", 17, fill=GRAY["dk"], bold=True, anchor="middle")
path("M 404 619 H 599", stroke=GRAY["dk"], sw=1.3)
T(502, 591, "read whole group,", 15, fill=MUTED, italic=True, anchor="middle")
T(502, 608, "then advance", 15, fill=MUTED, italic=True, anchor="middle")
upd = [[BLUE["cell"]] * 6 for _ in range(3)]
upd[1] = [BLUE["hi"]] * 6
cells(600, 592, 6, C, BLUE, rows=3, fills=upd)
T(722, 624, "Post-group memory", 17)

# ---- legend (right-aligned)
LY = 650
items = [(None, "frozen"), (BLUE, "memory (GDN)"), (AMBER, "question (full attn.)"), (GREEN, "selection score")]
x = 1296 - sum(19 + tw(l, 15) for _, l in items) - 16 * (len(items) - 1)
for pal, lab in items:
    if pal is None:
        snow(x + 6.5, LY - 5, 15)
    else:
        box(x, LY - 11, 13, 13, fill=pal["fill"], stroke=pal["st"], sw=1.1, rx=3)
    T(x + 19, LY, lab, 15, fill=MUTED)
    x += 19 + tw(lab, 15) + 16
T(36, LY, "Vectors are schematic, not measured scores.", 15, fill=MUTED, italic=True)

# ================================================================ assemble
markers = []
for col in {RULE, BLUE["st"], AMBER["st"], GREEN["st"], GRAY["dk"], INK}:
    markers.append(f'<marker id="ah-{col[1:]}" viewBox="0 0 10 10" refX="8.6" refY="5" '
                   f'markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">'
                   f'<path d="M0,1 L9,5 L0,9 L2.4,5 Z" fill="{col}"/></marker>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">\n'
       '<title>MINT: memory-informed token-aligned frame selection</title>\n'
       f'<defs>{"".join(markers)}{"".join(math_defs)}</defs>\n'
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n' + "\n".join(out) + "\n</svg>\n")
OUT.write_text(svg)
print(f"wrote {OUT} ({len(svg) / 1024:.0f} KB)")
