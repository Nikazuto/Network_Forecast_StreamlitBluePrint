import streamlit as st

from utils.theme import inject_css, PROJECT_META
from utils.components import status_badge, quiet_note
from pages_content import (
    page1_executive,
    page2_live_forecast,
    page3_world_model,
    page4_network_state,
    page5_probability_risk,
    page6_explainability,
    page7_mitre,
    page8_baseline,
    page9_evaluation,
    page10_architecture,
    page11_status,
    page12_notes,
    trajectory_simulator,
    judge_mode,
)

st.set_page_config(
    page_title="Predictive Cyber Defence — PS-26153",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

PAGES = {
    "1 · Executive Dashboard": page1_executive,
    "2 · Live / Demo Forecast": page2_live_forecast,
    "3 · World Model": page3_world_model,
    "4 · Network State": page4_network_state,
    "5 · Probability & Risk": page5_probability_risk,
    "6 · Explainability": page6_explainability,
    "7 · MITRE ATT&CK": page7_mitre,
    "8 · Baseline Comparison": page8_baseline,
    "9 · Evaluation": page9_evaluation,
    "10 · Architecture": page10_architecture,
    "11 · Implementation Status": page11_status,
    "12 · About / Technical Notes": page12_notes,
}

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding-bottom:6px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#3fd0e0; letter-spacing:0.1em;">
                {PROJECT_META['ps_code']} · {PROJECT_META['org']}
            </div>
            <div style="font-size:18px; font-weight:800; margin-top:2px;">Predictive Cyber Defence</div>
            <div style="font-size:12px; color:#8b96b3;">{PROJECT_META['event']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    status_badge("demo", "MODEL NOT TRAINED")
    st.markdown("---")

    if "judge_mode" not in st.session_state:
        st.session_state.judge_mode = False
    if "show_demo_script" not in st.session_state:
        st.session_state.show_demo_script = False

    st.session_state.judge_mode = st.toggle("🧑‍⚖️ Judge Mode", value=st.session_state.judge_mode)

    if st.button("▶ 2-Minute Demo Script", use_container_width=True):
        st.session_state.show_demo_script = not st.session_state.show_demo_script

    st.markdown("---")

    selection = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

    st.markdown("---")
    with st.expander("⚡ Attack Trajectory Simulator", expanded=False):
        trajectory_simulator.render()

    st.markdown("---")
    st.markdown(
        f"""
        <div style="font-size:11px; color:#5b657f; font-family:'JetBrains Mono',monospace; line-height:1.6;">
        "World Models for Predictive Cyber Defence"<br/>
        Offline Demonstration Prototype
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# MAIN AREA
# ------------------------------------------------------------------
if st.session_state.show_demo_script:
    judge_mode.render_demo_script()
    st.markdown("---")

if st.session_state.judge_mode:
    judge_mode.render_judge_tour()
else:
    PAGES[selection].render()

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align:center; color:#5b657f; font-family:'JetBrains Mono',monospace; font-size:11.5px; line-height:1.8; padding-bottom:12px;">
    {PROJECT_META['ps_code']} · {PROJECT_META['title']}<br/>
    "{PROJECT_META['theme']}" · "Offline Demonstration Prototype"<br/>
    Current demo uses representative data until trained model artifacts are available.
    </div>
    """,
    unsafe_allow_html=True,
)
