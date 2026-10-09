"""Hero banner: aurora + data rain + synthwave grid + glitch name + live panel."""
import random

from lib import BEAM_CSS, BLUR_DEFS, C, Typewriter, beam_border, esc, f, rounded_clip, smooth_path, svg


def hero():
    W, H = 1000, 460
    rnd = random.Random(11)

    # ── data rain ──────────────────────────────────────────────────────────
    glyphs = list("0101010110ΣσμκΔ%{}[]<>/|+=*#;:")
    rain = []
    for i in range(42):
        x = 14 + i * 24
        n = rnd.randint(9, 19)
        chars = [rnd.choice(glyphs) for _ in range(n)]
        dur = rnd.uniform(7, 15)
        delay = -rnd.uniform(0, dur)
        tsp = "".join(f'<tspan x="{x}" dy="20">{esc(c)}</tspan>' for c in chars[:-1])
        tsp += f'<tspan x="{x}" dy="20" fill="#F4FFD0">{esc(chars[-1])}</tspan>'
        rain.append(
            f'<g class="col" style="--h:{n * 20}px;animation-duration:{dur:.1f}s;'
            f'animation-delay:{delay:.1f}s"><text fill="url(#rainG)" font-size="16" y="-10">{tsp}</text></g>')

    # ── perspective grid (floor) ───────────────────────────────────────────
    vp_x, hz, bottom = 500, 296, 420
    grid = []
    for xb in range(-1400, 2401, 140):
        grid.append(f'<line x1="{vp_x}" y1="{hz}" x2="{xb}" y2="{bottom}"/>')
    for k in range(1, 9):
        y = hz + (bottom - hz) * (k / 8) ** 2.1
        grid.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')

    # ── right "live dashboard" panel ───────────────────────────────────────
    px, py, pw, ph = 636, 40, 322, 354
    pts = [(px + 22 + i * 25.2, py + 252 - v) for i, v in
           enumerate([6, 18, 12, 32, 26, 48, 40, 64, 56, 82, 74, 100])]
    line = smooth_path(pts)
    area = line + f"L{f(pts[-1][0])} {py + 252}L{f(pts[0][0])} {py + 252}Z"
    bars = []
    nb, bw, gap = 15, 12, 6.4
    for i in range(nb):
        h = rnd.randint(18, 56)
        bx = px + 22 + i * (bw + gap)
        by = py + 330 - h
        d = rnd.uniform(1.5, 3.2)
        bars.append(f'<rect class="eq" x="{f(bx)}" y="{by}" width="{bw}" height="{h}" rx="3" '
                    f'fill="url(#barG)" style="animation-duration:{d:.2f}s;animation-delay:-{rnd.uniform(0, d):.2f}s"/>')

    tw = Typewriter(cycle=15.0, per=0.055)
    roles = [
        ("Data Analyst × AI Evaluation", C["lime"]),
        ("messy datasets → tested pipelines", C["mint"]),
        ("evidence first, hype never", C["cyan"]),
    ]
    typed, t = [], 0.0
    for idx, (txt, col) in enumerate(roles):
        hold = 5.0 - len(txt) * tw.per
        typed.append(tw.line(txt, 82, 326, start=t, hold=hold, size=21, fill=col, cursor=col, alt=(idx > 0)))
        t += 5.0

    ticker_txt = "DATA QUALITY  ◆  LLM EVALUATION  ◆  DASHBOARDS THAT DECIDE  ◆  TESTED PIPELINES, NOT NOTEBOOK DEMOS  ◆  EVIDENCE FIRST, HYPE NEVER  ◆  "
    TW = int(len(ticker_txt) * 10.4)
    chips = [("Python", 48, 76), ("SQL", 134, 56), ("Power BI", 200, 96), ("LLM Evals", 306, 100), ("Streamlit", 416, 100)]
    chip_svg = "".join(
        f'<g class="chip" style="animation-delay:{i * .45:.2f}s"><rect x="{x}" y="356" width="{w}" height="28" rx="14" '
        f'fill="{C["lime"]}" fill-opacity=".07" stroke="{C["lime"]}" stroke-opacity=".35"/>'
        f'<text x="{x + w / 2}" y="375" text-anchor="middle" font-size="13" fill="{C["text"]}" '
        f'textLength="{w - 28}" lengthAdjust="spacingAndGlyphs">{esc(lbl)}</text></g>'
        for i, (lbl, x, w) in enumerate(chips))

    defs = f"""
{BLUR_DEFS}
{rounded_clip('rc', W, H, 24)}
<linearGradient id="rainG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['lime']}" stop-opacity="0"/><stop offset=".85" stop-color="{C['lime']}" stop-opacity=".55"/><stop offset="1" stop-color="{C['green']}"/></linearGradient>
<linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['bg0']}" stop-opacity=".92"/><stop offset=".55" stop-color="{C['bg0']}" stop-opacity=".62"/><stop offset="1" stop-color="{C['bg0']}" stop-opacity="0"/></linearGradient>
<linearGradient id="nameG" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="420" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{C['lime']}"/><stop offset=".5" stop-color="{C['mint']}"/><stop offset="1" stop-color="{C['cyan']}"/>
  <animate attributeName="x1" values="40;-340;40" dur="9s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="420;40;420" dur="9s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="barG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{C['green']}" stop-opacity=".25"/><stop offset="1" stop-color="{C['lime']}"/></linearGradient>
<linearGradient id="areaG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['lime']}" stop-opacity=".35"/><stop offset="1" stop-color="{C['lime']}" stop-opacity="0"/></linearGradient>
<linearGradient id="sweepG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['lime']}" stop-opacity="0"/><stop offset=".5" stop-color="{C['lime']}" stop-opacity=".35"/><stop offset="1" stop-color="{C['lime']}" stop-opacity="0"/></linearGradient>
<linearGradient id="hzG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['lime']}" stop-opacity=".0"/><stop offset="1" stop-color="{C['lime']}" stop-opacity=".16"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern>
<linearGradient id="tickFade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".06" stop-color="#fff"/><stop offset=".94" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="tickM"><rect width="{W}" height="40" fill="url(#tickFade)"/></mask>
"""
    css = BEAM_CSS + f"""
.aur{{animation:drift 16s ease-in-out infinite alternate}}
.a2{{animation-duration:21s;animation-delay:-6s}} .a3{{animation-duration:18s;animation-delay:-11s}}
@keyframes drift{{from{{transform:translate(-50px,-20px) scale(1)}}to{{transform:translate(70px,30px) scale(1.18)}}}}
.col{{animation:fall 10s linear infinite;transform-box:fill-box}}
@keyframes fall{{from{{transform:translateY(calc(-1 * var(--h)))}}to{{transform:translateY({H + 20}px)}}}}
.sweep{{animation:sweep 6s ease-in-out infinite}}
@keyframes sweep{{0%{{transform:translateX(-340px)}}100%{{transform:translateX(1060px)}}}}
.blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3.2);opacity:0}}}}
.g1,.g2{{opacity:0;animation:glitch 6.5s steps(1) infinite}} .g2{{animation-name:glitch2}}
@keyframes glitch{{0%,89%,100%{{opacity:0;transform:translate(0)}}90%{{opacity:.85;transform:translate(-6px,1px)}}91%{{opacity:0}}92%{{opacity:.8;transform:translate(5px,-2px)}}93.5%{{opacity:0}}}}
@keyframes glitch2{{0%,89%,100%{{opacity:0;transform:translate(0)}}90.5%{{opacity:.85;transform:translate(6px,-1px)}}91.5%{{opacity:0}}93%{{opacity:.8;transform:translate(-5px,2px)}}94%{{opacity:0}}}}
.name{{animation:jit 6.5s steps(1) infinite}}
@keyframes jit{{0%,89.5%,100%{{transform:none}}90%{{transform:skewX(-6deg) translateX(3px)}}91%{{transform:none}}92%{{transform:skewX(5deg) translateX(-2px)}}93.5%{{transform:none}}}}
.uline{{transform-box:fill-box;transform-origin:left;animation:uline 7s cubic-bezier(.2,.8,.2,1) infinite}}
@keyframes uline{{0%{{transform:scaleX(0)}}14%,88%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
.chip{{animation:float 4.5s ease-in-out infinite}} @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
.panel{{animation:hover 7s ease-in-out infinite}} @keyframes hover{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.eq{{transform-box:fill-box;transform-origin:50% 100%;animation:eq 2.2s ease-in-out infinite alternate}}
@keyframes eq{{from{{transform:scaleY(.28)}}to{{transform:scaleY(1)}}}}
.draw{{stroke-dasharray:100;animation:draw 6s ease-in-out infinite}}
@keyframes draw{{0%{{stroke-dashoffset:100}}35%,90%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:-100}}}}
.fadeA{{animation:fadeA 6s ease-in-out infinite}} @keyframes fadeA{{0%,15%{{opacity:0}}40%,88%{{opacity:1}}100%{{opacity:0}}}}
.comet{{stroke-dasharray:5 95;animation:comet 3.2s linear infinite}} @keyframes comet{{from{{stroke-dashoffset:5}}to{{stroke-dashoffset:-95}}}}
.tick{{animation:tick 38s linear infinite}} @keyframes tick{{to{{transform:translateX(-{TW}px)}}}}
{tw.keyframes()}
"""

    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
  <g opacity=".9">
    <ellipse class="aur" cx="190" cy="120" rx="270" ry="140" fill="{C['lime']}" opacity=".20" filter="url(#bl60)"/>
    <ellipse class="aur a2" cx="820" cy="360" rx="290" ry="150" fill="{C['cyan']}" opacity=".15" filter="url(#bl60)"/>
    <ellipse class="aur a3" cx="560" cy="40" rx="230" ry="110" fill="{C['violet']}" opacity=".13" filter="url(#bl60)"/>
  </g>
  <rect y="{hz}" width="{W}" height="{bottom - hz}" fill="url(#hzG)"/>
  <g stroke="{C['lime']}" stroke-opacity=".16" stroke-width="1" clip-path="url(#floor)">{''.join(grid)}</g>
  <clipPath id="floor"><rect y="{hz}" width="{W}" height="{bottom - hz}"/></clipPath>
  <rect class="sweep" y="{hz}" width="340" height="{bottom - hz}" fill="url(#sweepG)" clip-path="url(#floor)"/>
  <g opacity=".85">{''.join(rain)}</g>
  <rect width="{W}" height="{H}" fill="url(#scrim)"/>

  <!-- status chip -->
  <g>
    <rect x="48" y="36" width="246" height="30" rx="15" fill="{C['lime']}" fill-opacity=".08" stroke="{C['lime']}" stroke-opacity=".45"/>
    <circle class="pulse" cx="68" cy="51" r="4" fill="{C['lime']}"/><circle cx="68" cy="51" r="4" fill="{C['lime']}"/>
    <text x="84" y="56" font-size="12.5" letter-spacing="1.6" fill="{C['lime']}" textLength="196" lengthAdjust="spacing">OPEN TO ROLES · PUNE, IN</text>
  </g>

  <!-- name -->
  <g font-size="92" font-weight="800" letter-spacing="-2">
    <g class="g1" fill="{C['cyan']}"><text x="44" y="158">NILESH</text><text x="44" y="244">SINGH</text></g>
    <g class="g2" fill="{C['pink']}"><text x="44" y="158">NILESH</text><text x="44" y="244">SINGH</text></g>
    <g class="name" fill="url(#nameG)"><text x="44" y="158">NILESH</text><text x="44" y="244">SINGH</text></g>
  </g>
  <rect class="uline" x="48" y="268" width="330" height="3" rx="1.5" fill="url(#nameG)"/>

  <!-- role typewriter -->
  <text x="48" y="326" font-size="21" fill="{C['dim']}">➜</text>
  {''.join(typed)}
  {''.join(chip_svg)}

  <!-- live dashboard panel -->
  <g class="panel">
    <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="{C['bg1']}" fill-opacity=".72" stroke="{C['lime']}" stroke-opacity=".28"/>
    <circle cx="{px + 22}" cy="{py + 22}" r="5" fill="#FF5F57"/><circle cx="{px + 40}" cy="{py + 22}" r="5" fill="#FEBC2E"/><circle cx="{px + 58}" cy="{py + 22}" r="5" fill="#28C840"/>
    <text x="{px + pw - 18}" y="{py + 26}" text-anchor="end" font-size="12" fill="{C['dim']}">eval.dashboard · live</text>
    <text x="{px + 22}" y="{py + 72}" font-size="32" font-weight="800" fill="{C['lime']}">98.85%</text>
    <text x="{px + 22}" y="{py + 92}" font-size="11.5" fill="{C['dim']}">data quality score</text>
    <text x="{px + 176}" y="{py + 72}" font-size="28" font-weight="800" fill="{C['mint']}">κ 0.902</text>
    <text x="{px + 176}" y="{py + 92}" font-size="11.5" fill="{C['dim']}">human agreement</text>
    <g>
      <path class="fadeA" d="{area}" fill="url(#areaG)"/>
      <path class="draw" d="{line}" pathLength="100" fill="none" stroke="{C['lime']}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path class="comet" d="{line}" pathLength="100" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" opacity=".9"/>
      <circle class="fadeA" cx="{f(pts[-1][0])}" cy="{f(pts[-1][1])}" r="4" fill="{C['lime']}"/>
      <circle class="pulse" cx="{f(pts[-1][0])}" cy="{f(pts[-1][1])}" r="4" fill="{C['lime']}"/>
    </g>
    <line x1="{px + 22}" y1="{py + 330}" x2="{px + pw - 22}" y2="{py + 330}" stroke="{C['edge']}"/>
    {''.join(bars)}
  </g>

  <!-- ticker -->
  <rect y="{H - 42}" width="{W}" height="42" fill="#000" fill-opacity=".45"/>
  <line x1="0" y1="{H - 42}" x2="{W}" y2="{H - 42}" stroke="{C['lime']}" stroke-opacity=".25"/>
  <g transform="translate(0 {H - 42})" mask="url(#tickM)"><g class="tick">
    <text y="26" font-size="12.5" fill="{C['dim']}" textLength="{TW}" lengthAdjust="spacing">{esc(ticker_txt)}</text>
    <text x="{TW}" y="26" font-size="12.5" fill="{C['dim']}" textLength="{TW}" lengthAdjust="spacing">{esc(ticker_txt)}</text>
  </g></g>

  <rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5" pointer-events="none"/>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
</g>
{beam_border(W, H, 24)}
"""
    return svg(W, H, body, defs=defs, css=css,
               title="Nilesh Singh — Data Analyst × AI Evaluation",
               desc="Animated banner: data rain, a glitching gradient name, a typewriter cycling through "
                    "'Data Analyst × AI Evaluation', 'messy datasets → tested pipelines' and "
                    "'evidence first, hype never', and a live evaluation dashboard panel.")
