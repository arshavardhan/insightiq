# core/profiling_engine.py
from ydata_profiling import ProfileReport
import pandas as pd
from services.logger import get_logger

logger = get_logger()

def generate_profile_html(df: pd.DataFrame, minimal: bool = True) -> str:
    """
    Generate a fully local HTML profiling report using ydata-profiling v4.17+.
    """
    try:
        # Only pass supported arguments
        profile = ProfileReport(
            df,
            title="InsightIQ Profiling Report",
            minimal=minimal,
            explorative=True,          # extra statistics locally
            correlations={"pearson": {"calculate": True}},
            interactions=False         # reduce rendering issues
        )

        html = profile.to_html()
        return html

    except Exception as e:
        logger.exception("Profiling failed")
        # For debugging, you can also display the error
        return f"<p>Profiling failed. Check logs. Error: {e}</p>"
