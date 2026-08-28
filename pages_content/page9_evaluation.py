import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, status_badge, quiet_note
from utils.theme import ACCENT_CYAN, TEXT_MUTED


def render():
    page_header("ANALYSIS LAYER · P7", "Evaluation",
                "Classification metrics alone do not demonstrate predictive defence.")

    glass_card_open("A. CLASSIFICATION METRICS")
    cols = st.columns(4)
    for col, metric in zip(cols, ["F1", "Precision", "Recall", "False Positive Rate"]):
        with col:
            st.markdown(f"**{metric}**")
            status_badge("planned", "Pending real training")
    glass_card_close()

    glass_card_open("B. PREDICTIVE METRICS")
    st.markdown("**Forecast Lead Time**")
    st.code(
        "Forecast Lead Time =\n"
        "   Time of labelled attack onset\n"
        "   −\n"
        "   Time of first correct high-confidence forecast",
        language="text",
    )
    status_badge("planned", "Pending real training")
    quiet_note("This metric is made visually prominent because it demonstrates the project's predictive / pre-compromise value.")
    glass_card_close()

    glass_card_open("C. CALIBRATION")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Brier Score**")
        status_badge("planned", "Awaiting trained model evaluation")
    with c2:
        st.markdown("**Expected Calibration Error (ECE)**")
        status_badge("planned", "Awaiting trained model evaluation")

    st.markdown("**Reliability Diagram**")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines", line=dict(color=TEXT_MUTED, dash="dash"),
        name="Ideal calibration",
    ))
    fig.add_annotation(
        x=0.5, y=0.5, text="Awaiting trained model evaluation", showarrow=False,
        font=dict(color=TEXT_MUTED, size=14, family="JetBrains Mono"),
    )
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=340, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Predicted probability", range=[0, 1]),
        yaxis=dict(title="Observed frequency", range=[0, 1]),
    )
    st.plotly_chart(fig, use_container_width=True)
    glass_card_close()

    glass_card_open("D. EVALUATION PHILOSOPHY")
    st.markdown(
        "F1 alone does not demonstrate predictive defence. A successful system must provide "
        "an early and calibrated warning."
    )
    glass_card_close()
