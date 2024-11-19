This microservice allows you to request information about an NFL team, and receive a dictionary of their current season stats 
(using the SportRadar API).
To make a request of the microservice, the requesting program needs to have a team_id variable with the assigned value of 
a team ID compatable with the API, and have imported 'requests'. The request must be in the format: 
requests.get("http://localhost:5001/team_stats/{team_id}"), and the dictionary of stats will then be received in .json format.

<img width="708" alt="UML" src="https://github.com/user-attachments/assets/57bd9168-e194-47a7-81ef-e91a67902dc0">


The dictionary keys are:
'name'
'alias'
'market'
'wins'
losses'
'ties'
'passing_yards'
'rushing_yards'
'receiving_yards'
'total_touchdowns'
'passing_touchdowns'
'rushing_touchdowns'
'receiving_touchdowns'
'sacks'
'interceptions'
'forced_fumbles'
'opponents_passing_touchdowns'
'opponents_rushing_touchdowns'
'field_goals_made'
'kickoff_returns'

Example request/receive (with team_id='ad4ae08f-d808-42d5-a1e6-e9bc4e34d123'):
response = requests.get(http://localhost:5001/team_stats/ad4ae08f-d808-42d5-a1e6-e9bc4e34d123")
team_stats = response.json()
print("Team Stats:", team_stats)

Print results:
{'alias': 'CIN', 'field_goals_made': 15, 'forced_fumbles': 6, 'interceptions': 6, 'kickoff_returns': 288, 'losses': 7, 
'market': 'Cincinnati', 'name': 'Bengals', 'opponents_passing_touchdowns': 19, 'opponents_rushing_touchdowns': 15, 
'passing_touchdowns': 27, 'passing_yards': 2890, 'receiving_touchdowns': 27, 'receiving_yards': 3028, 'rushing_touchdowns': 
8, 'rushing_yards': 1007, 'sacks': 19.0, 'ties': 0, 'total_touchdowns': 36, 'wins': 4}
