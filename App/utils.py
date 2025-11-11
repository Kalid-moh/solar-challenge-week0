import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load local CSV data.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
    """
    df = pd.read_csv(filepath)
    return df

def filter_data(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """
    Filter dataset by selected countries.
    
    Args:
        df: Input DataFrame
        countries: List of country names to filter by
        
    Returns:
        Filtered DataFrame
    """
    if not countries:
        return df
    return df[df['country'].isin(countries)]

def plot_box(df: pd.DataFrame, y_col: str, x_col: str = "country", title: str = "") -> go.Figure:
    """
    Create an enhanced boxplot using Plotly.
    
    Args:
        df: Input DataFrame
        y_col: Column name for y-axis values
        x_col: Column name for x-axis categories (default: "country")
        title: Plot title
        
    Returns:
        Plotly figure object
    """
    # Define a nice color palette
    colors = px.colors.qualitative.Set3
    
    fig = px.box(
        df, 
        x=x_col, 
        y=y_col, 
        color=x_col,
        points="all",  # Show all points
        title=title,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(
        xaxis_title=x_col.title(),
        yaxis_title=y_col,
        template="plotly_white",
        showlegend=False,
        title_font_size=20,
        title_x=0.5,
        hovermode='closest',
        height=500,
        font=dict(size=12)
    )
    
    # Improve hover information
    fig.update_traces(
        marker=dict(size=4, opacity=0.6),
        boxmean='sd'  # Show mean and standard deviation
    )
    
    return fig

def top_regions_table(
    df: pd.DataFrame, 
    region_col: str, 
    metric_col: str, 
    top_n: int = 5
) -> pd.DataFrame:
    """
    Return top regions by average metric with additional statistics.
    
    Args:
        df: Input DataFrame
        region_col: Column name for regions
        metric_col: Column name for the metric to aggregate
        top_n: Number of top regions to return
        
    Returns:
        DataFrame with top regions and their average metrics
    """
    top = (
        df.groupby(region_col)[metric_col]
        .agg(['mean', 'count'])
        .round(2)
        .sort_values('mean', ascending=False)
        .head(top_n)
        .reset_index()
    )
    
    top.columns = ["Region", f"Avg {metric_col}", "Data Points"]
    
    return top

def get_summary_statistics(df: pd.DataFrame, metric_col: str) -> dict:
    """
    Calculate summary statistics for a given metric.
    
    Args:
        df: Input DataFrame
        metric_col: Column name for the metric
        
    Returns:
        Dictionary containing summary statistics
    """
    return {
        'mean': df[metric_col].mean(),
        'median': df[metric_col].median(),
        'std': df[metric_col].std(),
        'min': df[metric_col].min(),
        'max': df[metric_col].max(),
        'count': df[metric_col].count()
    }

def create_comparison_chart(
    df: pd.DataFrame, 
    metric: str, 
    countries: list[str]
) -> go.Figure:
    """
    Create a bar chart comparing average metrics across countries.
    
    Args:
        df: Input DataFrame
        metric: Metric column name
        countries: List of countries to compare
        
    Returns:
        Plotly figure object
    """
    filtered = df[df['country'].isin(countries)]
    avg_by_country = filtered.groupby('country')[metric].mean().sort_values(ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(
            x=avg_by_country.index,
            y=avg_by_country.values,
            marker_color='lightsalmon'
        )
    ])
    
    fig.update_layout(
        title=f"Average {metric} by Country",
        xaxis_title="Country",
        yaxis_title=f"Average {metric}",
        template="plotly_white",
        height=400
    )
    
    return fig