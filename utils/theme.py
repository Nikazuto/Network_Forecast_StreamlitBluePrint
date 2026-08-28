"""
Central design tokens + injected CSS for the "AI-Based Network Attack
Forecasting" SOC-style demonstrator.

Everything here is presentation only. No model logic lives in this file.
"""

import streamlit as st

# ----------------------------------------------------------------------
# COLOR TOKENS
# ----------------------------------------------------------------------
BG_PRIMARY = "#0a0e17"
BG_SECONDARY = "#0f1523"
BG_CARD = "#131a2b"
BG_CARD_HOVER = "#161e33"
BORDER = "#232d45"
BORDER_SOFT = "#1a2338"

TEXT_PRIMARY = "#e6ebf5"
TEXT_SECONDARY = "#8b96b3"
TEXT_MUTED = "#5b657f"

ACCENT_CYAN = "#3fd0e0"
ACCENT_BLUE = "#4f8cff"
ACCENT_PURPLE = "#8b7fff"

RISK_SAFE = "#2ecf8e"
RISK_LOW = "#5ec9e8"
RISK_ELEVATED = "#f2c94c"
RISK_HIGH = "#f2994a"
RISK_CRITICAL = "#eb5757"

STATUS_REAL = "#2ecf8e"
STATUS_DEMO = "#f2c94c"
STATUS_PLANNED = "#5b657f"
STATUS_FOUNDATION = "#4f8cff"

FONT_MONO = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"
FONT_SANS = "'Inter', 'Segoe UI', sans-serif"


def risk_color(level: str) -> str:
    return {
        "SAFE": RISK_SAFE,
        "LOW": RISK_LOW,
        "ELEVATED": RISK_ELEVATED,
        "HIGH": RISK_HIGH,
        "CRITICAL": RISK_CRITICAL,
    }.get(level.upper(), RISK_LOW)


