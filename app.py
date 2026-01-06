# app.py
# Streamlit front-end and orchestrator for InsightIQ

import streamlit as st
from core.pipeline_manager import PipelineManager  # Ensure core/__init__.py exists
from services.logger import get_logger
import yaml
from pathlib import Path

# --- Load config ---
CONFIG_PATH = Path("config.yaml")
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

# --- Setup logger ---
logger = get_logger()

st.set_page_config(page_title="InsightIQ", layout="wide")
st.title("🔎 InsightIQ — Automated Business Intelligence Pipeline")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.write(f"Mode: {config.get('app', {}).get('mode','local')}")
max_file_mb = config.get("app", {}).get("max_file_size_mb", 100)

# File upload
uploaded_file = st.file_uploader("Upload CSV/XLSX dataset", type=["csv", "xlsx"])
pm = PipelineManager(config=config)

if uploaded_file:
    try:
        with st.spinner("Loading dataset..."):
            df = pm.load_dataset(uploaded_file)
            st.success(f"Loaded dataset — {len(df):,} rows × {len(df.columns):,} columns")
            st.write("### Raw data sample")
            st.dataframe(df.head(250))

        if st.button("Run Full Analysis"):
            with st.spinner("Running full pipeline..."):
                result = pm.run_full_pipeline(df)
            st.success("Analysis complete ✅")

            st.write("### Key Performance Indicators (KPIs)")
            st.json(result["kpis"])
#if result.get("profile_html"):
#st.write("### Profiling Report")
#st.components.v1.html(result["profile_html"], height=600, scrolling=True)

            st.write("### AI Generated Insights")
            st.write(result.get("insights", "No insights generated."))

            st.write("### Visualizations")
            for _, fig in result.get("figures", []):
                st.plotly_chart(fig, use_container_width=True)

            report_path = result.get("report_path")
            if report_path:
                with open(report_path, "rb") as f:
                    st.download_button("Download PDF Report", data=f, file_name=Path(report_path).name)

    except Exception as e:
        logger.exception("Error in main app pipeline")
        st.error(f"Error: {e}")
else:
    st.info("Upload a CSV or XLSX file to begin analysis.")
