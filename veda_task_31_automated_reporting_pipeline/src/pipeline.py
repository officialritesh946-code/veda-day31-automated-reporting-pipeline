"""
Day 31 — Automated Reporting Pipeline
Ingest -> validate -> transform -> aggregate -> report.

Usage:
    python src/pipeline.py
or:
    python src/pipeline.py --input data/input --output data/output
"""
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

REQUIRED = [
    "EmpID","Age","AgeGroup","Attrition","BusinessTravel","DailyRate","Department",
    "DistanceFromHome","Education","EducationField","EmployeeCount","EmployeeNumber",
    "EnvironmentSatisfaction","Gender","HourlyRate","JobInvolvement","JobLevel",
    "JobRole","JobSatisfaction","MaritalStatus","MonthlyIncome","SalarySlab",
    "MonthlyRate","NumCompaniesWorked","Over18","OverTime","PercentSalaryHike",
    "PerformanceRating","RelationshipSatisfaction","StandardHours","StockOptionLevel",
    "TotalWorkingYears","TrainingTimesLastYear","WorkLifeBalance","YearsAtCompany",
    "YearsInCurrentRole","YearsSinceLastPromotion","YearsWithCurrManager"
]

NUMERIC = [
    "Age","DailyRate","DistanceFromHome","Education","EmployeeCount","EmployeeNumber",
    "EnvironmentSatisfaction","HourlyRate","JobInvolvement","JobLevel","JobSatisfaction",
    "MonthlyIncome","MonthlyRate","NumCompaniesWorked","PercentSalaryHike",
    "PerformanceRating","RelationshipSatisfaction","StandardHours","StockOptionLevel",
    "TotalWorkingYears","TrainingTimesLastYear","WorkLifeBalance","YearsAtCompany",
    "YearsInCurrentRole","YearsSinceLastPromotion","YearsWithCurrManager"
]

def transform(frames):
    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype("string").str.strip()
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.drop_duplicates(subset=["EmployeeNumber"], keep="last").copy()
    df["YearsWithCurrManager"] = df["YearsWithCurrManager"].fillna(
        df["YearsWithCurrManager"].median()
    )

    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0}).astype("int64")
    df["OverTimeFlag"] = df["OverTime"].map({"Yes": 1, "No": 0}).astype("int64")
    df["AnnualIncome"] = df["MonthlyIncome"] * 12
    df["AgeBand"] = pd.cut(df["Age"], [17,24,34,44,54,60],
                           labels=["18–24","25–34","35–44","45–54","55–60"],
                           include_lowest=True)
    df["TenureBand"] = pd.cut(df["YearsAtCompany"], [-1,1,3,7,15,100],
                              labels=["0–1 yr","2–3 yrs","4–7 yrs","8–15 yrs","16+ yrs"])
    df["DistanceBand"] = pd.cut(df["DistanceFromHome"], [0,5,10,20,100],
                                labels=["0–5 mi","6–10 mi","11–20 mi","21+ mi"])
    df["IncomeBand"] = pd.cut(df["MonthlyIncome"], [0,3000,6000,10000,20000],
                              labels=["< ₹3k","₹3k–₹6k","₹6k–₹10k","₹10k+"])
    df["TravelRiskFlag"] = df["BusinessTravel"].eq("Travel_Frequently").astype(int)
    df["HasStockOption"] = df["StockOptionLevel"].gt(0).astype(int)
    return df

def summary(df, col):
    out = df.groupby(col, observed=False).agg(
        Employees=("EmployeeNumber","count"),
        AttritionCases=("AttritionFlag","sum"),
        AvgMonthlyIncome=("MonthlyIncome","mean"),
        AvgYearsAtCompany=("YearsAtCompany","mean")
    ).reset_index()
    out["AttritionRate"] = out["AttritionCases"] / out["Employees"]
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/input")
    parser.add_argument("--output", default="data/output")
    args = parser.parse_args()

    input_dir, output_dir = Path(args.input), Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(input_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {input_dir}")

    frames = [pd.read_csv(f) for f in files]
    df = transform(frames)

    df.to_csv(output_dir/"dashboard_ready_employees.csv", index=False)

    kpis = pd.DataFrame([
        ["Employees", len(df)],
        ["Attrition cases", int(df.AttritionFlag.sum())],
        ["Attrition rate", df.AttritionFlag.mean()],
        ["Average monthly income", df.MonthlyIncome.mean()],
        ["Average age", df.Age.mean()],
        ["Average years at company", df.YearsAtCompany.mean()],
        ["Overtime attrition rate", df.loc[df.OverTime=="Yes","AttritionFlag"].mean()]
    ], columns=["Metric","Value"])
    kpis.to_csv(output_dir/"summary_kpis.csv", index=False)

    for col, filename in {
        "Department":"summary_by_department.csv",
        "JobRole":"summary_by_job_role.csv",
        "OverTime":"summary_by_overtime.csv",
        "AgeBand":"summary_by_age_group.csv"
    }.items():
        summary(df, col).to_csv(output_dir/filename, index=False)

    print(f"Pipeline completed at {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Rows processed: {len(df):,}")
    print(f"Output folder: {output_dir.resolve()}")

if __name__ == "__main__":
    main()
