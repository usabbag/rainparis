"""
Simple test script to verify Tomorrow.io API works
"""
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('TOMORROW_API_KEY')
if not API_KEY:
    raise ValueError("TOMORROW_API_KEY not found in .env file")

# Paris center coordinates
PARIS_LAT = 48.8566
PARIS_LON = 2.3522

def test_realtime_weather():
    """Test the Realtime API - current weather conditions"""
    print("\n=== TESTING REALTIME API ===")

    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {
        "location": f"{PARIS_LAT},{PARIS_LON}",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        values = data['data']['values']

        print(f"✓ API working!")
        print(f"Location: Paris, France")
        print(f"Time: {data['data']['time']}")
        print(f"\nCurrent conditions:")
        print(f"  Precipitation Intensity: {values.get('precipitationIntensity', 0)} mm/hr")
        print(f"  Temperature: {values.get('temperature', 'N/A')}°C")
        print(f"  Weather Code: {values.get('weatherCode', 'N/A')}")

        return True
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def test_minutely_forecast():
    """Test the Timeline API - minute-by-minute forecast"""
    print("\n=== TESTING MINUTELY FORECAST ===")

    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "location": f"{PARIS_LAT},{PARIS_LON}",
        "fields": "precipitationIntensity,precipitationProbability,precipitationType",
        "timesteps": "1m",
        "startTime": "now",
        "endTime": "nowPlus1h",
        "units": "metric",
        "timezone": "Europe/Paris",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        timeline = data['data']['timelines'][0]
        intervals = timeline['intervals']

        print(f"✓ Got {len(intervals)} minute-by-minute data points")
        print(f"\nNext 10 minutes:")

        for i, interval in enumerate(intervals[:10]):
            time = datetime.fromisoformat(interval['startTime'].replace('Z', '+00:00'))
            values = interval['values']
            precip = values.get('precipitationIntensity', 0)
            prob = values.get('precipitationProbability', 0)

            rain_status = "🌧️ RAIN" if precip > 0 else "☀️ dry"
            print(f"  {time.strftime('%H:%M')} - {precip:.2f} mm/hr ({prob}% chance) {rain_status}")

        # Summary
        any_rain = any(interval['values'].get('precipitationIntensity', 0) > 0
                      for interval in intervals)

        if any_rain:
            first_rain = next((i for i, interval in enumerate(intervals)
                             if interval['values'].get('precipitationIntensity', 0) > 0), None)
            print(f"\n⚠️  Rain detected in {first_rain} minutes!" if first_rain else "\n🌧️ Rain is happening now!")
        else:
            print(f"\n☀️  No rain expected in the next hour")

        return True
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return False


if __name__ == "__main__":
    print("Tomorrow.io API Test for Paris Rain Tracker")
    print("=" * 50)

    # Test both endpoints
    test_realtime_weather()
    test_minutely_forecast()

    print("\n" + "=" * 50)
    print("Tests complete!")
