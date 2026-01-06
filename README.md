# 🚀 InsightIQ – Automated Business Intelligence Pipeline

InsightIQ is a **no-code, AI-powered business intelligence platform** that converts raw data into **KPIs, dashboards, and human-readable insights** with minimal user effort.  
It enables users to upload CSV files or connect directly to SQL databases and instantly generate analytics without writing code.

---

## ✨ Key Features

- 📂 CSV file ingestion
- 🗄️ SQL database connectivity
- 🧩 Microsoft SQL Server integration
- 📊 Automatic KPI detection and computation
- 📈 Interactive data exploration
- 🧠 AI-generated plain-English insight summaries
- 📄 Automated report generation (PDF-ready pipeline)
- ⚡ Scalable analytics for large datasets (1M+ rows)

---

## 🔌 Supported Data Sources

### File-Based
- CSV uploads

### Database-Based
- PostgreSQL
- MySQL
- **Microsoft SQL Server**

---

## 🗄️ Microsoft SQL Server Integration

InsightIQ supports direct connectivity to **Microsoft SQL Server** using `pyodbc`, enabling seamless analytics on enterprise-grade relational databases.

### Capabilities
- Load complete SQL Server tables
- Execute custom SQL queries
- Analyze production-scale datasets
- Reuse the same analytics pipeline used for CSV data

### Required Driver
- **ODBC Driver 17 for SQL Server**

---

## 🧠 System Architecture

Data Source (CSV / SQL Server)
↓
Data Ingestion Layer
↓
Data Cleaning & Profiling
↓
Automated KPI Engine
↓
Visualization & AI Insight Layer
↓
Reports / Dashboards


---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **pyodbc**
- **Large Language Models (Flan-T5)**
- **FPDF / PDF automation**

---

## 📦 Installation

bash
git clone https://github.com/arshavardhan/insightiq.git
cd insightiq
pip install -r requirements.txt

▶️ Run the Application
streamlit run app.py

📌 Example Use Cases

Automated business KPI reporting

SQL-based analytics for non-technical users

Rapid exploratory data analysis

AI-assisted insight generation

No-code BI solutions for startups and enterprises

🚀 Why InsightIQ?

InsightIQ bridges the gap between raw data and decision-making by combining:

Data engineering pipelines

Analytics automation

AI-generated business insights

into a single, easy-to-use platform.

👤 Author

Dumpa Venkata Harsha Vardhan
Entry-level Python / Data / AI Engineer

GitHub: https://github.com/arshavardhan

LinkedIn: https://linkedin.com/in/harsha-vardhan-dumpa-862082233
