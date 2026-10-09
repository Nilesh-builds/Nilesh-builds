"""Content panels: metrics gauges, project cards, tech marquee, skill bars, timeline, certs."""
import math
import random
import textwrap

from lib import BEAM_CSS, BLUR_DEFS, C, beam_border, esc, f, ring_arc, rounded_clip, svg

CHAR = 0.6  # monospace advance in em; used only for *layout estimates*


def wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False)


def chips(labels, x0, y0, maxw, *, accent, size=11.5, h=26, gap=8, pad=14):
    """Flow-layout pills. Returns (svg, total_height). textLength pins width across fonts."""
    out, x, y = [], x0, y0
    for lbl in labels:
        tw = len(lbl) * size * CHAR
        w = tw + 2 * pad
        if x + w > x0 + maxw:
            x, y = x0, y + h + gap
        out.append(
            f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="{h}" rx="{h / 2}" fill="{accent}" fill-opacity=".08" '
            f'stroke="{accent}" stroke-opacity=".3"/>'
            f'<text x="{f(x + pad)}" y="{y + h / 2 + size * .35:.1f}" font-size="{size}" fill="{C["text"]}" '
            f'textLength="{f(tw)}" lengthAdjust="spacingAndGlyphs">{esc(lbl)}</text>')
        x += w + 8
    return "".join(out), y + h - y0


# ─────────────────────────────────────────────────────────────────────────────
def metrics():
    W, H = 1000, 304
    cards = [
        ("TRAINLENS", "98.85%", 98.85, "Data quality score", "Benchmarked on 852 synthetic support conversations", C["lime"], None),
        ("LLM-EVAL", "κ 0.902", 90.2, "Human agreement", "Human-vs-human κ on blind review of the judge outputs", C["cyan"], None),
        ("LLM-EVAL", "11/11", 100, "Judges validated", "LLM judges checked against reference answers", C["violet"], None),
        ("LLM-EVAL", "9", None, "Evaluation dimensions", "Factuality, bias, toxicity, refusal, injection, hallucination…", C["amber"], 9),
    ]
    cw, gap = 226, 32
    defs = f"""{BLUR_DEFS}"""
    css = """
.gauge{stroke-dasharray:100;animation:gauge 9s cubic-bezier(.3,.7,.2,1) infinite;animation-fill-mode:backwards}
@keyframes gauge{0%{stroke-dashoffset:100}16%,86%{stroke-dashoffset:var(--o)}96%,100%{stroke-dashoffset:100}}
.orbit{transform-box:view-box;animation:spin 7s linear infinite} @keyframes spin{to{transform:rotate(360deg)}}
.seg{animation:seg 9s ease-out infinite;animation-fill-mode:backwards;animation-delay:calc(var(--k) * .12s)}
@keyframes seg{0%{opacity:.08}5%,86%{opacity:1}96%,100%{opacity:.08}}
.num{animation:num 9s ease-out infinite;animation-fill-mode:backwards}
@keyframes num{0%{opacity:0;transform:translateY(8px)}10%,88%{opacity:1;transform:none}96%,100%{opacity:0;transform:none}}
.float{animation:fl 6s ease-in-out infinite} @keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.sw{animation:sw 6s linear infinite;animation-delay:var(--d)} @keyframes sw{from{transform:translateY(-30px)}to{transform:translateY(300px)}}
"""
    out = []
    for i, (tag, big, pct, label, cap, col, segs) in enumerate(cards):
        x = i * (cw + gap)
        cx, cy, r = x + cw / 2, 128, 60
        arc = ring_arc(cx, cy, r)
        if segs:
            ring = []
            gap_deg, span = 8, 360 / segs
            for k in range(segs):
                a0 = math.radians(-90 + k * span + gap_deg / 2)
                a1 = math.radians(-90 + (k + 1) * span - gap_deg / 2)
                p = lambda a: (cx + r * math.cos(a), cy + r * math.sin(a))
                (x0, y0), (x1, y1) = p(a0), p(a1)
                d = f"M{f(x0)} {f(y0)}A{r} {r} 0 0 1 {f(x1)} {f(y1)}"
                ring.append(f'<path class="seg" style="--k:{k}" d="{d}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round"/>')
            ring_svg = "".join(ring)
            spin = ""
        else:
            ring_svg = (f'<path d="{arc}" fill="none" stroke="{C["edge"]}" stroke-width="10"/>'
                        f'<path class="gauge" style="--o:{100 - pct:.2f};animation-delay:{i * .15:.2f}s" d="{arc}" pathLength="100" fill="none" '
                        f'stroke="{col}" stroke-width="10" stroke-linecap="round"/>')
            spin = ""
        orbit = (f'<g class="orbit" style="transform-origin:{f(cx)}px {cy}px;animation-delay:-{i * 1.3}s">'
                 f'<circle cx="{f(cx)}" cy="{cy - r - 16}" r="2.5" fill="{col}"/></g>')
        cap_lines = "".join(f'<text x="{f(cx)}" y="{236 + n * 15}" text-anchor="middle" font-size="11" fill="{C["dim"]}">{esc(l)}</text>'
                            for n, l in enumerate(wrap(cap, 31)[:3]))
        out.append(f"""
<g class="float" style="animation-delay:-{i * 1.5}s">
  <rect x="{x}" y="0" width="{cw}" height="{H - 6}" rx="20" fill="{C['bg1']}" stroke="{C['edge']}"/>
  <clipPath id="c{i}"><rect x="{x}" y="0" width="{cw}" height="{H - 6}" rx="20"/></clipPath>
  <g clip-path="url(#c{i})">
    <ellipse cx="{f(cx)}" cy="{cy}" rx="110" ry="90" fill="{col}" opacity=".13" filter="url(#bl60)"/>
    <rect class="sw" style="--d:-{i * 1.4}s" x="{x}" width="{cw}" height="30" fill="{col}" opacity=".05"/>
  </g>
  <text x="{x + 20}" y="30" font-size="11" letter-spacing="2" fill="{col}">{tag}</text>
  <circle cx="{x + cw - 24}" cy="26" r="3.5" fill="{col}"/>
  {ring_svg}{orbit}
  <text class="num" x="{f(cx)}" y="{cy + 10}" text-anchor="middle" font-size="{26 if len(big) < 6 else 22}" font-weight="800" fill="{C['text']}" style="animation-delay:{i * .15:.2f}s">{esc(big)}</text>
  <text x="{f(cx)}" y="212" text-anchor="middle" font-size="15" font-weight="700" fill="{C['text']}">{esc(label)}</text>
  {cap_lines}
</g>""")
    return svg(W, H, '<g transform="translate(0 7)">' + "".join(out) + "</g>", defs=defs, css=css, title="Impact at a glance",
               desc="98.85% data quality score on 852 synthetic conversations (TrainLens); κ 0.902 human-vs-human "
                    "agreement; 11 of 11 LLM judges validated against references; 9 evaluation dimensions.")


