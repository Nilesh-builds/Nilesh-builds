"""Page chrome: section headers, divider, link buttons, contact radar, footer waves."""
import math

from lib import BEAM_CSS, BLUR_DEFS, C, Typewriter, beam_border, esc, f, rounded_clip, svg

SPARK_DEFS = (f'<linearGradient id="sparkG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["lime"]}" stop-opacity="0"/>'
              f'<stop offset=".7" stop-color="{C["lime"]}"/><stop offset="1" stop-color="#F4FFD0"/></linearGradient>')


def section_header(index: str, cmd: str, tag: str, *, alt: str):
    W, H = 1000, 60
    tw = Typewriter(cycle=10.0, per=0.055)
    typed = tw.line(cmd, 108, 37, start=0.3, hold=10.0 - 0.3 - len(cmd) * tw.per - 0.2, size=18,
                    fill=C["text"], cursor=C["lime"])
    tag_w = len(tag) * 7.4 + 34
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 14)}{SPARK_DEFS}
<linearGradient id="hdrBg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>"""
    css = f"""
.spark{{animation:spark 4.2s cubic-bezier(.5,0,.5,1) infinite}}
@keyframes spark{{from{{transform:translateX(-200px)}}to{{transform:translateX({W + 60}px)}}}}
.idx{{animation:idx 3s ease-in-out infinite}} @keyframes idx{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
.dotp{{animation:dotp 1.6s ease-in-out infinite}} @keyframes dotp{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
{tw.keyframes()}
"""
    dots = "".join(f'<circle class="dotp" cx="{W - 24 - tag_w - 16 + i * 10}" cy="30" r="2.2" fill="{C["lime"]}" style="animation-delay:{i * .25}s"/>' for i in range(3))
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="url(#hdrBg)"/>
  <rect class="idx" x="14" y="12" width="36" height="36" rx="10" fill="{C['lime']}" fill-opacity=".1" stroke="{C['lime']}" stroke-opacity=".6"/>
  <text x="32" y="36" text-anchor="middle" font-size="16" font-weight="800" fill="{C['lime']}">{esc(index)}</text>
  <text x="66" y="37" font-size="18" font-weight="700" fill="{C['lime']}">❯</text>
  <text x="88" y="37" font-size="18" fill="{C['dim']}">$</text>
  {typed}
  {dots}
  <rect x="{W - 24 - tag_w}" y="18" width="{tag_w}" height="24" rx="12" fill="none" stroke="{C['edge']}"/>
  <text x="{W - 24 - tag_w / 2}" y="34.5" text-anchor="middle" font-size="12" letter-spacing=".6" fill="{C['dim']}">{esc(tag)}</text>
  <rect class="spark" y="{H - 2.5}" width="200" height="2.5" fill="url(#sparkG)"/>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="{C['edge']}" stroke-width="1.5"/>
"""
    return svg(W, H, body, defs=defs, css=css, title=alt, desc=f"Section header: $ {cmd}")


def divider():
    W, H = 1000, 24
    defs = f"""<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E8F2F" stop-opacity="0"/><stop offset=".5" stop-color="#5E8F2F" stop-opacity=".85"/><stop offset="1" stop-color="#5E8F2F" stop-opacity="0"/></linearGradient>
<linearGradient id="pl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['lime']}" stop-opacity="0"/><stop offset=".6" stop-color="{C['lime']}"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#ln)"/></mask>"""
    css = f"""
.pl{{animation:run 5s cubic-bezier(.45,0,.55,1) infinite}} @keyframes run{{from{{transform:translateX(-160px)}}to{{transform:translateX({W}px)}}}}
.dm{{transform-box:fill-box;transform-origin:center;animation:spin 8s linear infinite}} @keyframes spin{{to{{transform:rotate(360deg)}}}}
.pu{{transform-box:fill-box;transform-origin:center;animation:pu 2.4s ease-out infinite}} @keyframes pu{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(3);opacity:0}}}}
"""
    body = f"""
<rect y="11" width="{W}" height="2" fill="url(#ln)"/>
<g mask="url(#m)"><rect class="pl" y="10.5" width="160" height="3" rx="1.5" fill="url(#pl)"/></g>
<rect x="472" y="2" width="56" height="20" fill="#0A0F08" rx="10"/>
<rect class="dm" x="494" y="6" width="12" height="12" transform="translate(0 0)" fill="{C['lime']}" stroke="#0A0F08" stroke-width="2" rx="2"/>
<circle class="pu" cx="500" cy="12" r="5" fill="none" stroke="{C['lime']}" stroke-width="1.5"/>
<circle cx="482" cy="12" r="2" fill="{C['mute']}"/><circle cx="518" cy="12" r="2" fill="{C['mute']}"/>
"""
    return svg(W, H, body, defs=defs, css=css, title="divider", desc="")


