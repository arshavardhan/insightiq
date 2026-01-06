# core/clustering.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def run_kmeans(df: pd.DataFrame, n_clusters: int = 3, numeric_only: bool = True, use_pca: bool = True, pca_components: int = 5):
    """
    Performs KMeans on numeric columns. Returns dataframe with cluster labels and a summary dict.
    """
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] == 0:
        return pd.DataFrame(), {"message": "No numeric columns for clustering."}

    X = numeric.fillna(numeric.median())
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    if use_pca and Xs.shape[1] > pca_components:
        pca = PCA(n_components=min(pca_components, Xs.shape[1]), random_state=42)
        Xp = pca.fit_transform(Xs)
    else:
        Xp = Xs

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(Xp)

    out = df.copy()
    out["_cluster"] = labels

    # cluster centers (in original scaled space approx)
    centers = None
    try:
        if hasattr(kmeans, "cluster_centers_"):
            centers = kmeans.cluster_centers_.tolist()
    except Exception:
        centers = None

    summary = {
        "n_clusters": int(n_clusters),
        "counts": out["_cluster"].value_counts().to_dict(),
        "centers": centers
    }
    return out, summary
