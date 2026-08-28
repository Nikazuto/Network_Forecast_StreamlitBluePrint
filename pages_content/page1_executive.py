import numpy as np
import plotly.graph_objects as go
import streamlit as st

from demo_data.generator import build_forecast_frame
from utils.components import (
    metric_card, system_banner, page_header, glass_card_open, glass_card_close,
    quiet_note, illustrative_tag,
)
from utils.theme import RISK_HIGH, RISK_SAFE, ACCENT_CYAN, RISK_ELEVATED, TEXT_MUTED


def render():
    page_header(
        "PS-26153 · NTRO · SIH 2026",
        "Predictive Cyber Defence",
        "AI-Based Network Attack Forecasting — learning network-state dynamics "
        "to forecast attacker progression before compromise.",
    )

    system_banner()

    st.markdown(
        f"""
        <div style="text-align:center; padding: 10px 0 26px 0;">
            <span style="font-family:'JetBrains Mono',monospace; font-size:17px; color:{ACCENT_CYAN};
            border-top:1px solid #232d45; border-bottom:1px solid #232d45; padding: 10px 18px;">
            "Forecast the evolution of network state — not just classify the traffic you already observed."
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    scenario = "Mixed attack progression"
    df = build_forecast_frame(scenario, n_windows=72)
    threshold = 0.60
    current_prob = df["probability"].iloc[-1]
    n_flagged = int((df["probability"] >= threshold).sum())

    cols = st.columns(6)
    with cols[0]:
        metric_card("Current Network Risk", "ELEVATED", "demo")
    with cols[1]:
        metric_card("Forecast Probability", f"{current_prob*100:.1f}%", "demo")
    with cols[2]:
        metric_card("Windows Analysed", f"{len(df)}", "demo")
    with cols[3]:
        metric_card("High-Risk Windows", f"{n_flagged}", "demo")
    with cols[4]:
        metric_card("Forecast Horizon", "T+1 (60s)", "foundation")
    with cols[5]:
        metric_card("Model Status", "NOT TRAINED", "planned")

    st.markdown("<br>", unsafe_allow_html=True)
    glass_card_open("MAIN CHART")
    st.markdown("#### Network Infiltration Forecast Timeline")
    illustrative_tag()

    onset_idx = 24
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["window"], y=df["probability"], mode="lines",
        line=dict(color=ACCENT_CYAN, width=2.5),
        name="Infiltration probability",
        fill="tozeroy", fillcolor="rgba(63,208,224,0.08)",
        hovertemplate="Window %{x}<br>P(infiltration) = %{y:.2f}<extra></extra>",
    ))
    fig.add_hline(y=threshold, line_dash="dash", line_color=RISK_ELEVATED,
                  annotation_text="Warning threshold", annotation_font_color=RISK_ELEVATED)
    flagged = df[df["probability"] >= threshold]
    if len(flagged):
        fig.add_trace(go.Scatter(
            x=flagged["window"], y=flagged["probability"], mode="markers",
            marker=dict(color=RISK_HIGH, size=8, symbol="diamond"),
            name="Flagged window",
        ))
    fig.add_vline(x=onset_idx, line_dash="dot", line_color=RISK_HIGH,
                  annotation_text="Attack onset (illustrative)", annotation_font_color=RISK_HIGH)
    fig.add_vrect(x0=onset_idx, x1=df["window"].max(), fillcolor=RISK_HIGH, opacity=0.05, line_width=0)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Time (window index)",
        yaxis_title="Infiltration probability",
        yaxis_range=[0, 1],
        legend=dict(orientation="h", y=1.12),
        hoverlabel=dict(bgcolor="#131a2b", font_family="JetBrains Mono"),
    )
    st.plotly_chart(fig, use_container_width=True)
    quiet_note(
        "Probability is derived from the predicted future network state, "
        "not directly from an attack classifier."
    )
    glass_card_close()

    glass_card_open("WHY THIS IS PREDICTIVE")
    steps = [
        "Observed State S_t", "LSTM learns temporal dynamics", "Predicted State Ŝ(t+1)",
        "Risk Score", "Calibrated Probability", "Early Warning",
    ]
    cols = st.columns(len(steps))
    for c, s in zip(cols, steps):
        with c:
            st.markdown(
                f"""<div style="text-align:center; font-family:'JetBrains Mono',monospace;
                font-size:12.5px; color:{TEXT_MUTED}; border:1px solid #232d45; border-radius:10px;
                padding:12px 6px; background:#131a2b;">{s}</div>""",
                unsafe_allow_html=True,
            )
    glass_card_close()

    glass_card_open()
    st.markdown("#### Traditional IDS vs. This System")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Traditional IDS asks:**")
        st.markdown("> _\"Is this flow malicious?\"_")
        st.markdown("`Flow → Label`")
    with c2:
        st.markdown("**Our system asks:**")
        st.markdown("> _\"Given how the network has evolved so far, what state is it likely to enter next?\"_")
        st.markdown("`State history → Future state → Risk → Early warning`")
    glass_card_close()
