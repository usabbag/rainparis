pip install openmeteo-requests
pip install requests-cache retry-requests numpy pandas

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"daily": ["rain_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max"],
	"hourly": ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers"],
	"models": ["meteofrance_arome_france", "meteofrance_arome_france_hd", "best_match"],
	"current": ["precipitation", "rain"],
	"minutely_15": ["rain", "precipitation", "snowfall"],
}
responses = openmeteo.weather_api(url, params=params)

# Process 1 location and 3 models
for response in responses:
	print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
	print(f"Model Nº: {response.Model()}")
	
	# Process current data. The order of variables needs to be the same as requested.
	current = response.Current()
	current_precipitation = current.Variables(0).Value()
	current_rain = current.Variables(1).Value()
	
	print(f"\nCurrent time: {current.Time()}")
	print(f"Current precipitation: {current_precipitation}")
	print(f"Current rain: {current_rain}")
	
	# Process minutely_15 data. The order of variables needs to be the same as requested.
	minutely_15 = response.Minutely15()
	minutely_15_rain = minutely_15.Variables(0).ValuesAsNumpy()
	minutely_15_precipitation = minutely_15.Variables(1).ValuesAsNumpy()
	minutely_15_snowfall = minutely_15.Variables(2).ValuesAsNumpy()
	
	minutely_15_data = {"date": pd.date_range(
		start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
		end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = minutely_15.Interval()),
		inclusive = "left"
	)}
	
	minutely_15_data["rain"] = minutely_15_rain
	minutely_15_data["precipitation"] = minutely_15_precipitation
	minutely_15_data["snowfall"] = minutely_15_snowfall
	
	minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
	print("\nMinutely15 data\n", minutely_15_dataframe)
	
	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
	hourly_rain = hourly.Variables(3).ValuesAsNumpy()
	hourly_showers = hourly.Variables(4).ValuesAsNumpy()
	
	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["rain"] = hourly_rain
	hourly_data["showers"] = hourly_showers
	
	hourly_dataframe = pd.DataFrame(data = hourly_data)
	print("\nHourly data\n", hourly_dataframe)
	
	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_rain_sum = daily.Variables(0).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()
	daily_precipitation_hours = daily.Variables(2).ValuesAsNumpy()
	daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
	
	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	
	daily_data["rain_sum"] = daily_rain_sum
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["precipitation_hours"] = daily_precipitation_hours
	daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
	
	daily_dataframe = pd.DataFrame(data = daily_data)
	print("\nDaily data\n", daily_dataframe)
