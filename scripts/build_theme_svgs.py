#!/usr/bin/env python3
"""
build_theme_svgs.py
--------------------
Generates every dark/light SVG asset used by the GitHub profile README from
the templates and data defined in this file.

Why this exists (read before editing assets by hand):
  All visual assets share ONE color system so the GitHub profile stays in
  lock-step with the portfolio site's actual brand palette (same --paper,
  --ink, --rust, --copper, --sage tokens as saisantoshkumard/css/style.css).
  Editing colors, skills, projects, or timeline entries here and re-running
  this script regenerates every SVG consistently, instead of hand-editing
  16+ SVG files one at a time.

Usage:
    python3 scripts/build_theme_svgs.py

Requires: only the Python 3 standard library (no pip installs).
"""

import os
from string import Template
from xml.sax.saxutils import escape as xml_escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# ---------------------------------------------------------------------------
# Color tokens — copied 1:1 from saisantoshkumard/css/style.css so the GitHub
# profile and the portfolio site are visually the same brand, not two
# unrelated designs.
# ---------------------------------------------------------------------------
DARK = {
    "BG_DEEP": "#16140F",
    "BG_RAISED": "#1E1B16",
    "BG_DIM": "#262218",
    "TEXT_PRIMARY": "#F3EEE3",
    "TEXT_SECONDARY": "#C8C0AF",
    "TEXT_FAINT": "#938A78",
    "LINE": "#383226",
    "ACCENT_RUST": "#E4793F",
    "ACCENT_RUST_DARK": "#F4996A",
    "ACCENT_COPPER": "#D8A165",
    "ACCENT_SAGE": "#7FBE7A",
}

LIGHT = {
    "BG_DEEP": "#F7F3EA",
    "BG_RAISED": "#FFFDF8",
    "BG_DIM": "#EDE6D4",
    "TEXT_PRIMARY": "#1B1815",
    "TEXT_SECONDARY": "#524C44",
    "TEXT_FAINT": "#8A8272",
    "LINE": "#DCD0B8",
    "ACCENT_RUST": "#AE4A2A",
    "ACCENT_RUST_DARK": "#8A3A20",
    "ACCENT_COPPER": "#B5793F",
    "ACCENT_SAGE": "#4F5D40",
}

THEMES = {"dark": DARK, "light": LIGHT}

# ---------------------------------------------------------------------------
# Real content — no placeholder text anywhere below.
# ---------------------------------------------------------------------------
NAME = "Sai Santosh Kumar Devarasetty"
ROLE_LINE = "BACKEND SOFTWARE DEVELOPER · PYTHON, JAVA &amp; SAP ABAP"
TAGLINE_1 = "3+ years building REST/OData APIs, SAP S/4HANA solutions, and"
TAGLINE_2 = "cloud-native backend systems across the full Agile SDLC."
LOCATION_TEXT = "BENTONVILLE, AR · USA"

ROLES = [
    "Backend Software Developer",
    "SAP ABAP & RAP Developer",
    "Python Developer",
    "Java &amp; Spring Developer",
    "REST/OData API Developer",
    "Cloud-Native Systems Engineer",
]

SKILL_GROUPS = [
    ("Programming", ["Python", "Java", "SAP ABAP", "OO-ABAP", "SQL", "JSP/Servlets"]),
    ("Backend & Integration", ["REST APIs", "OData", "BAPI/BADI", "RFC", "IDoc", "JSON"]),
    ("Testing & Validation", ["Postman", "Unit Testing", "API Testing", "Code Reviews"]),
    ("SAP S/4HANA", ["RAP", "CDS Views", "AMDP", "ALV Reports", "Interfaces"]),
    ("Databases & OS", ["MySQL", "PostgreSQL", "Oracle", "SAP HANA", "Linux/Unix"]),
    ("Frameworks & Cloud", ["Spring Boot", "Spring Security", "Microservices", "AWS", "Kubernetes", "Docker", "Kafka", "Redis"]),
    ("Tools & Practices", ["Git", "SAP GUI", "Eclipse ADT", "Jenkins", "Azure DevOps", "Agile/Scrum"]),
]