def risk_level_from_probability(p: float) -> str:
    if p < 0.30:
        return "LOW"
    if p < 0.60:
        return "ELEVATED"
    if p < 0.80:
        return "HIGH"
    return "CRITICAL"


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_SANS};
        }}

        .stApp {{
            background: radial-gradient(circle at 15% 0%, #0d1524 0%, {BG_PRIMARY} 45%) fixed;
            color: {TEXT_PRIMARY};
        }}

        section[data-testid="stSidebar"] {{
            background: {BG_SECONDARY};
            border-right: 1px solid {BORDER_SOFT};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT_PRIMARY};
        }}

        h1, h2, h3, h4 {{
            font-family: {FONT_SANS};
            letter-spacing: -0.01em;
        }}

        p, li, span, div {{
            color: {TEXT_PRIMARY};
        }}

        hr {{
            border-color: {BORDER_SOFT};
        }}

        code, .mono {{
            font-family: {FONT_MONO} !important;
        }}

        /* ---- generic glass card ---- */
        .glass-card {{
            background: linear-gradient(180deg, {BG_CARD} 0%, {BG_SECONDARY} 100%);
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 20px 22px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.25);
            margin-bottom: 14px;
        }}

        .glass-card:hover {{
            border-color: {ACCENT_CYAN}55;
        }}

        /* ---- badges ---- */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: {FONT_MONO};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.06em;
            padding: 3px 10px;
            border-radius: 999px;
            border: 1px solid;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .badge-demo {{ color: {STATUS_DEMO}; border-color: {STATUS_DEMO}66; background: {STATUS_DEMO}14; }}
        .badge-real {{ color: {STATUS_REAL}; border-color: {STATUS_REAL}66; background: {STATUS_REAL}14; }}
        .badge-planned {{ color: {STATUS_PLANNED}; border-color: {STATUS_PLANNED}88; background: {STATUS_PLANNED}14; }}
        .badge-foundation {{ color: {STATUS_FOUNDATION}; border-color: {STATUS_FOUNDATION}66; background: {STATUS_FOUNDATION}14; }}
        .badge-heuristic {{ color: {ACCENT_PURPLE}; border-color: {ACCENT_PURPLE}66; background: {ACCENT_PURPLE}14; }}
        .badge-critical {{ color: {RISK_CRITICAL}; border-color: {RISK_CRITICAL}88; background: {RISK_CRITICAL}1a; }}
        .badge-high {{ color: {RISK_HIGH}; border-color: {RISK_HIGH}88; background: {RISK_HIGH}1a; }}
        .badge-elevated {{ color: {RISK_ELEVATED}; border-color: {RISK_ELEVATED}88; background: {RISK_ELEVATED}1a; }}
        .badge-safe {{ color: {RISK_SAFE}; border-color: {RISK_SAFE}88; background: {RISK_SAFE}1a; }}

        /* ---- system banner ---- */
        .system-banner {{
            border: 1px solid {STATUS_DEMO}55;
            background: linear-gradient(90deg, {STATUS_DEMO}12, transparent);
            border-left: 4px solid {STATUS_DEMO};
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 18px;
        }}

        /* ---- metric card ---- */
        .metric-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 16px 18px;
            min-height: 118px;
        }}
        .metric-label {{
            font-size: 12px;
            color: {TEXT_SECONDARY};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-family: {FONT_MONO};
            font-size: 26px;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            line-height: 1.1;
        }}

        /* ---- pipeline stage chip ---- */
        .pipeline-stage {{
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 10px 14px;
            text-align: center;
            font-family: {FONT_MONO};
            font-size: 13px;
            background: {BG_CARD};
            color: {TEXT_SECONDARY};
        }}
        .pipeline-stage.active {{
            border-color: {ACCENT_CYAN};
            color: {ACCENT_CYAN};
            background: {ACCENT_CYAN}12;
        }}
        .pipeline-stage.done {{
            border-color: {RISK_SAFE};
            color: {RISK_SAFE};
            background: {RISK_SAFE}10;
        }}

        /* ---- architecture node ---- */
        .arch-node {{
            border: 1px solid {BORDER};
            background: {BG_CARD};
            border-radius: 10px;
            padding: 12px 14px;
            font-family: {FONT_MONO};
            font-size: 12.5px;
            margin-bottom: 8px;
        }}
        .arch-node b {{ color: {ACCENT_CYAN}; }}

        .layer-label {{
            font-family: {FONT_MONO};
            font-size: 11px;
            letter-spacing: 0.12em;
            color: {TEXT_MUTED};
            text-transform: uppercase;
            margin: 6px 0 4px 2px;
        }}

        /* ---- section divider text ---- */
        .section-kicker {{
            font-family: {FONT_MONO};
            font-size: 12px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: {ACCENT_CYAN};
            font-weight: 700;
            margin-bottom: 2px;
        }}

        .quiet-note {{
            font-size: 12.5px;
            color: {TEXT_MUTED};
            font-style: italic;
        }}

        /* buttons */
        .stButton>button {{
            background: {BG_CARD};
            color: {TEXT_PRIMARY};
            border: 1px solid {BORDER};
            border-radius: 8px;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            border-color: {ACCENT_CYAN};
            color: {ACCENT_CYAN};
        }}

        div[data-baseweb="tab-list"] {{
            gap: 4px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# PROJECT-WIDE DEFAULTS (documented, configurable — not immutable)
# ----------------------------------------------------------------------
DEFAULT_BUCKET_SECONDS = 60
DEFAULT_HISTORY_T = 10
DEFAULT_STRIDE = 1
DEFAULT_RISK_THRESHOLD = 0.60

PROJECT_META = {
    "ps_code": "PS-26153",
    "title": "AI-Based Network Attack Forecasting from Network Traffic Data",
    "theme": "World Models for Predictive Cyber Defence",
    "org": "NTRO",
    "event": "Smart India Hackathon 2026",
}
