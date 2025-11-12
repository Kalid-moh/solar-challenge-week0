import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* DataFrame styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        border-radius: 10px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<p class="main-header">☀️ Solar Energy Insights Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive visualization and analysis of solar irradiance data across the globe 🌍</p>', unsafe_allow_html=True)

# -----------------------------
# DATA LOADING
# -----------------------------
@st.cache_data(show_spinner=False)
def get_data(path):
    """Load and cache data for better performance."""
    return load_data(path)

# Check if running locally or deployed
DATA_PATH = "data/solar_data.csv"

with st.spinner("🔄 Loading data..."):
    if not os.path.exists(DATA_PATH):
        st.info("📤 **Upload Mode**: Please upload your solar data CSV file to begin.")
        uploaded_file = st.file_uploader(
            "Upload solar_data.csv", 
            type="csv",
            help="Upload a CSV file containing solar irradiance data"
        )
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Successfully loaded **{len(df):,}** records!")
        else:
            st.warning("⚠️ Waiting for data upload...")
            st.markdown("""
                **Expected CSV columns:**
                - `country`: Country name
                - `region`: Region/location name
                - `GHI`: Global Horizontal Irradiance
                - `DNI`: Direct Normal Irradiance (optional)
                - `DHI`: Diffuse Horizontal Irradiance (optional)
                - Other solar metrics...
            """)
            st.stop()
    else:
        # Local development - load from file
        try:
            df = get_data(DATA_PATH)
            st.success(f"✅ Successfully loaded **{len(df):,}** records from the dataset!")
        except FileNotFoundError:
            st.error("⚠️ **Data file not found!** Please ensure `data/solar_data.csv` exists locally.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.stop()

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='color: #FF6B35;'>🎛️ Control Panel</h1>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Section 1: Geographic Filters
with st.sidebar.expander("🌍 **Geographic Filters**", expanded=True):
    countries = sorted(df["country"].unique().tolist()) if "country" in df.columns else []
    
    if countries:
        select_all = st.checkbox("Select All Countries", value=False, key="select_all")
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect(
                "Choose countries:",
                options=countries,
                default=countries[:3] if len(countries) >= 3 else countries,
                help="Select one or more countries to analyze"
            )
    else:
        st.warning("No 'country' column found in data")
        selected_countries = []

# Section 2: Metric Selection
with st.sidebar.expander("📊 **Metric Configuration**", expanded=True):
    available_metrics = ["GHI", "DNI", "DHI", "Tamb", "TModA", "TModB"]
    available_metrics = [m for m in available_metrics if m in df.columns]
    
    if not available_metrics:
        st.warning("No standard metrics found in data")
        available_metrics = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if available_metrics:
        metric = st.selectbox(
            "Primary Metric:",
            available_metrics,
            index=0,
            help="Choose the main metric for visualization"
        )
        
        # Add comparison metric option
        compare_metrics = st.checkbox("Compare Multiple Metrics", value=False)
        if compare_metrics:
            secondary_metric = st.selectbox(
                "Secondary Metric:",
                [m for m in available_metrics if m != metric],
                help="Choose a second metric for comparison"
            )
    else:
        st.error("No numeric columns found!")
        st.stop()

# Section 3: Visualization Options
with st.sidebar.expander("🎨 **Visualization Settings**", expanded=True):
    chart_type = st.radio(
        "Chart Type:",
        ["Box Plot", "Violin Plot", "Scatter Plot", "Time Series"],
        help="Select visualization type"
    )
    
    show_outliers = st.checkbox("Show Outliers", value=True)
    color_scheme = st.selectbox(
        "Color Scheme:",
        ["Plotly", "Viridis", "Plasma", "Inferno", "Turbo"],
        help="Choose color palette"
    )

# Section 4: Analysis Options
with st.sidebar.expander("🔍 **Analysis Options**", expanded=False):
    top_n = st.slider(
        "Top Regions to Show:",
        min_value=3,
        max_value=20,
        value=5,
        step=1,
        help="Number of top-performing regions"
    )
    
    show_statistics = st.checkbox("Show Detailed Statistics", value=True)
    show_raw_data = st.checkbox("Enable Data Table", value=False)
    enable_download = st.checkbox("Enable Data Export", value=True)

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>💡 <strong>Pro Tip:</strong> Use filters to focus on specific regions and metrics</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# FILTER DATA
# -----------------------------
if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar to begin analysis.")
    st.stop()

filtered_df = filter_data(df, selected_countries)

if len(filtered_df) == 0:
    st.error("❌ No data available for selected filters. Please adjust your selection.")
    st.stop()

# -----------------------------
# KEY METRICS SECTION
# -----------------------------
if show_statistics:
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🌍 Countries",
            value=len(selected_countries),
            delta=f"{len(selected_countries)/len(countries)*100:.0f}% selected" if countries else None
        )
    
    with col2:
        st.metric(
            label="📊 Total Records",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df)/len(df)*100:.1f}% of dataset"
        )
    
    with col3:
        avg_value = filtered_df[metric].mean()
        global_avg = df[metric].mean()
        delta_pct = ((avg_value - global_avg) / global_avg * 100)
        st.metric(
            label=f"🔆 Avg {metric}",
            value=f"{avg_value:.2f}",
            delta=f"{delta_pct:+.1f}% vs global"
        )
    
    with col4:
        max_value = filtered_df[metric].max()
        st.metric(
            label=f"⚡ Max {metric}",
            value=f"{max_value:.2f}",
            delta=f"σ = {filtered_df[metric].std():.2f}"
        )
    
    with col5:
        min_value = filtered_df[metric].min()
        range_value = max_value - min_value
        st.metric(
            label=f"📉 Min {metric}",
            value=f"{min_value:.2f}",
            delta=f"Range: {range_value:.2f}"
        )

