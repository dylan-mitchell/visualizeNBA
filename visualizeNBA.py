import requests
import json
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import flask
import os
import sys
import datetime

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))


colors = {
    'background': '#545556',
    'text': '#CECECE',
    'inputcolor': '#FF206E',
}

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True
app.title = "5x5Stats"

main_api = 'https://data.nba.net/'
year = '2018'
games = []

# http://data.nba.net/10s/prod/v1/today.json
today_api = main_api + '10s/prod/v1/today.json'
url = today_api
today_data = requests.get(url).json()
today_data = today_data['links']
# today = today_data['anchorDate']
today = datetime.datetime.today().strftime('%Y%m%d')



player_info_api = main_api + '10s/prod/v1/' + year + '/players.json'

url = player_info_api
json_data = requests.get(url).json()
json_data = json_data['league']
json_data = json_data['standard']

tab_style = {
    'backgroundColor': colors['background'],
    'padding': '6px',
    'color': colors['text'],
    'font-size': '1.2em',
    'border': 'none',
    'borderTop': '2px solid #CECECE',
}

tab_selected_style = {
    'border': 'none',
    'borderTop': '2px solid red',
    'backgroundColor': colors['background'],
    'color': colors['text'],
    'padding': '6px',
    'font-size': '1.2em'
}

tabs_styles = {
    'height': '44px',
    'width': '40%'
}


app.layout =  html.Div([
        html.Div(className='header', children=[
        html.Img(className='titleImg', src='assets\\5by5.png'),
        dcc.Tabs(id="tabs", value='tab-1', parent_className='custom-tabs', className='custom-tabs-container',children=[
        dcc.Tab(className='custom-tab', style=tab_style, selected_style=tab_selected_style, selected_className='custom-tab--selected', label='Today\'s Games', value='tab-1'),
        dcc.Tab(className='custom-tab', style=tab_style, selected_style=tab_selected_style, selected_className='custom-tab--selected', label='Current Player Stats', value='tab-2'),
        dcc.Tab(className='custom-tab', style=tab_style, selected_style=tab_selected_style, selected_className='custom-tab--selected', label='League Standings', value='tab-3'),
        ], style=tabs_styles),
        html.Div(id='tabs-content')]),
        html.Div(className='row', children=[html.Div(id="output-games", className='col s12 m6 l6')]),
        dcc.Interval(
            id='score-interval',
            interval=60*1*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='league-interval',
            interval=5*60*1*1000, # in milliseconds
            n_intervals=0
        )
        # html.H1(" "),
        # html.Div(className='footer', children=[
        #     html.H5("By Dylan Mitchell"),
        #     html.H5("Stats from data.nba.net"),
        #
        # ])

    ])

