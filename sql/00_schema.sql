-- 00_schema.sql (SQLite)

DROP TABLE IF EXISTS crm_leads;
DROP TABLE IF EXISTS training_attendance;
DROP TABLE IF EXISTS survey_feedback;

CREATE TABLE crm_leads (
  lead_id TEXT PRIMARY KEY,
  created_date TEXT,
  channel TEXT,
  company TEXT,
  region TEXT,
  status TEXT
);

CREATE TABLE training_attendance (
  booking_id TEXT PRIMARY KEY,
  lead_id TEXT,
  course_id TEXT,
  session_date TEXT,
  attended INTEGER,
  completion_status TEXT,
  price_gbp INTEGER
);

CREATE TABLE survey_feedback (
  booking_id TEXT,
  rating_1to5 INTEGER,
  nps INTEGER,
  submitted_date TEXT
);