def button(label: str, glyph: str, delay: float):
    W, H = 232, 60
    css = BEAM_CSS + f"""
.shine{{animation:shine 5s ease-in-out infinite;animation-delay:{delay}s}}
@keyframes shine{{0%,55%{{transform:translateX(-90px) skewX(-20deg)}}100%{{transform:translateX({W + 90}px) skewX(-20deg)}}}}
.arrow{{animation:nudge 1.8s ease-in-out infinite}} @keyframes nudge{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(3px,-3px)}}}}
"""
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 16)}
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>"""
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg1']}"/>
  <rect class="shine" x="0" y="0" width="70" height="{H}" fill="url(#sh)"/>
  <rect x="12" y="12" width="36" height="36" rx="10" fill="{C['lime']}"/>
  <text x="30" y="36" text-anchor="middle" font-size="15" font-weight="800" fill="{C['bg0']}">{esc(glyph)}</text>
  <text x="62" y="36" font-size="15" font-weight="700" letter-spacing="1.4" fill="{C['text']}">{esc(label)}</text>
  <text class="arrow" x="{W - 30}" y="37" font-size="18" font-weight="700" fill="{C['lime']}">↗</text>
</g>
{beam_border(W, H, 16, dur=5.5, delay=-delay * 2, inset=1.2)}
"""
    return svg(W, H, body, defs=defs, css=css, title=label.title(), desc=f"Link button: {label.title()}")


def contact_banner():
    W, H = 1000, 250
    cx, cy = 790, 125
    blips = [(-52, -30), (44, 38), (70, -50), (-20, 62), (22, -70)]
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 24)}
<radialGradient id="sw" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({cx} {cy}) scale(125)"><stop offset="0" stop-color="{C['lime']}" stop-opacity=".0"/><stop offset="1" stop-color="{C['lime']}" stop-opacity=".55"/></radialGradient>
<pattern id="dg" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="{C['lime']}" opacity=".13"/></pattern>
<linearGradient id="hl" gradientUnits="userSpaceOnUse" x1="48" y1="0" x2="520" y2="0"><stop offset="0" stop-color="{C['lime']}"/><stop offset=".6" stop-color="{C['mint']}"/><stop offset="1" stop-color="{C['cyan']}"/></linearGradient>"""
    tw = Typewriter(cycle=12.0, per=0.05)
    sub = "open to: data analyst · business analyst · ai trainer · ai evaluation"
    typed = tw.line(sub, 48, 168, start=0.5, hold=12 - 0.5 - len(sub) * tw.per - 0.4, size=14,
                    fill=C["text"], cursor=C["lime"])
    css = BEAM_CSS + f"""
