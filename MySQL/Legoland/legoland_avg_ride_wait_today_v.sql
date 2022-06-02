create or replace view legoland_avg_ride_wait_today_v as
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , avg(ride_wait_time) average_wait
from wait_time_fact_v
where is_open = 1
and date(run_date) = date(sysdate())
group by  land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 order by hour_logged, land_name , ride_name;