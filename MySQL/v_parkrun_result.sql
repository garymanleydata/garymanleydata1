create or replace view v_parkrun_result as
## Inital version GM
## 1.1. - Chanege to cater for manual entires, change to logic in event location
select 	      
		substr(mailtext,
               locate('Your time was',mailtext)+14, 
               8) event_time, 
        cast(substr(mailtext,
               locate('Congratulations on completing your ',mailtext)+35, 
               3) as DECIMAL) parkrun_number, 
        -- get place
		substr(replace(Subject , 'Your result from ',''),1,
		(locate(',',replace(Subject , 'Your result from ',''))
		-1)) parkrun_place, 
		-- get position
        cast(substr(mailtext,
               locate('today. You finished in',mailtext)+22, 
               4) as DECIMAL) parkrun_position, 
        -- get total participants
          cast(substr(mailtext,
               locate('out of a field of ',mailtext)+18, 
               4) as DECIMAL) total_field,       
        -- age category 
         substr(mailtext,
               locate('category VM',mailtext)+9, 
               7) age_category,         
        -- age grading (as percentage)
         cast(substr(mailtext,
               locate('You achieved an age-graded score of ',mailtext)+36, 
               5) as DECIMAL(4,2)) age_rating,          
        date(cast(date as datetime)) event_date
from ext_tab_parkrun_email
union all  
select '00:21:15' event_time, 192 parkrun_number,'Eastbourne parkrun' place, 30, 343 , 'VM35-39' , 62.04, date('2022-03-05') union all
select '00:21:22' event_time, 191 parkrun_number,'Eastbourne parkrun' place, 28, 338 , 'VM35-39' , 99, date('2022-02-26') union all
select '00:22:52' event_time, 190 parkrun_number,'Eastbourne parkrun' place, 37, 318 , 'VM35-39' , 62.04, date('2022-02-12') union all
select convert('00:19:37',time) event_time, 189 parkrun_number,'Eastbourne parkrun' place, 15, 355 , 'VM35-39' , 99, date('2022-02-05') 
;
		
