# Project Documentation — Automated Reporting Pipeline

## 1. Objective
Build an analyst-friendly automated reporting pipeline that ingests recurring CSV data, applies repeatable transformations and validation, and produces dashboard-ready reporting outputs.

## 2. Architecture

**Input CSV files**
→ **Ingestion**
→ **Schema validation**
→ **Data cleaning**
→ **Business transformations**
→ **KPI aggregation**
→ **Dashboard-ready CSVs**
→ **HTML / Power BI dashboard**

## 3. Ingestion
The pipeline reads every `.csv` file from `data/input/`. This makes the solution reusable for recurring files rather than dependent on one manually edited workbook.

## 4. Validation
Checks include:
- required-column presence
- numeric conversion
- employee-key uniqueness
- valid Attrition values
- missing-value detection
- duplicate handling

## 5. Transformation
The pipeline creates numeric flags and useful reporting dimensions such as AgeBand, TenureBand, DistanceBand and IncomeBand. Annual income is derived from monthly income.

## 6. Missing-value strategy
The source contained 57 missing values in `YearsWithCurrManager`. The pipeline fills these with the median value so the reporting output has no missing values in this field. In a production HR environment, this rule should be approved by the data owner.

## 7. Output
The main output is `dashboard_ready_employees.csv`. Separate summary tables support simple BI ingestion and testing.

## 8. Reporting insights
The supplied dataset has an overall attrition rate of 16.12%. Overtime employees have an attrition rate of 30.53%. These figures are descriptive and should not be treated as causal conclusions.

## 9. Idempotency / rerun safety
The pipeline is designed to be rerun. It reads the current input folder, rebuilds outputs and deduplicates by `EmployeeNumber`. This avoids accumulating duplicate employee records when recurring files overlap.

## 10. Failure handling
The script stops with a clear error when required columns are missing or when no CSV files exist. A production implementation should add structured logs, alerting, and an archive folder.

## 11. Interview questions
### What is idempotency?
It means rerunning the same pipeline does not unintentionally create duplicate or inconsistent results.

### How would you schedule the pipeline?
Use Windows Task Scheduler, cron, GitHub Actions, Airflow, or another orchestration platform depending on the deployment environment.

### Why separate ingestion, transformation and reporting?
Separation makes the workflow easier to test, debug, maintain and reuse.

### What would you monitor in production?
File arrival, row counts, schema changes, duplicate keys, missingness, pipeline duration, failures and dashboard refresh status.
