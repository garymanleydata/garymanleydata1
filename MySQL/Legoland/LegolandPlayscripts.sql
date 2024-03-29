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

create or replace view legoland_avg_ride_wait_v as
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , round(avg(ride_wait_time)) average_wait, count(*) data_points
from wait_time_fact_v
where is_open = 1
group by  land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1;

select * from legoland_avg_ride_wait_v;
select * from wait_time_fact_v;

create table aml_wait_time_fact
as select * from wait_time_fact_v;
truncate table aml_wait_time_fact;

insert into  aml_wait_time_fact
select * from wait_time_fact_v;

select * from aml_wait_time_fact



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
select * from ride_best_worst_times_v;

select max(`queue.STANDBY.waitTime`) maxTime, avg(`queue.STANDBY.waitTime`) average from all_ride_data_time where status = 'OPERATING';

create or replace view ride_best_worst_times_v as 
select land_name, ride_name , max(best_time) best_hour, max(worst_time) worst_hour FROM(
select land_name, ride_name, average_wait, GROUP_CONCAT(hour_logged order by hour_logged) best_time, NULL worst_time
from legoland_avg_ride_wait_v l
where exists (
select null from (
select ride_name,  min(average_wait) shortest_wait
from legoland_avg_ride_wait_v
group by ride_name)
x where x.ride_Name = l.ride_name and l.average_wait = x.shortest_wait)
group by land_name, ride_name, average_wait
UNION ALL 
select land_name, ride_name, average_wait, null best, GROUP_CONCAT(hour_logged order by hour_logged) worst_time
from legoland_avg_ride_wait_v l
where exists (
select null from (
select ride_name,  max(average_wait) shortest_wait
from legoland_avg_ride_wait_v
group by ride_name)
x where x.ride_Name = l.ride_name and l.average_wait = x.shortest_wait)
group by land_name, ride_name, average_wait
) y
group by land_name, ride_name
; 

select * from wait_time_fact_v
order by log_time desc
;

create or replace view live_wait_times_v as 
select land_name, 
		ride_name , 
		case when is_open = 1 then ride_wait_time else -1 end as ride_wait_time
from wait_time_fact_v dt
where lastUpdated = (select max(dtt.lastUpdated) from wait_time_fact_v dtt where dt.ride_name = dtt.ride_name)
and date(lastUpdated) = date(sysdate()) 
group by land_name, 
		ride_name , 
		case when is_open = 1 then ride_wait_time else -1 end 
order by ride_wait_time desc
;


create table location_lat_lon as
select 'Legoland' park_name, 
		'Flight of the Sky Lion' as ride_name, 
		 51.46339542 lat,
		 -0.6468901247 lon
		
		 ;
		 select * from all_ride_data_time order by run_date desc, run_time desc,  name ;
		 SELECT * FROM legoland_avg_ride_wait_v;
		
		-- there are some missing rides 
		-- but start with these 
		select * from land_ride_dim
		order by ride_name;
		
	
	
	live_wait_times_v;
	

create or replace view legoland_overall_waits_v as
select land_name, ride_name , round(avg(ride_wait_time)) average_wait, count(*) data_points
from wait_time_fact_v
where is_open = 1
group by  land_name, ride_name;

select * from legoland_overall_waits_v
order by land_name, ride_name; 

select * from wait_time_fact_v;

select * from legoland_avg_ride_wait_v
order by ride_name, hour_logged;

select * from land_ride_dim
order by land_name, ride_name;

select * from live_wait_times_v;


create or replace view live_wait_times_v as 
select land_name, 
		ride_name , 
		case when is_open = 1 then ride_wait_time else -1 end as ride_wait_time
from wait_time_fact_v dt
where exists (select null from 
(
select ride_name, max(dtt.lastUpdated) max_entry from wait_time_fact_v dtt group by ride_name
) dtt
where dt.ride_name = dtt.ride_name and dt.lastUpdated = dtt.max_entry
)
#(select max(dtt.lastUpdated) from wait_time_fact_v dtt where dt.ride_name = dtt.ride_name)
group by land_name, 
		ride_name , 
		case when is_open = 1 then ride_wait_time else -1 end 
order by ride_wait_time desc
;

create or replace view legoland_avg_ride_wait_today_v as
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , avg(ride_wait_time) average_wait
from wait_time_fact_v
where is_open = 1
and date(log_time) = date(sysdate())
group by  land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 order by hour_logged, land_name , ride_name;


## why are there so many entires?  
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , count(*)
from wait_time_fact_v
where is_open = 0
and date(log_time) = date(sysdate())
## hard code this to a set list of rides 
and ride_name not in ('Castaway Camp','Cole�s Rock Climb','Creature Creation','DUPLO� Playtown','LEGO� Reef',
						'Miniland','Pirate Goldwash','Remote Control Boats','The Brick','The Magical Forest','DUPLO� Valley Theatre'
						,'LEGO� Friends: Girls on a Mission','','','')
group by land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 
 order by hour_logged, land_name , ride_name;