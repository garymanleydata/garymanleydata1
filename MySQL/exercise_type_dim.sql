SELECT 
	Timestamp,
	Date, 
	1 activity_Type_id,
	COALESCE(Pull_up,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	Date, 
	2 activity_Type_id,
	COALESCE(Crunch,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	Date, 
	3 activity_Type_id,
	COALESCE(Push_up,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	TimeStamp,
	Date, 
	4 activity_Type_id,
	COALESCE(Plank_time,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	TimeStamp,
	Date, 
	5 activity_Type_id,
	COALESCE(Dumbbell,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	TimeStamp,
	Date, 
	6 activity_Type_id,
	COALESCE(Box_jump,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
;
-- SNOWFLAKE TRANSFORMATIONS ARE CASE SENSITIVE
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done, 
	1 activity_Type_id,
	COALESCE(Pull_up,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done, 
	2 activity_Type_id,
	COALESCE(Crunch,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done, 
	3 activity_Type_id,
	COALESCE(Push_up,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done,  
	4 activity_Type_id,
	COALESCE(Plank_time,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done, 
	5 activity_Type_id,
	COALESCE(Dumbbell,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
UNION ALL 
SELECT 
	Timestamp,
	to_date(Date,'DD/MM/YYYY') Date_done, 
	6 activity_Type_id,
	COALESCE(Box_jump,0) Activity_COUNT
    FROM `exercise--responses--form-responses-1`
;

CREATE OR REPLACE TABLE exercise_fact as
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done, 
	1 activity_Type_id,
	COALESCE("Pull_up",0) Activity_COUNT
    FROM stg_exercise
UNION ALL 
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done, 
	2 activity_Type_id,
	COALESCE("Crunch",0) Activity_COUNT
    FROM stg_exercise
UNION ALL 
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done,  
	3 activity_Type_id,
	COALESCE("Push_up",0) Activity_COUNT
    FROM stg_exercise
UNION ALL 
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done,  
	4 activity_Type_id,
	COALESCE("Plank_time",0) Activity_COUNT
    FROM stg_exercise
UNION ALL 
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done, 
	5 activity_Type_id,
	COALESCE("Dumbbell",0) Activity_COUNT
    FROM stg_exercise
UNION ALL 
SELECT 
	"Timestamp",
	to_date("Date",'DD/MM/YYYY') Date_done, 
	6 activity_Type_id,
	COALESCE("Box_jump",0) Activity_COUNT
    FROM stg_exercise
;

create table activity_type_dim as 
select  1 id, 'Pull Up' Description
UNION ALL 
select  2 id, 'Crunch' Description
UNION ALL 
select  3 id, 'Push Up' Description
UNION ALL 
select  4 id, 'Plank Time' Description
UNION ALL 
select  5 id, 'Dumbbells' Description
UNION ALL 
select  6 id, 'Box Jump' Description;
; 

1 id, 'Pull Up' Description;

SELECT 
	"TIMESTAMP",
   to_date("DATE",'DD/MM/YYYY') DATE_DONE, 
	1 ACTIVITY_TYPE_ID,
	PULL_UP ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
	
CREATE OR REPLACE TABLE exercise_fact as
SELECT 
	"TIMESTAMP",
   to_date("DATE",'DD/MM/YYYY') DATE_DONE, 
	1 ACTIVITY_TYPE_ID,
	PULL_UP ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
UNION ALL 
SELECT 
	"TIMESTAMP",
    to_date("DATE",'DD/MM/YYYY') DATE_DONE,  
	2 ACTIVITY_TYPE_ID,
	CRUNCH ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
UNION ALL 
SELECT 
	"TIMESTAMP",
    to_date("DATE",'DD/MM/YYYY') DATE_DONE,  
	3 ACTIVITY_TYPE_ID,
	PUSH_UP ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
UNION ALL 
SELECT 
	"TIMESTAMP",
    to_date("DATE",'DD/MM/YYYY') DATE_DONE,  
	4 ACTIVITY_TYPE_ID,
	PLANK_TIME ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
UNION ALL 
SELECT 
	"TIMESTAMP",
    to_date("DATE",'DD/MM/YYYY') DATE_DONE, 
	5 ACTIVITY_TYPE_ID,
	DUMBBELL ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
UNION ALL 
SELECT 
	"TIMESTAMP",
    to_date("DATE",'DD/MM/YYYY') DATE_DONE, 
	6 ACTIVITY_TYPE_ID,
	BOX_JUMP ACTIVITY_COUNT
    FROM EXT_TAB_EXERCISE
;