PROJECTS = [
    {
        "title": "SAP Payment Data Retention & Separation",
        "meta": "CVS Health — CDS Views & AMDP",
        "desc": "Configurable TVARVC retention + data separation across 1B+ records.",
        "tags": ["CDS Views", "AMDP", "TVARVC"],
        "stat": "1B+ records",
    },
    {
        "title": "Microservices Platform Modernization",
        "meta": "Cloudninetek — Spring Boot & K8s",
        "desc": "Spring Cloud Netflix microservices with Kafka, Redis, and Kubernetes.",
        "tags": ["Spring Boot", "Kafka", "Kubernetes"],
        "stat": "High availability",
    },
    {
        "title": "Automated Test & CI/CD Pipeline",
        "meta": "Cloudninetek — Selenium & Azure DevOps",
        "desc": "Selenium/Maven/TestNG framework wired into Jenkins and Azure DevOps.",
        "tags": ["Selenium", "Jenkins", "Azure DevOps"],
        "stat": "Faster releases",
    },
]

TIMELINE = [
    ("2021", "B.Sc. Computer Science, Mathematics & Statistics", "Acharya Nagarjuna University"),
    ("2021", "Programmer Trainee", "Cognizant Technology Solutions — Oct 2021 to Jul 2022"),
    ("2023", "M.S. Computer & Information Science completed", "University of Southern Mississippi — Dec 2023"),
    ("2024", "Software Developer", "Cloudninetek LLC — Feb 2024 to Jan 2025"),
    ("2025", "SAP ABAP Developer, Contract", "CVS Health — Jan 2025 to Jan 2026"),
    ("2026", "Python Developer", "Tech Pro — Feb 2026 to present"),
]

CONTACTS = [
    ("GitHub", "github.com/dsaisantoshkumar", "https://github.com/dsaisantoshkumar"),
    ("LinkedIn", "linkedin.com/in/santosh29", "https://linkedin.com/in/santosh29"),
    ("Portfolio", "dsaisantoshkumar.github.io", "https://dsaisantoshkumar.github.io/saisantoshkumard/"),
    ("Email", "dsaisantoshkumar@gmail.com", "mailto:dsaisantoshkumar@gmail.com"),
]

TERMINAL_LINES = [
    "$ whoami",
    "sai_santosh_kumar_devarasetty",
    "$ cat focus.txt",
    "Backend systems in Python/Java + SAP ABAP, shipped and supported in prod.",
    "$ python run_tests.py --suite api",
    "[INFO] Postman + unit/API tests — all endpoints validated ✓",
]


def apply(template: str, tokens: dict) -> str:
    return Template(template).safe_substitute(tokens)


def _estimate_text_width(text: str) -> float:
    """Rough glyph-width estimate at ~13.5px Segoe UI: uppercase/digits render
    noticeably wider than lowercase, which plain len() ignores — SAP-heavy
    strings (SQL, CDS, AMDP, ST05) were overflowing project cards until this
    weighting was added."""
    width = 0.0
    for ch in text:
        if ch == " ":
            width += 3.6
        elif ch.isupper() or ch.isdigit():
            width += 7.6
        else:
            width += 4.3
    return width


def _fit_attr(text: str, avail_px: float) -> str:
    """Returns an SVG textLength/lengthAdjust attribute string that compresses
    text to fit avail_px, but only when the estimated width would overflow —
    short text is left at its natural width rather than stretched."""
    est = _estimate_text_width(text)
    if est > avail_px:
        return f' textLength="{avail_px:.0f}" lengthAdjust="spacingAndGlyphs"'
    return ""


def write(theme: str, filename: str, svg: str) -> None:
    out_dir = os.path.join(ASSETS, theme)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg.strip() + "\n")
    print(f"wrote {os.path.relpath(path, ROOT)}")


# ---------------------------------------------------------------------------
# 1. divider.svg
# ---------------------------------------------------------------------------
DIVIDER_TMPL = """
<svg width="100%" viewBox="0 0 900 28" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="section divider">
  <defs>
    <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="$LINE" stop-opacity="0"/>
      <stop offset="50%" stop-color="$ACCENT_COPPER" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="$LINE" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="$ACCENT_RUST" stop-opacity="0"/>
      <stop offset="50%" stop-color="$ACCENT_RUST" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="$ACCENT_RUST" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="13" width="900" height="2" fill="url(#lineGrad)"/>
  <rect x="-220" y="13" width="220" height="2" fill="url(#shine)">
    <animate attributeName="x" values="-220;900" dur="3.6s" repeatCount="indefinite"/>
  </rect>
  <circle cx="450" cy="14" r="3" fill="$ACCENT_RUST">
    <animate attributeName="r" values="2;3.6;2" dur="2.2s" repeatCount="indefinite"/>
  </circle>
</svg>
"""

