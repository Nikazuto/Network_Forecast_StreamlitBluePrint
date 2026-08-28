import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, status_badge, quiet_note


def render():
    page_header("MODELING LAYER · P6", "Does Temporal Modelling Add Value?",
                "The logistic regression baseline exists to isolate the contribution of temporal modelling.")

    glass_card_open("EXPERIMENTAL DESIGN")
    st.code(
        "               Same input features\n"
        "                       ↓\n"
        "        ┌──────────────┴──────────────┐\n"
        "        │                             │\n"
        "  LSTM World Model           Logistic Regression\n"
        "        │                             │\n"
        "   Future state                Attack/Benign\n"
        "        │                             │\n"
        "  Risk forecast                Classification\n"
        "        └──────────────┬──────────────┘\n"
        "                       ↓\n"
        "                  Evaluation",
        language="text",
    )
    st.markdown(
        "The baseline uses the identical feature schema and split, allowing the temporal "
        "modelling contribution to be evaluated fairly."
    )
    glass_card_close()

    glass_card_open("METRIC COMPARISON")
    cols = st.columns([1.4, 1, 1])
    with cols[0]:
        st.markdown("**Metric**")
    with cols[1]:
        st.markdown("**World Model**")
    with cols[2]:
        st.markdown("**Baseline**")

    for metric in ["F1", "Precision", "Recall", "False Positive Rate"]:
        c1, c2, c3 = st.columns([1.4, 1, 1])
        with c1:
            st.markdown(metric)
        with c2:
            status_badge("planned", "Pending real training")
        with c3:
            status_badge("planned", "Pending real training")
    glass_card_close()

    quiet_note(
        "Numbers are intentionally withheld rather than invented — evaluators may ask where "
        "figures came from, and none exist until the model is trained."
    )
