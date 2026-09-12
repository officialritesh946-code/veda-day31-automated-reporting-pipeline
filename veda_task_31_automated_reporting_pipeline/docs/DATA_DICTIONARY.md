# Data Dictionary

## Source fields
The source dataset contains employee-level HR analytics fields including demographics, job information, compensation, satisfaction, travel, overtime and tenure.

| Field | Meaning |
|---|---|
| EmpID | Employee identifier |
| EmployeeNumber | Stable numeric employee key used for deduplication |
| Age | Employee age |
| AgeGroup | Source-provided age grouping |
| Attrition | Whether the employee left (`Yes`/`No`) |
| BusinessTravel | Travel frequency |
| Department | Employee department |
| JobRole | Employee job role |
| MonthlyIncome | Monthly income |
| OverTime | Whether the employee works overtime |
| YearsAtCompany | Tenure with the company |
| YearsWithCurrManager | Years with current manager |
| DistanceFromHome | Distance from home |
| JobSatisfaction | Job satisfaction rating |
| EnvironmentSatisfaction | Work-environment satisfaction rating |
| WorkLifeBalance | Work-life balance rating |
| PercentSalaryHike | Salary increase percentage |
| TrainingTimesLastYear | Training sessions last year |

## Derived reporting fields
| Field | Purpose |
|---|---|
| AttritionFlag | Numeric 1/0 version of Attrition |
| OverTimeFlag | Numeric 1/0 version of OverTime |
| AnnualIncome | Monthly income × 12 |
| AgeBand | Standardized age bands for dashboard grouping |
| TenureBand | Company-tenure bands |
| DistanceBand | Home-distance bands |
| IncomeBand | Monthly-income bands |
| TravelRiskFlag | 1 when BusinessTravel is Travel_Frequently |
| HasStockOption | 1 when StockOptionLevel > 0 |
| ManagerTenureBand | Current-manager tenure grouping |

## Data-quality treatment
- Leading/trailing whitespace is removed from text fields.
- Numeric columns are coerced to numeric values.
- Duplicate `EmployeeNumber` records are removed, keeping the last occurrence.
- Missing `YearsWithCurrManager` values are imputed with the median of that field.
- Attrition and overtime are validated through explicit Yes/No mappings.