# ---------------------------------------------------------------------------
# 2. hero.svg
# ---------------------------------------------------------------------------
HERO_TMPL = """
<svg width="100%" viewBox="0 0 1200 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="$NAME — hero banner">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="$BG_DEEP"/>
      <stop offset="100%" stop-color="$BG_DIM"/>
    </linearGradient>
    <radialGradient id="glowA" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="$ACCENT_RUST" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="$ACCENT_RUST" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="$ACCENT_COPPER" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="$ACCENT_COPPER" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="$ACCENT_RUST_DARK">
        <animate attributeName="offset" values="0;0.15;0" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="$ACCENT_COPPER"/>
    </linearGradient>
    <filter id="softBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect width="1200" height="380" fill="url(#bgGrad)"/>

  <circle cx="1010" cy="80" r="190" fill="url(#glowA)" filter="url(#softBlur)">
    <animate attributeName="cy" values="80;55;80" dur="8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="170" cy="330" r="150" fill="url(#glowB)" filter="url(#softBlur)">
    <animate attributeName="cy" values="330;305;330" dur="10s" repeatCount="indefinite"/>
  </circle>

  <g fill="$ACCENT_COPPER" opacity="0.75">
    <circle cx="120" cy="55" r="2.2"><animate attributeName="cy" values="55;35;55" dur="5s" repeatCount="indefinite"/></circle>
    <circle cx="980" cy="235" r="1.8"><animate attributeName="cy" values="235;215;235" dur="6s" repeatCount="indefinite"/></circle>
    <circle cx="1120" cy="330" r="2.4"><animate attributeName="cy" values="330;310;330" dur="7s" repeatCount="indefinite"/></circle>
    <circle cx="55" cy="215" r="1.6"><animate attributeName="cy" values="215;195;215" dur="6.5s" repeatCount="indefinite"/></circle>
    <circle cx="700" cy="35" r="2"><animate attributeName="cy" values="35;18;35" dur="5.6s" repeatCount="indefinite"/></circle>
    <circle cx="500" cy="360" r="1.6"><animate attributeName="cy" values="360;345;360" dur="5.2s" repeatCount="indefinite"/></circle>
  </g>

  <rect x="40" y="36" width="1120" height="308" rx="26" fill="$BG_RAISED" fill-opacity="0.55" stroke="$LINE" stroke-width="1.2"/>
  <rect x="40" y="36" width="1120" height="308" rx="26" fill="none" stroke="$ACCENT_RUST" stroke-opacity="0.4" stroke-width="1.1">
    <animate attributeName="stroke-opacity" values="0.15;0.55;0.15" dur="4.5s" repeatCount="indefinite"/>
  </rect>

  <text x="82" y="148" font-family="Georgia, 'Times New Roman', serif" font-size="48" font-weight="600" fill="url(#nameGrad)">$NAME</text>
  <text x="84" y="186" font-family="'Segoe UI', Arial, sans-serif" font-size="17" letter-spacing="2.4" font-weight="700" fill="$ACCENT_RUST">$ROLE_LINE</text>

  <text x="84" y="230" font-family="'Segoe UI', Arial, sans-serif" font-size="16" fill="$TEXT_SECONDARY">$TAGLINE_1</text>
  <text x="84" y="253" font-family="'Segoe UI', Arial, sans-serif" font-size="16" fill="$TEXT_SECONDARY">$TAGLINE_2</text>

  <g transform="translate(84 272)">
    <rect width="214" height="28" rx="14" fill="$BG_DIM" stroke="$LINE"/>
    <circle cx="18" cy="14" r="4" fill="$ACCENT_RUST"/>
    <text x="32" y="18" font-family="'Segoe UI', Arial, sans-serif" font-size="11.5" font-weight="700" fill="$TEXT_SECONDARY">$LOCATION_TEXT</text>
  </g>

  <g font-family="'Segoe UI', Arial, sans-serif">
    <g transform="translate(84 336)">
      <text font-size="21" font-weight="800" fill="$ACCENT_RUST">1B+</text>
      <text y="18" font-size="10" font-weight="700" letter-spacing="1" fill="$TEXT_FAINT">RECORDS PROCESSED</text>
    </g>
    <g transform="translate(300 336)">
      <text font-size="21" font-weight="800" fill="$ACCENT_RUST">3+</text>
      <text y="18" font-size="10" font-weight="700" letter-spacing="1" fill="$TEXT_FAINT">YEARS EXPERIENCE</text>
    </g>
    <g transform="translate(478 336)">
      <text font-size="21" font-weight="800" fill="$ACCENT_RUST">3</text>
      <text y="18" font-size="10" font-weight="700" letter-spacing="1" fill="$TEXT_FAINT">FEATURED PROJECTS</text>
    </g>
    <g transform="translate(680 336)">
      <text font-size="21" font-weight="800" fill="$ACCENT_RUST">5</text>
      <text y="18" font-size="10" font-weight="700" letter-spacing="1" fill="$TEXT_FAINT">CERTIFICATIONS</text>
    </g>
  </g>
</svg>
"""