def player2graph(input_data):
    player_id = 0
    player = input_data.lower()
    for x in range(0, len(json_data)):
        player_data = json_data[x]
        if(player_data['lastName'].lower() == player or player_data['firstName'].lower() == player or player_data['firstName'].lower() + " " + player_data['lastName'].lower() == player):
            if len(player) > 1:
                player_id = player_data['personId']
                player = player_data['firstName'].lower() + " " + player_data['lastName'].lower()
                print(player_id)


    # http://data.nba.net/10s/prod/v1/2018/players/2544_profile.json is example of Lebron James
    individual_api = main_api + '10s/prod/v1/' + year + "/players/" + player_id + "_profile.json"
    url = individual_api
    player_data = requests.get(url).json()
    player_data = player_data['league']
    player_data = player_data['standard']
    player_data = player_data['stats']
    player_data = player_data['regularSeason']
    player_data = player_data['season']

    years = []
    ppg = []
    rpg = []
    apg = []
    bpg = []
    spg = []
    gamesPlayed = []

    for x in range(0, len(player_data)):
        # print(player_data[x])
        stats_data = player_data[x]
        syear = stats_data['seasonYear']
        stats_data = stats_data['total']

        print(str(syear) + ": " + str(stats_data['ppg']))
        if float(stats_data['ppg']) != 0:
            ppg.append(float(stats_data['ppg']))
            rpg.append(float(stats_data['rpg']))
            apg.append(float(stats_data['apg']))
            gamesPlayed.append(float(stats_data['gamesPlayed']))
            bpg.append(float(stats_data['bpg']))
            spg.append(float(stats_data['spg']))
            years.append(syear)



    ppg.reverse()
    rpg.reverse()
    apg.reverse()
    spg.reverse()
    years.reverse()
    gamesPlayed.reverse()
    bpg.reverse()

    tracePPG = go.Scatter(
        x = years,
        y = ppg,
        name = 'Points per Game',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
        )

    traceRPG = go.Scatter(
        x = years,
        y = rpg,
        name = 'Rebounds per Game',
        line = dict(
            color = ('rgb(65, 244, 172)'),
            width = 4)
        )

    traceAPG = go.Scatter(
        x = years,
        y = apg,
        name = 'Assists per Game',
        line = dict(
            color = ('rgb(0, 120, 124)'),
            width = 4)
        )

    traceGamesPlayed = go.Scatter(
        x = years,
        y = gamesPlayed,
        name = 'Games Played',
        line = dict(
            color = ('rgb(137, 66, 244)'),
            width = 4)
        )

    traceBPG = go.Scatter(
        x = years,
        y = bpg,
        name = 'Blocks per Game',
        line = dict(
            color = ('rgb(208, 242, 41)'),
            width = 4)
        )

    traceSPG = go.Scatter(
        x = years,
        y = spg,
        name = 'Steals per Game',
        line = dict(
            color = ('rgb(191, 66, 244)'),
            width = 4)
        )

    return dcc.Graph(
            figure=go.Figure(
                data=[traceGamesPlayed, tracePPG, traceRPG, traceAPG, traceBPG, traceSPG],
                layout=go.Layout(
                    title=player.upper(),
                    showlegend=True,
                    font={'color':colors['text'], },
                    plot_bgcolor = colors['background'],
                    paper_bgcolor = colors['background'],
                )
            ),
            style={'height': 800},
            id='my-graph',
            className='col s12 m12 l12'
        )

def generateGames(date):
    # http://data.nba.net/10s/prod/v1/20181016/scoreboard.json
    scoreboard_api = main_api + '10s/prod/v1/' + date + '/scoreboard.json'
    url = scoreboard_api
    scoreboard_data = requests.get(url).json()
    scoreboard_data = scoreboard_data['games']
    gameCount = 0

    for x in range(0,len(scoreboard_data)):
        gameCount += 1

    #                           0                   1         2           3             4           5                 6             7       8           9        10         11      12
    # List of game info EX:[Home Team Tri Code, Home Team ID, HomeWin, HomeLoss, HomeScore,  Away Team Tri Code, Away Team ID, AwayWin, AwayLoss, Away Score, Game Time, televised, clock]


    for x in range(0, gameCount):
        game_data = scoreboard_data[x]
        timeOfGame = game_data['startTimeEastern']
        period = game_data['period']
        televised = game_data['watch']
        televised = televised['broadcast']
        televised = televised['broadcasters']
        televised = televised['national']
        if len(televised) > 0:
            televised = televised[0]
            televised = televised['shortName']
        else:
            televised = "blank"

        home_team_data = game_data['vTeam']
        away_team_data = game_data['hTeam']


        if game_data['isGameActivated'] == False and home_team_data['score'] != '' and home_team_data['score'] != "0" :
             clock = "Game Ended" 
        elif game_data['isGameActivated'] == False:
            clock = " "
        elif game_data['isGameActivated'] == True:
            time = game_data['clock']
            if period['current'] == 1:
                clock = "1st " + str(time)
                if period['isEndOfPeriod'] == True:
                    clock = "End of the 1st"
            if period['current'] == 2:
                clock = "2nd " + str(time)
                if period['isEndOfPeriod'] == True:
                    clock = "HalfTime"
            if period['current'] == 3:
                clock = "3rd " + str(time)
                if period['isEndOfPeriod'] == True:
                    clock = "End of the 3rd"
            if period['current'] == 4:
                clock = "4th " + str(time)
                if period['isEndOfPeriod'] == True:
                    clock = "Game Ended"   
        


        games.append([home_team_data['triCode'], home_team_data['teamId'], home_team_data['win'], home_team_data['loss'], home_team_data['score'], away_team_data['triCode'], away_team_data['teamId'], away_team_data['win'], away_team_data['loss'], away_team_data['score'], timeOfGame, televised, clock])
        print("Added Game: " + games[x][1] + " VS " + games[x][6])
    return games


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-2':
        return html.Div(className='currentStats', children=[
            html.H2('NBA Stats'),
            dcc.Input(id='input', value='', type='text', placeholder='Enter Current NBA Player Name', style={'color':colors['inputcolor']}),
            html.Div(id='output-graph')])

    elif tab == 'tab-1':
        global games
        global today
        games.clear()
        games = generateGames(today)
        return html.Div(id='output', children=[
                html.Div(id='todaysGames'),
                 dcc.Dropdown(
                    id='gameDropdown',
                    options=[
                        {'label': games[x][0] + ' VS ' + games[x][5], 'value': games[x][0] + ' VS ' + games[x][5]} for x in range(0,len(games))
                        ],
                    placeholder="Select a game to analyze...",
                    searchable=False
                    ),
                html.H1(""),
                html.Div(id='output-trends')
        ])

    elif tab == 'tab-3':
        return html.Div(id='league-output', children=[
                html.H2("League Standings"),
                html.Div(id='league-graph')
        ])

