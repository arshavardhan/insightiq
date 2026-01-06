# core/insights_engine.py
# Generate plain-English insights using a local transformer model (Flan-T5-small by default)

from transformers import pipeline
import streamlit as st
import os

@st.cache_resource(show_spinner=False)
def load_model(model_name="google/flan-t5-small"):
    """
    Cached model load so Streamlit doesn't re-download repeatedly.
    """
    return pipeline("text2text-generation", model=model_name, device= -1)  # device=-1 uses CPU

def build_insight_prompt(kpis: dict, sample_rows=None):
    """
    Compose a short prompt describing the dataset and KPIs for the LLM to summarize.
    Keep prompt short to keep inference fast.
    """
    lines = []
    lines.append(f"The dataset has {kpis.get('row_count')} rows and {kpis.get('column_count')} columns.")
    lines.append(f"Overall missing data is {kpis.get('missing_pct_overall')} percent.")
    duplicates = kpis.get("duplicate_rows", 0)
    lines.append(f"Duplicate rows: {duplicates}.")
    # numeric stats
    numeric_stats = kpis.get("numeric_sample_stats", {})
    if numeric_stats:
        for col, stats in numeric_stats.items():
            lines.append(f"Column {col}: mean {round(stats.get('mean',0),3)}, median {round(stats.get('median',0),3)}.")
    if sample_rows is not None:
        lines.append("Here are a few sample rows:")
        # add compact sample rows text
        lines.append(str(sample_rows.head(3).to_dict(orient="records")))
    prompt = "Summarize the following dataset in plain business English and point out possible wins, risks, and anomalies:\n" + "\n".join(lines)
    return prompt

def generate_insights(kpis: dict, sample_rows=None, model_name=None, max_length=120):
    if model_name is None:
        model_name = os.getenv("INSIGHT_MODEL", "google/flan-t5-small")
    nlp = load_model(model_name)
    prompt = build_insight_prompt(kpis, sample_rows)
    out = nlp(prompt, max_length=max_length, do_sample=False)
    text = out[0]["generated_text"]
    return text