# ---------------------------------------------------------------------------
# 3. terminal.svg (animated ascii/terminal art)
# ---------------------------------------------------------------------------

def build_terminal(tokens: dict) -> str:
    tmpl = """
<svg width="100%" viewBox="0 0 900 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="terminal animation">
  <defs>
    <linearGradient id="termBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="$BG_RAISED"/>
      <stop offset="100%" stop-color="$BG_DEEP"/>
    </linearGradient>
    <clipPath id="termClip"><rect x="0" y="0" width="900" height="260" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#termClip)">
    <rect width="900" height="260" fill="url(#termBg)"/>

    <!-- scanlines -->
    <g opacity="0.05">
      __SCANLINES__
    </g>

    <!-- title bar -->
    <rect width="900" height="34" fill="$BG_DIM"/>
    <circle cx="22" cy="17" r="6" fill="$ACCENT_RUST"/>
    <circle cx="44" cy="17" r="6" fill="$ACCENT_COPPER"/>
    <circle cx="66" cy="17" r="6" fill="$ACCENT_SAGE"/>
    <text x="450" y="21" text-anchor="middle" font-family="'Cascadia Code','Consolas',monospace" font-size="12" fill="$TEXT_FAINT">sai@devbox: ~/portfolio</text>

    <g font-family="'Cascadia Code','Consolas',monospace" font-size="15">
      __LINES__
    </g>

    <!-- glow sweep -->
    <rect x="-300" y="34" width="300" height="226" fill="$ACCENT_RUST" opacity="0.05">
      <animate attributeName="x" values="-300;900" dur="5s" repeatCount="indefinite"/>
    </rect>
  </g>

  <rect x="0.75" y="0.75" width="898.5" height="258.5" rx="16" fill="none" stroke="$LINE" stroke-width="1.2"/>
</svg>
"""
    scanlines = "\n      ".join(
        f'<rect x="0" y="{y}" width="900" height="1" fill="{tokens["TEXT_PRIMARY"]}"/>' for y in range(0, 260, 4)
    )

    lines_svg = []
    y = 66
    for i, line in enumerate(TERMINAL_LINES):
        is_prompt = line.startswith("$")
        color = tokens["ACCENT_SAGE"] if is_prompt else tokens["TEXT_SECONDARY"]
        weight = "700" if is_prompt else "400"
        lines_svg.append(
            f'<text x="24" y="{y}" fill="{color}" font-weight="{weight}" opacity="0">{xml_escape(line)}'
            f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{i/6:.4f};{(i+0.15)/6:.4f};1" '
            f'dur="9s" begin="0s" repeatCount="indefinite"/></text>'
        )
        y += 28

    # blinking cursor sits after the final line, blinks continuously
    cursor = (
        f'<rect x="24" y="{y - 14}" width="9" height="16" fill="{tokens["ACCENT_RUST"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/>'
        f"</rect>"
    )
    lines_svg.append(cursor)

    svg = tmpl.replace("__SCANLINES__", scanlines).replace("__LINES__", "\n      ".join(lines_svg))
    return apply(svg, tokens)


# ---------------------------------------------------------------------------
# 4. typing.svg (pure SMIL typing/deleting loop — no external service)
# ---------------------------------------------------------------------------

