import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Kenya Retail Sales Dashboard", page_icon="📊", layout="wide")

REQUIRED = ["date", "county", "category", "units", "revenue_kes"]


@st.cache_data
def make_sample_data(seed: int = 42) -> pd.DataFrame:
    """Simulated daily sales so the dashboard works out of the box."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", "2026-10-31", freq="D")
    counties = {"Nairobi": 1.8, "Mombasa": 1.2, "Kisumu": 0.9, "Nakuru": 1.0, "Eldoret": 0.8, "Kiambu": 1.1}
    cats = {"Electronics": 1500, "Groceries": 400, "Fashion": 800, "Home": 1000, "Health": 600}
    rows = []
    for d in dates:
        season = 1 + 0.25 * np.sin(2 * np.pi * d.day_of_year / 365) + (0.3 if d.month == 12 else 0)
        for c, cw in counties.items():
            for k, price in cats.items():
                units = max(0, int(rng.poisson(12 * cw * season)))
                rows.append((d, c, k, units, units * price * rng.uniform(0.9, 1.1)))
    return pd.DataFrame(rows, columns=REQUIRED)


@st.cache_data
def load_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


st.title("📊 Kenya Retail Sales Dashboard")
st.caption("Interactive analytics built with Streamlit, Pandas and Plotly.")

with st.sidebar:
    st.header("Data")
    up = st.file_uploader("Upload your own CSV", type="csv",
                          help=f"Required columns: {', '.join(REQUIRED)}")
    if up:
        df = load_csv(up)
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            st.error(f"Missing columns: {missing}. Using sample data instead.")
            df = make_sample_data()
        else:
            st.success("Custom data loaded")
    else:
        df = make_sample_data()
        st.info("Using simulated sample data.")

df["date"] = pd.to_datetime(df["date"])

with st.sidebar:
    st.header("Filters")
    dmin, dmax = df["date"].min().date(), df["date"].max().date()
    date_range = st.date_input("Date range", (dmin, dmax), min_value=dmin, max_value=dmax)
    counties = st.multiselect("County", sorted(df["county"].unique()), default=sorted(df["county"].unique()))
    cats = st.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    freq = st.radio("Trend granularity", ["Daily", "Weekly", "Monthly"], index=2)

if len(date_range) != 2:
    st.warning("Select both a start and end date.")
    st.stop()

mask = (
    df["date"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
    & df["county"].isin(counties)
    & df["category"].isin(cats)
)
f = df[mask]
if f.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# KPIs
total_rev = f["revenue_kes"].sum()
total_units = f["units"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total revenue", f"KES {total_rev:,.0f}")
c2.metric("Units sold", f"{total_units:,.0f}")
c3.metric("Avg. price / unit", f"KES {total_rev / max(total_units, 1):,.0f}")
c4.metric("Top county", f.groupby("county")["revenue_kes"].sum().idxmax())

tab1, tab2, tab3 = st.tabs(["Trends", "Breakdown", "Data"])

with tab1:
    rule = {"Daily": "D", "Weekly": "W", "Monthly": "MS"}[freq]
    trend = f.set_index("date").groupby("county")["revenue_kes"].resample(rule).sum().reset_index()
    st.plotly_chart(px.line(trend, x="date", y="revenue_kes", color="county",
                            title=f"{freq} revenue by county", labels={"revenue_kes": "Revenue (KES)"}),
                    width="stretch")
    monthly = f.assign(month=f["date"].dt.month_name(), dow=f["date"].dt.day_name())
    heat = monthly.pivot_table(index="dow", columns="month", values="revenue_kes", aggfunc="sum")
    dows = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat = heat.reindex([d for d in dows if d in heat.index])
    st.plotly_chart(px.imshow(heat, aspect="auto", color_continuous_scale="Blues",
                              title="Revenue heatmap: weekday vs month"), width="stretch")

with tab2:
    a, b = st.columns(2)
    by_county = f.groupby("county", as_index=False)["revenue_kes"].sum().sort_values("revenue_kes")
    a.plotly_chart(px.bar(by_county, x="revenue_kes", y="county", orientation="h",
                          title="Revenue by county"), width="stretch")
    by_cat = f.groupby("category", as_index=False)["revenue_kes"].sum()
    b.plotly_chart(px.pie(by_cat, names="category", values="revenue_kes", hole=0.45,
                          title="Revenue share by category"), width="stretch")
    st.plotly_chart(px.treemap(f, path=["county", "category"], values="revenue_kes",
                               title="County → category drill-down"), width="stretch")

with tab3:
    st.dataframe(f.sort_values("date", ascending=False), width="stretch", hide_index=True)
    st.download_button("Download filtered data (CSV)", f.to_csv(index=False).encode(),
                       "filtered_sales.csv", "text/csv")

st.divider()
st.caption("Open University of Kenya · Module 6 Mini Project")
