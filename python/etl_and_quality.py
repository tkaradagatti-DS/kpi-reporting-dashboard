"""ETL + Data Quality (Project 1)

- Reads raw CSVs
- Cleans + standardises columns
- Runs basic validation checks
- Loads to SQLite
- Outputs a KPI summary and an HTML data quality report

Run:
  pip install -r requirements.txt
  python etl_and_quality.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

OUTPUTS.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

def standardise_channel(x: str) -> str:
    if pd.isna(x):
        return "Unknown"
    x = str(x).strip()
    # normalise casing
    x = x.replace("_", " ")
    return x.title()

def main() -> None:
    leads = pd.read_csv(RAW / "crm_leads.csv")
    attendance = pd.read_csv(RAW / "training_attendance.csv")
    survey = pd.read_csv(RAW / "survey_feedback.csv")

    # -------------------------
    # Cleaning / standardisation
    # -------------------------
    leads["channel"] = leads["channel"].apply(standardise_channel)
    leads["region"] = leads["region"].fillna("Unknown")
    leads["company"] = leads["company"].replace("", pd.NA)

    # remove duplicates by primary key (keep first)
    leads = leads.drop_duplicates(subset=["lead_id"], keep="first")
    attendance = attendance.drop_duplicates(subset=["booking_id"], keep="first")

    # enforce types
    for col in ["created_date"]:
        leads[col] = pd.to_datetime(leads[col], errors="coerce").dt.date

    attendance["session_date"] = pd.to_datetime(attendance["session_date"], errors="coerce").dt.date
    attendance["attended"] = attendance["attended"].fillna(0).astype(int)

    survey["submitted_date"] = pd.to_datetime(survey["submitted_date"], errors="coerce").dt.date

    # -------------------------
    # Validation rules (quality checks)
    # -------------------------
    issues = []

    # FK check: attendance lead_id must exist in leads
    bad_fk = attendance.loc[~attendance["lead_id"].isin(leads["lead_id"]), ["booking_id", "lead_id"]]
    if not bad_fk.empty:
        issues.append(("Attendance lead_id missing in CRM", bad_fk))

    # price must be > 0
    bad_price = attendance.loc[(attendance["price_gbp"].isna()) | (attendance["price_gbp"] <= 0), ["booking_id", "price_gbp"]]
    if not bad_price.empty:
        issues.append(("Invalid price (<=0 or NULL)", bad_price))

    # rating must be 1-5
    bad_rating = survey.loc[(survey["rating_1to5"].isna()) | (~survey["rating_1to5"].between(1, 5)), ["booking_id", "rating_1to5"]]
    if not bad_rating.empty:
        issues.append(("Invalid rating (NULL or outside 1-5)", bad_rating))

    # -------------------------
    # Save processed datasets
    # -------------------------
    leads.to_csv(PROCESSED / "crm_leads_clean.csv", index=False)
    attendance.to_csv(PROCESSED / "training_attendance_clean.csv", index=False)
    survey.to_csv(PROCESSED / "survey_feedback_clean.csv", index=False)

    # -------------------------
    # Load to SQLite
    # -------------------------
    db_path = OUTPUTS / "reporting.db"
    conn = sqlite3.connect(db_path)
    leads.to_sql("crm_leads", conn, if_exists="replace", index=False)
    attendance.to_sql("training_attendance", conn, if_exists="replace", index=False)
    survey.to_sql("survey_feedback", conn, if_exists="replace", index=False)

    # KPI summary (monthly)
    kpi = pd.read_sql_query(
        """SELECT
              substr(session_date, 1, 7) AS month,
              COUNT(*) AS bookings,
              AVG(attended) AS attendance_rate,
              SUM(CASE WHEN attended = 1 AND price_gbp > 0 THEN price_gbp ELSE 0 END) AS revenue_gbp
            FROM training_attendance
            GROUP BY 1
            ORDER BY 1""",
        conn
    )
    kpi.to_csv(OUTPUTS / "kpi_summary.csv", index=False)

    # -------------------------
    # Build a simple HTML quality report
    # -------------------------
    html_parts = [
        "<h1>Data Quality Report — Project 1</h1>",
        "<p>Checks: referential integrity, invalid values, missing data.</p>",
    ]
    if not issues:
        html_parts.append("<h2>✅ No issues found</h2>")
    else:
        html_parts.append(f"<h2>⚠️ Issues found: {len(issues)}</h2>")
        for title, df in issues:
            html_parts.append(f"<h3>{title} (rows: {len(df)})</h3>")
            html_parts.append(df.head(50).to_html(index=False))

    (OUTPUTS / "quality_report.html").write_text("\n".join(html_parts), encoding="utf-8")
    conn.close()

    print("Done.")
    print(f"- DB: {db_path}")
    print(f"- KPI summary: {OUTPUTS/'kpi_summary.csv'}")
    print(f"- Quality report: {OUTPUTS/'quality_report.html'}")

if __name__ == "__main__":
    main()