def build_typing(tokens: dict) -> str:
    n = len(ROLES)
    seg = 1.0 / n
    type_frac, hold_frac, delete_frac = 0.18, 0.62, 0.20
    total_dur = 16  # seconds for the full cycle

    char_w = 11.5  # approximate monospace advance width at font-size 26
    x0 = 24

    phrase_texts = []
    cursor_keytimes = ["0"]
    cursor_values = [str(x0)]

    for i, role in enumerate(ROLES):
        w_full = len(role.replace("&amp;", "&")) * char_w
        seg_start = i * seg
        t_type_end = seg_start + seg * type_frac
        t_hold_end = t_type_end + seg * hold_frac
        seg_end = (i + 1) * seg

        key_times = [seg_start, t_type_end, t_hold_end, seg_end]
        widths = [0, w_full, w_full, 0]

        # clamp keyTimes to 4 significant decimals and ensure monotonic increase
        kt_str = ";".join(f"{max(0, min(1, k)):.4f}" for k in key_times)
        w_str = ";".join(f"{w:.1f}" for w in widths)

        clip_id = f"clipT{i}"
        phrase_texts.append(f"""
    <clipPath id="{clip_id}">
      <rect x="{x0}" y="0" height="40" width="0">
        <animate attributeName="width" values="{w_str}" keyTimes="{kt_str}" dur="{total_dur}s" begin="0s" repeatCount="indefinite"/>
      </rect>
    </clipPath>""")
        phrase_texts.append(
            f'<text x="{x0}" y="27" clip-path="url(#{clip_id})" '
            f'font-family="\'Cascadia Code\',\'Consolas\',monospace" font-size="26" font-weight="600" '
            f'fill="$ACCENT_RUST">{xml_escape(role)}</text>'
        )

        # cursor keyframes: stays at x0 until typing starts, moves to x0+w_full during typing,
        # holds, moves back to x0 during delete
        cursor_keytimes += [f"{t_type_end:.4f}", f"{t_hold_end:.4f}", f"{seg_end:.4f}"]
        cursor_values += [f"{x0 + w_full:.1f}", f"{x0 + w_full:.1f}", f"{x0:.1f}"]

    cursor_kt = ";".join(cursor_keytimes)
    cursor_vals = ";".join(cursor_values)

    tmpl = """
<svg width="100%" viewBox="0 0 640 44" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="rotating role titles">
  <defs>
__PHRASES__
  </defs>

  <rect width="640" height="44" fill="$BG_DEEP" opacity="0"/>
__TEXTS__

  <rect y="6" width="3" height="30" fill="$ACCENT_COPPER">
    <animate attributeName="x" values="__CURSOR_VALS__" keyTimes="__CURSOR_KT__" dur="__TOTAL__s" begin="0s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/>
  </rect>
</svg>
"""
    clip_defs = "\n".join(t for t in phrase_texts if t.strip().startswith("<clipPath"))
    text_els = "\n".join(t for t in phrase_texts if t.strip().startswith("<text"))

    svg = (
        tmpl.replace("__PHRASES__", clip_defs)
        .replace("__TEXTS__", text_els)
        .replace("__CURSOR_VALS__", cursor_vals)
        .replace("__CURSOR_KT__", cursor_kt)
        .replace("__TOTAL__", str(total_dur))
    )
    return apply(svg, tokens)


# ---------------------------------------------------------------------------
# 5. skills.svg
# ---------------------------------------------------------------------------

ICONS = {
    "code": '<path d="M8 9 4 12l4 3M16 9l4 3-4 3M13.5 6.5l-3 11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5-9-5Z M3 13l9 5 9-5 M3 18l9 5 9-5" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" fill="none"/>',
    "building": '<path d="M4 20V9l8-5 8 5v11M4 20h16M9 20v-6h6v6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "trend": '<path d="M4 20 9 12l4 4 7-10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="9" cy="12" r="1.3" fill="currentColor"/><circle cx="13" cy="16" r="1.3" fill="currentColor"/><circle cx="20" cy="6" r="1.3" fill="currentColor"/>',
    "database": '<ellipse cx="12" cy="6" rx="8" ry="3" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" stroke="currentColor" stroke-width="1.6" fill="none"/>',
    "check": '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M8 12.5 10.5 15 16 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 1 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2 2.6-2.6Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/>',
}

GROUP_ICON = ["code", "layers", "building", "trend", "database", "check", "tool"]


