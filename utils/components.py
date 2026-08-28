"""
Reusable Streamlit UI components used across every page.
Keep these presentation-only: no data generation or model logic here.
"""

import streamlit as st
from utils.theme import risk_color, risk_level_from_probability


def status_badge(kind: str, text: str = None):
    """
    kind: one of 'real' | 'demo' | 'planned' | 'foundation' | 'heuristic'
          | 'safe' | 'elevated' | 'high' | 'critical'
    """
    labels = {
        "real": "REAL",
        "demo": "DEMO",
        "planned": "PLANNED",
        "foundation": "FOUNDATION",
        "heuristic": "HEURISTIC",
        "safe": "SAFE",
        "elevated": "ELEVATED",
        "high": "HIGH",
        "critical": "CRITICAL",
    }
    text = text or labels.get(kind, kind.upper())
    st.markdown(
        f'<span class="badge badge-{kind}">{text}</span>',
        unsafe_allow_html=True,
    )


def badge_html(kind: str, text: str = None) -> str:
    labels = {
        "real": "REAL", "demo": "DEMO", "planned": "PLANNED",
        "foundation": "FOUNDATION", "heuristic": "HEURISTIC",
        "safe": "SAFE", "elevated": "ELEVATED", "high": "HIGH", "critical": "CRITICAL",
    }
    text = text or labels.get(kind, kind.upper())
    return f'<span class="badge badge-{kind}">{text}</span>'


def system_banner():
    st.markdown(
        """
        <div class="system-banner">
            <span class="badge badge-demo">DEMO MODE — MODEL NOT TRAINED</span>
            <p style="margin-top:10px; margin-bottom:0; font-size:14px; color:#c3cbe0;">
            The current interface demonstrates the intended end-to-end system behaviour
            using representative / simulated outputs. Replace demo artifacts with trained
            model artifacts to activate real inference.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, badge_kind: str = "demo", sub: str = None):
    sub_html = f'<div style="margin-top:6px;">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div style="margin-top:8px;">{badge_html(badge_kind)}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card_open(kicker: str = None):
    kicker_html = f'<div class="section-kicker">{kicker}</div>' if kicker else ""
    st.markdown(f'<div class="glass-card">{kicker_html}', unsafe_allow_html=True)


def glass_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def pipeline_flow(stages: list, active_index: int = None, done_upto: int = -1):
    """
    stages: list of short labels e.g. ["P1 Ingestion", "P2 Preprocessing", ...]
    active_index: index currently "in progress"
    done_upto: indices <= this are marked complete
    """
    cols = st.columns(len(stages))
    for i, (col, label) in enumerate(zip(cols, stages)):
        cls = "pipeline-stage"
        prefix = "○"
        if i <= done_upto:
            cls += " done"
            prefix = "✓"
        if active_index is not None and i == active_index:
            cls += " active"
            prefix = "→"
        with col:
            st.markdown(
                f'<div class="{cls}">{prefix} {label}</div>',
                unsafe_allow_html=True,
            )


def arch_node(code: str, title: str, detail: str):
    st.markdown(
        f"""
        <div class="arch-node">
            <b>{code}</b> — {title}<br/>
            <span style="color:#8b96b3;">{detail}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def layer_label(text: str):
    st.markdown(f'<div class="layer-label">{text}</div>', unsafe_allow_html=True)


def quiet_note(text: str):
    st.markdown(f'<div class="quiet-note">{text}</div>', unsafe_allow_html=True)


def risk_badge_for_probability(p: float):
    level = risk_level_from_probability(p)
    kind_map = {"LOW": "safe", "ELEVATED": "elevated", "HIGH": "high", "CRITICAL": "critical"}
    status_badge(kind_map[level], level)


def illustrative_tag(text: str = "ILLUSTRATIVE / DEMO DATA"):
    st.markdown(
        f'<span class="badge badge-demo" style="opacity:0.85;">{text}</span>',
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str = None):
    st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(
            f'<p style="color:#8b96b3; font-size:15px; margin-top:-6px;">{subtitle}</p>',
            unsafe_allow_html=True,
        )
