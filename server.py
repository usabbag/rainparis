"""
Flask server for Rain Paris - Minimalist rain forecast app
"""
import os
import logging
from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
from arrondissements import ARRONDISSEMENTS, get_coordinates

load_dotenv()
API_KEY = os.getenv('TOMORROW_API_KEY')

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html', arrondissements=ARRONDISSEMENTS)


@app.route('/api/weather/<int:arr_number>')
def get_weather(arr_number):
    """Get weather data for an arrondissement"""
    try:
        # Check if API key is configured
        if not API_KEY:
            logger.error("TOMORROW_API_KEY not configured")
            return jsonify({'error': 'API key not configured'}), 500

        coords = get_coordinates(arr_number)
        if not coords:
            return jsonify({'error': 'Invalid arrondissement'}), 404

        lat, lon = coords
        logger.info(f"Fetching weather for arrondissement {arr_number} ({lat}, {lon})")

        # Fetch realtime weather
        realtime_url = "https://api.tomorrow.io/v4/weather/realtime"
        realtime_params = {
            "location": f"{lat},{lon}",
            "apikey": API_KEY
        }

        try:
            realtime_response = requests.get(realtime_url, params=realtime_params, timeout=10)
            logger.info(f"Realtime API status: {realtime_response.status_code}")

            if realtime_response.status_code != 200:
                logger.error(f"Realtime API error: {realtime_response.text}")
                return jsonify({'error': f'Weather API returned {realtime_response.status_code}'}), 500

            realtime_data = realtime_response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Realtime API request failed: {str(e)}")
            return jsonify({'error': 'Failed to connect to weather service'}), 500

        # Fetch minutely forecast
        timeline_url = "https://api.tomorrow.io/v4/timelines"
        timeline_params = {
            "location": f"{lat},{lon}",
            "fields": "precipitationIntensity,precipitationProbability",
            "timesteps": "1m",
            "startTime": "now",
            "endTime": "nowPlus1h",
            "units": "metric",
            "timezone": "Europe/Paris",
            "apikey": API_KEY
        }

        try:
            timeline_response = requests.get(timeline_url, params=timeline_params, timeout=10)
            logger.info(f"Timeline API status: {timeline_response.status_code}")

            if timeline_response.status_code != 200:
                logger.error(f"Timeline API error: {timeline_response.text}")
                return jsonify({'error': f'Forecast API returned {timeline_response.status_code}'}), 500

            timeline_data = timeline_response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Timeline API request failed: {str(e)}")
            return jsonify({'error': 'Failed to connect to forecast service'}), 500

        # Process data
        try:
            current_values = realtime_data['data']['values']
            intervals = timeline_data['data']['timelines'][0]['intervals']

            # Generate rain summary
            summary = generate_rain_summary(intervals)

            # Prepare chart data (every minute for next hour)
            chart_data = []
            for interval in intervals:
                time = datetime.fromisoformat(interval['startTime'].replace('Z', '+00:00'))
                precip = interval['values'].get('precipitationIntensity', 0)
                chart_data.append({
                    'time': time.strftime('%H:%M'),
                    'precipitation': precip
                })

            return jsonify({
                'temperature': current_values.get('temperature'),
                'precipitation': current_values.get('precipitationIntensity', 0),
                'summary': summary,
                'chart_data': chart_data
            })
        except (KeyError, IndexError) as e:
            logger.error(f"Data processing error: {str(e)}")
            logger.error(f"Realtime data: {realtime_data}")
            logger.error(f"Timeline data: {timeline_data}")
            return jsonify({'error': 'Invalid data structure from weather API'}), 500

    except Exception as e:
        logger.error(f"Unexpected error in get_weather: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


def generate_rain_summary(intervals):
    """Generate DarkSky-style rain summary"""
    current_precip = intervals[0]['values'].get('precipitationIntensity', 0)

    # Find when rain starts or stops
    for i, interval in enumerate(intervals):
        precip = interval['values'].get('precipitationIntensity', 0)

        if current_precip == 0 and precip > 0:
            return f"Rain starting in {i} minute{'s' if i != 1 else ''}"
        elif current_precip > 0 and precip == 0:
            return f"Rain stopping in {i} minute{'s' if i != 1 else ''}"

    if current_precip > 0:
        return "Rain for the next hour"
    else:
        return "No rain for the next hour"


if __name__ == '__main__':
    # Use PORT environment variable for production, fallback to 5001 for local dev (5000 is used by AirPlay on macOS)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=os.environ.get('FLASK_ENV') != 'production', host='0.0.0.0', port=port)
