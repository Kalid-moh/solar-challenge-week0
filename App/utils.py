import pandas as pd
import plotly.express as px

def load_data(filepath: str) -> pd.DataFrame:
    """Load local CSV data."""
    return pd.read_csv(filepath)

def filter_data(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """Filter dataset by selected countries."""
    if not countries:
        return df
    return df[df['country'].isin(countries)]

def plot_box(df: pd.DataFrame, y_col: str, x_col: str = "country", title: str = ""):
    """Create a boxplot using Plotly."""
    fig = px.box(df, x=x_col, y=y_col, color=x_col, points="all", title=title)
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title=y_col,
        template="plotly_white",
        showlegend=False
    )
    return fig

def top_regions_table(df: pd.DataFrame, region_col: str, metric_col: str, top_n: int = 5) -> pd.DataFrame:
    """Return top regions by average metric."""
    top = (
        df.groupby(region_col)[metric_col]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    top.columns = ["Region", f"Avg {metric_col}"]
    return top