def build_skills(tokens: dict) -> str:
    cols = 2
    card_w, card_h, gap = 470, 128, 20
    x_pad, y_pad = 20, 20

    cards = []
    for i, (title, tags) in enumerate(SKILL_GROUPS):
        col = i % cols
        row = i // cols
        x = x_pad + col * (card_w + gap)
        y = y_pad + row * (card_h + gap)
        icon = ICONS[GROUP_ICON[i % len(GROUP_ICON)]]

        tag_els = []
        tx, ty = 18, 66
        for tag in tags:
            tw = len(tag) * 6.6 + 22
            if tx + tw > card_w - 18:
                tx = 18
                ty += 30
            tag_els.append(
                f'<g transform="translate({tx} {ty})">'
                f'<rect width="{tw:.0f}" height="24" rx="12" fill="$BG_DIM" stroke="$LINE"/>'
                f'<text x="{tw/2:.0f}" y="16" text-anchor="middle" font-family="\'Segoe UI\',Arial,sans-serif" '
                f'font-size="11.5" font-weight="600" fill="$TEXT_SECONDARY">{xml_escape(tag)}</text></g>'
            )
            tx += tw + 8

        card = f"""
  <g transform="translate({x} {y})">
    <rect width="{card_w}" height="{card_h}" rx="16" fill="$BG_RAISED" stroke="$LINE" stroke-width="1.2"/>
    <rect width="{card_w}" height="{card_h}" rx="16" fill="none" stroke="$ACCENT_RUST" stroke-opacity="0">
      <animate attributeName="stroke-opacity" values="0;0.5;0" dur="4s" begin="{i * 0.5}s" repeatCount="indefinite"/>
    </rect>
    <g transform="translate(18 18)" color="$ACCENT_RUST" width="20" height="20" viewBox="0 0 24 24">
      <svg x="0" y="0" width="20" height="20" viewBox="0 0 24 24">{icon}</svg>
    </g>
    <text x="46" y="33" font-family="'Segoe UI',Arial,sans-serif" font-size="13.5" font-weight="700"
          letter-spacing="0.4" fill="$TEXT_FAINT">{xml_escape(title.upper())}</text>
    {''.join(tag_els)}
  </g>"""
        cards.append(card)

    rows = (len(SKILL_GROUPS) + cols - 1) // cols
    total_h = y_pad * 2 + rows * card_h + (rows - 1) * gap
    total_w = x_pad * 2 + cols * card_w + (cols - 1) * gap

    tmpl = f"""
<svg width="100%" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="technical skills">
  <rect width="{total_w}" height="{total_h}" fill="$BG_DEEP"/>
  {''.join(cards)}
</svg>
"""
    return apply(tmpl, tokens)


# ---------------------------------------------------------------------------
# 6. projects.svg
# ---------------------------------------------------------------------------

def build_projects(tokens: dict) -> str:
    cols = 2
    card_w, card_h, gap, pad = 560, 190, 24, 24
    cards = []
    for i, p in enumerate(PROJECTS):
        col = i % cols
        row = i // cols
        x = pad + col * (card_w + gap)
        y = pad + row * (card_h + gap)

        tag_els = []
        tx = 24
        for tag in p["tags"]:
            tw = len(tag) * 6.4 + 20
            tag_els.append(
                f'<g transform="translate({tx} 148)">'
                f'<rect width="{tw:.0f}" height="22" rx="11" fill="$BG_DIM" stroke="$LINE"/>'
                f'<text x="{tw/2:.0f}" y="15" text-anchor="middle" font-family="\'Segoe UI\',Arial,sans-serif" '
                f'font-size="10.5" font-weight="600" fill="$TEXT_SECONDARY">{xml_escape(tag)}</text></g>'
            )
            tx += tw + 8

        cards.append(f"""
  <g transform="translate({x} {y})">
    <rect width="{card_w}" height="{card_h}" rx="18" fill="$BG_RAISED" stroke="$LINE" stroke-width="1.2"/>
    <rect width="{card_w}" height="{card_h}" rx="18" fill="none" stroke="$ACCENT_RUST" stroke-width="1.4" stroke-opacity="0.15">
      <animate attributeName="stroke-opacity" values="0.1;0.5;0.1" dur="4.5s" begin="{i * 0.6}s" repeatCount="indefinite"/>
    </rect>
    <rect x="24" y="22" width="5" height="26" rx="2.5" fill="$ACCENT_RUST"/>
    <text x="40" y="42" font-family="Georgia, serif" font-size="19" font-weight="600" fill="$TEXT_PRIMARY">{xml_escape(p['title'])}</text>
    <text x="40" y="64" font-family="'Segoe UI',Arial,sans-serif" font-size="11.5" font-weight="700"
          letter-spacing="0.5" fill="$ACCENT_COPPER">{xml_escape(p['meta'].upper())}</text>
    <text x="24" y="96" font-family="'Segoe UI',Arial,sans-serif" font-size="13.5" fill="$TEXT_SECONDARY"{_fit_attr(p['desc'], card_w - 48)}>{xml_escape(p['desc'])}</text>
    {''.join(tag_els)}
    <text x="{card_w - 24}" y="163" text-anchor="end" font-family="'Segoe UI',Arial,sans-serif"
          font-size="12" font-weight="700" fill="$ACCENT_SAGE">{xml_escape(p['stat'])}</text>
  </g>""")

    rows = (len(PROJECTS) + cols - 1) // cols
    total_h = pad * 2 + rows * card_h + (rows - 1) * gap
    total_w = pad * 2 + cols * card_w + (cols - 1) * gap

    tmpl = f"""
<svg width="100%" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="featured projects">
  <rect width="{total_w}" height="{total_h}" fill="$BG_DEEP"/>
  {''.join(cards)}
</svg>
"""
    return apply(tmpl, tokens)


