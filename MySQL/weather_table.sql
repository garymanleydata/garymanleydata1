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

select * from weather