# ─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    dict(slug="trainlens", n="01", title="TrainLens", sub="AI training-data quality platform", badge="LIVE DEMO", col=C["lime"],
         desc="Five quality dimensions, eleven checks, Groq batch labeling with a rule-based fallback, and a confidence-based human review queue.",
         stats=[("98.85%", "quality score"), ("852", "conversations"), ("11", "checks")],
         stack=["Python", "pandas", "DuckDB", "Streamlit", "Plotly", "scikit-learn"]),
    dict(slug="llm-eval", n="02", title="LLM Safety Eval", sub="9-dimension response benchmark", badge="LIVE DEMO", col=C["cyan"],
         desc="Rule-based checks plus a 2-model LLM-judge ensemble with 95% bootstrap intervals, validated against references and blind human review.",
         stats=[("9", "dimensions"), ("κ 0.902", "human agreement"), ("4.28", "120B composite")],
         stack=["Python", "Groq", "pandas", "matplotlib", "Streamlit", "Jupyter"]),
    dict(slug="churn", n="03", title="Customer Churn", sub="Telco decision-support analysis", badge="LIVE DEMO", col=C["violet"],
         desc="Leakage-safe modeling with cross-validation, calibration and cost-sensitive thresholds. Balanced Random Forest chosen on business reasoning, not accuracy alone.",
         stats=[("SQL", "analysis views"), ("CV", "cross-validated"), ("Live", "review dashboard")],
         stack=["Python", "SQL", "pandas", "scikit-learn", "Streamlit"]),
    dict(slug="hr-suite", n="04", title="AI HR Automation", sub="6 n8n workflows, end to end", badge="AUTOMATION", col=C["amber"],
         desc="Onboarding, leave management, sentiment analysis, policy Q&A, an AI resume screener and a WhatsApp HR chatbot. Sheets as the store, GPT-4 as the brain.",
         stats=[("6", "workflows"), ("GPT-4", "AI layer"), ("3", "alert channels")],
         stack=["n8n", "Google Sheets", "OpenAI GPT-4", "Gmail", "Slack", "WhatsApp"]),
]


