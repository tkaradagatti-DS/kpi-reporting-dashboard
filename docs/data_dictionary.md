# Data Dictionary (Project 1)

## crm_leads
| Column | Type | Example | Notes |
|---|---|---|---|
| lead_id | text | L10001 | Primary key |
| created_date | date | 2025-07-18 | Date lead created |
| channel | text | LinkedIn | Standardised in cleaning |
| company | text | Company 117 | Blank values treated as missing |
| region | text | East Midlands | Missing -> 'Unknown' |
| status | text | Qualified | CRM status |

## training_attendance
| Column | Type | Example | Notes |
|---|---|---|---|
| booking_id | text | B20001 | Primary key |
| lead_id | text | L10018 | FK to crm_leads |
| course_id | text | SQL-101 | Course code |
| session_date | date | 2024-07-27 | Session date |
| attended | int (0/1) | 1 | No-show = 0 |
| completion_status | text | Completed | Derived from attended |
| price_gbp | int | 249 | Must be > 0 |

## survey_feedback
| Column | Type | Example | Notes |
|---|---|---|---|
| booking_id | text | B20433 | FK to training_attendance |
| rating_1to5 | int | 4 | Valid: 1-5 |
| nps | int | 47 | -100 to 100 |
| submitted_date | date | 2025-07-06 | Survey submission date |
