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