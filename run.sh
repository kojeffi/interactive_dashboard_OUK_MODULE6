#!/usr/bin/env bash
# One-click launcher for macOS/Linux: creates a virtual env, installs requirements, runs the dashboard.
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo "Starting dashboard at http://localhost:8501"
streamlit run app.py
