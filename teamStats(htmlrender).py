# Name: Auberon Orbock
# OSU Email: orbocka@oregonstate.edu
# Course: CS361
# Assignment 8: Microservice A
# Due Date: 11/18/24

from flask import Flask, jsonify, render_template
import requests
from config import Config
from flask_caching import Cache
import datetime

app = Flask(__name__)

# Test ID of team being looked up:
team_id = 'ad4ae08f-d808-42d5-a1e6-e9bc4e34d123'

# Set cache for one day:
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 86400})

# Helper function to get the current year:
def get_current_year():
    return datetime.date.today().strftime("%Y")

# Helper function to fetch data from API:
def fetch_data(url, api_key):
    try:
        response = requests.get(f"{url}?api_key={api_key}")
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Error occurred fetching data: {e}"

# Helper function to safely extract values:
def safe_get(data, key, default='N/A'):
    return data.get(key, default) if data else default

# Helper function to extract stats for different categories:
def extract_stats(data, category, subcategory=None):
    stats = safe_get(data, category, {})
    if subcategory:
        return safe_get(stats, subcategory, 'N/A')
    return stats or 'N/A'

# Rout and set cache:
@app.route('/teams/<team_id>/')
@cache.cached(timeout=60, key_prefix=f"team_{team_id}_year_{get_current_year()}_season_REG")
def get_team_stats(team_id):
    api_key = Config.SPORTRADAR_API_KEY
    year = get_current_year()
    current_season = 'REG'

    # Set SportRadar API URLs:
    statistics_url = f"https://api.sportradar.com/nfl/official/trial/v7/en/seasons/{year}/{current_season}/teams/{team_id}/statistics.json"
    standings_url = f"https://api.sportradar.com/nfl/official/trial/v7/en/seasons/{year}/{current_season}/standings/season.json"
    try:
        # Fetch data from SportRadar API (with error handling):
        statistics_data, statistics_error = fetch_data(statistics_url, api_key)
        standings_data, standings_error = fetch_data(standings_url, api_key)
        if statistics_error or standings_error:
            return statistics_error or standings_error

        # Get basic team info (and set initial default value for wins/losses/ties):
        team_info = {
            'name': safe_get(statistics_data, 'name'),
            'alias': safe_get(statistics_data, 'alias'),
            'market': safe_get(statistics_data, 'market')
        }
        # Get win/loss/tie record from standings and update their values in team_info{}:
        for conference in standings_data.get('conferences', []):
            for division in conference.get('divisions', []):
                for team in division.get('teams', []):
                    if team.get('id') == team_id:
                        team_info.update({
                            'wins': safe_get(team, 'wins'),
                            'losses': safe_get(team, 'losses'),
                            'ties': safe_get(team, 'ties')
                        })

        # Extract offensive stats:
        team_info.update({
            'passing_yards': extract_stats(statistics_data.get('record', {}), 'passing', 'yards'),
            'rushing_yards': extract_stats(statistics_data.get('record', {}), 'rushing', 'yards'),
            'receiving_yards': extract_stats(statistics_data.get('record', {}), 'receiving', 'yards'),
            'total_touchdowns': extract_stats(statistics_data.get('record', {}), 'touchdowns', 'total'),
            'passing_touchdowns': extract_stats(statistics_data.get('record', {}), 'touchdowns', 'pass'),
            'rushing_touchdowns': extract_stats(statistics_data.get('record', {}), 'touchdowns', 'rush'),
            'receiving_touchdowns': extract_stats(statistics_data.get('record', {}), 'receiving', 'touchdowns')
        })

        # Extract defensive stats:
        team_info.update({
            'sacks': extract_stats(statistics_data.get('record', {}), 'defense', 'sacks'),
            'interceptions': extract_stats(statistics_data.get('record', {}), 'defense', 'interceptions'),
            'forced_fumbles': extract_stats(statistics_data.get('record', {}), 'defense', 'forced_fumbles'),
            'opponents_passing_touchdowns': extract_stats(statistics_data.get('opponents', {}), 'touchdowns', 'pass'),
            'opponents_rushing_touchdowns': extract_stats(statistics_data.get('opponents', {}), 'touchdowns', 'rush'),
            'field_goals_made': extract_stats(statistics_data.get('record', {}), 'field_goals', 'made'),
            'kickoff_returns': extract_stats(statistics_data.get('record', {}), 'kickoffs', 'return_yards')
        })
        # Render stats:
        return render_template('team_stats.html', team_info=team_info)
        
    # If errors encountered, return error message
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'An error occurred while fetching team data: {e}'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)