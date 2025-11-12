import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load local CSV data with error handling.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """
    try:
        df = pd.read_csv(filepath)
        
        # Basic data validation
        if df.empty:
            raise ValueError("Loaded data is empty")
        
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {filepath}")
    except pd.errors.EmptyDataError:
        raise ValueError("Data file is empty")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def filter_data(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """
    Filter dataset by selected countries with validation.
    
    Args:
        df: Input DataFrame
        countries: List of country names to filter by
        
    Returns:
        Filtered DataFrame
    """
    if not countries:
        return df
    
    if 'country' not in df.columns:
        return df
    
    return df[df['country'].isin(countries)]

def plot_box(
    df: pd.DataFrame, 
    y_col: str, 
    x_col: str = "country", 
    title: str = ""
) -> go.Figure:
    """
    Create an enhanced boxplot using Plotly with custom styling.
    
    Args:
        df: Input DataFrame
        y_col: Column name for y-axis values
        x_col: Column name for x-axis categories (default: "country")
        title: Plot title
        
    Returns:
        Plotly figure object
    """
    # Color palette
    colors = px.colors.qualitative.Set3
    
    fig = px.box(
        df, 
        x=x_col, 
        y=y_col, 
        color=x_col,
        points="all",
        title=title,
        color_discrete_sequence=colors,
        hover_data=df.columns
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
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    fig.update_traces(
        marker=dict(size=5, opacity=0.7, line=dict(width=1, color='white')),
        boxmean='sd'
    )
    
    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
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
        DataFrame with top regions and their statistics
    """
    if region_col not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    
    top = (
        df.groupby(region_col)[metric_col]
        .agg(['mean', 'count', 'std'])
        .round(2)
        .sort_values('mean', ascending=False)
        .head(top_n)
        .reset_index()
    )
    
    top.columns = ["Region", f"Avg {metric_col}", "Data Points", "Std Dev"]
    
    return top

def get_summary_statistics(df: pd.DataFrame, metric_col: str) -> dict:
    """
    Calculate comprehensive summary statistics for a metric.
    
    Args:
        df: Input DataFrame
        metric_col: Column name for the metric
        
    Returns:
        Dictionary containing summary statistics
    """
    if metric_col not in df.columns:
        return {}
    
    data = df[metric_col].dropna()
    
    return {
        'mean': data.mean(),
        'median': data.median(),
        'mode': data.mode()[0] if len(data.mode()) > 0 else None,
        'std': data.std(),
        'variance': data.var(),
        'min': data.min(),
        'max': data.max(),
        'range': data.max() - data.min(),
        'q1': data.quantile(0.25),
        'q3': data.quantile(0.75),
        'iqr': data.quantile(0.75) - data.quantile(0.25),
        'count': data.count(),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis()
    }