# ---------------------------------------------------------------------------
# 7. timeline.svg
# ---------------------------------------------------------------------------

def build_timeline(tokens: dict) -> str:
    n = len(TIMELINE)
    row_h = 78
    pad_top = 30
    total_h = pad_top * 2 + row_h * (n - 1) + 20
    total_w = 780
    line_x = 100

    nodes = []
    for i, (year, title, meta) in enumerate(TIMELINE):
        cy = pad_top + i * row_h
        nodes.append(f"""
  <g>
    <text x="{line_x - 24}" y="{cy + 5}" text-anchor="end" font-family="'Segoe UI',Arial,sans-serif"
          font-size="14" font-weight="800" fill="$ACCENT_RUST">{xml_escape(year)}</text>
    <circle cx="{line_x}" cy="{cy}" r="7" fill="$BG_DEEP" stroke="$ACCENT_RUST" stroke-width="2.4"/>
    <circle cx="{line_x}" cy="{cy}" r="7" fill="$ACCENT_RUST" opacity="0">
      <animate attributeName="opacity" values="0;0.55;0" dur="2.6s" begin="{i * 0.4}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="7;13;7" dur="2.6s" begin="{i * 0.4}s" repeatCount="indefinite"/>
    </circle>
    <text x="{line_x + 28}" y="{cy - 3}" font-family="'Segoe UI',Arial,sans-serif" font-size="15"
          font-weight="700" fill="$TEXT_PRIMARY">{xml_escape(title)}</text>
    <text x="{line_x + 28}" y="{cy + 18}" font-family="'Segoe UI',Arial,sans-serif" font-size="12.5"
          fill="$TEXT_FAINT">{xml_escape(meta)}</text>
  </g>""")

    tmpl = f"""
<svg width="100%" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="career and education timeline">
  <rect width="{total_w}" height="{total_h}" fill="$BG_DEEP"/>
  <line x1="{line_x}" y1="{pad_top}" x2="{line_x}" y2="{pad_top + row_h * (n - 1)}" stroke="$LINE" stroke-width="2"/>
  <line x1="{line_x}" y1="{pad_top}" x2="{line_x}" y2="{pad_top + row_h * (n - 1)}" stroke="$ACCENT_COPPER" stroke-width="2" stroke-dasharray="6 420" >
    <animate attributeName="stroke-dashoffset" values="6;-420" dur="6s" repeatCount="indefinite"/>
  </line>
  {''.join(nodes)}
</svg>
"""
    return apply(tmpl, tokens)


# ---------------------------------------------------------------------------
# 8. contact.svg
# ---------------------------------------------------------------------------

def build_contact(tokens: dict) -> str:
    card_w, card_h, gap, pad = 270, 84, 20, 20
    cols = 2
    cards = []
    for i, (label, display, _url) in enumerate(CONTACTS):
        col = i % cols
        row = i // cols
        x = pad + col * (card_w + gap)
        y = pad + row * (card_h + gap)
        cards.append(f"""
  <g transform="translate({x} {y})">
    <rect width="{card_w}" height="{card_h}" rx="16" fill="$BG_RAISED" stroke="$LINE" stroke-width="1.2"/>
    <rect width="{card_w}" height="{card_h}" rx="16" fill="none" stroke="$ACCENT_RUST" stroke-opacity="0">
      <animate attributeName="stroke-opacity" values="0;0.5;0" dur="3.6s" begin="{i * 0.5}s" repeatCount="indefinite"/>
    </rect>
    <circle cx="34" cy="{card_h/2:.0f}" r="17" fill="$BG_DIM" stroke="$LINE"/>
    <circle cx="34" cy="{card_h/2:.0f}" r="3.4" fill="$ACCENT_RUST"/>
    <text x="62" y="{card_h/2 - 6:.0f}" font-family="'Segoe UI',Arial,sans-serif" font-size="12.5"
          font-weight="700" letter-spacing="0.4" fill="$ACCENT_COPPER">{xml_escape(label.upper())}</text>
    <text x="62" y="{card_h/2 + 14:.0f}" font-family="'Segoe UI',Arial,sans-serif" font-size="13"
          fill="$TEXT_SECONDARY">{xml_escape(display)}</text>
  </g>""")

    rows = (len(CONTACTS) + cols - 1) // cols
    total_h = pad * 2 + rows * card_h + (rows - 1) * gap
    total_w = pad * 2 + cols * card_w + (cols - 1) * gap
    tmpl = f"""
<svg width="100%" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="contact links">
  <rect width="{total_w}" height="{total_h}" fill="$BG_DEEP"/>
  {''.join(cards)}
</svg>
"""
    return apply(tmpl, tokens)


