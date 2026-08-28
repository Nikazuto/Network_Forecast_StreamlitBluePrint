# Predictive Cyber Defence — PS-26153 (Streamlit Demonstrator)

AI-Based Network Attack Forecasting from Network Traffic Data
Theme: World Models for Predictive Cyber Defence · NTRO · Smart India Hackathon 2026

## What this is

This is an **interactive system demonstrator**, not a working ML product. The real
LSTM World Model, preprocessing pipeline, SHAP explainability, and ATT&CK mapping
are **not yet trained/implemented** — this app exists to communicate the complete
architecture and intended analyst workflow to judges within 2-3 minutes.

Every simulated value in the UI is clearly labeled **DEMO / SIMULATED / ILLUSTRATIVE**.
Nothing here should be read as a real model output, a real accuracy number, or working
real-time detection.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

No internet connection or GPU is required — the demo data engine (`demo_data/generator.py`)
produces deterministic synthetic time series entirely offline.

## Structure

```
app.py                     Sidebar navigation + page router
utils/theme.py              Design tokens + injected CSS (dark SOC theme)
utils/components.py         Reusable badges, metric cards, pipeline stages, etc.
demo_data/generator.py      Deterministic synthetic data engine (NOT a trained model)
pages_content/page*.py      One module per sidebar page (12 pages)
pages_content/trajectory_simulator.py   Attack Trajectory Simulator (sidebar widget)
pages_content/judge_mode.py             Judge Mode guided tour + 2-Minute Demo script
```

## Honesty conventions used throughout

- `REAL` / `DEMO` / `PLANNED` / `FOUNDATION` / `HEURISTIC` badges appear next to every
  value that could be mistaken for a genuine model output.
- The Executive Dashboard's system banner ("DEMO MODE — MODEL NOT TRAINED") is always visible.
- The Baseline Comparison and Evaluation pages deliberately show "Pending real training"
  instead of inventing metrics.
