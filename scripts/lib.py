"""Shared building blocks for the profile-README SVG generator.

Everything here is plain string templating so the output stays dependency free
and renders inside GitHub's <img> sandbox (no scripts, no external requests,
system fonts only).
"""
from __future__ import annotations

import html
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ── palette ────────────────────────────────────────────────────────────────
C = dict(
    bg0="#050A07",
    bg1="#0A0F08",
    panel="#0D1610",
    edge="#22331E",
    lime="#CAFF3C",
    green="#8AFF57",
    mint="#4DFFB4",
    cyan="#3CE8FF",
    violet="#B28CFF",
    pink="#FF4FB8",
    amber="#FFC84A",
    dim="#7A8B6F",
    mute="#4A5C44",
    text="#E8F5E1",
)

FONT = (
    "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,"
    "'Liberation Mono','DejaVu Sans Mono',monospace"
)


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def f(n: float) -> str:
    """Compact number formatting for path data."""
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# Reduced-motion: kill CSS animation and reveal anything that starts hidden.
BASE_CSS = """
text{font-family:%s}
.pre{white-space:pre}
.rv{opacity:0}
@media (prefers-reduced-motion:reduce){
*{animation:none!important}
.rv{opacity:1!important}
.alt{display:none}
}
""" % FONT


def svg(w, h, body, *, title, desc="", defs="", css="", bg=None):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" '
        f'font-family="{FONT}">\n'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>\n'
        f"<defs>{defs}</defs>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(content, encoding="utf-8")
    print(f"  wrote assets/{name:<28} {len(content) / 1024:6.1f} KB")


# ── geometry helpers ───────────────────────────────────────────────────────
def smooth_path(points):
    """Catmull-Rom → cubic Bézier path through points."""
    if len(points) < 3:
        return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in points)
    d = [f"M{f(points[0][0])} {f(points[0][1])}"]
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    return "".join(d)


def ring_arc(cx, cy, r):
    """Circle path starting at 12 o'clock, clockwise (for stroke-dash gauges)."""
    return (f"M{f(cx)} {f(cy - r)}a{f(r)} {f(r)} 0 1 1 0 {f(2 * r)}"
            f"a{f(r)} {f(r)} 0 1 1 0 {f(-2 * r)}")


def rounded_clip(cid, w, h, rx):
    return f'<clipPath id="{cid}"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'


def beam_border(w, h, rx, *, dur=7, delay=0, color=None, inset=1.5, glow=True):
    """Static hairline border plus a lime comet that circles the edge."""
    color = color or C["lime"]
    attrs = (f'x="{inset}" y="{inset}" width="{w - 2 * inset}" height="{h - 2 * inset}" '
             f'rx="{rx}" pathLength="100" fill="none"')
    style = f'style="animation-duration:{dur}s;animation-delay:{delay}s"'
    out = [f'<rect {attrs} stroke="{C["edge"]}" stroke-width="1.5"/>']
    if glow:
        out.append(f'<rect class="beam" {attrs} stroke="{color}" stroke-width="5" '
                   f'opacity=".45" filter="url(#bl4)" {style}/>')
    out.append(f'<rect class="beam" {attrs} stroke="{color}" stroke-width="2" '
               f'stroke-linecap="round" {style}/>')
    return "".join(out)


BEAM_CSS = (".beam{stroke-dasharray:12 88;animation:beam 7s linear infinite}"
            "@keyframes beam{to{stroke-dashoffset:-100}}")
BLUR_DEFS = ('<filter id="bl4" x="-20%" y="-20%" width="140%" height="140%">'
             '<feGaussianBlur stdDeviation="4"/></filter>'
             '<filter id="bl60" x="-50%" y="-50%" width="200%" height="200%">'
             '<feGaussianBlur stdDeviation="60"/></filter>'
             '<filter id="bl2" x="-20%" y="-20%" width="140%" height="140%">'
             '<feGaussianBlur stdDeviation="2"/></filter>')


# ── typewriter ─────────────────────────────────────────────────────────────
class Typewriter:
    """Typed-text effect using two CSS animations per line (clip reveal + cursor).

    `textLength` pins the advance so glyph k always sits at x + k*cw; the reveal
    and the block cursor then step through identical offsets in any monospace
    fallback font. With reduced motion the animation is off, the text shows in
    full and the cursor stays hidden.
    """

    def __init__(self, cycle: float, per: float = 0.055):
        self.cycle = cycle
        self.per = per
        self.css: list[str] = []
        self.n = 0

    def keyframes(self) -> str:
        return "".join(self.css)

    def line(self, text, x, y, *, start, hold, size, fill=C["lime"], cursor=C["lime"], alt=False):
        k = self.n
        self.n += 1
        n = len(text)
        cw = size * 0.6
        W = n * cw
        pct = lambda t: t / self.cycle * 100
        S, E = pct(start), pct(start + n * self.per)
        H = pct(start + n * self.per + hold)
        eps = 0.01
        hide = "clip-path:inset(0 100% 0 0)"
        show = "clip-path:inset(0 0 0 0)"
        first = f"0%,{S:.3f}%" if S > 0 else "0%"
        end_clip = f"{H + eps:.3f}%,100%{{{hide}}}" if H + eps < 100 else ""
        end_cur = (f"{H + eps:.3f}%,100%{{opacity:0;transform:translateX({W:.1f}px)}}" if H + eps < 100 else "")
        self.css.append(
            f"@keyframes tw{k}{{{first}{{{hide};animation-timing-function:steps({n},end)}}"
            f"{E:.3f}%,{min(H, 100):.3f}%{{{show}}}{end_clip}}}"
            f"@keyframes tc{k}{{0%{{opacity:0}}"
            + (f"{max(S - eps, eps):.3f}%{{opacity:0}}" if S > 0 else "")
            + f"{S:.3f}%{{opacity:1;transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{E:.3f}%,{min(H, 100):.3f}%{{opacity:1;transform:translateX({W:.1f}px)}}"
            f"{end_cur}}}"
            f".tw{k}{{animation:tw{k} {self.cycle}s linear infinite}}"
            f".tc{k}{{opacity:0;animation:tc{k} {self.cycle}s linear infinite}}")
        a = " alt" if alt else ""
        return (
            f'<text class="tw{k}{a} pre" x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'textLength="{W:.1f}" lengthAdjust="spacing">{esc(text)}</text>'
            f'<rect class="tc{k}{a}" x="{x}" y="{y - size * .8:.1f}" width="{cw * .9:.1f}" height="{size * 1.05:.1f}" fill="{cursor}"/>')
