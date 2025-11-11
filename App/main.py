import streamlit as st
import pandas as pd
from utils import load_data, filter_data, plot_box, top_regions_table

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Solar Insights Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="main-header">☀️ Solar Energy Insights Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive visualization of Global Horizontal Irradiance (GHI) and solar metrics worldwide</p>', unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
DATA_PATH = "data/benin.csv"

@st.cache_data
def get_data(path):
    """Load and cache data for better performance."""
    return load_data(path)

try:
    df = get_data(DATA_PATH)
    st.success(f"✅ Successfully loaded {len(df):,} records from the dataset!")
except FileNotFoundError:
    st.error("⚠️ **Data file not found!** Please ensure `data/solar_data.csv` exists locally.")
    st.info("📁 Expected path: `data/solar_data.csv`")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=100)
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")

# Country Selection
st.sidebar.subheader("🌍 Country Selection")
countries = sorted(df["country"].unique().tolist())

select_all = st.sidebar.checkbox("Select All Countries", value=False)

if select_all:
    selected_countries = countries
else:
    selected_countries = st.sidebar.multiselect(
        "Choose countries to analyze:",
        options=countries,
        default=countries[:3] if len(countries) >= 3 else countries,
        help="Select one or more countries to visualize"
    )

# Metric Selection
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Metric Selection")
available_metrics = ["GHI", "DNI", "DHI", "Tamb", "ModA", "ModB"]
# Filter to only include metrics that exist in the dataframe
available_metrics = [m for m in available_metrics if m in df.columns]

if not available_metrics:
    st.error("No valid metrics found in the dataset!")
    st.stop()

metric = st.sidebar.selectbox(
    "Select metric for visualization:",
    available_metrics,
    index=0,
    help="Choose the solar metric to analyze"
)

# Top N Selection
st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Top Regions")
top_n = st.sidebar.slider(
    "Number of top regions to display:",
    min_value=3,
    max_value=15,
    value=5,
    step=1,
    help="Select how many top regions to show in the table"
)

# Display Options
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Display Options")
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=False)
show_statistics = st.sidebar.checkbox("Show Statistics", value=True)

# -----------------------------
# FILTER DATA
# -----------------------------
if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar.")
    st.stop()

filtered_df = filter_data(df, selected_countries)

# -----------------------------
# SUMMARY METRICS
# -----------------------------
if show_statistics:
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Countries Selected",
            value=len(selected_countries),
            delta=f"{len(selected_countries)/len(countries)*100:.1f}% of total"
        )
    
    with col2:
        st.metric(
            label="Total Records",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df)/len(df)*100:.1f}% of dataset"
        )
    
    with col3:
        avg_value = filtered_df[metric].mean()
        st.metric(
            label=f"Avg {metric}",
            value=f"{avg_value:.2f}",
            delta=f"±{filtered_df[metric].std():.2f}"
        )
    
    with col4:
        max_value = filtered_df[metric].max()
        st.metric(
            label=f"Max {metric}",
            value=f"{max_value:.2f}"
        )

st.markdown("---")

# -----------------------------
# MAIN VISUALIZATIONS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📊 Distribution Analysis", "🏆 Top Regions", "📋 Data Table"])

with tab1:
    st.subheader(f"Distribution of {metric} by Country")
    st.markdown(f"This boxplot shows the distribution of **{metric}** values across selected countries, including outliers.")
    
    if len(filtered_df) > 0:
        fig = plot_box(filtered_df, y_col=metric, title=f"{metric} Distribution by Country")
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        with st.expander("ℹ️ Understanding the Boxplot"):
            st.markdown("""
            - **Box**: Shows the interquartile range (25th to 75th percentile)
            - **Line in box**: Represents the median value
            - **Whiskers**: Extend to show the range of the data
            - **Points**: Individual data points (all shown for detailed analysis)
            """)
    else:
        st.warning("No data available for the selected countries.")

with tab2:
    st.subheader(f"Top {top_n} Regions by Average {metric}")
    
    if "region" in df.columns:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            top_regions = top_regions_table(df, region_col="region", metric_col=metric, top_n=top_n)
            st.dataframe(
                top_regions,
                use_container_width=True,
                hide_index=True
            )
        
        with col_right:
            st.markdown("### 💡 Insights")
            if len(top_regions) > 0:
                best_region = top_regions.iloc[0]["Region"]
                best_value = top_regions.iloc[0][f"Avg {metric}"]
                st.info(f"**Best Region**: {best_region}")
                st.success(f"**Avg {metric}**: {best_value:.2f}")
                
                if len(top_regions) > 1:
                    diff = top_regions.iloc[0][f"Avg {metric}"] - top_regions.iloc[1][f"Avg {metric}"]
                    st.metric(
                        "Lead over 2nd place",
                        f"{diff:.2f}",
                        delta=f"{diff/top_regions.iloc[1][f'Avg {metric}']*100:.1f}%"
                    )
    else:
        st.warning("⚠️ 'region' column not found in the dataset. Cannot display top regions.")

with tab3:
    st.subheader("📋 Filtered Dataset")
    
    if show_raw_data:
        st.markdown(f"Showing **{len(filtered_df):,}** records for selected countries")
        
        # Add search functionality
        search_term = st.text_input("🔍 Search in data:", "")
        
        if search_term:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            display_df = filtered_df[mask]
            st.markdown(f"Found **{len(display_df)}** matching records")
        else:
            display_df = filtered_df
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"solar_data_filtered_{metric}.csv",
            mime="text/csv",
        )
    else:
        st.info("👆 Enable 'Show Raw Data' in the sidebar to view the dataset")
        st.markdown("**Preview (first 5 rows):**")
        st.dataframe(filtered_df.head(), use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📊 Total Countries in Dataset**")
    st.markdown(f"**{len(countries)}** countries available")

with col2:
    st.markdown("**🌍 Selected Countries**")
    st.markdown(f"**{len(selected_countries)}** currently analyzed")

with col3:
    st.markdown("**📈 Current Metric**")
    st.markdown(f"**{metric}** visualization")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>☀️ <strong>Solar Energy Insights Dashboard</strong> | Built with Streamlit</p>
        <p style='font-size: 0.8rem;'>Interactive • Clean • Production-Ready</p>
    </div>
""", unsafe_allow_html=True)