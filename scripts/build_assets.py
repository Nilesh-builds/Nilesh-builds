#!/usr/bin/env python3
"""Regenerate every SVG in ../assets.

    python3 scripts/build_assets.py            # build everything
    python3 scripts/build_assets.py hero       # build selected targets

Requires Pillow + numpy (only for vectorising the portrait).
"""
import sys

from lib import write

TARGETS = {}


def target(fn):
    TARGETS[fn.__name__] = fn
    return fn


def build_hero():
    from hero import hero
    write("hero.svg", hero())


TARGETS["hero"] = build_hero


def build_profile():
    from profile_card import profile_card
    write("profile-card.svg", profile_card())


TARGETS["profile"] = build_profile

def build_chrome():
    import chrome
    write("divider.svg", chrome.divider())
    write("contact-banner.svg", chrome.contact_banner())
    write("footer.svg", chrome.footer())
    for slug, label, glyph, delay in [("linkedin", "LINKEDIN", "in", 0), ("email", "EMAIL", "@", 1.2),
                                      ("github", "GITHUB", "gh", 2.4), ("portfolio", "PORTFOLIO", "⌘", 3.6)]:
        write(f"btn-{slug}.svg", chrome.button(label, glyph, delay))
    for slug, idx, cmd, tag, alt in HEADERS:
        write(f"h-{slug}.svg", chrome.section_header(idx, cmd, tag, alt=alt))


def build_panels():
    import panels
    write("metrics.svg", panels.metrics())
    write("stack.svg", panels.stack())
    write("skills.svg", panels.skills())
    write("journey.svg", panels.journey())
    write("certs.svg", panels.certs())
    for i, p in enumerate(panels.PROJECTS):
        write(f"project-{p['slug']}.svg", panels.project_card(p, i))


TARGETS["panels"] = build_panels


HEADERS = [
    ("projects", "01", "ls /projects --sort=impact", "4 repositories", "Projects, sorted by impact"),
    ("stack", "02", "ls /tech-stack --grouped", "python · sql · bi", "Tech stack"),
    ("expertise", "03", "cat analytics-expertise.json", "6 domains", "Analytics expertise"),
    ("journey", "04", "git log --oneline /experience /education", "timeline", "Experience and education"),
    ("certs", "05", "cat certifications.sh", "9 verified", "Certifications"),
    ("stats", "06", "git stats --global", "live", "GitHub activity"),
    ("focus", "07", "cat current-focus.yaml", "in progress", "Current focus"),
    ("contact", "08", "ping me", "reply: yes", "Contact"),
]
TARGETS["chrome"] = build_chrome


if __name__ == "__main__":
    names = sys.argv[1:] or list(TARGETS)
    for n in names:
        TARGETS[n]()
