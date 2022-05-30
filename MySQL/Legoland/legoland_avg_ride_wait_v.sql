create or replace view legoland_avg_ride_wait_v as
select land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1 as hour_logged , round(avg(ride_wait_time)) average_wait, count(*) data_points
from wait_time_fact_v
where is_open = 1
group by  land_name, ride_name,  hour(CAST(log_time AS DATETIME))+1;
