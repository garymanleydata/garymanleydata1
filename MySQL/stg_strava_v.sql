create or replace view stg_strava_v as
select 	name,
		distance,
		moving_time,
		elapsed_time,
		total_elevation_gain,
		`type`,
		id,
		start_date_local,
		average_speed,
		max_speed,
		average_cadence,
		average_heartrate,
		max_heartrate,
		elev_high,
		elev_low,
		upload_id,
		upload_id_str
	from pre_stg_strava ps where not exists (select null from stg_strava ss where ss.id = ps.id )