.rip{{transform-box:fill-box;transform-origin:center;animation:rip 4.8s ease-out infinite}}
@keyframes rip{{0%{{transform:scale(.15);opacity:.9}}100%{{transform:scale(1);opacity:0}}}}
.sw{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:rot 6s linear infinite}} @keyframes rot{{to{{transform:rotate(360deg)}}}}
.bl{{opacity:0;animation:bl 6s linear infinite}} @keyframes bl{{0%{{opacity:1}}60%,100%{{opacity:0}}}}
.cen{{transform-box:fill-box;transform-origin:center;animation:cen 2.6s ease-in-out infinite}} @keyframes cen{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.18)}}}}
.fl{{animation:fl 5s ease-in-out infinite}} @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
.blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
{tw.keyframes()}
"""
    rings = "".join(f'<circle class="rip" cx="{cx}" cy="{cy}" r="120" fill="none" stroke="{C["lime"]}" stroke-width="1.6" style="animation-delay:{i * 1.2}s"/>' for i in range(4))
    static = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["lime"]}" stroke-opacity=".16"/>' for r in (40, 80, 120))
    bl = "".join(f'<circle class="bl" cx="{cx + dx}" cy="{cy + dy}" r="4" fill="{C["mint"]}" style="animation-delay:{(math.degrees(math.atan2(dy, dx)) % 360) / 360 * 6:.2f}s"/>' for dx, dy in blips)
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
  <rect width="{W}" height="{H}" fill="url(#dg)"/>
  <ellipse cx="{cx}" cy="{cy}" rx="260" ry="170" fill="{C['lime']}" opacity=".12" filter="url(#bl60)"/>
  <ellipse cx="120" cy="230" rx="260" ry="100" fill="{C['cyan']}" opacity=".07" filter="url(#bl60)"/>
  <line x1="{cx - 125}" y1="{cy}" x2="{cx + 125}" y2="{cy}" stroke="{C['lime']}" stroke-opacity=".16"/><line x1="{cx}" y1="{cy - 125}" x2="{cx}" y2="{cy + 125}" stroke="{C['lime']}" stroke-opacity=".16"/>
  {static}{rings}
  <g class="sw"><path d="M{cx} {cy}L{cx + 120} {cy}A120 120 0 0 0 {cx + 120 * math.cos(-math.pi / 2.6):.1f} {cy + 120 * math.sin(-math.pi / 2.6):.1f}Z" fill="url(#sw)"/><line x1="{cx}" y1="{cy}" x2="{cx + 120}" y2="{cy}" stroke="{C['lime']}" stroke-width="2"/></g>
  {bl}
  <circle class="cen" cx="{cx}" cy="{cy}" r="9" fill="{C['lime']}"/>
  <circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{C['lime']}" stroke-opacity=".6"/>

  <text x="48" y="64" font-size="13" letter-spacing="2.4" fill="{C['dim']}">// SIGNAL DETECTED</text>
  <text x="46" y="122" font-size="52" font-weight="800" letter-spacing="-1" fill="url(#hl)">LET'S TALK DATA.</text>
  {typed}
  <text x="48" y="206" font-size="13" fill="{C['dim']}">replies land in my inbox — evidence-based answers guaranteed*</text>
  <text x="48" y="226" font-size="10.5" fill="{C['mute']}">*as far as the sample size allows</text>
</g>
{beam_border(W, H, 24, dur=9)}
"""
    return svg(W, H, body, defs=defs, css=css, title="Let's talk data — open to roles",
               desc="Animated radar. Open to Data Analyst, Business Analyst, AI Trainer and AI Evaluation roles.")


def footer():
    W, H = 1000, 170
    rows = [(0.74, 20, 560, C["lime"], .14, 19), (0.83, 15, 420, C["mint"], .12, 27), (0.91, 10, 300, C["cyan"], .1, 38)]
    waves = []
    for k, (base, amp, period, col, op, dur) in enumerate(rows):
        pts = [(x, H * base + amp * math.sin(2 * math.pi * x / period + k)) for x in range(0, W + period + 1, 10)]
        d = "M" + "L".join(f"{x} {f(y)}" for x, y in pts) + f"L{pts[-1][0]} {H}L0 {H}Z"
        waves.append(f'<path class="wv" d="{d}" fill="{col}" fill-opacity="{op}" style="--p:{period}px;animation-duration:{dur}s;'
                     f'animation-direction:{"reverse" if k % 2 else "normal"}"/>')
    pts = [(x, H * .74 + 20 * math.sin(2 * math.pi * x / 560)) for x in range(0, W + 561, 10)]
    edge = "M" + "L".join(f"{x} {f(y)}" for x, y in pts)
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 24)}
<linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>"""
    css = """
.wv{animation:wv 20s linear infinite} @keyframes wv{to{transform:translateX(calc(-1 * var(--p)))}}
.tw1{animation:tw1 6s ease-in-out infinite} @keyframes tw1{0%,100%{opacity:.75}50%{opacity:1}}
"""
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="url(#fbg)"/>
  {''.join(waves)}
  <path class="wv" d="{edge}" fill="none" stroke="{C['lime']}" stroke-opacity=".7" stroke-width="1.6" style="--p:560px;animation-duration:19s"/>
  <text class="tw1" x="{W / 2}" y="54" text-anchor="middle" font-size="16" fill="{C['text']}">// student by day  |  building an analytics portfolio, one dataset at a time</text>
  <text x="{W / 2}" y="80" text-anchor="middle" font-size="12" letter-spacing="1.2" fill="{C['dim']}">hand-drawn SVG · pure CSS motion · zero JavaScript · zero trackers</text>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="{C['edge']}" stroke-width="1.5"/>
"""
    return svg(W, H, body, defs=defs, css=css, title="Footer",
               desc="Student by day, building an analytics portfolio one dataset at a time.")