@app.callback(
    Output('todaysGames', 'children'),
    [Input('score-interval', 'n_intervals')])
def update_today(n):
    try:
        global games
        global today
        games.clear()
        games = generateGames(today)
        return html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th("Home"),
                                      html.Th("Away"),
                                      html.Th("Time"),
                                      html.Th("Score"),
                                      html.Th(""),
                                      html.Th("")],
                                  style={'color':colors['text']}
                                  )
                              ),
                          html.Tbody(
                              [

                              html.Tr(
                                  children=[
                                    #   Home Logo
                                      html.Td(html.Img(className='logo', src='assets\\' + games[x][0] + '.png' )),
                                    #   Away Logo
                                      html.Td(html.Img(className='logo', src='assets\\' + games[x][5] + '.png' )),
                                    #   Game Time Start
                                      html.Td(games[x][10]),
                                    #   Game Score
                                      html.Td(games[x][4] + " - " + games[x][9]),
                                    #   Time Remaining in Game
                                      html.Td(games[x][12]),
                                    #   National TV schedule Logo
                                      html.Td(html.Img(src='assets\\' + games[x][11] + '.png' ))
                                      ], style={'color':colors['text']}
                                  )for x in range(0,len(games))])
                          ]
                          )
    except:
        return "Oops... something went wrong :("


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')])
def updateStatChart(input_data):
    try:
        return player2graph(input_data)
    except:
        if(len(input_data)>0):
            return ""

@app.callback(
    Output('output-trends', 'children'),
    [Input('gameDropdown', 'value')])
