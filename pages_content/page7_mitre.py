import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, status_badge, quiet_note
from utils.theme import ACCENT_CYAN, RISK_HIGH


def render():
    page_header("ANALYSIS LAYER · P9", "Attack Behaviour Mapping",
                "The current ATT&CK mapping is heuristic, not learned ground truth.")

    status_badge("heuristic")
    status_badge("planned", "NOT MODEL OUTPUT")

    glass_card_open("ILLUSTRATIVE ATTACK PROGRESSION")
    st.code(
        "Reconnaissance\n      ↓\nCredential Access\n      ↓\nCommand & Control\n      ↓\nLateral Movement\n      ↓\nExfiltration",
        language="text",
    )
    glass_card_close()

    glass_card_open("FLAGGED WINDOW EXAMPLE")
    st.markdown("**Window #42**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("Risk")
        status_badge("high")
    with c2:
        st.markdown("Pattern")
        st.markdown("`Port-scan-like`")
    with c3:
        st.markdown("ATT&CK Tactic")
        st.markdown("`Reconnaissance`")
    status_badge("heuristic", "Confidence: Heuristic mapping")
    glass_card_close()

    glass_card_open("HEURISTIC MAPPING RULES (ILLUSTRATIVE)")
    st.markdown(
        "- Port-scan-like traffic → **Reconnaissance**\n"
        "- Periodic beacon-like traffic → **Command and Control**\n"
        "- Brute-force-like activity → **Credential Access**"
    )
    quiet_note("The dataset does not contain native ATT&CK labels; mappings above are heuristic pattern rules, not learned outputs.")
    glass_card_close()
