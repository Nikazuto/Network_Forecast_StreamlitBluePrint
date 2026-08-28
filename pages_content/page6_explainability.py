import plotly.graph_objects as go
import streamlit as st

from demo_data.generator import SHAP_CASE_STUDIES
from utils.components import page_header, glass_card_open, glass_card_close, quiet_note, status_badge
from utils.theme import RISK_SAFE, RISK_HIGH

INTERPRETATIONS = {
    "Port Scan / Reconnaissance": (
        "Elevated port diversity and SYN activity contributed most strongly to the forecasted risk. "
        "This pattern is consistent with reconnaissance / scanning behaviour."
    ),
    "C2 Beacon-like activity": (
        "Low inter-arrival variance combined with periodic byte-volume patterns dominated the "
        "attribution, consistent with beacon-like command-and-control traffic."
    ),
    "Brute Force": (
        "A high ACK-to-RST ratio alongside sustained packet volume dominated the attribution, "
        "consistent with repeated authentication attempts."
    ),
}


def render():
    page_header("ANALYSIS LAYER · P8", "Why did the system forecast elevated risk?",
                "Illustrative SHAP attribution — real values will be generated after model training.")

    status_badge("demo", "ILLUSTRATIVE SHAP")

    case = st.selectbox("Case study", list(SHAP_CASE_STUDIES.keys()))
    contributions = SHAP_CASE_STUDIES[case]

    glass_card_open("FEATURE CONTRIBUTION")
    features = [c[0] for c in contributions]
    values = [c[1] for c in contributions]
    colors = [RISK_HIGH if v > 0 else RISK_SAFE for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=features, orientation="h", marker_color=colors,
        text=[f"{v:+.2f}" for v in values], textposition="outside",
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=320, margin=dict(l=10, r=40, t=10, b=10), xaxis_title="Contribution to risk forecast",
    )
    st.plotly_chart(fig, use_container_width=True)
    glass_card_close()

    glass_card_open("HUMAN INTERPRETATION")
    st.markdown(f"> {INTERPRETATIONS.get(case, 'Interpretation pending real SHAP values.')}")
    quiet_note("Do not treat this narrative as learned from real data in demo mode — it illustrates the intended output format.")
    glass_card_close()

    glass_card_open("ATTRIBUTION CHAIN")
    st.code(
        "FEATURE\n   ↓\nMODEL CONTRIBUTION\n   ↓\nNETWORK BEHAVIOUR\n   ↓\nSECURITY INTERPRETATION",
        language="text",
    )
    glass_card_close()

    glass_card_open("CASE STUDIES")
    st.markdown(
        "- **Case Study A** — Port Scan / Reconnaissance\n"
        "- **Case Study B** — C2 Beacon-like Traffic\n"
        "- **Case Study C** — Brute Force-like Activity\n\n"
        "Concrete case studies are used so explainability is not merely a generic SHAP plot."
    )
    glass_card_close()
