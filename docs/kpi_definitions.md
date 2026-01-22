# KPI Definitions (Project 1)

## Attendance Rate
**Definition:** attended bookings / total bookings  
**SQL idea:** `AVG(attended)` where attended is 0/1

## Revenue (GBP)
**Definition:** sum of `price_gbp` for attended bookings  
(You can also include no-shows if your business charges regardless—state your assumption.)

## Average Rating
**Definition:** average of `rating_1to5` (1–5)

## Completion Rate
**Definition:** completed / attended  
**SQL idea:** `SUM(CASE WHEN completion_status='Completed' THEN 1 END) / SUM(attended)`

