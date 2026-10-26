"""
FindIt - looks (themes)

Pick the look by changing ACTIVE below, then restart the app.
Each theme = Streamlit base colors (written to .streamlit/config.toml by the launcher)
             + extra CSS for fonts, cards, buttons and headings.
"""

import os

ACTIVE = os.environ.get("FINDIT_THEME", "sticker")   # neon, pop, varsity, arcade, sticker, sunset, comic ("plain" = no skin)

THEMES = {
    # 1) Night Neon: dark, gamer-style glow
    "neon": {
        "label": "🌙 Night Neon",
        "base": "dark",
        "primary": "#C6FF3D",
        "bg": "#100C26",
        "bg2": "#1D1744",
        "text": "#F2EEFF",
        "accent": "#FF4FD8",
        "head_font": "Space Grotesk",
        "body_font": "Nunito Sans",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Nunito+Sans:wght@400;700;800&display=swap",
        "radius": "18px",
        "card_border": "1px solid rgba(198,255,61,.35)",
        "card_shadow": "0 0 0 1px rgba(255,79,216,.15), 0 8px 28px rgba(198,255,61,.12)",
        "title_style": "background:linear-gradient(90deg,#C6FF3D,#3DF2FF 55%,#FF4FD8);"
                       "-webkit-background-clip:text;background-clip:text;color:transparent;",
        "button_text": "#100C26",
        "sidebar_bg": "linear-gradient(180deg,#1D1744,#100C26)",
    },
    # 2) Bubble Pop: bright pastel, rounded, playful
    "pop": {
        "label": "🍬 Bubble Pop",
        "base": "light",
        "primary": "#FF3D8B",
        "bg": "#FFF5FA",
        "bg2": "#F3E9FF",
        "text": "#2A1745",
        "accent": "#7B5CFF",
        "head_font": "Fredoka",
        "body_font": "Nunito Sans",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito+Sans:wght@400;700;800&display=swap",
        "radius": "24px",
        "card_border": "2px solid #2A1745",
        "card_shadow": "5px 5px 0 #7B5CFF",
        "title_style": "color:#2A1745;text-shadow:3px 3px 0 #FFC94D;",
        "button_text": "#FFFFFF",
        "sidebar_bg": "linear-gradient(180deg,#FFE3F0,#EDE3FF)",
    },
    # 3) Varsity: bold sporty, thick lines, school-jersey energy
    "varsity": {
        "label": "⚡ Varsity",
        "base": "light",
        "primary": "#FF5A1F",
        "bg": "#F4F1E8",
        "bg2": "#FFFFFF",
        "text": "#121212",
        "accent": "#1E3A8A",
        "head_font": "Archivo Black",
        "body_font": "Rubik",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Archivo+Black&family=Rubik:wght@400;500;700&display=swap",
        "radius": "6px",
        "card_border": "3px solid #121212",
        "card_shadow": "6px 6px 0 #121212",
        "title_style": "color:#121212;text-transform:uppercase;letter-spacing:.5px;"
                       "border-bottom:8px solid #FF5A1F;display:inline-block;padding-bottom:2px;",
        "button_text": "#FFFFFF",
        "sidebar_bg": "#121212",
    },
    # 4) Arcade Blast: dark game-lobby, neon glow, things pulse and pop
    "arcade": {
        "label": "🕹️ Arcade Blast",
        "base": "dark",
        "primary": "#00F5D4",
        "bg": "#120B2E",
        "bg2": "#1C1446",
        "text": "#F4F1FF",
        "accent": "#FF2E97",
        "head_font": "Bungee",
        "body_font": "Outfit",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Bungee&family=Outfit:wght@400;600;800&display=swap",
        "radius": "18px",
        "card_border": "2px solid rgba(0,245,212,.55)",
        "card_shadow": "0 0 18px rgba(0,245,212,.25), inset 0 0 22px rgba(255,46,151,.08)",
        "title_style": "background:linear-gradient(90deg,#00F5D4,#FFE66D,#FF2E97,#00F5D4);background-size:300% 100%;"
                       "-webkit-background-clip:text;background-clip:text;color:transparent;"
                       "animation:fi-slide 6s linear infinite;filter:drop-shadow(0 0 10px rgba(255,46,151,.45));",
        "button_text": "#120B2E",
        "sidebar_bg": "linear-gradient(180deg,#24105E,#120B2E)",
        "extra": """
@keyframes fi-slide { to { background-position: 300% 0; } }
@keyframes fi-pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(255,46,151,.55); } 50% { box-shadow: 0 0 22px 6px rgba(255,46,151,.35); } }
@keyframes fi-stripes { to { background-position: 40px 0; } }
[data-testid="stApp"] {
  background: radial-gradient(circle at 12% 18%, rgba(255,46,151,.28), transparent 32%),
              radial-gradient(circle at 88% 12%, rgba(0,245,212,.22), transparent 30%),
              radial-gradient(circle at 70% 90%, rgba(255,230,109,.14), transparent 35%), #120B2E;
  background-attachment: fixed;
}
[class*="st-key-card_"]:hover { transform: translateY(-6px) scale(1.02) rotate(-.6deg);
  box-shadow: 0 0 28px rgba(255,46,151,.55), 0 0 8px rgba(0,245,212,.6); border-color: #FF2E97 !important; }
button[data-testid^="stBaseButton-primary"] { animation: fi-pulse 2.2s ease-in-out infinite; text-transform: uppercase; letter-spacing: .5px; }
[data-testid="stMetricValue"] { color: #FFE66D !important; text-shadow: 0 0 12px rgba(255,230,109,.6); }
[data-testid="stProgress"] div[role="progressbar"] > div > div {
  background: repeating-linear-gradient(45deg,#00F5D4 0 12px,#FF2E97 12px 24px) !important;
  background-size: 40px 100% !important; animation: fi-stripes 1s linear infinite; }
""",
    },
    # 5) Sticker Bomb: notebook full of stickers, tilted cards, bold outlines
    "sticker": {
        "label": "🌈 Sticker Bomb",
        "base": "light",
        "primary": "#FF5DA2",
        "bg": "#FFF8E7",
        "bg2": "#FFFFFF",
        "text": "#1B1B1B",
        "accent": "#3EC1F3",
        "head_font": "Lilita One",
        "body_font": "Nunito Sans",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Lilita+One&family=Nunito+Sans:wght@400;700;800&display=swap",
        "radius": "20px",
        "card_border": "3px solid #1B1B1B",
        "card_shadow": "6px 6px 0 #1B1B1B",
        "title_style": "color:#1B1B1B;letter-spacing:1px;text-shadow:3px 3px 0 #FF5DA2,6px 6px 0 #3EC1F3;",
        "button_text": "#1B1B1B",
        "sidebar_bg": "#3EC1F3",
        "side_text": "#1B1B1B",
        "extra": """
@keyframes fi-wiggle { 0%,100% { transform: rotate(0) scale(1.04); } 25% { transform: rotate(-2deg) scale(1.04); } 75% { transform: rotate(2deg) scale(1.04); } }
[data-testid="stApp"] { background-color: #FFF8E7;
  background-image: radial-gradient(#F5C84C 1.6px, transparent 1.7px); background-size: 24px 24px; }
[data-testid="stColumn"]:nth-child(3n+1) [class*="st-key-card_"] { transform: rotate(-1.4deg); border-top: 12px solid #FF5DA2 !important; }
[data-testid="stColumn"]:nth-child(3n+2) [class*="st-key-card_"] { transform: rotate(1.1deg);  border-top: 12px solid #3EC1F3 !important; }
[data-testid="stColumn"]:nth-child(3n)   [class*="st-key-card_"] { transform: rotate(-.6deg);  border-top: 12px solid #7ED957 !important; }
[class*="st-key-card_"]:hover { animation: fi-wiggle .45s ease-in-out; transform: rotate(0) scale(1.04) !important; }
button[data-testid^="stBaseButton-primary"] { background: #FFD23F !important; border: 3px solid #1B1B1B !important;
  box-shadow: 4px 4px 0 #1B1B1B; border-radius: 14px !important; }
button[data-testid^="stBaseButton-primary"]:active { transform: translate(4px,4px); box-shadow: none; }
button[data-testid^="stBaseButton-secondary"] { border: 2px solid #1B1B1B !important; }
[data-testid="stMetric"] { box-shadow: 5px 5px 0 #FF5DA2; transform: rotate(-1deg); }
section[data-testid="stSidebar"] h1 { color: #FFD23F !important; text-shadow: 2px 2px 0 #1B1B1B, -1px -1px 0 #1B1B1B; }
""",
    },
    # 6) Sunset Wave: moving sunset gradient, frosted-glass cards, floaty
    "sunset": {
        "label": "🌅 Sunset Wave",
        "base": "light",
        "primary": "#7B2FF7",
        "bg": "#FFD3C2",
        "bg2": "rgba(255,255,255,.72)",
        "cfg_bg2": "#FFF1F6",
        "text": "#2B1B3D",
        "accent": "#FF5E9C",
        "head_font": "Baloo 2",
        "body_font": "Nunito Sans",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Nunito+Sans:wght@400;700;800&display=swap",
        "radius": "26px",
        "card_border": "1.5px solid rgba(255,255,255,.9)",
        "card_shadow": "0 12px 30px rgba(123,47,247,.18)",
        "title_style": "background:linear-gradient(90deg,#7B2FF7,#FF5E9C,#FF8A3D);-webkit-background-clip:text;"
                       "background-clip:text;color:transparent;font-weight:800;",
        "button_text": "#FFFFFF",
        "sidebar_bg": "rgba(255,255,255,.35)",
        "extra": """
@keyframes fi-sky { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes fi-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
[data-testid="stApp"] { background: linear-gradient(120deg,#FF7A2F,#FF3D8B,#A93DF5,#3D7BFF,#FF7A2F);
  background-size: 400% 400%; animation: fi-sky 18s ease infinite; }
[data-testid="stMainBlockContainer"] { background: rgba(255,255,255,.38); border-radius: 32px;
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); margin-top: 24px; }
section[data-testid="stSidebar"] { background: transparent !important; }
section[data-testid="stSidebar"] > div { backdrop-filter: blur(14px); border-right: 1px solid rgba(255,255,255,.6); }
[data-testid="stMetric"] { background: rgba(255,255,255,.8) !important; }
[class*="st-key-card_"] { backdrop-filter: blur(10px); }
[class*="st-key-card_"]:hover { animation: fi-float 1.4s ease-in-out infinite; box-shadow: 0 18px 40px rgba(255,94,156,.35); }
""",
    },
    # 7) Comic Pop: comic-book page, halftone dots, BAM! headings
    "comic": {
        "label": "💥 Comic Pop",
        "base": "light",
        "primary": "#FF3B3B",
        "bg": "#FFE14D",
        "bg2": "#FFFFFF",
        "text": "#141414",
        "accent": "#1E6BFF",
        "head_font": "Bangers",
        "body_font": "Rubik",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Bangers&family=Rubik:wght@400;500;700&display=swap",
        "radius": "6px",
        "card_border": "4px solid #141414",
        "card_shadow": "8px 8px 0 #1E6BFF",
        "title_style": "color:#FF3B3B;-webkit-text-stroke:2px #141414;text-shadow:5px 5px 0 #141414;"
                       "letter-spacing:2px;font-size:3.4rem !important;transform:rotate(-2deg);display:inline-block;",
        "button_text": "#FFFFFF",
        "sidebar_bg": "#1E6BFF",
        "side_text": "#FFFFFF",
        "extra": """
@keyframes fi-shake { 0%,100% { transform: translate(0,0) rotate(0); } 20% { transform: translate(-3px,1px) rotate(-1deg); }
  40% { transform: translate(3px,-1px) rotate(1deg); } 60% { transform: translate(-2px,0) rotate(-.5deg); } 80% { transform: translate(2px,1px); } }
[data-testid="stApp"] { background-color: #FFE14D;
  background-image: radial-gradient(rgba(20,20,20,.16) 1.3px, transparent 1.4px); background-size: 11px 11px; }
h2, h3 { letter-spacing: 1.5px; }
[class*="st-key-card_"]:hover { animation: fi-shake .4s ease-in-out; box-shadow: 10px 10px 0 #FF3B3B; }
button[data-testid^="stBaseButton-primary"] { background: #FF3B3B !important; border: 3px solid #141414 !important;
  border-radius: 8px !important; font-family: 'Bangers', sans-serif !important; letter-spacing: 1.5px; font-size: 1.15rem !important;
  box-shadow: 4px 4px 0 #141414; }
button[data-testid^="stBaseButton-primary"]:hover { transform: translateY(-3px) rotate(-1deg); }
[data-testid="stMetric"] { border-radius: 40px !important; border: 3px solid #141414 !important; box-shadow: 5px 5px 0 #141414; }
section[data-testid="stSidebar"] h1 { color: #FFE14D !important; text-shadow: 3px 3px 0 #141414; }
""",
    },
}


