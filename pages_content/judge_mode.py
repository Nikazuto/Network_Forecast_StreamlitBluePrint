import streamlit as st

from utils.components import glass_card_open, glass_card_close, status_badge, quiet_note

JUDGE_STEPS = [
    ("1. Observe network traffic",
     "Raw flow records arrive from the network and are ingested (P1).",
     "Input: CIC-IDS2017 flow CSV. Output: parsed flow records feeding preprocessing."),
    ("2. Build temporal network states",
     "Flows are aggregated into fixed-duration windows to form the network state S_t (P3).",
     "60-second buckets by default; each S_t is a normalised feature vector (SYN ratio, port diversity, IAT stats, ...)."),
    ("3. Predict next network state",
     "The LSTM World Model consumes a history of states and predicts Ŝ(t+1) (P4).",
     "Self-supervised next-state prediction — the label is never the direct training target."),
    ("4. Derive infiltration probability",
     "The predicted state is scored and calibrated into P(infiltration) (P5).",
     "Raw risk score → calibration curve → bounded [0,1] probability."),
    ("5. Explain why risk increased",
     "SHAP attributes the forecast to specific state features for a flagged window (P8).",
     "Illustrative in demo mode; will use real trained SHAP values once training completes."),
    ("6. Map behaviour to ATT&CK",
     "A heuristic mapping links the observed pattern to a MITRE ATT&CK tactic (P9).",
     "Heuristic pattern rules today — not a learned or ground-truth-labelled mapping."),
]

DEMO_SCRIPT = [
    "Select \"Port Scan Progression\"",
    "Show network state changing",
    "Show LSTM world model concept",
    "Show predicted future state",
    "Show probability rising",
    "Highlight flagged window",
    "Show SHAP explanation",
    "Show ATT&CK Reconnaissance mapping",
    "Show baseline comparison",
    "Finish with architecture diagram",
]


def render_judge_tour():
    st.markdown("### Judge Mode — Guided Tour")
    status_badge("demo", "CONDENSED WALKTHROUGH")
    st.caption("Observe → Predict → Score → Explain → Map")

    for title, sentence, detail in JUDGE_STEPS:
        glass_card_open()
        st.markdown(f"#### {title}")
        st.markdown(sentence)
        st.code(detail, language="text")
        glass_card_close()


def render_demo_script():
    st.markdown("### 2-Minute Demo Script")
    st.caption("Observe → Predict → Score → Explain → Map")
    for i, step in enumerate(DEMO_SCRIPT, start=1):
        st.markdown(f"**{i}.** {step}")
    quiet_note("Use this checklist while presenting to judges; it mirrors the pipeline shown in Live / Demo Forecast and Architecture.")
