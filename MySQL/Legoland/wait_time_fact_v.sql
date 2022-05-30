create or replace view wait_time_fact_v as
select 	coalesce(fd.land_id,-99) land_id ,
		coalesce(fd.land_name,'Legoland') land_name, 
		id as ride_id, 
		name as ride_name, 
		CASE WHEN status = 'OPERATING' THEN 1 ELSE 0 END as isopen,
		run_time as log_time, 
		`queue.STANDBY.waitTime` as ride_wait_time, 
		run_date, 
		lastUpdated 		
from all_ride_data_time rdt
left outer join land_ride_dim fd on rdt.name = fd.ride_name
order by name; 