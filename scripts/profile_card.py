"""Profile card: vectorised dot-matrix portrait (scan-beam reveal) + typed profile.json."""
import numpy as np
from PIL import Image

from lib import BEAM_CSS, BLUR_DEFS, C, ROOT, beam_border, esc, f, rounded_clip, svg

PITCH, ORIGIN = 14, 5  # dot grid of assets/portrait_terminal.png


def vectorise_portrait(src=ROOT / "assets" / "portrait_terminal.png", crop=(380, 30, 1166, 1115)):
    """Turn the dot-matrix PNG into (x, y, r, tier) dots + tier colours + bbox."""
    a = np.asarray(Image.open(src).convert("RGB")).astype(int)
    H, W, _ = a.shape
    dots = []
    for j in range(1, (H - ORIGIN) // PITCH - 1):
        for i in range(1, (W - ORIGIN) // PITCH - 1):
            cx, cy = ORIGIN + i * PITCH, ORIGIN + j * PITCH
            if not (crop[0] <= cx <= crop[2] and crop[1] <= cy <= crop[3]):
                continue
            win = a[cy - 7:cy + 7, cx - 7:cx + 7]
            on = win.max(2) > 40
            n = int(on.sum())
            if n < 4:
                continue
            col = np.median(win[on], axis=0)
            dots.append((cx, cy, max(1.2, round(np.sqrt(n / np.pi) * 4) / 4), col))
    # 5-tier colour quantisation (k-means on the colours, deterministic init)
    cols = np.array([d[3] for d in dots])
    order = np.argsort(cols[:, 1])
    centers = cols[order[[int(len(order) * q) for q in (.05, .3, .55, .8, .97)]]].astype(float)
    for _ in range(12):
        lab = np.argmin(((cols[:, None, :] - centers[None]) ** 2).sum(2), axis=1)
        for k in range(5):
            if (lab == k).any():
                centers[k] = cols[lab == k].mean(0)
    rank = np.argsort(centers[:, 1])  # dim → bright
    remap = {int(k): r for r, k in enumerate(rank)}
    tiers = ["#%02x%02x%02x" % tuple(int(v) for v in centers[k]) for k in rank]
    out = [(x, y, r, remap[int(l)]) for (x, y, r, _), l in zip(dots, lab)]
    xs, ys = [d[0] for d in out], [d[1] for d in out]
    return out, tiers, (min(xs) - 8, min(ys) - 8, max(xs) + 8, max(ys) + 8)


def profile_card():
    W, H = 1000, 420
    dots, tiers, (bx0, by0, bx1, by1) = vectorise_portrait()
    bw, bh = bx1 - bx0, by1 - by0

    # portrait panel
    qx, qy, qw, qh = 24, 24, 300, 372
    pad = 12
    s = min((qw - 2 * pad) / bw, (qh - 2 * pad - 30) / bh)
    ox = qx + (qw - bw * s) / 2 - bx0 * s
    oy = qy + pad - by0 * s
    # rows → bands for the scan-flash
    band_rows = 3
    bands: dict[int, dict[int, list]] = {}
    for x, y, r, t in dots:
        b = ((y - ORIGIN) // PITCH) // band_rows
        bands.setdefault(b, {}).setdefault(t, []).append((x, y, r))
    SCAN = 7.0
    groups = []
    for b in sorted(bands):
        yc = ORIGIN + (b * band_rows + 1) * PITCH
        frac = (oy + yc * s - qy) / (qh + 26)  # when the beam's bright edge reaches this band
        inner = "".join(
            f'<g fill="{tiers[t]}">' + "".join(
                f'<circle cx="{x}" cy="{y}" r="{r:g}"/>' for x, y, r in sorted(items, key=lambda d: (d[1], d[0]))
            ) + "</g>" for t, items in sorted(bands[b].items()))
        groups.append(f'<g class="pb" style="animation-delay:{frac * SCAN:.2f}s">{inner}</g>')
    glow = "".join(f'<circle cx="{x}" cy="{y}" r="{r:g}"/>' for x, y, r, t in dots if t >= 3)

    # terminal JSON
    K, S, P, B = "#7DE3FF", C["lime"], "#5E7355", C["green"]

    def row(key=None, val=None, indent=1, last=False, raw=None):
        if raw is not None:
            return [(raw, B)]
        segs = [("  " * indent, P), ('"' + key + '"', K), (": ", P)]
        pad_ = " " * (10 - len(key))
        segs.append((pad_, P))
        if isinstance(val, list):
            segs.append(("[", B))
            for n, v in enumerate(val):
                segs += [('"' + v + '"', S)] + ([(", ", P)] if n < len(val) - 1 else [])
            segs.append(("]", B))
        else:
            segs.append(('"' + val + '"', S))
        if not last:
            segs.append((",", P))
        return segs

    lines = [
        row(raw="{"),
        row("name", "Nilesh Singh"),
        row("role", "Data Analyst | AI Evaluation"),
        row("studying", "BCA Data Science · Sri Balaji University"),
        row("domain", ["Analytics", "Data Quality", "AI Evaluation"]),
        row("tools", ["Python", "SQL", "Power BI", "Excel", "R"]),
        row("intern", "Cloud App Developer · Codefirst Technology"),
        row("location", "Pune, India"),
        row("open_to", ["Data Analyst", "AI Trainer", "AI Evaluation"], last=True),
        row(raw="}"),
    ]
    tx, ty, tw_, th = 350, 24, 626, 372
    y0, step = ty + 36 + 36, 29
    term = []
    for n, segs in enumerate(lines):
        tsp = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in segs)
        term.append(f'<text class="rv pre ln" x="{tx + 24}" y="{y0 + n * step}" font-size="15" '
                    f'style="--i:{n}">{tsp}</text>')
    prompt_y = y0 + len(lines) * step + 6
    term.append(f'<text class="rv pre ln" x="{tx + 24}" y="{prompt_y}" font-size="15" style="--i:{len(lines)}">'
                f'<tspan fill="{C["dim"]}">➜ ~ </tspan><tspan class="blink" fill="{C["lime"]}">█</tspan></text>')

    def bracket(x, y, dx, dy):
        return f'<path d="M{x} {y + dy * 18}V{y}H{x + dx * 18}" fill="none" stroke="{C["lime"]}" stroke-width="2.5" stroke-linecap="square"/>'

    defs = f"""
{BLUR_DEFS}
{rounded_clip('rc', W, H, 24)}
{rounded_clip('pc', qw, qh, 16)}
<linearGradient id="beamG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['lime']}" stop-opacity="0"/><stop offset=".92" stop-color="{C['lime']}" stop-opacity=".35"/><stop offset="1" stop-color="#F4FFD0" stop-opacity=".95"/></linearGradient>
<pattern id="dotgrid" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="{C['lime']}" opacity=".12"/></pattern>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>
<radialGradient id="pv" cx=".5" cy=".45" r=".8"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
"""
    css = BEAM_CSS + f"""
.pb{{opacity:.55;animation:pscan {SCAN}s linear infinite}}
@keyframes pscan{{0%{{opacity:1}}12%{{opacity:.8}}30%,100%{{opacity:.55}}}}
.scanbeam{{animation:sy {SCAN}s linear infinite}}
@keyframes sy{{from{{transform:translateY(0)}}to{{transform:translateY({qh + 26}px)}}}}
.breathe{{animation:br 4s ease-in-out infinite}} @keyframes br{{0%,100%{{opacity:.35}}50%{{opacity:.6}}}}
.ln{{animation:lnIn 16s cubic-bezier(.2,.8,.2,1) infinite;animation-delay:calc(var(--i) * .32s)}}
@keyframes lnIn{{0%{{opacity:0;transform:translateX(-14px)}}2.5%,90%{{opacity:1;transform:none}}95%,100%{{opacity:0;transform:none}}}}
.blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3.2);opacity:0}}}}
"""
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
  <ellipse cx="170" cy="210" rx="230" ry="190" fill="{C['lime']}" opacity=".13" filter="url(#bl60)" class="breathe"/>
  <ellipse cx="860" cy="360" rx="260" ry="120" fill="{C['cyan']}" opacity=".08" filter="url(#bl60)"/>

  <!-- portrait -->
  <g transform="translate({qx} {qy})">
    <rect width="{qw}" height="{qh}" rx="16" fill="{C['bg1']}" stroke="{C['edge']}"/>
    <rect width="{qw}" height="{qh}" rx="16" fill="url(#dotgrid)"/>
  </g>
  <g clip-path="url(#pc)" transform="translate({qx} {qy})"><g transform="translate({f(ox - qx)} {f(oy - qy)}) scale({s:.4f})">
    <g filter="url(#bl4)" opacity=".5" fill="{C['green']}">{glow}</g>
    {''.join(groups)}
  </g></g>
  <g clip-path="url(#pc)" transform="translate({qx} {qy})"><rect class="scanbeam" y="-26" width="{qw}" height="26" fill="url(#beamG)"/></g>
  <rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" rx="16" fill="url(#pv)"/>
  <rect x="{qx}" y="{qy + qh - 38}" width="{qw}" height="38" rx="0" fill="#000" fill-opacity=".55" clip-path="url(#pcb)"/>
  <clipPath id="pcb"><rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" rx="16"/></clipPath>
  {bracket(qx + 10, qy + 10, 1, 1)}{bracket(qx + qw - 10, qy + 10, -1, 1)}{bracket(qx + 10, qy + qh - 10, 1, -1)}{bracket(qx + qw - 10, qy + qh - 10, -1, -1)}
  <text x="{qx + 24}" y="{qy + 30}" font-size="11" letter-spacing="1.5" fill="{C['dim']}">SUBJECT // NS-001</text>
  <text x="{qx + 20}" y="{qy + qh - 14}" font-size="14" font-weight="700" letter-spacing="1" fill="{C['lime']}">NILESH SINGH</text>
  <circle class="pulse" cx="{qx + qw - 74}" cy="{qy + qh - 19}" r="3.5" fill="{C['green']}"/><circle cx="{qx + qw - 74}" cy="{qy + qh - 19}" r="3.5" fill="{C['green']}"/>
  <text x="{qx + qw - 64}" y="{qy + qh - 14}" font-size="11" letter-spacing="1.2" fill="{C['green']}">ONLINE</text>

  <!-- terminal -->
  <rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" rx="16" fill="{C['bg1']}" fill-opacity=".82" stroke="{C['edge']}"/>
  <path d="M{tx} {ty + 16}a16 16 0 0 1 16 -16h{tw_ - 32}a16 16 0 0 1 16 16v20h-{tw_}z" fill="#060D08"/>
  <circle cx="{tx + 24}" cy="{ty + 18}" r="6" fill="#FF5F57"/><circle cx="{tx + 46}" cy="{ty + 18}" r="6" fill="#FEBC2E"/><circle cx="{tx + 68}" cy="{ty + 18}" r="6" fill="#28C840"/>
  <text x="{tx + tw_ / 2}" y="{ty + 23}" text-anchor="middle" font-size="13" fill="{C['dim']}">~/nilesh/profile.json</text>
  <line x1="{tx}" y1="{ty + 36}" x2="{tx + tw_}" y2="{ty + 36}" stroke="{C['edge']}"/>
  {''.join(term)}

  <rect width="{W}" height="{H}" fill="url(#scan)" opacity=".45"/>
</g>
{beam_border(W, H, 24, delay=-3.5)}
"""
    return svg(W, H, body, defs=defs, css=css,
               title="Profile card — Nilesh Singh",
               desc="Dot-matrix portrait with a scanning beam next to a typed profile.json: "
                    "Data Analyst | AI Evaluation; BCA Data Science at Sri Balaji University; "
                    "Python, SQL, Power BI, Excel, R; Cloud Application Developer intern at Codefirst Technology; "
                    "Pune, India; open to Data Analyst, AI Trainer and AI Evaluation roles.")