def update_output(gameName):
    game = []
    for x in range(0, len(games)-1):
        name = games[x][0] + ' VS ' + games[x][5]
        if name == gameName:
            game = games[x]

    # http://data.nba.net/10s/prod/2018/teams_config.json
    teams_api = main_api + '10s/prod/' + year + '/teams_config.json'
    url = teams_api
    teams_data = requests.get(url).json()
    teams_data = teams_data['teams']
    teams_data = teams_data['config']


    for x in range(0, 47):
        team_data = teams_data[x]
        try:
            if team_data['teamId'] == game[1]:
                color1 = team_data['primaryColor']
            if team_data['teamId'] == game[6]:
                color2 = team_data['primaryColor']
        except:
            # Do Nothing
            count = 0

    # http://data.nba.net/10s/prod/v1/2018/team_stats_rankings.json
    teams_api = main_api + '10s/prod/v1/' + year + '/team_stats_rankings.json'
    url = teams_api
    teams_data = requests.get(url).json()
    teams_data = teams_data['league']
    teams_data = teams_data['standard']
    teams_data = teams_data['regularSeason']
    teams_data = teams_data['teams']

    for x in range(0, len(teams_data)):
        team_data = teams_data[x]
        if team_data['teamId'] == game[1]:
            team1ppg = team_data['ppg']
            team1ppg = team1ppg['avg']
            team1oppg = team_data['oppg']
            team1oppg = team1oppg['avg']
            team1apg = team_data['apg']
            team1apg = team1apg['avg']
            team1trpg = team_data['trpg']
            team1trpg = team1trpg['avg']
        if team_data['teamId'] == game[6]:
            team2ppg = team_data['ppg']
            team2ppg = team2ppg['avg']
            team2oppg = team_data['oppg']
            team2oppg = team2oppg['avg']
            team2apg = team_data['apg']
            team2apg = team2apg['avg']
            team2trpg = team_data['trpg']
            team2trpg = team2trpg['avg']



    #                           0                   1         2           3             4           5                 6             7       8           9        10         11      12
    # List of game info EX:[Home Team Tri Code, Home Team ID, HomeWin, HomeLoss, HomeScore,  Away Team Tri Code, Away Team ID, AwayWin, AwayLoss, Away Score, Game Time, televised, clock]

    x = ['Wins', 'Losses', "Points per Game", "Oppenent Points per Game", "Assist per Game", "Rebounds per Game"]
    y = [game[2], game[3], team1ppg, team1oppg, team1apg, team1trpg]
    y2 = [game[7], game[8], team2ppg, team2oppg, team2apg, team2trpg]

    trace1 = go.Bar(
        name = game[0],
        x=x,
        y=y,
        text=game[0],
        textposition = 'auto',
        marker=dict(
            color=color1,
            line=dict(
                color=color1,
                width=.5),
            ),
        opacity=0.6
    )

    trace2 = go.Bar(
        name = game[5],
        x=x,
        y=y2,
        text=game[5],
        textposition = 'auto',
        marker=dict(
            color=color2,
            line=dict(
                color=color2,
                width=.5),
            ),
        opacity=0.6
        )

    return dcc.Graph(
                figure=go.Figure(
                    data=[trace1, trace2],
                    layout=go.Layout(
                        title=game[0] + ' VS ' + game[5],
                        showlegend=True,
                        font={'color':colors['text']},
                        plot_bgcolor = colors['background'],
                        paper_bgcolor = colors['background'],
                    )
                ),
                style={'height': 800},
                id='trend-graph',
                className='col s12 m12 l12'
            )

@app.callback(
    Output('league-graph', 'children'),
    [Input('league-interval', 'n_intervals')])
def update_standings(n):

# http://data.nba.net/10s/prod/v1/current/standings_conference.json
    league_standings_api = main_api + '/10s/prod/v1/current/standings_conference.json'

    url = league_standings_api
    league_data = requests.get(url).json()
    league_data = league_data['league']
    league_data = league_data['standard']
    league_data = league_data['conference']
    east_data = league_data['east']
    west_data = league_data['west']
    
    idEast = []
    winEast = []
    lossEast = []
    streakEast = []

    for x in range(0, 15):
        team_data = east_data[x]
        idEast.append(team_data['teamId'])
        winEast.append(team_data['win'])
        lossEast.append(team_data['loss'])
        streakEast.append(team_data['streak'])

    idWest = []
    winWest = []
    lossWest = []
    streakWest = []

    for x in range(0, 15):
        team_data = west_data[x]
        idWest.append(team_data['teamId'])
        winWest.append(team_data['win'])
        lossWest.append(team_data['loss'])
        streakWest.append(team_data['streak'])

    colorsEast = []
    colorsWest = []

    teams_api = main_api + '10s/prod/' + year + '/teams_config.json'
    url = teams_api
    teams_data = requests.get(url).json()
    teams_data = teams_data['teams']
    teams_data = teams_data['config']
    

    for x in range(0, len(idEast) - 1):
        for y in range(0, 48):
            team_data = teams_data[y]
            if team_data['teamId'] == idEast[x]:
                colorsEast.append(team_data['primaryColor'])
            if team_data['teamId'] == idWest[x]:
                colorsWest.append(team_data['primaryColor'])    
       


    return html.H2("Coming Soon!")


app.scripts.append_script({
'external_url': 'assets\\gtag.js'
})

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
