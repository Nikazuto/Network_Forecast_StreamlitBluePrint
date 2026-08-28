import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, status_badge
from utils.theme import PROJECT_META, DEFAULT_BUCKET_SECONDS, DEFAULT_HISTORY_T, DEFAULT_STRIDE


def render():
    page_header("REFERENCE", "About / Technical Notes", "Project configuration and scope boundaries.")

    glass_card_open("PROJECT")
    st.markdown(
        f"**{PROJECT_META['ps_code']}** — {PROJECT_META['title']}  \n"
        f"Theme: *{PROJECT_META['theme']}*  \n"
        f"Organisation: {PROJECT_META['org']} · {PROJECT_META['event']}"
    )
    glass_card_close()

    c1, c2 = st.columns(2)
    with c1:
        glass_card_open("CONFIGURATION")
        st.code(
            f"Dataset:        CIC-IDS2017\n"
            f"Window:         {DEFAULT_BUCKET_SECONDS} seconds\n"
            f"History:        T = {DEFAULT_HISTORY_T}\n"
            f"Stride:         {DEFAULT_STRIDE}\n"
            f"Aggregation:    per-scenario global buckets\n"
            f"Split:          70 / 15 / 15 chronological\n"
            f"Holdout:        Thursday files\n"
            f"Prediction:     one-step S_t → S_(t+1)\n"
            f"Architecture:   LSTM\n"
            f"Baseline:       Logistic Regression\n"
            f"Explainability: SHAP\n"
            f"Threat mapping: MITRE ATT&CK heuristic mapping\n"
            f"Runtime:        Offline / local",
            language="text",
        )
        glass_card_close()

    with c2:
        glass_card_open("OUT OF SCOPE FOR CURRENT MVP")
        st.markdown(
            "- K-step autoregressive rollout\n"
            "- Full packet-level PCAP processing\n"
            "- GNN architecture\n"
            "- Transformer architecture"
        )
        st.caption("These do not appear as implemented features anywhere in this demo.")
        glass_card_close()

    glass_card_open("HONESTY STATES USED THROUGHOUT THIS APPLICATION")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("**Model Status**")
        status_badge("demo", "SIMULATED DEMO")
    with c2:
        st.markdown("**Real Model**")
        status_badge("planned", "Not loaded")
    with c3:
        st.markdown("**Training Status**")
        status_badge("planned", "Pending")
    with c4:
        st.markdown("**SHAP**")
        status_badge("demo", "Illustrative")
    with c5:
        st.markdown("**ATT&CK**")
        status_badge("heuristic", "Heuristic demonstration")
    glass_card_close()

    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center; color:#5b657f; font-family:'JetBrains Mono',monospace; font-size:12px; line-height:1.8;">
        {PROJECT_META['ps_code']} · {PROJECT_META['title']}<br/>
        "{PROJECT_META['theme']}"<br/>
        "Offline Demonstration Prototype"<br/>
        Current demo uses representative data until trained model artifacts are available.
        </div>
        """,
        unsafe_allow_html=True,
    )
