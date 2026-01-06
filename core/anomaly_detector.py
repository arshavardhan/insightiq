# core/anomaly_detector.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(df: pd.DataFrame, numeric_only: bool = True, n_estimators: int = 100, contamination: float = 0.01):
    """
    Run IsolationForest on numeric features and return:
      - anomalies: DataFrame with anomaly score and flag
      - summary: dict with counts
    """
    numeric = df.select_dtypes(include="number")
    if numeric_only and numeric.shape[1] == 0:
        return pd.DataFrame(), {"message": "No numeric columns for anomaly detection."}

    # Fill NaNs (simple)
    X = numeric.fillna(numeric.median())
    # scale
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    iso = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)
    iso.fit(Xs)
    scores = iso.decision_function(Xs)  # higher is normal, lower is anomaly
    preds = iso.predict(Xs)  # -1 anomaly, 1 normal

    out = df.copy()
    out["_anomaly_score"] = scores
    out["_anomaly_flag"] = (preds == -1)

    summary = {
        "total_rows": len(df),
        "anomaly_count": int((out["_anomaly_flag"]).sum()),
        "anomaly_fraction": float((out["_anomaly_flag"]).mean())
    }
    return out, summary
