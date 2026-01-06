# core/pipeline_manager.py
# Orchestrates the full InsightIQ pipeline

import pandas as pd
from core.data_cleaning import basic_cleaning
from core.profiling_engine import generate_profile_html
from core.kpi_extractor import compute_basic_kpis
from core.insights_engine import generate_insights
from core.visualization import generate_top_visuals
from core.report_generator import PDFReport
from pathlib import Path
import os
from services.logger import get_logger

logger = get_logger()

class PipelineManager:
    def __init__(self, config=None):
        self.config = config or {}
        self.data_dir = Path(self.config.get("paths", {}).get("data_dir", "data"))
        self.report_dir = Path(self.config.get("paths", {}).get("report_dir", "reports"))
        self.model_name = self.config.get("llm", {}).get("model_name", "google/flan-t5-small")
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def load_dataset(self, uploaded_file) -> pd.DataFrame:
        """Load CSV or XLSX dataset"""
        name = getattr(uploaded_file, "name", "")
        if name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df

    def run_full_pipeline(self, df: pd.DataFrame) -> dict:
        """Run the full pipeline and return results"""
        results = {}

        # 1️⃣ Cleaning
        cleaned_df, clean_summary = basic_cleaning(df)
        results["clean_summary"] = clean_summary

        # 2️⃣ Profiling
        try:
            profile_html = generate_profile_html(cleaned_df, minimal=True)
            results["profile_html"] = profile_html
        except Exception as e:
            logger.exception("Profiling failed")
            results["profile_html"] = None

        # 3️⃣ KPI extraction
        kpis = compute_basic_kpis(cleaned_df)
        results["kpis"] = kpis

        # 4️⃣ Visualizations
        figs = generate_top_visuals(cleaned_df)
        results["figures"] = figs

        # 5️⃣ Insights
        try:
            insights = generate_insights(kpis=kpis, sample_rows=cleaned_df.head(50), model_name=self.model_name)
            results["insights"] = insights
        except Exception as e:
            logger.exception("Insight generation failed")
            results["insights"] = "Insight generation failed."

        # 6️⃣ Report
        try:
            report = PDFReport()
            report.add_title()
            report.add_kpis(kpis)
            report.add_insights(results.get("insights", ""))
            for _, fig in figs[:3]:
                report.add_figure(fig)
            out_path = self.report_dir / f"insightiq_report_{os.getpid()}_{int(pd.Timestamp.now().timestamp())}.pdf"
            report.output(str(out_path))
            results["report_path"] = str(out_path)
        except Exception as e:
            logger.exception("Report generation failed")
            results["report_path"] = None

        return results
