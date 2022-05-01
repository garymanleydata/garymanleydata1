create or replace view v_parkrun_processed as
select TIME_FORMAT(STR_TO_DATE(event_time, '%H:%i:%s'),'%H:%i:%s') event_time, 
	   extract(MINUTE FROM TIME_FORMAT(STR_TO_DATE(event_time, '%H:%i:%s'),'%H:%i:%s')) * 60
       + extract(SECOND FROM TIME_FORMAT(STR_TO_DATE(event_time, '%H:%i:%s'),'%H:%i:%s')) total_seconds,
       	(extract(MINUTE FROM TIME_FORMAT(STR_TO_DATE(event_time, '%H:%i:%s'),'%H:%i:%s')) * 60
       + extract(SECOND FROM TIME_FORMAT(STR_TO_DATE(event_time, '%H:%i:%s'),'%H:%i:%s')))/60 decimal_minute,
       parkrun_number, 
       parkrun_position, 
       total_field, 
       age_category, 
       event_date, 
       parkrun_place, 
       age_rating
       -- time in seconds and deciaml time in minute. 
from v_parkrun_result
