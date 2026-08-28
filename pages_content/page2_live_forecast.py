import time

import plotly.graph_objects as go
import streamlit as st

from demo_data.generator import SCENARIOS, build_forecast_frame, ATTACK_TACTIC_MAP
from utils.components import (
    page_header, glass_card_open, glass_card_close, pipeline_flow,
    quiet_note, illustrative_tag, status_badge,
)
from utils.theme import (
    DEFAULT_BUCKET_SECONDS, DEFAULT_HISTORY_T, DEFAULT_STRIDE,
    DEFAULT_RISK_THRESHOLD, ACCENT_CYAN, RISK_HIGH, RISK_ELEVATED,
)


def render():
    page_header(
        "ANALYST WORKFLOW",
        "Run an Offline Forecast",
        "Upload flow data or load a demonstration scenario to walk through the full pipeline.",
    )

    tab1, tab2 = st.tabs(["📁 Upload CIC-IDS2017 CSV", "🧪 Load Demonstration Scenario"])

    with tab1:
        uploaded = st.file_uploader("Upload CIC-IDS2017 flow CSV", type=["csv"])
        if uploaded is not None:
            st.warning(
                "CSV ingestion (P1) and preprocessing (P2) are part of the module "
                "contract but are **not yet implemented / trained**. The file has been "
                "received but the pipeline below will run in illustrative demo mode."
            )
        quiet_note("Real ingestion is PENDING REAL ML RUN — see Implementation Status.")

    with tab2:
        scenario = st.selectbox("Demo scenario", SCENARIOS, index=5)
        status_badge("demo", "SIMULATED / CASE-STUDY DATA")

    st.markdown("<br>", unsafe_allow_html=True)
    glass_card_open("PIPELINE PARAMETERS")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        bucket = st.slider("Window size (seconds)", 10, 120, DEFAULT_BUCKET_SECONDS, 10)
    with c2:
        history_t = st.slider("History length T", 2, 20, DEFAULT_HISTORY_T)
    with c3:
        stride = st.slider("Sliding stride", 1, 5, DEFAULT_STRIDE)
    with c4:
        threshold = st.slider("Risk threshold", 0.0, 1.0, DEFAULT_RISK_THRESHOLD, 0.05)
    quiet_note(
        f"Documented defaults: bucket = {DEFAULT_BUCKET_SECONDS}s, T = {DEFAULT_HISTORY_T}, "
        f"stride = {DEFAULT_STRIDE}. These are configurable defaults, not immutable constants."
    )
    glass_card_close()

    run = st.button("▶ Run Offline Forecast (Demo)", type="primary")

    stages = [
        "P1 Ingestion", "P2 Preprocessing", "P3 State Construction",
        "P4 World Model", "P5 Risk Derivation", "P8 Explainability", "P9 ATT&CK Mapping",
    ]

    st.markdown("<br>", unsafe_allow_html=True)
    glass_card_open("PIPELINE EXECUTION")

    placeholder = st.empty()
    if run:
        for i in range(len(stages)):
            with placeholder.container():
                pipeline_flow(stages, active_index=i, done_upto=i - 1)
            time.sleep(0.35)
        with placeholder.container():
            pipeline_flow(stages, active_index=None, done_upto=len(stages) - 1)
        st.success("Demo pipeline complete — outputs below are illustrative, not real inference.")
    else:
        with placeholder.container():
            pipeline_flow(stages, active_index=None, done_upto=-1)
        quiet_note("Click \"Run Offline Forecast\" to animate the pipeline stages.")
    glass_card_close()

    df = build_forecast_frame(scenario, n_windows=60)
    glass_card_open("FORECAST OUTPUT")
    illustrative_tag()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["window"], y=df["probability"], mode="lines",
        line=dict(color=ACCENT_CYAN, width=2.5), fill="tozeroy",
        fillcolor="rgba(63,208,224,0.08)", name="P(infiltration)",
    ))
    fig.add_hline(y=threshold, line_dash="dash", line_color=RISK_ELEVATED)
    flagged = df[df["probability"] >= threshold]
    if len(flagged):
        fig.add_trace(go.Scatter(
            x=flagged["window"], y=flagged["probability"], mode="markers",
            marker=dict(color=RISK_HIGH, size=8, symbol="diamond"), name="Flagged",
        ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=340, margin=dict(l=10, r=10, t=10, b=10), yaxis_range=[0, 1],
        xaxis_title="Window", yaxis_title="Probability",
    )
    st.plotly_chart(fig, use_container_width=True)

    if len(flagged):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Flagged windows", len(flagged))
        with c2:
            st.metric("Peak probability", f"{df['probability'].max()*100:.1f}%")
        with c3:
            st.markdown(f"**Heuristic ATT&CK tactic**  \n{ATTACK_TACTIC_MAP.get(scenario, 'N/A')}")
            status_badge("heuristic")
    glass_card_close()
