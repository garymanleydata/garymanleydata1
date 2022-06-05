create or replace view legoland_overall_waits_v as
select 	land_name, 
		ride_name , 
		round(avg(ride_wait_time)) average_wait, 
		count(*) data_points, 
		round(avg(case when c.peak_ind =  'Peak' THEN ride_wait_time else NULL END)) average_wait_peak, 
		round(avg(case when c.peak_ind =  'Off-Peak' THEN ride_wait_time else NULL END)) average_wait_off_peak
from wait_time_fact_v v
inner join calendar_dim c on v.run_date = c.date
where is_open = 1
group by  land_name, ride_name;