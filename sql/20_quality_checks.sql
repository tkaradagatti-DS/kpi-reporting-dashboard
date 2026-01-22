-- 20_quality_checks.sql (SQLite)

-- 1) Duplicates (should be 0)
-- Leads: duplicate lead_id
SELECT lead_id, COUNT(*) AS cnt
FROM crm_leads
GROUP BY lead_id
HAVING COUNT(*) > 1;

-- Attendance: duplicate booking_id
SELECT booking_id, COUNT(*) AS cnt
FROM training_attendance
GROUP BY booking_id
HAVING COUNT(*) > 1;

-- 2) Referential integrity: attendance lead_id missing in CRM
SELECT a.booking_id, a.lead_id
FROM training_attendance a
LEFT JOIN crm_leads l ON a.lead_id = l.lead_id
WHERE l.lead_id IS NULL;

-- 3) Invalid price
SELECT booking_id, price_gbp
FROM training_attendance
WHERE price_gbp <= 0 OR price_gbp IS NULL;

-- 4) Missing/invalid rating
SELECT booking_id, rating_1to5
FROM survey_feedback
WHERE rating_1to5 IS NULL OR rating_1to5 NOT BETWEEN 1 AND 5;
