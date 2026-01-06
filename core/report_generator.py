# core/report_generator.py
# Generate PDF report using fpdf and images from Plotly figures

from fpdf import FPDF
import tempfile
from pathlib import Path
import plotly.io as pio
import os

class PDFReport:
    def __init__(self, title="InsightIQ Report"):
        self.pdf = FPDF()
        self.title = title

    def add_title(self):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.add_page()
        self.pdf.cell(0, 10, self.title, ln=1, align="C")
        self.pdf.ln(4)

    def add_kpis(self, kpis: dict):
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 8, "Key Metrics:", ln=1)
        for k, v in kpis.items():
            self.pdf.multi_cell(0, 7, f"- {k}: {v}")

    def add_insights(self, insights_text: str):
        self.pdf.ln(4)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "AI-Generated Insights:", ln=1)
        self.pdf.set_font("Arial", size=11)
        self.pdf.multi_cell(0, 7, insights_text)

    def add_figure(self, fig, caption=None):
        # Save Plotly fig to a temporary PNG and add to PDF
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.close()
        try:
            pio.write_image(fig, tmp.name, format="png", scale=1)
            self.pdf.ln(4)
            self.pdf.image(tmp.name, w=180)
            if caption:
                self.pdf.set_font("Arial", size=10)
                self.pdf.multi_cell(0, 6, caption)
        except Exception as e:
            # If image writing fails, simply skip figure
            print("Failed to add figure to PDF:", e)
        finally:
            try:
                os.unlink(tmp.name)
            except:
                pass

    def output(self, path):
        self.pdf.output(path)
        return path
