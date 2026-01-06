# core/kpi_extractor.py
# Extract KPIs and summary stats

import pandas as pd
import numpy as np

def compute_basic_kpis(df: pd.DataFrame) -> dict:
    kpis = {}
    kpis["row_count"] = int(len(df))
    kpis["column_count"] = int(len(df.columns))
    kpis["missing_pct_overall"] = float(round(df.isnull().mean().mean() * 100, 4))
    kpis["duplicate_rows"] = int(df.duplicated().sum())
    kpis["numeric_columns"] = int(len(df.select_dtypes(include="number").columns))
    kpis["categorical_columns"] = int(len(df.select_dtypes(include="object").columns))

    # A few sample numeric KPIs: means of top numeric columns
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        top_cols = numeric.columns[:5].tolist()
        kpis["numeric_sample_stats"] = {c: {"mean": float(np.nanmean(numeric[c])), "median": float(np.nanmedian(numeric[c]))} for c in top_cols}
    else:
        kpis["numeric_sample_stats"] = {}
    return kpis
