create or replace view legoland_avg_ride_wait as
select ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , avg(ride_wait_time) average_wait
from wait_time_fact
where is_open = 1
group by  ride_name,  hour(CAST(log_time AS DATETIME))+1;