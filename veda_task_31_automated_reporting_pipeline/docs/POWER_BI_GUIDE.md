# Power BI Dashboard Guide

## 1. Load the data
Open Power BI Desktop and select **Get Data → Text/CSV**. Load:
- `data/output/dashboard_ready_employees.csv`

For a simple model, one employee table is enough.

## 2. Recommended report pages
### Page 1 — Executive Overview
Cards:
- Employees
- Attrition cases
- Attrition rate
- Average monthly income
- Average tenure

Charts:
- Attrition rate by Department
- Attrition rate by OverTime
- Attrition rate by AgeBand

Slicers:
- Department
- JobRole
- Gender
- BusinessTravel
- OverTime
- AgeBand

### Page 2 — Workforce Risk
Charts:
- Attrition rate by JobRole
- Attrition rate by TenureBand
- Attrition rate by IncomeBand
- Attrition rate by DistanceBand

### Page 3 — Compensation & Experience
Charts:
- Average MonthlyIncome by JobRole
- Average YearsAtCompany by Department
- Attrition rate by SalarySlab

## 3. DAX measures
```DAX
Employees = DISTINCTCOUNT(Employees[EmployeeNumber])

Attrition Cases =
CALCULATE(
    [Employees],
    Employees[Attrition] = "Yes"
)

Attrition Rate =
DIVIDE([Attrition Cases], [Employees])

Average Monthly Income =
AVERAGE(Employees[MonthlyIncome])

Average Tenure =
AVERAGE(Employees[YearsAtCompany])

Overtime Attrition Rate =
CALCULATE(
    [Attrition Rate],
    Employees[OverTime] = "Yes"
)
```

## 4. Professional design
Use a restrained corporate layout:
- Dark navy header
- White cards
- Light grey report background
- One accent color for key risk metrics
- Consistent typography
- Clear chart titles with units
- Avoid 3D visuals and unnecessary decoration

## 5. Refresh design
The Python pipeline writes a stable `dashboard_ready_employees.csv`. In Power BI, connect to that output file. After each scheduled pipeline run, refresh the Power BI dataset.

## 6. Scheduling concept
`Recurring CSVs → Python pipeline → validated output CSV → Power BI refresh → management dashboard`

For production, use a scheduler and add failure alerts, row-count thresholds, schema validation, and archived outputs.
