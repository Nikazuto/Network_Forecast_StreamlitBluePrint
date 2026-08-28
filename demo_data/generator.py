"""
DEMO DATA ENGINE
================
Generates deterministic, illustrative time-series data used ONLY to make the
interface demonstrable while the real LSTM World Model / preprocessing
pipeline is not yet trained.

Nothing in this module is a trained model. Every array produced here is
synthetic and clearly surfaced as such by the UI layer (see
utils/components.py -> illustrative_tag / status_badge).

All generators are deterministic given a scenario + seed, so the demo is
reproducible across a run and across judges' laptops.
"""

import numpy as np
import pandas as pd

SCENARIOS = [
    "Benign traffic",
    "Port Scan / Reconnaissance",
    "Brute Force",
    "DoS-like activity",
    "C2 Beacon-like activity",
    "Mixed attack progression",
]

STATE_FEATURES = [
    "SYN ratio",
    "ACK ratio",
    "RST ratio",
    "Packet volume",
    "Byte volume",
    "IAT mean",
    "IAT variance",
    "Port diversity",
    "Bidirectional ratio",
]


def _rng(scenario: str, seed_offset: int = 0) -> np.random.Generator:
    seed = (abs(hash(scenario)) % (10 ** 6)) + seed_offset
    return np.random.default_rng(seed)


