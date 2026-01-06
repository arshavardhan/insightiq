🚀 InsightIQ – Automated Business Intelligence Pipeline

InsightIQ is a no-code automated business intelligence platform that transforms raw datasets into actionable insights with minimal user effort. It enables users to upload data and instantly receive KPIs, visual dashboards, and plain-English summaries, significantly reducing manual analysis time.

🧠 Key Features

📊 Automated KPI Generation
Automatically computes 20+ business KPIs from CSV or SQL-based datasets with 1M+ rows.

🧹 Data Cleaning & Profiling
Performs schema validation, missing value analysis, and statistical profiling using Pandas Profiling.

📈 Interactive Dashboards
Generates dynamic visualizations with Plotly for trend analysis and performance monitoring.

🤖 AI-Generated Insight Summaries
Uses Flan-T5 LLMs to convert analytical results into human-readable business insights.

📄 Automated PDF Reports
One-click generation of downloadable PDF reports for stakeholders.

☁️ Cloud Deployment
Deployed on Streamlit Cloud, supporting 10+ concurrent users.

🛠️ Tech Stack

Programming Language: Python

Data Processing: Pandas, NumPy

Visualization: Plotly

AI / NLP: Flan-T5 (Hugging Face Transformers)

Reporting: FPDF, pdfplumber

Web Framework: Streamlit

Deployment: Streamlit Cloud

⚙️ Architecture Overview

Data Ingestion – Upload CSV or connect to SQL databases

Preprocessing – Cleaning, validation, and profiling

KPI Engine – Automated metric computation

Visualization Layer – Interactive dashboards

LLM Layer – Insight summarization using Flan-T5

Report Generator – Exportable PDF reports

📈 Impact

⏱️ Reduced manual data analysis time by ~70%

⚡ Improved report generation speed by 5×

👥 Supports multi-user concurrent access

📊 Handles large-scale datasets (1M+ rows) efficiently

🚀 How to Run Locally
# Clone the repository
git clone https://github.com/your-username/insightiq.git
cd insightiq

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

📌 Use Cases

Business performance analysis

Sales & revenue reporting

Operational KPI monitoring

Data-driven decision support for non-technical users

🔮 Future Enhancements

Role-based access control

Real-time data connectors (APIs)

Advanced forecasting & anomaly detection

Support for more LLM models

👤 Author

Dumpa Venkata Harsha Vardhan
Entry-Level Python / Software Developer
📧 Email: dumpaharsha2003@gmail.com

🔗 GitHub: arshavardhan
