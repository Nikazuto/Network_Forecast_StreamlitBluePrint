import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, arch_node, layer_label, quiet_note
from utils.theme import ACCENT_CYAN

MODULE_DETAILS = {
    "P1": ("Data Ingestion", "Reads raw network flow records (CIC-IDS2017 schema) from CSV. "
           "Input: raw flow CSV. Output: parsed flow records."),
    "P2": ("Preprocessing & Normalisation", "Cleans and normalises flow-level features onto a "
           "consistent scale ahead of temporal aggregation."),
    "P3": ("Windowing / State Construction", "Aggregates flow-level observations into fixed-duration "
           "buckets to construct the network state vector S_t."),
    "P4": ("LSTM World Model", "Learns one-step network-state transition dynamics.\n"
           "Input: history ending at S_t\nOutput: predicted S_(t+1)\nTarget: future state vector\nNOT attack/benign label."),
    "P5": ("Probability Derivation", "Input: predicted future state\nOutput: calibrated infiltration probability."),
    "P6": ("Logistic Regression Baseline", "Trained on the identical feature schema/split to isolate the "
           "value added by temporal modelling."),
    "P7": ("Evaluation", "Computes classification metrics, forecast lead time, and calibration diagnostics."),
    "P8": ("SHAP", "Explains selected high-risk windows via feature attribution."),
    "P9": ("ATT&CK", "Applies documented heuristic mapping from behaviour pattern to MITRE ATT&CK tactic."),
    "P10": ("Streamlit Dashboard", "Presents the full analyst workflow described on this page."),
}


def render():
    page_header("SYSTEM DESIGN", "Architecture",
                "Four layers take raw traffic to an explained, mapped, calibrated forecast.")

    glass_card_open("CENTRAL PATH")
    st.code(
        "CSV → Clean → Window → S_t → LSTM → Ŝ(t+1) → Risk Score → Probability → SHAP / ATT&CK → Dashboard",
        language="text",
    )
    glass_card_close()

    col1, col2 = st.columns(2)
    with col1:
        layer_label("Data Layer")
        arch_node("P1", "Data Ingestion", "Raw CIC-IDS2017 flow records")
        arch_node("P2", "Preprocessing & Normalisation", "Cleaning + feature scaling")
        arch_node("P3", "Windowing / State Construction", "Builds network state S_t")

        layer_label("Modeling Layer")
        arch_node("P4", "LSTM World Model", "S_t history → Ŝ(t+1)")
        arch_node("P6", "Logistic Regression Baseline", "Same features, flow/window → label")

    with col2:
        layer_label("Analysis Layer")
        arch_node("P5", "Probability Derivation & Calibration", "Ŝ(t+1) → P(infiltration)")
        arch_node("P7", "Evaluation", "Metrics, lead time, calibration")
        arch_node("P8", "SHAP Explainability", "Attribution for flagged windows")
        arch_node("P9", "MITRE ATT&CK Heuristic Mapping", "Pattern → tactic")

        layer_label("Presentation Layer")
        arch_node("P10", "Streamlit Dashboard", "This application")

    st.markdown("<br>", unsafe_allow_html=True)
    glass_card_open("MODULE DETAIL")
    choice = st.selectbox("Select a module to inspect", list(MODULE_DETAILS.keys()),
                           format_func=lambda k: f"{k} — {MODULE_DETAILS[k][0]}")
    title, detail = MODULE_DETAILS[choice]
    st.markdown(f"#### {choice} — {title}")
    st.code(detail, language="text")
    glass_card_close()

    quiet_note("This is an offline / local demonstration. No cloud inference or external API calls are part of the architecture.")
