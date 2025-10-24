"""
Test fetching weather data for different Paris arrondissements
"""
import os
import requests
from dotenv import load_dotenv
from arrondissements import get_arrondissement, get_coordinates

load_dotenv()
API_KEY = os.getenv('TOMORROW_API_KEY')

def get_rain_for_arrondissement(number):
    """Get current rain status for an arrondissement"""
    coords = get_coordinates(number)
    if not coords:
        return None

    lat, lon = coords
    arr = get_arrondissement(number)

    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {
        "location": f"{lat},{lon}",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        values = data['data']['values']
        precip = values.get('precipitationIntensity', 0)
        temp = values.get('temperature', 'N/A')

        return {
            "name": arr['name'],
            "precip": precip,
            "temp": temp,
            "is_raining": precip > 0
        }
    return None

if __name__ == "__main__":
    # Test a few arrondissements
    test_arr = [1, 11, 18]  # Louvre, Popincourt, Montmartre

    print("Rain Status Across Paris Arrondissements")
    print("=" * 60)

    for num in test_arr:
        result = get_rain_for_arrondissement(num)
        if result:
            rain_icon = "🌧️" if result['is_raining'] else "☀️"
            print(f"{rain_icon} {result['name']:30s} {result['precip']:.2f} mm/hr, {result['temp']}°C")

    print("\nNote: Testing only 3 arrondissements to stay within API limits")
