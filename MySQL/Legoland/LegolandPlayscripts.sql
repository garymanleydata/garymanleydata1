create table testing
as 
select 1 
union all 
select 2 
union all 
select 3;

select * from testing;

select * from ride_data ; 
-- create a run dim, join to that instead of having log tim and date? 
SHOW VARIABLES LIKE "%version%";


select 	lands_0_id as land_id, 
		lands_0_name as lands_name, 
		lands_0_rides_0_Id as ride_id, 
		lands_0_rides_0_name as ride_name,
		lands_0_rides_0_is_open as is_open,
		lands_0_rides_0_last_updated as log_time, 
		lands_0_rides_0_wait_time as ride_wait_time		
from ride_data 
union 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_0_Id as ride_idq, 
		lands_1_rides_0_name as ride_name,
		lands_1_rides_0_is_open as is_open,
		lands_1_rides_0_last_updated as log_time,  
		lands_1_rides_0_wait_time as ride_wait_time		
from ride_data 
union  
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_1_Id as ride_idq, 
		lands_1_rides_1_name as ride_name,
		lands_1_rides_1_is_open as is_open,
		lands_1_rides_1_last_updated as log_time,
		lands_1_rides_1_wait_time as ride_wait_time		
from ride_data 
;
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_2_Id as ride_idq, 
		lands_1_rides_2_name as ride_name,
		lands_1_rides_2_is_open as is_open,
		lands_1_rides_2_last_updated as log_time, 
		lands_1_rides_2_wait_time as ride_wait_time		
from ride_data
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_3_Id as ride_idq, 
		lands_1_rides_3_name as ride_name,
		lands_1_rides_3_is_open as is_open,
		lands_1_rides_3_last_updated as log_time, 
		lands_1_rides_3_wait_time as ride_wait_time		
from ride_data
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_4_Id as ride_idq, 
		lands_1_rides_4_name as ride_name,
		lands_1_rides_4_is_open as is_open,
		lands_1_rides_4_last_updated as log_time, 
		lands_1_rides_4_wait_time as ride_wait_time		
from ride_data
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_5_Id as ride_idq, 
		lands_1_rides_5_name as ride_name,
		lands_1_rides_5_is_open as is_open,
		lands_1_rides_5_last_updated as log_time, 
		lands_1_rides_5_wait_time as ride_wait_time		
from ride_data
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_6_Id as ride_idq, 
		lands_1_rides_6_name as ride_name,
		lands_1_rides_6_is_open as is_open,
		lands_1_rides_6_last_updated as log_time, 
		lands_1_rides_6_wait_time as ride_wait_time		
from ride_data 
;

-- write a view to transform this 
-- would be good to get this running on a schedule on python anywhere 
-- look at cost and then want to get this and the weather data running
-- can I connect this to Google Data Studio and Streamlit? 

--- land dim / land id and and name 
--- ride dim , ride name, ride id and land id and land name - avoids snowflaking
-- is open dim 
-- fact table is ride id, is open and wait time 

--- build vies for average wait time by hour
--- ride closures 
--- and by day when I have rhe data 
;

create or replace view legoland_avg_ride_wait as
select lands_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , avg(ride_wait_time) average_wait
from wait_time_fact
where is_open = 1
group by  lands_name, ride_name,  hour(CAST(log_time AS DATETIME))+1;

# max queue times 
select lands_name, ride_name, average_wait, GROUP_CONCAT(hour_logged order by hour_logged) best_time
from legoland_avg_ride_wait l
where exists (
select null from (
select ride_name,  min(average_wait) shortest_wait
from legoland_avg_ride_wait
group by ride_name)
x where x.ride_Name = l.ride_name and l.average_wait = x.shortest_wait)
group by lands_name, ride_name, average_wait
; 


lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_6_Id as ride_idq, 
		lands_1_rides_6_name as ride_name,
		lands_1_rides_6_is_open as is_open,
		lands_1_rides_6_last_updated as log_time, 
		lands_1_rides_6_wait_time as ride_wait_time	
		;


create or replace view wait_time_fact_v as
select 	coalesce(fd.land_id,-99) land_id ,
		coalesce(fd.land_name,'Legoland') land_name, 
		id as ride_id, 
		name as ride_name, 
		CASE WHEN status = 'OPERATING' THEN 1 ELSE 0 END as is_open,
		run_time as log_time, 
		coalesce(`queue.STANDBY.waitTime`,0) as ride_wait_time, 
		run_date, 
		lastUpdated 		
from all_ride_data_time rdt
left outer join land_ride_dim fd on rdt.name = fd.ride_name
order by name; 

#create or replace view legoland_avg_ride_wait as
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , round(avg(ride_wait_time)) average_wait
from wait_time_fact_v
where is_open = 1
group by  land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1;

create table land_ride_dim as 
select distinct land_id, lands_name as land_name, ride_name from wait_time_fact;

insert into all_ride_data_time(id,name,entityType,parkId,externalId,status,lastUpdated,`queue.STANDBY.waitTime`,run_time,run_date)
select 	cast(ride_id as char) , 
		ride_name, 
		'ATTRACTION' entity_type, 
		'a4f71074-e616-4de4-9278-72fdecbdc995' park_id,
		'9999' external_id, 
		case when is_open = 1 then 'OPERATING' else 'CLOSED'end as is_open, 
		log_time, 
		ride_wait_time, 
		time(CAST(log_time AS DATETIME)) TIMEONLY,
		date(CAST(log_time AS DATETIME)) DATEONLY
from wait_time_fact;

#last updated date wait time , run_time, run_Date

select * from all_ride_data_time order by name;
select * from land_ride_dim;
select * from  wait_time_fact;