def project_card(p, idx):
    W, H = 440, 372
    col = p["col"]
    pad = 24
    inner = W - 2 * pad
    desc = "".join(
        f'<text x="{pad}" y="{144 + n * 19}" font-size="12.5" fill="{C["text"]}" fill-opacity=".86">{esc(l)}</text>'
        for n, l in enumerate(wrap(p["desc"], 50)[:4]))
    stats = []
    for k, (num, lbl) in enumerate(p["stats"]):
        sx = pad + k * (inner / 3)
        if k:
            stats.append(f'<line x1="{f(sx - 10)}" y1="228" x2="{f(sx - 10)}" y2="272" stroke="{C["edge"]}"/>')
        size = 24 if len(num) < 6 else 20
        stats.append(f'<text x="{f(sx)}" y="252" font-size="{size}" font-weight="800" fill="{col}">{esc(num)}</text>'
                     f'<text x="{f(sx)}" y="270" font-size="11" fill="{C["dim"]}">{esc(lbl)}</text>')
    chip_svg, _ = chips(p["stack"], pad, 300, inner, accent=col)
    badge_w = len(p["badge"]) * 7.8 + 46
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 22)}
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="{C['text']}"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="dg" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="{col}" opacity=".16"/></pattern>
<linearGradient id="dgF" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="dgM"><rect width="{W}" height="{H}" fill="url(#dgF)"/></mask>"""
    css = BEAM_CSS + f"""
