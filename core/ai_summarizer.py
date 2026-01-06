# core/ai_summarizer.py
from transformers import pipeline
import streamlit as st
import os
import pandas as pd

@st.cache_resource(show_spinner=False)
def load_summarizer(model_name: str = None):
    """
    Load Flan-T5 or other text2text model. CPU by default (device=-1).
    """
    if model_name is None:
        model_name = os.getenv("INSIGHT_MODEL", "google/flan-t5-small")
    return pipeline("text2text-generation", model=model_name, device=-1)

def build_summarizer_prompt(kpis: dict, sample_rows: pd.DataFrame = None, max_cols=6, max_rows=10):
    """
    Make a compact prompt summarizing KPIs and a small sample of rows.
    Truncates wide tables to avoid long sequences.
    """
    lines = []
    lines.append(f"Dataset summary: {kpis.get('row_count', '?')} rows, {kpis.get('column_count', '?')} columns.")
    lines.append(f"Missing % overall: {kpis.get('missing_pct_overall', '?'):.4f}")
    lines.append(f"Duplicates: {kpis.get('duplicate_rows', 0)}.")
    numeric_sample = kpis.get("numeric_sample_stats", {})
    if numeric_sample:
        for col, stats in list(numeric_sample.items())[:3]:
            lines.append(f"{col} mean {stats.get('mean',0):.2f}, median {stats.get('median',0):.2f}.")
    if sample_rows is not None and not sample_rows.empty:
        small = sample_rows.iloc[:max_rows, :max_cols]
        lines.append("Sample rows (truncated):")
        # convert to short tabular text
        lines.append(small.to_csv(index=False, line_terminator=" | ", header=True))
    prompt = (
        "You are a helpful data analyst. Summarize the dataset in plain business English, "
        "mention obvious trends, potential anomalies, and one or two recommendations:\n\n"
        + "\n".join(lines)
    )
    return prompt

def generate_summary(kpis: dict, sample_rows: pd.DataFrame = None, model_name: str = None, max_length: int = 120):
    """
    Generate human-readable summary using local model.
    Keep sample_rows small to avoid token length errors.
    """
    model = load_summarizer(model_name)
    prompt = build_summarizer_prompt(kpis, sample_rows=sample_rows)
    # Ensure we don't exceed token limits by limiting prompt length (heuristic)
    if len(prompt) > 2000:
        prompt = prompt[:2000] + "\n\n[truncated input]"
    out = model(prompt, max_new_tokens=150, do_sample=False)
    text = out[0].get("generated_text") or out[0].get("summary_text") or str(out[0])
    return text
