# kpi-reporting-dashboard
## Business Question
How can we combine CRM leads, training attendance, and learner feedback into a single KPI reporting view that supports monthly performance tracking (bookings, revenue, attendance rate) and highlights data quality issues before reporting?

## What I delivered
- Cleaned and standardised 3 data sources (CRM leads, attendance, survey feedback) into analysis-ready datasets.
- Built a repeatable KPI summary output (monthly bookings, revenue, attendance rate) for dashboard use.
- Produced a data quality report to surface join gaps, invalid values, and missing/incorrect entries.
- Documented KPI definitions + a lightweight data dictionary so stakeholders interpret metrics consistently.

## Key checks / assumptions
- Enforced referential integrity checks between attendance `lead_id` and CRM `lead_id` (to avoid missing joins in reporting).
- Validated pricing (non-null, > 0) and feedback ratings (must be 1–5) before using in KPI calculations.
- Defined attendance rate as: `attended / total bookings` per month.
- Assumed survey feedback is optional; reported response rate separately to avoid biasing satisfaction metrics.

## Insights (3 bullets)
- Revenue peaked in **May 2024 (£10,702)** and was lowest in **Nov 2024 (£3,915)**, tracking closely with booking volume (useful for capacity planning).
- Attendance performance varied significantly: best month hit **96.4% (Oct 2024)**, while the lowest dropped to **67.7% (Jul 2025)** — highlighting a no‑show risk period worth investigating.
- Feedback coverage was **56% survey response rate** with an average rating of **3.68/5** (overall NPS slightly negative), suggesting stable satisfaction but clear opportunity to improve learner advocacy.

## Repo structure
```
01-kpi-reporting-dashboard/
  data/
    raw/
    processed/
  python/
    etl_and_quality.py
    requirements.txt
  sql/
    00_schema.sql
    10_views.sql
    20_quality_checks.sql
  docs/
    data_dictionary.md
    kpi_definitions.md
    dax_measures.md
    stakeholder_questions.md
```

## Run (local)
```bash
pip install -r python/requirements.txt
python python/etl_and_quality.py
```

Outputs:
- Processed CSVs in `data/processed/`
- `outputs/quality_report.html`
- `outputs/kpi_summary.csv`
- `outputs/reporting.db` (SQLite)

## Dashboard build notes (Power BI)
- Import `outputs/reporting.db` (SQLite) or the processed CSVs
- Create measures listed in `docs/dax_measures.md`
- Recommended report pages:
  - Executive overview (Monthly KPI trend)
  - Course performance
  - Lead channel performance
  - Data quality (counts of issues by type)

