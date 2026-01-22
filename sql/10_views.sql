-- 10_views.sql (SQLite)
-- KPI view by month (YYYY-MM)

DROP VIEW IF EXISTS vw_monthly_kpis;

CREATE VIEW vw_monthly_kpis AS
SELECT
  substr(session_date, 1, 7) AS month,
  COUNT(*) AS bookings,
  AVG(attended) AS attendance_rate,
  SUM(CASE WHEN attended = 1 AND price_gbp > 0 THEN price_gbp ELSE 0 END) AS revenue_gbp,
  AVG(CASE WHEN s.rating_1to5 BETWEEN 1 AND 5 THEN s.rating_1to5 END) AS avg_rating
FROM training_attendance a
LEFT JOIN survey_feedback s ON a.booking_id = s.booking_id
GROUP BY 1
ORDER BY 1;

-- Course performance
DROP VIEW IF EXISTS vw_course_kpis;

CREATE VIEW vw_course_kpis AS
SELECT
  course_id,
  COUNT(*) AS bookings,
  AVG(attended) AS attendance_rate,
  SUM(CASE WHEN attended = 1 AND price_gbp > 0 THEN price_gbp ELSE 0 END) AS revenue_gbp
FROM training_attendance
GROUP BY 1
ORDER BY revenue_gbp DESC;
