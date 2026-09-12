# Day 31 — Automated Reporting Pipeline

## Project overview
This project implements a practical **ingestion → validation → transformation → reporting** workflow for recurring employee analytics CSV files.

The supplied dataset contains **1,480 employee records and 38 source columns**. The reporting layer turns the raw employee dataset into clean, analysis-ready outputs for a dashboard and Power BI.

> Note: The task page mentions recurring sales CSVs as a suggested dataset, while the supplied file is an employee/attrition dataset. The implementation therefore applies the same automated-reporting architecture to the supplied employee data rather than pretending it is sales data.

## Deliverables
- `src/pipeline.py` — reusable ingestion and transformation pipeline.
- `src/build_dashboard.py` — dashboard asset helper.
- `data/input/employee_data.csv` — supplied input dataset.
- `data/output/dashboard_ready_employees.csv` — cleaned dashboard-ready dataset.
- `data/output/summary_*.csv` — KPI and reporting tables.
- `data/output/data_quality_report.csv` — validation results.
- `dashboard/dashboard.html` — professional static dashboard.
- `docs/POWER_BI_GUIDE.md` — Power BI data model, measures and layout.
- `docs/DATA_DICTIONARY.md` — source and derived-field definitions.
- `docs/PROJECT_DOCUMENTATION.md` — complete technical documentation.
- `logs/pipeline_run_log.csv` — example run metadata.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Git hygiene.

## Key results from the supplied dataset
- Employees: **1,470**
- Attrition cases: **237**
- Overall attrition rate: **16.12%**
- Average monthly income: **₹6,503**
- Average age: **36.9 years**
- Average tenure: **7.0 years**
- Overtime attrition rate: **30.53%**

## How to run
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python src/pipeline.py
```

To process recurring files, place new CSV files in `data/input/`. The pipeline reads all CSV files, validates the schema, combines them, removes duplicate employee IDs, handles missing manager-tenure values, creates reporting fields, and refreshes the output tables.

## Production scheduling
For a real deployment, schedule the same command with Windows Task Scheduler, cron, GitHub Actions, or an orchestration tool such as Airflow. A production version should also add email/Teams alerts, data-volume thresholds, schema-change detection, and persistent run history.

## GitHub
Recommended repository name: `veda-day31-automated-reporting-pipeline`