.orb{{animation:orb 11s ease-in-out infinite alternate}} @keyframes orb{{from{{transform:translate(0,0)}}to{{transform:translate(-60px,50px) scale(1.2)}}}}
.shine{{animation:shine 8s ease-in-out infinite;animation-delay:{idx * 1.3}s}}
@keyframes shine{{0%,60%{{transform:translateX(-160px) skewX(-18deg)}}100%{{transform:translateX({W + 160}px) skewX(-18deg)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3);opacity:0}}}}
.ul{{transform-box:fill-box;transform-origin:left;animation:ul 8s cubic-bezier(.2,.8,.2,1) infinite;animation-delay:{idx * .4}s}}
@keyframes ul{{0%{{transform:scaleX(0)}}12%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
"""
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg1']}"/>
  <rect width="{W}" height="{H}" fill="url(#dg)" mask="url(#dgM)"/>
  <ellipse class="orb" cx="{W - 30}" cy="20" rx="180" ry="120" fill="{col}" opacity=".2" filter="url(#bl60)"/>
  <rect class="shine" x="0" y="0" width="120" height="{H}" fill="url(#sh)"/>
  <text x="{pad}" y="38" font-size="11" letter-spacing="2.4" fill="{C['dim']}">PROJECT {p['n']}</text>
  <g>
    <rect x="{W - pad - badge_w}" y="20" width="{badge_w}" height="26" rx="13" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".5"/>
    <circle class="pulse" cx="{W - pad - badge_w + 16}" cy="33" r="3.2" fill="{col}"/><circle cx="{W - pad - badge_w + 16}" cy="33" r="3.2" fill="{col}"/>
    <text x="{W - pad - badge_w + 28}" y="37.5" font-size="11" font-weight="700" letter-spacing="1.2" fill="{col}">{esc(p['badge'])}</text>
  </g>
  <text x="{pad}" y="82" font-size="26" font-weight="800" fill="url(#tg)">{esc(p['title'])}</text>
  <rect class="ul" x="{pad}" y="92" width="56" height="3" rx="1.5" fill="{col}"/>
  <text x="{pad}" y="116" font-size="13" fill="{col}" fill-opacity=".85">{esc(p['sub'])}</text>
  {desc}
  <line x1="{pad}" y1="216" x2="{W - pad}" y2="216" stroke="{C['edge']}"/>
  {''.join(stats)}
  <line x1="{pad}" y1="284" x2="{W - pad}" y2="284" stroke="{C['edge']}" stroke-dasharray="2 5"/>
  {chip_svg}
</g>
{beam_border(W, H, 22, dur=9, delay=-idx * 2.2, color=col)}
"""
    return svg(W, H, body, defs=defs, css=css, title=f"{p['title']} — {p['sub']}",
               desc=f"{p['desc']} Stats: " + ", ".join(f"{a} {b}" for a, b in p["stats"]) + ". Stack: " + ", ".join(p["stack"]) + ".")


# ─────────────────────────────────────────────────────────────────────────────
STACK_ROWS = [
    [("Python", C["lime"]), ("SQL", C["lime"]), ("R", C["lime"]), ("Bash", C["lime"]), ("HTML", C["lime"]), ("CSS", C["lime"]),
     ("PostgreSQL", C["cyan"]), ("MySQL", C["cyan"]), ("DuckDB", C["cyan"]), ("AWS", C["violet"]), ("Git", C["violet"]),
     ("GitHub", C["violet"]), ("VS Code", C["violet"])],
    [("pandas", C["mint"]), ("scikit-learn", C["mint"]), ("matplotlib", C["mint"]), ("seaborn", C["mint"]), ("Plotly", C["mint"]),
     ("Streamlit", C["amber"]), ("Power BI", C["amber"]), ("Excel", C["amber"]), ("PySpark", C["amber"]), ("Jupyter", C["amber"]),
     ("n8n", C["pink"]), ("Groq API", C["pink"]), ("OpenAI GPT-4", C["pink"])],
]


def stack():
    W, H = 1000, 142
    rows_svg, css_rows = [], []
    for r, items in enumerate(STACK_ROWS):
        ph, gap = 44, 12
        x, pills = 0, []
        for name, col in items:
            tw = len(name) * 14 * CHAR
            w = tw + 56
            pills.append(
                f'<g><rect x="{f(x)}" y="0" width="{f(w)}" height="{ph}" rx="{ph / 2}" fill="{C["bg1"]}" stroke="{C["edge"]}"/>'
                f'<circle cx="{f(x + 24)}" cy="{ph / 2}" r="4.5" fill="{col}"/><circle cx="{f(x + 24)}" cy="{ph / 2}" r="4.5" fill="{col}" opacity=".5" filter="url(#bl4)"/>'
                f'<text x="{f(x + 40)}" y="{ph / 2 + 5}" font-size="14" fill="{C["text"]}" textLength="{f(tw)}" lengthAdjust="spacingAndGlyphs">{esc(name)}</text></g>')
            x += w + gap
        set_w = x
        reps = math.ceil(W / set_w) + 1
        track = "".join(f'<g transform="translate({f(k * set_w)} 0)">{"".join(pills)}</g>' for k in range(reps))
        dur = set_w / 42
        rows_svg.append(f'<g transform="translate(0 {10 + r * 66})" mask="url(#fade)"><g class="trk{r}">{track}</g></g>')
        d_from, d_to = (0, -set_w) if r % 2 == 0 else (-set_w, 0)
        css_rows.append(f".trk{r}{{animation:m{r} {dur:.1f}s linear infinite}}"
                        f"@keyframes m{r}{{from{{transform:translateX({f(d_from)}px)}}to{{transform:translateX({f(d_to)}px)}}}}")
    defs = f"""{BLUR_DEFS}
<linearGradient id="ef" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#ef)"/></mask>"""
    return svg(W, H, "".join(rows_svg), defs=defs, css="".join(css_rows), title="Tech stack",
               desc="Python, SQL, R, Bash, HTML, CSS, PostgreSQL, MySQL, DuckDB, AWS, Git, GitHub, VS Code, pandas, scikit-learn, "
                    "matplotlib, seaborn, Plotly, Streamlit, Power BI, Excel, PySpark, Jupyter, n8n, Groq API, OpenAI GPT-4.")


# ─────────────────────────────────────────────────────────────────────────────
SKILLS = [
    ("Data Cleaning & EDA", 5, "Advanced", "Pandas, missing-value handling, outlier detection, feature engineering"),
    ("Machine Learning", 4, "Intermediate", "Logistic Regression, Random Forest, Decision Trees, model selection on business criteria"),
    ("Data Visualization", 4, "Intermediate", "Power BI dashboards, Excel reporting, matplotlib / seaborn charting"),
    ("SQL & Databases", 4, "Intermediate", "Querying, joins and aggregation for analysis-ready datasets"),
    ("Statistical Analysis", 4, "Intermediate", "Hypothesis-driven EDA, risk scoring, business recommendation write-ups"),
    ("Cloud (AWS)", 3, "Working Knowledge", "Cloud-native architecture from the Codefirst Technology internship"),
]
LEVEL_COL = {"Advanced": C["lime"], "Intermediate": C["mint"], "Working Knowledge": C["cyan"]}


def skills():
    rh = 78
    W, H = 1000, 24 + rh * len(SKILLS) + 12
    rows = []
    for i, (name, lvl, lab, detail) in enumerate(SKILLS):
        y = 24 + i * rh
        col = LEVEL_COL[lab]
        det = "".join(f'<text x="44" y="{y + 44 + n * 17}" font-size="12" fill="{C["dim"]}">{esc(l)}</text>' for n, l in enumerate(wrap(detail, 62)[:2]))
        segs = "".join(
            f'<rect x="{628 + k * 40}" y="{y + 12}" width="34" height="16" rx="4" fill="{C["edge"]}"/>'
            + (f'<rect class="sg" style="--i:{i * 5 + k}" x="{628 + k * 40}" y="{y + 12}" width="34" height="16" rx="4" fill="{col}"/>' if k < lvl else "")
            for k in range(5))
        rows.append(f"""
<g>
  <rect x="24" y="{y}" width="3" height="{rh - 14}" rx="1.5" fill="{col}" opacity=".85"/>
  <text x="44" y="{y + 22}" font-size="16" font-weight="700" fill="{C['text']}">{esc(name)}</text>
  {det}
  {segs}
  <text x="842" y="{y + 25}" font-size="12.5" font-weight="700" letter-spacing=".6" fill="{col}" textLength="{len(lab) * 7.5:.0f}" lengthAdjust="spacingAndGlyphs">{esc(lab)}</text>
  <text x="628" y="{y + 50}" font-size="11" fill="{C['mute']}">{lvl}/5</text>
  <line x1="44" y1="{y + rh - 8}" x2="{W - 24}" y2="{y + rh - 8}" stroke="{C['edge']}" stroke-opacity=".55"/>
</g>""")
    defs = f"""{BLUR_DEFS}{rounded_clip('rc', W, H, 22)}
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['lime']}" stop-opacity="0"/><stop offset="1" stop-color="{C['lime']}" stop-opacity=".1"/></linearGradient>"""
    css = BEAM_CSS + f"""
.sg{{transform-box:fill-box;transform-origin:left;animation:sg 10s cubic-bezier(.2,.8,.2,1) infinite;animation-delay:calc(var(--i) * .07s);animation-fill-mode:backwards}}
@keyframes sg{{0%{{transform:scaleX(0)}}6%,88%{{transform:scaleX(1)}}96%,100%{{transform:scaleX(0)}}}}
.scan{{animation:scan 6s ease-in-out infinite}} @keyframes scan{{from{{transform:translateY(-60px)}}to{{transform:translateY({H}px)}}}}
"""
    body = f"""
<g clip-path="url(#rc)">
  <rect width="{W}" height="{H}" fill="{C['bg1']}"/>
  <rect class="scan" width="{W}" height="60" fill="url(#scanG)"/>
  {''.join(rows)}
</g>
{beam_border(W, H, 22, dur=14, delay=-5)}
"""
    return svg(W, H, body, defs=defs, css=css, title="Analytics expertise",
               desc="; ".join(f"{n}: {l} ({d})" for n, _, l, d in SKILLS))


# ─────────────────────────────────────────────────────────────────────────────
def journey():
    W, H = 1000, 336
    stops = [
        dict(x=170, tag="EDUCATION", col=C["lime"], title="BCA — Data Science", l1="Sri Balaji University", l2="Pune, India",
             chips=["Python", "SQL", "R", "Power BI"]),
        dict(x=500, tag="EXPERIENCE", col=C["cyan"], title="Cloud App Developer", l1="Intern · Codefirst Technology", l2="Cloud-native apps, AWS fundamentals",
             chips=["AWS", "Cloud-Native", "App Dev"]),
        dict(x=830, tag="NOW", col=C["amber"], title="Open to work", l1="Data Analyst · AI Trainer", l2="AI Evaluation · Business Analyst",
             chips=["Pune", "Evidence-first"]),
    ]
    ly = 88
    defs = f"""{BLUR_DEFS}
<linearGradient id="lg" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="940" y2="0"><stop offset="0" stop-color="{C['lime']}"/><stop offset=".5" stop-color="{C['cyan']}"/><stop offset="1" stop-color="{C['amber']}"/></linearGradient>"""
    css = """
.draw{stroke-dasharray:100;animation:draw 10s ease-in-out infinite} @keyframes draw{0%{stroke-dashoffset:100}22%,88%{stroke-dashoffset:0}100%{stroke-dashoffset:-100}}
.comet{stroke-dasharray:6 94;animation:comet 4.5s linear infinite} @keyframes comet{from{stroke-dashoffset:6}to{stroke-dashoffset:-94}}
.pulse{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite} @keyframes ping{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.4);opacity:0}}
.card{animation:fl 6s ease-in-out infinite} @keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.pop{animation:pop 10s cubic-bezier(.2,.9,.3,1.2) infinite;animation-fill-mode:backwards;transform-box:fill-box;transform-origin:center}
@keyframes pop{0%{opacity:0;transform:scale(.4)}8%,90%{opacity:1;transform:scale(1)}98%,100%{opacity:0;transform:scale(1)}}
"""
    out = [f'<rect width="{W}" height="{H}" rx="22" fill="{C["bg0"]}"/><rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="22" fill="none" stroke="{C["edge"]}" stroke-width="1.5"/>',
           f'<line x1="60" y1="{ly}" x2="940" y2="{ly}" stroke="{C["edge"]}" stroke-width="3" stroke-linecap="round"/>',
           f'<path class="draw" d="M60 {ly}H940" pathLength="100" stroke="url(#lg)" stroke-width="3" stroke-linecap="round" fill="none"/>',
           f'<path class="comet" d="M60 {ly}H940" pathLength="100" stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none" opacity=".9"/>']
    for i, s in enumerate(stops):
        x, col = s["x"], s["col"]
        cw, ch, cy0 = 306, 184, 132
        chip_svg, _ = chips(s["chips"], x - cw / 2 + 20, cy0 + 126, cw - 36, accent=col, size=11, h=24, pad=11)
        out.append(f"""
<g>
  <text x="{x}" y="{ly - 30}" text-anchor="middle" font-size="12" letter-spacing="3" fill="{col}">{s['tag']}</text>
  <circle class="pulse" style="animation-delay:{i * .8}s" cx="{x}" cy="{ly}" r="9" fill="{col}"/>
  <circle class="pop" style="animation-delay:{i * .5}s" cx="{x}" cy="{ly}" r="10" fill="{C['bg0']}" stroke="{col}" stroke-width="3"/>
  <circle class="pop" style="animation-delay:{i * .5 + .15}s" cx="{x}" cy="{ly}" r="4" fill="{col}"/>
  <line x1="{x}" y1="{ly + 12}" x2="{x}" y2="{cy0}" stroke="{col}" stroke-opacity=".5" stroke-dasharray="3 4"/>
  <g class="card" style="animation-delay:-{i * 2}s">
    <rect x="{x - cw / 2}" y="{cy0}" width="{cw}" height="{ch}" rx="18" fill="{C['bg1']}" stroke="{col}" stroke-opacity=".35"/>
    <rect x="{x - cw / 2}" y="{cy0}" width="{cw}" height="4" rx="2" fill="{col}" opacity=".9"/>
    <text x="{x - cw / 2 + 20}" y="{cy0 + 40}" font-size="18" font-weight="800" fill="{C['text']}">{esc(s['title'])}</text>
    <text x="{x - cw / 2 + 20}" y="{cy0 + 66}" font-size="13" fill="{col}">{esc(s['l1'])}</text>
    <text x="{x - cw / 2 + 20}" y="{cy0 + 88}" font-size="12" fill="{C['dim']}">{esc(s['l2'])}</text>
    <line x1="{x - cw / 2 + 20}" y1="{cy0 + 106}" x2="{x + cw / 2 - 20}" y2="{cy0 + 106}" stroke="{C['edge']}"/>
    {chip_svg}
  </g>
</g>""")
    return svg(W, H, "".join(out), defs=defs, css=css, title="Experience and education timeline",
               desc="Education: BCA in Data Science at Sri Balaji University, Pune. Experience: Cloud Application Developer intern at "
                    "Codefirst Technology (AWS, cloud-native architecture, application development). Now: open to Data Analyst, "
                    "AI Trainer, AI Evaluation and Business Analyst roles.")


# ─────────────────────────────────────────────────────────────────────────────
CERTS = [
    ("Power BI for Data Analysts", "MICROSOFT PRESS", C["amber"]),
    ("SQL for Data Analysis", "SQL", C["cyan"]),
    ("Python for Data Analysis", "PYTHON", C["lime"]),
    ("Machine Learning with Python", "MACHINE LEARNING", C["mint"]),
    ("Deep Learning: Image Recognition", "DEEP LEARNING", C["violet"]),
    ("R for Data Science", "R", C["cyan"]),
    ("Excel + ChatGPT Power Tips", "EXCEL · AI", C["amber"]),
    ("Intro to Data Science", "FOUNDATIONS", C["lime"]),
    ("Advanced Algorithmic Thinking", "ALGORITHMS", C["mint"]),
]


def certs():
    W, cw, ch, gx, gy = 1000, 316, 70, 26, 16
    H = 3 * ch + 2 * gy + 8
    css = """
.sheen{animation:sheen 7s ease-in-out infinite;animation-delay:var(--d)} @keyframes sheen{0%,62%{transform:translateX(-120px) skewX(-20deg)}100%{transform:translateX(440px) skewX(-20deg)}}
.chk{stroke-dasharray:24;animation:chk 8s ease-out infinite;animation-delay:var(--d);animation-fill-mode:backwards}
@keyframes chk{0%{stroke-dashoffset:24}8%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:24}}
.ch{animation:fl 6s ease-in-out infinite;animation-delay:var(--d)} @keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
"""
    out = []
    for i, (name, tag, col) in enumerate(CERTS):
        r, c = divmod(i, 3)
        x, y = c * (cw + gx), r * (ch + gy) + 4
        tw = len(name) * 12.5 * CHAR
        out.append(f"""
<g class="ch" style="--d:-{i * .7:.1f}s">
  <clipPath id="k{i}"><rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16"/></clipPath>
  <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{C['bg1']}" stroke="{C['edge']}"/>
  <rect x="{x}" y="{y + 14}" width="3" height="{ch - 28}" rx="1.5" fill="{col}"/>
  <g clip-path="url(#k{i})"><rect class="sheen" style="--d:{i * .6:.1f}s" x="{x}" y="{y}" width="60" height="{ch}" fill="#fff" opacity=".06"/></g>
  <circle cx="{x + 34}" cy="{y + ch / 2}" r="14" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6"/>
  <path class="chk" style="--d:{i * .25:.2f}s" d="M{x + 27} {y + ch / 2 + .5}l5 5l9 -10" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="{x + 62}" y="{y + 31}" font-size="12.5" font-weight="700" fill="{C['text']}" textLength="{f(tw)}" lengthAdjust="spacingAndGlyphs">{esc(name)}</text>
  <text x="{x + 62}" y="{y + 52}" font-size="10.5" letter-spacing="1.6" fill="{col}" fill-opacity=".85">{esc(tag)}</text>
</g>""")
    return svg(W, H, "".join(out), title="Certifications",
               desc="Certifications: " + "; ".join(n for n, _, _ in CERTS) + ".")
