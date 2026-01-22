# DAX Measures (Power BI)

```DAX
Bookings = COUNTROWS(training_attendance)

Attended Bookings = CALCULATE([Bookings], training_attendance[attended] = 1)

Attendance Rate = DIVIDE([Attended Bookings], [Bookings])

Revenue (Attended) = 
SUMX(
    FILTER(training_attendance, training_attendance[attended] = 1),
    training_attendance[price_gbp]
)

Avg Rating = AVERAGE(survey_feedback[rating_1to5])
```

