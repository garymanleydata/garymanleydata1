WITH w_activities AS (
SELECT 
	 "UPLOAD_ID", 
	"TYPE", 
	TO_DATE(SUBSTR(START_DATE_LOCAL,1,10),'YYYY-MM-DD')	activity_date, 
	distance distance_metres,
	distance/1000 distance_km,
	round(distance/1609,4) distance_miles,	
	moving_time moving_time_seconds,
	round(moving_time/60) moving_time_minutes, 
	TOTAL_ELEVATION_GAIN , 
	AVERAGE_SPEED , 
	AVERAGE_CADENCE, 
	AVERAGE_HEARTRATE, 
	MAX_SPEED , 
	MAX_HEARTRATE 
	
	FROM STG_STRAVA )
SELECT * 
FROM w_activities a
INNER JOIN DATES_DIM D ON a.activity_date = D.date_day


		