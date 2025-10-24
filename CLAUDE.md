# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rain Paris is a DarkSky-inspired weather application providing minute-by-minute rain forecasts for Paris arrondissements. It features two interfaces: a minimalist web app and a CLI tool.

## Core Architecture

### Data Flow

The application has a single source of truth for Paris arrondissement coordinates (`arrondissements.py`) that feeds into two independent interfaces:

1. **Web Interface** (`server.py` → `templates/index.html` → `static/js/app.js`)
   - Flask serves a single-page app
   - Frontend makes AJAX calls to `/api/weather/<arr_number>`
   - Server fetches from two Tomorrow.io endpoints in parallel:
     - Realtime API: current conditions
     - Timeline API: minute-by-minute forecast (1m timestep, next hour)
   - Data processed server-side, then sent to frontend for Chart.js visualization

2. **CLI Tool** (`rainparis` executable)
   - Standalone Python script with same API logic as web server
   - Uses argparse for command-line interface
   - Formats output with emoji and terminal-friendly tables

### Tomorrow.io API Integration

**Critical Rate Limits:**
- 25 requests/hour (most restrictive)
- 500 requests/day
- 3 requests/second

**API Endpoints Used:**
- `https://api.tomorrow.io/v4/weather/realtime` - Current conditions
- `https://api.tomorrow.io/v4/timelines` - Minutely forecasts

**Required Parameters:**
- `location`: `{lat},{lon}` format
- `timesteps`: `"1m"` for minute-by-minute (limited to 24h window)
- `timezone`: `"Europe/Paris"`
- `apikey`: From `.env` file

### DarkSky-Style Rain Summary Algorithm

Located in both `server.py` and `rainparis` CLI (duplicated for independence):

```python
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
```

This algorithm iterates through minute-by-minute intervals to detect state changes (dry→rain or rain→dry).

### Paris Arrondissements Data

`arrondissements.py` contains hardcoded center coordinates for all 20 Paris arrondissements, sourced from OpenDataSoft. The dictionary structure is:

```python
ARRONDISSEMENTS = {
    1: {"name": "1er - Louvre", "lat": 48.8625627018, "lon": 2.33644336205},
    # ... 2-20
}
```

Helper functions:
- `get_arrondissement(number)` - Returns dict for single arrondissement
- `get_coordinates(number)` - Returns `(lat, lon)` tuple
- `get_all_arrondissements()` - Returns list of all

## Common Commands

### Development

**Run web server:**
```bash
python server.py
# Opens on http://localhost:5000
# Debug mode enabled by default (auto-reloads on code changes)
```

**Run CLI tool:**
```bash
./rainparis 11              # Check 11th arrondissement
./rainparis 2 -v            # Verbose mode (minute-by-minute table)
./rainparis --list          # List all arrondissements
```

**Install CLI globally:**
```bash
pip install -e .
# Now 'rainparis' works from any directory
```

### Testing

**Test API connection:**
```bash
python test_api.py
# Tests both Realtime and Timeline APIs for Paris center
```

**Test multiple arrondissements:**
```bash
python test_arrondissement.py
# Tests 3 arrondissements (stays within API limits)
```

### Setup

**First-time setup:**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Tomorrow.io API key
```

## Key Technical Details

### Why Two Separate Interfaces?

The web server and CLI tool are intentionally independent (code duplication exists) to allow:
- CLI tool to be a standalone executable without Flask dependency
- Each interface to be deployed/distributed separately
- CLI to work even if web server is down/not installed

### Frontend Architecture (Web UI)

The web interface is deliberately minimalist:
- **No frontend framework** (React, Vue, etc.) - pure vanilla JS
- **Single Chart.js dependency** for precipitation visualization
- **No build step** - HTML/CSS/JS served directly
- **Client-side rendering** - all formatting happens in browser

This keeps the app lightweight and maintains the Apple/Notion-inspired aesthetic.

### Design Philosophy

The UI follows these principles:
- Minimalism over features
- Large, thin typography (system fonts)
- Generous whitespace
- Gradient backgrounds (#667eea to #764ba2)
- 24px border-radius for cards
- Subtle animations (0.4s ease transitions)

## Environment Variables

Required in `.env`:
```
TOMORROW_API_KEY=your_key_here
```

Get a free key at: https://www.tomorrow.io/

## Important Constraints

1. **API Rate Limits**: Always respect 25 req/hour limit. Consider caching if adding new features.
2. **Minute-by-minute timestep**: Only works for 24h windows (API limitation)
3. **Timezone**: All forecasts use `Europe/Paris` timezone
4. **Arrondissement Count**: Hardcoded to 20 (Paris administrative division)

## When Adding Features

- If modifying rain summary logic, update BOTH `server.py` and `rainparis` CLI
- Test with multiple arrondissements (not just #1) due to geographic variance
- Consider API rate limits when adding new data fetches
- Maintain design minimalism - avoid adding UI clutter