# ---------------------------------------------------------------------------
# 9. footer.svg
# ---------------------------------------------------------------------------
FOOTER_TMPL = """
<svg width="100%" viewBox="0 0 1200 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="footer">
  <defs>
    <linearGradient id="footBg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="$BG_DEEP"/>
      <stop offset="50%" stop-color="$BG_DIM"/>
      <stop offset="100%" stop-color="$BG_DEEP"/>
    </linearGradient>
    <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="$ACCENT_RUST" stop-opacity="0"/>
      <stop offset="50%" stop-color="$ACCENT_RUST" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="$ACCENT_RUST" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="160" fill="url(#footBg)"/>

  <path d="M0 40 Q 300 10 600 40 T 1200 40" fill="none" stroke="url(#wave)" stroke-width="2">
    <animate attributeName="d"
      values="M0 40 Q 300 10 600 40 T 1200 40;M0 40 Q 300 65 600 40 T 1200 40;M0 40 Q 300 10 600 40 T 1200 40"
      dur="6s" repeatCount="indefinite"/>
  </path>

  <g fill="$ACCENT_COPPER" opacity="0.8">
    <circle cx="80" cy="30" r="1.6"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.4s" repeatCount="indefinite"/></circle>
    <circle cx="200" cy="70" r="2"><animate attributeName="opacity" values="0.2;1;0.2" dur="3.1s" repeatCount="indefinite"/></circle>
    <circle cx="360" cy="24" r="1.4"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.8s" repeatCount="indefinite"/></circle>
    <circle cx="520" cy="60" r="1.8"><animate attributeName="opacity" values="0.2;1;0.2" dur="3.4s" repeatCount="indefinite"/></circle>
    <circle cx="700" cy="20" r="1.5"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.6s" repeatCount="indefinite"/></circle>
    <circle cx="880" cy="65" r="2"><animate attributeName="opacity" values="0.2;1;0.2" dur="3.6s" repeatCount="indefinite"/></circle>
    <circle cx="1020" cy="28" r="1.6"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.9s" repeatCount="indefinite"/></circle>
    <circle cx="1140" cy="55" r="1.4"><animate attributeName="opacity" values="0.2;1;0.2" dur="3.2s" repeatCount="indefinite"/></circle>
  </g>

  <!-- shooting particle -->
  <circle r="2.4" fill="$ACCENT_RUST">
    <animateMotion path="M-20 100 L 1220 40" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite"/>
  </circle>

  <text x="600" y="112" text-anchor="middle" font-family="Georgia, serif" font-size="20" font-weight="600" fill="$TEXT_PRIMARY">Thanks for stopping by — let&#8217;s build something reliable.</text>
  <g font-family="'Cascadia Code','Consolas',monospace" font-size="14">
    <text x="600" y="138" text-anchor="middle" fill="$ACCENT_RUST">$ echo &quot;always open to interesting problems&quot;<tspan fill="$ACCENT_COPPER">_</tspan></text>
  </g>
</svg>
"""


def main():
    for theme, tokens in THEMES.items():
        hero_tokens = {**tokens, "NAME": NAME, "ROLE_LINE": ROLE_LINE, "TAGLINE_1": TAGLINE_1, "TAGLINE_2": TAGLINE_2, "LOCATION_TEXT": LOCATION_TEXT}
        write(theme, "divider.svg", apply(DIVIDER_TMPL, tokens))
        write(theme, "hero.svg", apply(HERO_TMPL, hero_tokens))
        write(theme, "terminal.svg", build_terminal(tokens))
        write(theme, "typing.svg", build_typing(tokens))
        write(theme, "skills.svg", build_skills(tokens))
        write(theme, "projects.svg", build_projects(tokens))
        write(theme, "timeline.svg", build_timeline(tokens))
        write(theme, "contact.svg", build_contact(tokens))
        write(theme, "footer.svg", apply(FOOTER_TMPL, tokens))
    print("\nAll SVG assets generated for dark + light themes.")


if __name__ == "__main__":
    main()
