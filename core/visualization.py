# core/visualization.py
# Plotly helpers: generate a few standard charts automatically

import plotly.express as px
import pandas as pd


def generate_top_visuals(df: pd.DataFrame, max_charts: int = 5):
    """
    Returns list of (title, fig) tuples for display.

    Strategy:
    - Numeric columns:
        * Histograms (distributions)
        * Correlation heatmap
        * Time-series trends if a datetime column exists
        * Scatter-matrix (pairplot) for key numeric features
    - Categorical columns:
        * Top value counts
        * Box plots: numeric vs categorical (distribution per category)
    """
    figs = []

    # Basic type splits
    numeric = df.select_dtypes(include="number")
    categorical = df.select_dtypes(include="object")
    datetime_cols = df.select_dtypes(include="datetime64[ns]").columns

    # 1) Numeric histograms for first 3 numeric cols
    for col in numeric.columns[:3]:
        fig = px.histogram(df, x=col, nbins=30, title=f"Distribution — {col}")
        figs.append((f"hist_{col}", fig))
        if len(figs) >= max_charts:
            return figs

    # 2) Correlation heatmap (if enough numeric cols)
    if numeric.shape[1] >= 2:
        corr = numeric.corr()
        fig = px.imshow(corr, text_auto=True, title="Correlation Matrix")
        figs.append(("corr_matrix", fig))
        if len(figs) >= max_charts:
            return figs

    # 3) Time-series trends (if datetime + numeric)
    if len(datetime_cols) and numeric.shape[1]:
        date_col = datetime_cols[0]
        # Sort by date for a proper time axis
        df_sorted = df.sort_values(date_col)
        for col in numeric.columns[:2]:
            fig = px.line(
                df_sorted,
                x=date_col,
                y=col,
                title=f"Trend over time — {col}",
            )
            figs.append((f"trend_{col}", fig))
            if len(figs) >= max_charts:
                return figs

    # 4) Scatter-matrix (pairplot) for key numeric features
    if numeric.shape[1] >= 3:
        cols = numeric.columns[:4]  # limit for readability
        fig = px.scatter_matrix(
            df,
            dimensions=cols,
            title="Scatter Matrix — key numeric features",
        )
        figs.append(("scatter_matrix", fig))
        if len(figs) >= max_charts:
            return figs

    # 5) Categorical top values (bar charts)
    for col in categorical.columns[:3]:
        vc = df[col].value_counts().nlargest(10)
        fig = px.bar(
            x=vc.index.astype(str),
            y=vc.values,
            labels={"x": col, "y": "count"},
            title=f"Top values — {col}",
        )
        figs.append((f"cat_top_{col}", fig))
        if len(figs) >= max_charts:
            return figs

    # 6) Box plots: numeric vs first categorical
    if len(categorical.columns) and numeric.shape[1]:
        cat = categorical.columns[0]
        for col in numeric.columns[:2]:
            fig = px.box(
                df,
                x=cat,
                y=col,
                points="outliers",
                title=f"{col} by {cat}",
            )
            figs.append((f"box_{col}_by_{cat}", fig))
            if len(figs) >= max_charts:
                return figs

    return figs
