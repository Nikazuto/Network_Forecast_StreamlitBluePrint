import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.components import glass_card_open, glass_card_close, illustrative_tag, status_badge, quiet_note
from utils.theme import ACCENT_CYAN, RISK_SAFE, RISK_ELEVATED, RISK_HIGH, RISK_CRITICAL, risk_level_from_probability


STAGE_LABELS = [
    (0, "Normal"),
    (25, "Reconnaissance indicators emerging"),
    (50, "Elevated suspicious activity"),
    (75, "High infiltration probability"),
    (100, "Attack trajectory strongly indicated"),
]

STAGE_TACTIC = [
    (0, "None"),
    (20, "Reconnaissance"),
    (45, "Credential Access"),
    (70, "Command and Control"),
    (90, "Lateral Movement"),
]


def _stage_text(pct: int) -> str:
    label = STAGE_LABELS[0][1]
    for threshold, text in STAGE_LABELS:
        if pct >= threshold:
            label = text
    return label


def _tactic_for(pct: int) -> str:
    tactic = STAGE_TACTIC[0][1]
    for threshold, text in STAGE_TACTIC:
        if pct >= threshold:
            tactic = text
    return tactic


def render():
    st.markdown("#### Attack Trajectory Simulator")
    illustrative_tag()
    st.caption("THIS IS A SIMULATION OF THE INTENDED MODEL BEHAVIOUR, NOT A REAL MODEL.")

    pct = st.slider("Attack Progression", 0, 100, 40, 1, key="trajectory_pct")

    # illustrative monotonic-ish curves driven purely by the slider position
    rng = np.random.default_rng(7)
    port_diversity = np.clip(0.15 + (pct / 100) * 0.75 + rng.normal(0, 0.01), 0, 1)
    syn_ratio = np.clip(0.20 + (pct / 100) * 0.65 + rng.normal(0, 0.01), 0, 1)
    iat_variance = np.clip(0.30 - (pct / 100) * 0.15 + rng.normal(0, 0.01), 0, 1)
    raw_risk = np.clip(0.10 + (pct / 100) * 0.85, 0, 1)
    probability = 1 / (1 + np.exp(-((raw_risk - 0.5) * 6)))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Network State", _stage_text(pct))
    with c2:
        st.metric("Risk Score (raw)", f"{raw_risk:.2f}")
    with c3:
        st.metric("Probability", f"{probability*100:.1f}%")
    with c4:
        st.metric("ATT&CK Tactic (heuristic)", _tactic_for(pct))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number={"suffix": "%", "font": {"family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": ACCENT_CYAN},
            "steps": [
                {"range": [0, 30], "color": "rgba(46,207,142,0.25)"},
                {"range": [30, 60], "color": "rgba(242,201,76,0.25)"},
                {"range": [60, 80], "color": "rgba(242,153,74,0.25)"},
                {"range": [80, 100], "color": "rgba(235,87,87,0.25)"},
            ],
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        height=260, margin=dict(l=20, r=20, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    quiet_note(
        "Network State → Predicted Future State → Risk Score → Probability → ATT&CK tactic "
        "all update together as the slider moves, illustrating the intended end-to-end reaction "
        "to an evolving attack trajectory."
    )