def theme():
    return THEMES.get(ACTIVE, THEMES["pop"])


def config_toml(name=None):
    """The [theme] section for .streamlit/config.toml."""
    t = THEMES.get(name or ACTIVE, THEMES["pop"])
    return (
        "[theme]\n"
        f'base = "{t["base"]}"\n'
        f'primaryColor = "{t["primary"]}"\n'
        f'backgroundColor = "{t["bg"]}"\n'
        f'secondaryBackgroundColor = "{t.get("cfg_bg2", t["bg2"])}"\n'
        f'textColor = "{t["text"]}"\n'
        "\n[browser]\ngatherUsageStats = false\n"
    )


def css():
    if ACTIVE not in THEMES:
        return ""            # plain Streamlit look
    t = theme()
    side_text = t.get("side_text", "#F4F1E8" if ACTIVE == "varsity" else t["text"])
    return f"""
<style>
@import url('{t["fonts_url"]}');

html, body, p, li, label, input, textarea, button,
[data-testid="stMarkdownContainer"], [data-testid="stMetricLabel"] {{
  font-family: '{t["body_font"]}', sans-serif;
}}
h1, h2, h3, [data-testid="stMetricValue"] {{
  font-family: '{t["head_font"]}', sans-serif !important;
  letter-spacing: -0.3px;
}}
[data-testid="stMain"] h1 {{ {t["title_style"]} }}

[data-testid="stHeader"] {{ background: transparent; }}

/* Sidebar */
section[data-testid="stSidebar"] > div {{ background: {t["sidebar_bg"]}; }}
section[data-testid="stSidebar"] h1 {{
  font-family: '{t["head_font"]}', sans-serif !important; color: {t["primary"]} !important;
}}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{ color: {side_text} !important; }}

/* Cards */
[class*="st-key-card_"] {{
  border: {t["card_border"]} !important;
  border-radius: {t["radius"]} !important;
  box-shadow: {t["card_shadow"]};
  background: {t["bg2"]};
  transition: transform .12s ease;
}}
[class*="st-key-card_"]:hover {{ transform: translateY(-3px); }}
[data-testid="stImage"] img {{ border-radius: calc({t["radius"]} - 8px); }}

/* Buttons */
button[data-testid^="stBaseButton-primary"] {{
  background: linear-gradient(90deg, {t["primary"]}, {t["accent"]}) !important;
  color: {t["button_text"]} !important; border: none !important;
  border-radius: 999px !important; font-weight: 800 !important;
}}
button[data-testid^="stBaseButton-secondary"] {{ border-radius: 999px !important; font-weight: 700; }}

/* Metrics as chunky stat tiles */
[data-testid="stMetric"] {{
  background: {t["bg2"]}; border-radius: {t["radius"]}; padding: 14px 18px;
  border: {t["card_border"]};
}}
[data-testid="stMetricValue"] {{ color: {t["primary"]}; }}

/* Progress bars */
[data-testid="stProgress"] div[role="progressbar"] > div > div {{
  background: linear-gradient(90deg, {t["primary"]}, {t["accent"]}) !important;
}}
{t.get("extra", "")}
</style>
"""