def generate_state_timeseries(scenario: str, n_windows: int = 60) -> pd.DataFrame:
    """
    Returns a DataFrame of shape (n_windows, len(STATE_FEATURES)) representing
    the synthetic S_t sequence for a scenario, all values in [0, 1].
    """
    rng = _rng(scenario)
    t = np.linspace(0, 1, n_windows)
    base = {f: rng.uniform(0.15, 0.35, size=n_windows) for f in STATE_FEATURES}

    def ramp(start, end, curve=1.0):
        return start + (end - start) * (t ** curve)

    if scenario == "Benign traffic":
        for f in STATE_FEATURES:
            base[f] = np.clip(base[f] + rng.normal(0, 0.03, n_windows), 0.05, 0.45)

    elif scenario == "Port Scan / Reconnaissance":
        base["Port diversity"] = np.clip(ramp(0.2, 0.92, 1.4) + rng.normal(0, 0.02, n_windows), 0, 1)
        base["SYN ratio"] = np.clip(ramp(0.25, 0.85, 1.2) + rng.normal(0, 0.03, n_windows), 0, 1)
        base["RST ratio"] = np.clip(ramp(0.15, 0.6, 1.1) + rng.normal(0, 0.03, n_windows), 0, 1)
        base["Packet volume"] = np.clip(ramp(0.3, 0.65, 1.0) + rng.normal(0, 0.03, n_windows), 0, 1)

    elif scenario == "Brute Force":
        base["ACK ratio"] = np.clip(ramp(0.3, 0.8, 1.3) + rng.normal(0, 0.02, n_windows), 0, 1)
        base["RST ratio"] = np.clip(ramp(0.2, 0.75, 1.2) + rng.normal(0, 0.03, n_windows), 0, 1)
        base["Packet volume"] = np.clip(ramp(0.35, 0.7, 1.0) + rng.normal(0, 0.03, n_windows), 0, 1)
        base["Bidirectional ratio"] = np.clip(ramp(0.3, 0.7, 1.1), 0, 1)

    elif scenario == "DoS-like activity":
        base["Packet volume"] = np.clip(ramp(0.3, 0.97, 1.6) + rng.normal(0, 0.02, n_windows), 0, 1)
        base["Byte volume"] = np.clip(ramp(0.3, 0.95, 1.6) + rng.normal(0, 0.02, n_windows), 0, 1)
        base["SYN ratio"] = np.clip(ramp(0.3, 0.8, 1.3), 0, 1)
        base["IAT mean"] = np.clip(1 - ramp(0.0, 0.6, 1.2), 0, 1)

    elif scenario == "C2 Beacon-like activity":
        period = max(3, n_windows // 8)
        beacon = 0.5 + 0.35 * np.sin(2 * np.pi * t * (n_windows / period) / n_windows * n_windows / 6)
        base["IAT variance"] = np.clip(0.15 + 0.05 * np.abs(np.sin(t * 20)) + ramp(0, 0.1, 1), 0, 1)
        base["IAT mean"] = np.clip(0.5 + 0.05 * np.sin(t * 25), 0.2, 0.8)
        base["Byte volume"] = np.clip(0.3 + 0.1 * np.sin(t * 25) + ramp(0, 0.25, 1.3), 0, 1)
        base["Port diversity"] = np.clip(0.2 + ramp(0, 0.35, 1.4), 0, 1)

    elif scenario == "Mixed attack progression":
        third = n_windows // 3
        mid_len = (2 * third) - third
        tail_len = n_windows - 2 * third

        base["Port diversity"][:third] = np.clip(
            np.linspace(0.2, 0.6, third) + rng.normal(0, 0.02, third), 0, 1
        )
        base["SYN ratio"][:third] = np.clip(np.linspace(0.25, 0.55, third), 0, 1)

        if mid_len > 0:
            base["ACK ratio"][third:2 * third] = np.clip(np.linspace(0.3, 0.75, mid_len), 0, 1)
            base["RST ratio"][third:2 * third] = np.clip(np.linspace(0.25, 0.65, mid_len), 0, 1)

        if tail_len > 0:
            base["Packet volume"][2 * third:] = np.clip(np.linspace(0.4, 0.95, tail_len), 0, 1)
            base["Byte volume"][2 * third:] = np.clip(np.linspace(0.4, 0.9, tail_len), 0, 1)

    df = pd.DataFrame(base)
    df = df[STATE_FEATURES]
    df.insert(0, "window", np.arange(n_windows))
    return df


def raw_risk_from_state(row: pd.Series) -> float:
    """
    Purely illustrative state -> raw risk scoring heuristic, standing in for
    the future "state-space risk scoring" stage (P5) until that module is
    trained/calibrated. NOT a learned function.
    """
    weights = {
        "SYN ratio": 0.18,
        "ACK ratio": 0.05,
        "RST ratio": 0.14,
        "Packet volume": 0.12,
        "Byte volume": 0.10,
        "IAT mean": -0.08,
        "IAT variance": 0.10,
        "Port diversity": 0.22,
        "Bidirectional ratio": -0.05,
    }
    score = sum(row[f] * w for f, w in weights.items())
    return float(np.clip(score + 0.15, 0, 1))


def calibrate(raw_risk: float) -> float:
    """Illustrative sigmoid-style calibration standing in for P5 calibration."""
    x = (raw_risk - 0.5) * 6
    return float(1 / (1 + np.exp(-x)))


def build_forecast_frame(scenario: str, n_windows: int = 60) -> pd.DataFrame:
    state_df = generate_state_timeseries(scenario, n_windows)
    raw = state_df.apply(raw_risk_from_state, axis=1)
    prob = raw.apply(calibrate)
    out = state_df.copy()
    out["raw_risk"] = raw
    out["probability"] = prob
    return out


def predicted_next_state(current_row: pd.Series, scenario: str) -> pd.Series:
    """
    Illustrative S_hat_(t+1): nudges the current state slightly in the
    direction the scenario is trending, standing in for the LSTM's one-step
    prediction until real training is complete.
    """
    rng = _rng(scenario, seed_offset=int(current_row.get("window", 0)) + 1)
    drift = {
        "Benign traffic": 0.0,
        "Port Scan / Reconnaissance": 0.03,
        "Brute Force": 0.025,
        "DoS-like activity": 0.05,
        "C2 Beacon-like activity": 0.015,
        "Mixed attack progression": 0.03,
    }.get(scenario, 0.02)

    next_state = current_row[STATE_FEATURES].copy()
    for f in STATE_FEATURES:
        noise = rng.normal(0, 0.015)
        next_state[f] = float(np.clip(next_state[f] + drift * rng.uniform(0.4, 1.2) + noise, 0, 1))
    return next_state


SHAP_CASE_STUDIES = {
    "Port Scan / Reconnaissance": [
        ("Port diversity", 0.31),
        ("SYN packet ratio", 0.27),
        ("Inter-arrival variance", 0.14),
        ("Destination port entropy", 0.12),
        ("Packet volume", 0.08),
        ("Bidirectional ratio", -0.04),
    ],
    "C2 Beacon-like activity": [
        ("Inter-arrival variance (low)", 0.29),
        ("Byte volume periodicity", 0.24),
        ("IAT mean stability", 0.19),
        ("Port diversity", 0.07),
        ("SYN packet ratio", 0.03),
        ("Bidirectional ratio", -0.06),
    ],
    "Brute Force": [
        ("ACK ratio", 0.28),
        ("RST ratio", 0.24),
        ("Packet volume", 0.17),
        ("Bidirectional ratio", 0.11),
        ("Port diversity", 0.05),
        ("IAT variance", -0.03),
    ],
}

ATTACK_TACTIC_MAP = {
    "Benign traffic": "None",
    "Port Scan / Reconnaissance": "Reconnaissance",
    "Brute Force": "Credential Access",
    "DoS-like activity": "Impact",
    "C2 Beacon-like activity": "Command and Control",
    "Mixed attack progression": "Reconnaissance -> Credential Access -> C2",
}