st.markdown("---")

# -----------------------------
# MAIN VISUALIZATION TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribution Analysis",
    "🗺️ Geographic Insights",
    "🏆 Top Performers",
    "📋 Data Explorer",
    "📈 Advanced Analytics"
])

# TAB 1: Distribution Analysis
with tab1:
    st.markdown(f"### Distribution of {metric} by Country")
    st.markdown(f"*Analyzing {len(filtered_df):,} data points across {len(selected_countries)} countries*")
    
    col_main, col_info = st.columns([3, 1])
    
    with col_main:
        if chart_type == "Box Plot":
            fig = plot_box(filtered_df, y_col=metric, title=f"{metric} Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Violin Plot":
            fig = px.violin(
                filtered_df,
                x="country",
                y=metric,
                color="country",
                box=True,
                points="all" if show_outliers else False,
                title=f"{metric} Distribution (Violin Plot)"
            )
            fig.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Scatter Plot":
            if compare_metrics and 'secondary_metric' in locals():
                fig = px.scatter(
                    filtered_df,
                    x=metric,
                    y=secondary_metric,
                    color="country",
                    title=f"{metric} vs {secondary_metric}",
                    trendline="ols"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Enable 'Compare Multiple Metrics' in sidebar for scatter plot")
        
        elif chart_type == "Time Series":
            if 'Timestamp' in filtered_df.columns or 'timestamp' in filtered_df.columns:
                time_col = 'Timestamp' if 'Timestamp' in filtered_df.columns else 'timestamp'
                fig = px.line(
                    filtered_df,
                    x=time_col,
                    y=metric,
                    color="country",
                    title=f"{metric} Over Time"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No timestamp column found in dataset")
    
    with col_info:
        st.markdown("#### 📊 Statistics")
        stats_df = pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Range'],
            'Value': [
                f"{filtered_df[metric].mean():.2f}",
                f"{filtered_df[metric].median():.2f}",
                f"{filtered_df[metric].std():.2f}",
                f"{filtered_df[metric].min():.2f}",
                f"{filtered_df[metric].max():.2f}",
                f"{filtered_df[metric].max() - filtered_df[metric].min():.2f}"
            ]
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        st.markdown("#### ℹ️ Chart Guide")
        if chart_type == "Box Plot":
            st.markdown("""
            - **Box**: 25th to 75th percentile
            - **Line**: Median value
            - **Whiskers**: Data range
            - **Points**: Individual values
            """)
        elif chart_type == "Violin Plot":
            st.markdown("""
            - **Width**: Data density
            - **Box**: Quartile range
            - **Thick line**: Median
            """)

# TAB 2: Geographic Insights
with tab2:
    st.markdown("### 🗺️ Geographic Analysis")
    
    col_map, col_bar = st.columns([2, 1])
    
    with col_map:
        # Create choropleth if coordinates available
        if all(col in filtered_df.columns for col in ['country', metric]):
            country_avg = filtered_df.groupby('country')[metric].mean().reset_index()
            
            fig = px.choropleth(
                country_avg,
                locations='country',
                locationmode='country names',
                color=metric,
                title=f"Global Distribution of {metric}",
                color_continuous_scale=color_scheme,
                labels={metric: f'Avg {metric}'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Geographic coordinates not available for map visualization")
    
    with col_bar:
        st.markdown("#### Country Rankings")
        country_ranking = filtered_df.groupby('country')[metric].mean().sort_values(ascending=False)
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=country_ranking.values,
                y=country_ranking.index,
                orientation='h',
                marker_color='lightblue'
            )
        ])
        fig_bar.update_layout(
            title=f"Average {metric} by Country",
            xaxis_title=f"Avg {metric}",
            yaxis_title="Country",
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# TAB 3: Top Performers
with tab3:
    st.markdown(f"### 🏆 Top {top_n} Performing Regions")
    
    if "region" in df.columns:
        col_table, col_chart = st.columns([2, 1])
        
        with col_table:
            top_regions = top_regions_table(df, region_col="region", metric_col=metric, top_n=top_n)
            
            # Add ranking column
            top_regions.insert(0, 'Rank', range(1, len(top_regions) + 1))
            
            # Style the dataframe
            st.dataframe(
                top_regions,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn("🏅 Rank", width="small"),
                    "Region": st.column_config.TextColumn("Region", width="medium"),
                    f"Avg {metric}": st.column_config.NumberColumn(
                        f"Avg {metric}",
                        format="%.2f",
                        width="medium"
                    )
                }
            )
        
        with col_chart:
            st.markdown("#### 💡 Key Insights")
            
            if len(top_regions) > 0:
                best_region = top_regions.iloc[0]["Region"]
                best_value = top_regions.iloc[0][f"Avg {metric}"]
                
                st.success(f"**🥇 Top Region**\n\n{best_region}")
                st.metric("Performance", f"{best_value:.2f}")
                
                if len(top_regions) > 1:
                    second_value = top_regions.iloc[1][f"Avg {metric}"]
                    diff = best_value - second_value
                    diff_pct = (diff / second_value) * 100
                    
                    st.info(f"**Lead over 2nd place:**\n\n{diff:.2f} ({diff_pct:.1f}%)")
                
                # Quick visualization
                fig_top = px.bar(
                    top_regions,
                    x=f"Avg {metric}",
                    y="Region",
                    orientation='h',
                    title="Top Performers",
                    color=f"Avg {metric}",
                    color_continuous_scale="Viridis"
                )
                fig_top.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.warning("⚠️ 'region' column not found in dataset")

# TAB 4: Data Explorer
with tab4:
    st.markdown("### 📋 Interactive Data Explorer")
    
    if show_raw_data:
        # Search and filter controls
        col_search, col_filter = st.columns([3, 1])
        
        with col_search:
            search_term = st.text_input(
                "🔍 Search in data:",
                placeholder="Enter search term...",
                help="Search across all columns"
            )
        
        with col_filter:
            sort_column = st.selectbox(
                "Sort by:",
                options=filtered_df.columns.tolist(),
                index=list(filtered_df.columns).index(metric) if metric in filtered_df.columns else 0
            )
        
        # Apply search filter
        if search_term:
            mask = filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            display_df = filtered_df[mask].sort_values(by=sort_column, ascending=False)
            st.info(f"Found **{len(display_df)}** matching records")
        else:
            display_df = filtered_df.sort_values(by=sort_column, ascending=False)
        
        st.markdown(f"Displaying **{len(display_df):,}** records")
        
        # Display dataframe with pagination
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Download options
        if enable_download:
            col_csv, col_json = st.columns(2)
            
            with col_csv:
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"solar_data_{metric}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_json:
                json_data = display_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name=f"solar_data_{metric}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    else:
        st.info("👆 Enable 'Enable Data Table' in the sidebar to explore the full dataset")
        st.markdown("**Quick Preview (First 10 rows):**")
        st.dataframe(filtered_df.head(10), use_container_width=True)

# TAB 5: Advanced Analytics
with tab5:
    st.markdown("### 📈 Advanced Statistical Analysis")
    
    col_corr, col_dist = st.columns(2)
    
    with col_corr:
        st.markdown("#### Correlation Matrix")
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) > 1:
            corr_matrix = filtered_df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Feature Correlations"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Not enough numeric columns for correlation analysis")
    
    with col_dist:
        st.markdown("#### Distribution Analysis")
        
        fig_hist = px.histogram(
            filtered_df,
            x=metric,
            nbins=50,
            title=f"Distribution of {metric}",
            marginal="box",
            color_discrete_sequence=['#FFA500']
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Additional insights
    st.markdown("---")
    st.markdown("#### 📊 Summary Statistics by Country")
    
    summary_stats = filtered_df.groupby('country')[metric].agg([
        ('Count', 'count'),
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2).reset_index()
    
    st.dataframe(summary_stats, use_container_width=True, hide_index=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <h3 style='color: white; margin: 0;'>☀️ Solar Energy Insights Dashboard</h3>
        <p style='color: white; margin: 0.5rem 0;'>Built with Streamlit | Powered by Plotly</p>
        <p style='color: white; font-size: 0.9rem; margin: 0;'>
            Interactive • Responsive • Production-Ready
        </p>
    </div>
""", unsafe_allow_html=True)