import streamlit as st

from utils.components import page_header, glass_card_open, glass_card_close, status_badge, quiet_note


def render():
    page_header("ENGINEERING ROADMAP", "Implementation Status",
                "What is real today, what is demonstrated, and what is pending real model training.")

    c1, c2, c3 = st.columns(3)

    with c1:
        glass_card_open()
        status_badge("foundation")
        st.markdown("#### Implemented Foundation")
        st.markdown(
            "- Repository structure\n"
            "- Module contracts\n"
            "- Shared data types\n"
            "- Configuration\n"
            "- CLI skeleton\n"
            "- Contract tests\n"
            "- Architecture\n"
            "- Data contracts"
        )
        glass_card_close()

    with c2:
        glass_card_open()
        status_badge("demo")
        st.markdown("#### In Development / Demonstrated")
        st.markdown(
            "- Streamlit presentation\n"
            "- Demo scenarios\n"
            "- Visualization layer"
        )
        glass_card_close()

    with c3:
        glass_card_open()
        status_badge("planned", "PENDING MODEL")
        st.markdown("#### Pending Real ML Run")
        st.markdown(
            "- CSV ingestion\n"
            "- Preprocessing\n"
            "- State construction\n"
            "- LSTM training\n"
            "- Probability calibration\n"
            "- Baseline training\n"
            "- Evaluation\n"
            "- SHAP\n"
            "- ATT&CK mapping\n"
            "- Real inference"
        )
        glass_card_close()

    st.warning(
        "The repository currently has the contract skeleton and tests, but the actual "
        "ingestion / training / SHAP / ATT&CK / dashboard logic is not implemented. "
        "This is not concealed anywhere in this application."
    )

    glass_card_open("WHY DEMONSTRATE THE INTERFACE BEFORE MODEL TRAINING?")
    st.markdown(
        "The frontend is designed against the frozen module contracts, allowing the complete "
        "analyst workflow and system architecture to be validated independently of the final "
        "trained weights."
    )
    glass_card_close()
