# Kenya Retail Sales Dashboard

Interactive Streamlit dashboard for the Open University of Kenya, Module 6 Mini Project.

## Features
- KPI cards (revenue, units, average price, top county)
- Sidebar filters: date range, county, category, trend granularity
- Trend lines, weekday/month heatmap, county bar, category donut, treemap drill-down
- Upload your own CSV (columns: `date, county, category, units, revenue_kes`)
- Download the filtered data as CSV

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (free)
1. Create a GitHub repo and push `app.py`, `requirements.txt` and `README.md`.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, pick the repo, branch `main`, main file `app.py`.
4. Click **Deploy**. After a minute you get a public URL like `https://<your-app>.streamlit.app`.
5. Paste that URL in the Moodle "Online text" submission box.

## One-click run
- **Windows:** double-click `run.bat`
- **macOS/Linux:** `./run.sh`

Both create a `.venv`, install `requirements.txt` and open the dashboard at http://localhost:8501.
Requires Python 3.9+. `sample_upload.csv` is an example file to try the upload feature.
