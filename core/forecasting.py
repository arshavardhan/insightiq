# core/forecasting.py
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from typing import Tuple

def _ensure_datetime_index(df: pd.DataFrame, date_col: str):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(date_col)
    df = df.set_index(date_col)
    return df

def simple_forecast(df: pd.DataFrame, date_col: str, target_col: str, periods: int = 12, method: str = "holt"):
    """
    Forecast target_col using either 'holt' (ExponentialSmoothing) or 'arima'.
    Returns forecast Series and model diagnostics dict.
    """
    if date_col not in df.columns or target_col not in df.columns:
        return pd.Series(dtype=float), {"error": "date or target column missing"}

    df2 = _ensure_datetime_index(df[[date_col, target_col]], date_col)
    ts = df2[target_col].astype(float).fillna(method="ffill").fillna(method="bfill")

    if len(ts) < 6:
        return pd.Series(dtype=float), {"error": "Not enough history for forecasting"}

    try:
        if method == "holt":
            model = ExponentialSmoothing(ts, trend="add", seasonal=None, initialization_method="estimated")
            fit = model.fit()
            pred = fit.forecast(periods)
            diag = {"method": "holt", "aic": None}
        else:
            # ARIMA simple (p,d,q) auto fallback
            model = ARIMA(ts, order=(1,1,1))
            fit = model.fit()
            pred = fit.predict(start=len(ts), end=len(ts)+periods-1)
            diag = {"method": "arima", "aic": float(getattr(fit, "aic", np.nan))}
        return pd.Series(pred), diag
    except Exception as e:
        return pd.Series(dtype=float), {"error": str(e)}
