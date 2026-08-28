import streamlit as st

from demo_data.generator import generate_state_timeseries, raw_risk_from_state, calibrate, SCENARIOS
from utils.components import page_header, glass_card_open, glass_card_close, illustrative_tag, quiet_note, status_badge
from utils.theme import risk_level_from_probability, RISK_SAFE, RISK_ELEVATED, RISK_HIGH, RISK_CRITICAL


def render():
    page_header("ANALYSIS LAYER · P5", "Probability & Risk",
                "Turning a predicted future state into an actionable, calibrated infiltration probability.")

    scenario = st.selectbox("Scenario", SCENARIOS, index=1, key="pr_scenario")
    df = generate_state_timeseries(scenario, n_windows=30)
    row = df.iloc[-1]
    raw = raw_risk_from_state(row)
    prob = calibrate(raw)
    illustrative_tag()

    glass_card_open("THREE-STAGE DERIVATION")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Predicted Future State**")
        st.markdown("`Ŝ(t+1)`")
        status_badge("demo")
    with c2:
        st.markdown("**2. Raw Risk Score**")
        st.markdown(f"`Raw Risk Score = {raw:.2f}`")
        status_badge("demo")
    with c3:
        st.markdown("**3. Calibrated Infiltration Probability**")
        st.markdown(f"`P(infiltration) = {prob:.2f}`")
        status_badge("demo")
    st.code(
        f"Ŝ(t+1)\n   ↓\nState-space risk scoring\n   ↓\nRaw Risk Score = {raw:.2f}\n   ↓\nCalibration\n   ↓\nP(infiltration) = {prob:.2f}",
        language="text",
    )
    glass_card_close()

    glass_card_open("WHY DOESN'T THE LSTM OUTPUT PROBABILITY DIRECTLY?")
    st.markdown(
        "Because the model's primary role is to learn network-state transition dynamics. "
        "The probability layer converts the predicted state into an actionable risk estimate. "
        "This preserves the distinction between dynamics prediction and attack classification."
    )
    glass_card_close()

    glass_card_open("RISK THRESHOLD BANDS")
    threshold_bands = [
        ("LOW RISK", "0–30%", RISK_SAFE),
        ("ELEVATED", "30–60%", RISK_ELEVATED),
        ("HIGH", "60–80%", RISK_HIGH),
        ("CRITICAL", "80–100%", RISK_CRITICAL),
    ]
    cols = st.columns(4)
    for col, (name, rng, color) in zip(cols, threshold_bands):
        with col:
            st.markdown(
                f"""<div style="border:1px solid {color}55; background:{color}14; border-radius:10px;
                padding:12px; text-align:center;">
                <div style="font-weight:700; color:{color};">{name}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#c3cbe0;">{rng}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    live_threshold = st.slider("Adjust warning threshold interactively", 0.0, 1.0, 0.60, 0.05)
    level = risk_level_from_probability(prob)
    st.markdown(
        f"Current illustrative probability **{prob*100:.1f}%** falls in band **{level}**. "
        f"{'⚠️ Above' if prob >= live_threshold else '✅ Below'} the selected threshold of {live_threshold*100:.0f}%."
    )
    glass_card_close()
    quiet_note("Raw risk scoring and calibration shown here are placeholder heuristics pending real training and calibration.")
