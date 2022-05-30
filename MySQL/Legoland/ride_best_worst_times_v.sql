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