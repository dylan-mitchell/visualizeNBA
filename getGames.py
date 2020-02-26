import datetime
import urllib.parse
import requests
import json

main_api = 'https://data.nba.net/'

today = datetime.datetime.today().strftime('%Y%m%d')
print(today)

# http://data.nba.net/10s/prod/v1/20181016/scoreboard.json
scoreboard_api = main_api + '10s/prod/v1/' + today + '/scoreboard.json'
url = scoreboard_api
scoreboard_data = requests.get(url, timeout=5).json()
scoreboard_data = scoreboard_data['games']
gameCount = 0

for x in range(0,len(scoreboard_data)):
    gameCount += 1

#                           0                   1       2           3               4           5
# List of game info EX:[Home Team Tri Code, HomeWin, HomeLoss, Away Team Tri Code, AwayWin, AwayLoss]
games = []

for x in range(0, gameCount - 1):
    game_data = scoreboard_data[x]
    home_team_data = game_data['vTeam']
    away_team_data = game_data['hTeam']
    games.append([home_team_data['triCode'], home_team_data['win'], home_team_data['loss'], away_team_data['triCode'], away_team_data['win'], away_team_data['loss']])
    print("Added Game: " + games[x][0] + " VS " + games[x][3])
