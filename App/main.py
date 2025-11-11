import streamlit as st
from app.utils import load_data, filter_data, plot_box, top_regions_table

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Solar Insights Dashboard",
    page_icon="☀️",
    layout="wide",
)

st.title("☀️ Solar Energy Insights Dashboard")
st.markdown("An interactive dashboard to explore **Global Horizontal Irradiance (GHI)** and regional solar insights.")

# -----------------------------
# LOAD DATA
# -----------------------------
DATA_PATH = "data/solar_data.csv"  # Example path, ignored by git
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error("⚠️ Data file not found. Please ensure `data/solar_data.csv` exists locally.")
    st.stop()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filter Options")

countries = sorted(df["country"].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select countries to visualize:",
    options=countries,
    default=countries[:3] if countries else []
)

metric = st.sidebar.selectbox(
    "Select metric for visualization:",
    ["GHI", "DNI", "DHI"],  # example columns
    index=0
)

# -----------------------------
# FILTERED DATA
# -----------------------------
filtered_df = filter_data(df, selected_countries)

# -----------------------------
# MAIN DASHBOARD
# -----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Distribution of {metric}")
    fig = plot_box(filtered_df, y_col=metric, title=f"{metric} Distribution by Country")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Regions by Average GHI")
    top_regions = top_regions_table(df, region_col="region", metric_col=metric, top_n=5)
    st.dataframe(top_regions, use_container_width=True)

st.markdown("---")
st.markdown("📈 Built with Streamlit • Interactive • Clean • Ready for Deployment")

