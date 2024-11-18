import requests

team_id = 'ad4ae08f-d808-42d5-a1e6-e9bc4e34d123' # Holds id of team being requested
url = f"http://localhost:5001/team_stats/{team_id}" # URL to request

# Try sending request:
try:
    response = requests.get(url) # Send request
    
    # Check if the response was successful or not:
    if response.status_code == 200:
        team_stats = response.json()
        print("Team Stats:", team_stats)
    else:
        print(f"Failed to retrieve team stats: HTTP {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