def create_comparison_chart(
    df: pd.DataFrame, 
    metric: str, 
    countries: list[str],
    chart_type: str = 'bar'
) -> go.Figure:
    """
    Create comparison charts across countries.
    
    Args:
        df: Input DataFrame
        metric: Metric column name
        countries: List of countries to compare
        chart_type: Type of chart ('bar', 'line', 'area')
        
    Returns:
        Plotly figure object
    """
    filtered = df[df['country'].isin(countries)]
    avg_by_country = filtered.groupby('country')[metric].mean().sort_values(ascending=False)
    
    if chart_type == 'bar':
        fig = go.Figure(data=[
            go.Bar(
                x=avg_by_country.index,
                y=avg_by_country.values,
                marker_color='lightsalmon',
                text=avg_by_country.values.round(2),
                textposition='auto',
            )
        ])
    elif chart_type == 'line':
        fig = go.Figure(data=[
            go.Scatter(
                x=avg_by_country.index,
                y=avg_by_country.values,
                mode='lines+markers',
                line=dict(color='royalblue', width=3),
                marker=dict(size=10)
            )
        ])
    else:  # area
        fig = go.Figure(data=[
            go.Scatter(
                x=avg_by_country.index,
                y=avg_by_country.values,
                fill='tozeroy',
                mode='lines',
                line=dict(color='seagreen')
            )
        ])
    
    fig.update_layout(
        title=f"Average {metric} by Country",
        xaxis_title="Country",
        yaxis_title=f"Average {metric}",
        template="plotly_white",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_correlation_heatmap(df: pd.DataFrame, columns: list = None) -> go.Figure:
    """
    Create correlation heatmap for numeric columns.
    
    Args:
        df: Input DataFrame
        columns: List of columns to include (None for all numeric)
        
    Returns:
        Plotly figure object
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    corr_matrix = df[columns].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Correlation Matrix",
        labels=dict(color="Correlation")
    )
    
    fig.update_layout(
        width=600,
        height=600
    )
    
    return fig

def create_time_series_plot(
    df: pd.DataFrame,
    time_col: str,
    metric_col: str,
    group_col: str = None,
    title: str = ""
) -> go.Figure:
    """
    Create time series visualization.
    
    Args:
        df: Input DataFrame
        time_col: Column name for time/date
        metric_col: Column name for metric values
        group_col: Optional column for grouping (e.g., country)
        title: Plot title
        
    Returns:
        Plotly figure object
    """
    if group_col:
        fig = px.line(
            df,
            x=time_col,
            y=metric_col,
            color=group_col,
            title=title or f"{metric_col} Over Time",
            markers=True
        )
    else:
        fig = px.line(
            df,
            x=time_col,
            y=metric_col,
            title=title or f"{metric_col} Over Time",
            markers=True
        )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=metric_col,
        template="plotly_white",
        height=500,
        hovermode='x unified'
    )
    
    return fig

def calculate_percentile_ranks(df: pd.DataFrame, metric_col: str) -> pd.DataFrame:
    """
    Calculate percentile ranks for a metric.
    
    Args:
        df: Input DataFrame
        metric_col: Column name for the metric
        
    Returns:
        DataFrame with added percentile rank column
    """
    df_copy = df.copy()
    df_copy[f'{metric_col}_percentile'] = df_copy[metric_col].rank(pct=True) * 100
    return df_copy

def detect_outliers(df: pd.DataFrame, metric_col: str, method: str = 'iqr') -> pd.DataFrame:
    """
    Detect outliers using IQR or Z-score method.
    
    Args:
        df: Input DataFrame
        metric_col: Column name for the metric
        method: 'iqr' or 'zscore'
        
    Returns:
        DataFrame with outlier indicator column
    """
    df_copy = df.copy()
    
    if method == 'iqr':
        Q1 = df[metric_col].quantile(0.25)
        Q3 = df[metric_col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_copy['is_outlier'] = (df[metric_col] < lower_bound) | (df[metric_col] > upper_bound)
    else:  # zscore
        z_scores = np.abs((df[metric_col] - df[metric_col].mean()) / df[metric_col].std())
        df_copy['is_outlier'] = z_scores > 3
    
    return df_copy

def create_distribution_plot(
    df: pd.DataFrame,
    metric_col: str,
    bins: int = 30
) -> go.Figure:
    """
    Create histogram with distribution curve.
    
    Args:
        df: Input DataFrame
        metric_col: Column name for the metric
        bins: Number of histogram bins
        
    Returns:
        Plotly figure object
    """
    fig = px.histogram(
        df,
        x=metric_col,
        nbins=bins,
        title=f"Distribution of {metric_col}",
        marginal="box",
        histnorm='probability density'
    )
    
    # Add normal distribution curve
    mean = df[metric_col].mean()
    std = df[metric_col].std()
    x_range = np.linspace(df[metric_col].min(), df[metric_col].max(), 100)
    normal_dist = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mean) / std) ** 2)
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=normal_dist,
        mode='lines',
        name='Normal Distribution',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        template="plotly_white",
        height=500,
        showlegend=True
    )
    
    return fig