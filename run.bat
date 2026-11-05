@echo off
REM One-click launcher for Windows: creates a virtual env, installs requirements, runs the dashboard.
cd /d "%~dp0"
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
echo Installing requirements...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo Starting dashboard at http://localhost:8501
streamlit run app.py
pause
