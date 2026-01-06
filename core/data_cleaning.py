# core/data_cleaning.py
# Functions for data cleaning and preprocessing.

import pandas as pd
from sklearn.impute import SimpleImputer

def basic_cleaning(df: pd.DataFrame, drop_threshold=0.9, fill_numeric_strategy="mean"):
    """
    - Drop columns with > drop_threshold fraction of missing values
    - Fill numeric missing values with mean/median and categorical with 'Unknown'
    - Drop exact duplicate rows
    Returns cleaned dataframe and a dict with cleaning summary.
    """
    summary = {}
    initial_shape = df.shape
    summary["initial_shape"] = initial_shape

    # Drop columns with too many nulls
    col_null_frac = df.isnull().mean()
    drop_cols = col_null_frac[col_null_frac > drop_threshold].index.tolist()
    df = df.drop(columns=drop_cols)
    summary["dropped_columns"] = drop_cols

    # Drop duplicate rows
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    summary["duplicates_removed"] = int(dup_count)

    # Numeric imputation
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols):
        num_imp = SimpleImputer(strategy=fill_numeric_strategy)
        df[num_cols] = pd.DataFrame(num_imp.fit_transform(df[num_cols]), columns=num_cols)

    # Categorical fill
    cat_cols = df.select_dtypes(include="object").columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")

    summary["final_shape"] = df.shape
    return df, summary
