# kpi-reporting-dashboard

## Scenario
You support a training provider. Teams need monthly KPIs:
- Bookings, attendance rate, revenue
- Course performance
- Channel performance (where leads come from)
- Customer satisfaction (survey rating)

## Data sources (synthetic)
All data is **synthetic** (safe to publish):
- `crm_leads.csv` — lead creation + channel + region
- `training_attendance.csv` — bookings, attendance, completion, price
- `survey_feedback.csv` — post‑session survey ratings

## What you will build
1. **Cleaned datasets** in `data/processed/`
2. **SQL schema + views** for KPI tables (`sql/`)
3. **Power BI dashboard** (store `.pbix` in `powerbi/` + screenshots in `docs/images/`)
4. **Monthly KPI pack** in Excel (`excel/`)

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

