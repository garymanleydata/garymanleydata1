Create TABLE weather (	
LocationName	VARCHAR(100),
LocationRegion	VARCHAR(100),
LocationCountry	VARCHAR(100),
LocationLat	FLOAT,
LocationLon	FLOAT,
LocationTzId	VARCHAR(100),
LocationLocaltimeEpoch	FLOAT,
LocationLocaltime	FLOAT,
CurrentLastUpdatedEpoch	FLOAT,
CurrentLastUpdated	FLOAT,
CurrentTempC	FLOAT,
CurrentTempF	FLOAT,
CurrentIsDay	FLOAT,
CurrentConditionText	VARCHAR(100),
CurrentConditionIcon	VARCHAR(200),
CurrentConditionCode	FLOAT,
CurrentWindMph	FLOAT,
CurrentWindKph	FLOAT,
CurrentWindDegree	FLOAT,
CurrentWindDir	VARCHAR(100),
CurrentPressureMb	FLOAT,
CurrentPressureIn	FLOAT,
CurrentPrecipMm	FLOAT,
CurrentPrecipIn	FLOAT,
CurrentHumidity	FLOAT,
CurrentCloud	FLOAT,
CurrentFeelslikeC	FLOAT,
CurrentFeelslikeF	FLOAT,
CurrentVisKm	FLOAT,
CurrentVisMiles	FLOAT,
CurrentUv	FLOAT,
CurrentGustMph	FLOAT,
CurrentGustKph	FLOAT,
CurrentAirQualityCo	FLOAT,
CurrentAirQualityNo2	FLOAT,
CurrentAirQualityO3	FLOAT,
CurrentAirQualitySo2	FLOAT,
CurrentAirQualityPm25	FLOAT,
CurrentAirQualityPm10	FLOAT,
CurrentAQUsepaindex	FLOAT,
CurrentAQGbdefraindex	FLOAT);

DROP table weather;

Create TABLE weather (	
LocationName	VARCHAR(100),
LocationRegion	VARCHAR(100),
LocationCountry	VARCHAR(100),
LocationLat	VARCHAR(100),
LocationLon	VARCHAR(100),
LocationTzId	VARCHAR(100),
LocationLocaltimeEpoch	VARCHAR(100),
LocationLocaltime	VARCHAR(100),
CurrentLastUpdatedEpoch	VARCHAR(100),
CurrentLastUpdated	VARCHAR(100),
CurrentTempC	VARCHAR(100),
CurrentTempF	VARCHAR(100),
CurrentIsDay	VARCHAR(100),
CurrentConditionText	VARCHAR(100),
CurrentConditionIcon	VARCHAR(200),
CurrentConditionCode	VARCHAR(100),
CurrentWindMph	VARCHAR(100),
CurrentWindKph	VARCHAR(100),
CurrentWindDegree	VARCHAR(100),
CurrentWindDir	VARCHAR(100),
CurrentPressureMb	VARCHAR(100),
CurrentPressureIn	VARCHAR(100),
CurrentPrecipMm	VARCHAR(100),
CurrentPrecipIn	VARCHAR(100),
CurrentHumidity	VARCHAR(100),
CurrentCloud	VARCHAR(100),
CurrentFeelslikeC	VARCHAR(100),
CurrentFeelslikeF	VARCHAR(100),
CurrentVisKm	VARCHAR(100),
CurrentVisMiles	VARCHAR(100),
CurrentUv	VARCHAR(100),
CurrentGustMph	VARCHAR(100),
CurrentGustKph	VARCHAR(100),
CurrentAirQualityCo	VARCHAR(100),
CurrentAirQualityNo2	VARCHAR(100),
CurrentAirQualityO3	VARCHAR(100),
CurrentAirQualitySo2	VARCHAR(100),
CurrentAirQualityPm25	VARCHAR(100),
CurrentAirQualityPm10	VARCHAR(100),
CurrentAQUsepaindex	VARCHAR(100),
CurrentAQGbdefraindex	VARCHAR(100));

select * from stg_weather sw ;

select location_name, location_region  , location_country  , location_lat  , location_lon  , current_last_updated  , current_temp_c  , current_condition_text , current_wind_mph , current_precip_mm  , current_humidity  , current_cloud , current_feelslike_c  from stg_weather
;
select location_name locationName, location_region LocationRegion , location_country LocationCountry , location_lat latitude , location_lon longitude , current_last_updated currentLastUpdated , current_temp_c currentTempC , current_condition_text currentCondText, current_wind_mph windMph , current_precip_mm rainMM , current_humidity humidity , current_cloud cloud , current_feelslike_c feelsLikeC  from stg_weather
;

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
	from pre_stg_strava ps where not exists (select null from stg_strava ss where ss.id = ps.id ); 
	

## Create an ETL group table, have insert into this upon completion of steps in the ETL package
## This can be used to get last run date and hold config 
## And put exception handling in the python code 
## have functions to be called by python - ETL to run. Pass back true / false 

select parkrun_place , event_date, age_category , parkrun_number , event_time , parkrun_position , age_rating from v_parkrun_processed vpp ;

SELECT parkrun_place , event_date, age_category , parkrun_number , event_time , parkrun_position  from v_parkrun_processed