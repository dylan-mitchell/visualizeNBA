from basketball_reference_web_scraper import client
from operator import itemgetter


# box_scores = client.player_box_scores(day=1, month=1, year=2017)
# print('***** BOX SCORES *****')
# for box_score in box_scores[:10]:
#   print(box_score)

# print('***** GAMES *****')
# games = client.season_schedule(season_end_year=2019)
# for game in games[:10]:
#   print(game)

def getMoreStats(season_stats):
    for player_totals in season_stats:
        twoPointers = (player_totals['made_field_goals'] - player_totals['made_three_point_field_goals'])*2
        threePointers = player_totals['made_three_point_field_goals']*3
        points = twoPointers + threePointers + player_totals['made_free_throws']
        points_per_game = round(points/player_totals['games_played'], 1)
        assists_per_game = round(player_totals['assists']/player_totals['games_played'], 1)
        blocks_per_game = round(player_totals['blocks']/player_totals['games_played'], 1)
        steals_per_game = round(player_totals['steals']/player_totals['games_played'], 1)
        total_rebounds = player_totals['offensive_rebounds'] + player_totals['defensive_rebounds']

        player_totals.update({'points':points, 'points_per_game':points_per_game, 'assists_per_game':assists_per_game, 'blocks_per_game':blocks_per_game, 'steals_per_game':steals_per_game, 'total_rebounds':total_rebounds})

    return season_stats

def getLeagueTotals(season_stats):
    leaguePoints = 0
    leagueAssists = 0
    leagueTurnovers = 0
    leagueFGA = 0
    leagueFGM = 0
    leagueFTM = 0
    leagueORB = 0
    leagueFTA = 0
    leagueTRB = 0
    leaguePF = 0
    for player in season_stats:
        leaguePoints += player['points']
        leagueAssists += player['assists']
        leagueTurnovers += player['turnovers']
        leagueFGA += player['attempted_field_goals']
        leagueFGM += player['made_field_goals']
        leagueFTM += player['made_free_throws']
        leagueFTA += player['attempted_free_throws']
        leagueORB += player['offensive_rebounds']
        leagueTRB += player['total_rebounds']
        leaguePF += player['personal_fouls']

    leagueTotals = {
		"leaguePoints" : leaguePoints,
		"leagueAssists" : leagueAssists,
		"leagueTurnovers" : leagueTurnovers,
		"leagueFGA" : leagueFGA,
		"leagueFGM" : leagueFGM,
		"leagueFTM" : leagueFTM,
        "leagueFTA" : leagueFTA,
        "leagueORB" : leagueORB,
        "leagueTRB" : leagueTRB,
        "leaguePF" : leaguePF
	}

    return leagueTotals

class TeamStats():
    teamAssists = 0
    teamFGM = 0

def getTeamTotals(season_stats):



    teamTotals = {
        "ATLANTA HAWKS" : TeamStats(),
        "BOSTON CELTICS" : TeamStats(),
        "BROOKLYN NETS" : TeamStats(),
        "CHARLOTTE HORNETS" : TeamStats(),
        "CHICAGO BULLS" : TeamStats(),
        "CLEVELAND CAVALIERS" : TeamStats(),
        "DALLAS MAVERICKS" : TeamStats(),
        "DENVER NUGGETS" : TeamStats(),
        "DETROIT PISTONS" : TeamStats(),
        "GOLDEN STATE WARRIORS" : TeamStats(),
        "HOUSTON ROCKETS" : TeamStats(),
        "INDIANA PACERS" : TeamStats(),
        "LOS ANGELES CLIPPERS" : TeamStats(),
        "LOS ANGELES LAKERS" : TeamStats(),
        "MEMPHIS GRIZZLIES" : TeamStats(),
        "MIAMI HEAT" : TeamStats(),
        "MILWAUKEE BUCKS" : TeamStats(),
        "MINNESOTA TIMBERWOLVES" : TeamStats(),
        "NEW ORLEANS PELICANS" : TeamStats(),
        "NEW YORK KNICKS" : TeamStats(),
        "OKLAHOMA CITY THUNDER" : TeamStats(),
        "ORLANDO MAGIC" : TeamStats(),
        "PHILADELPHIA 76ERS" : TeamStats(),
        "PHOENIX SUNS" : TeamStats(),
        "PORTLAND TRAIL BLAZERS" : TeamStats(),
        "SACRAMENTO KINGS" : TeamStats(),
        "SAN ANTONIO SPURS" : TeamStats(),
        "TORONTO RAPTORS" : TeamStats(),
        "UTAH JAZZ" : TeamStats(),
        "WASHINGTON WIZARDS" : TeamStats(),

        # Deprecated
        "CHARLOTTE BOBCATS" : TeamStats(),
        "NEW JERSEY NETS" : TeamStats(),
        "NEW ORLEANS HORNETS" : TeamStats(),
        "NEW ORLEANS OKLAHOMA CITY HORNETS" : TeamStats(),
        "SEATTLE SUPERSONICS" : TeamStats(),
        "VANCOUVER GRIZZLIES" : TeamStats()
    }

    for total in season_stats:
        teamTotals[total['team'].value].teamAssists += total["assists"]
        teamTotals[total['team'].value].teamFGM += total["made_field_goals"]

    return teamTotals


def getAdvancedStats(season_stats, leagueTotals, teamTotals):
    factor = (2/3) - ((.5*(leagueTotals["leagueAssists"]/leagueTotals["leagueFGM"]))/(2*(leagueTotals["leagueFGM"]/leagueTotals["leagueFTM"])))
    vop = leagueTotals['leaguePoints']/(leagueTotals['leagueFGA'] - leagueTotals['leagueORB'] + leagueTotals['leagueTurnovers'] + .44 * leagueTotals['leagueFTA'])
    drbp = (leagueTotals['leagueTRB'] - leagueTotals['leagueORB']) / leagueTotals['leagueTRB']

    for player_totals in season_stats:
        teamAssists = teamTotals[player_totals['team'].value].teamAssists
        teamFGM = teamTotals[player_totals['team'].value].teamFGM
        min = player_totals['minutes_played']
        threePointers = player_totals['made_three_point_field_goals']
        personalFouls = player_totals['personal_fouls']
        leagueFTM = leagueTotals['leagueFTM']
        leagueFTA = leagueTotals['leagueFTA']
        leaguePF = leagueTotals['leaguePF']
        ftm = player_totals['made_free_throws']
        fta = player_totals['attempted_free_throws']
        fgm = player_totals['made_field_goals']
        fga = player_totals['attempted_field_goals']
        trb = player_totals['total_rebounds']
        ast = player_totals['assists']
        orb = player_totals['offensive_rebounds']
        blk = player_totals['blocks']
        to = player_totals['turnovers']
        stl = player_totals['steals']

        if min > 10:
            uPER = (1/min) * (threePointers - ((personalFouls*leagueFTM)/leaguePF) + ((ftm/2) * (2 - (teamAssists/(3*teamFGM)))) + (fgm * (2 - ((factor * teamAssists)/teamFGM))) + ((2 * ast)/3) + vop * (drbp * (2 * orb + blk - .2464 * (fta - ftm) - (fga - fgm) - trb) + ((.44*leagueFTA*personalFouls)/leaguePF) - (to + orb) + stl + trb - .1936 * (fta - ftm) ) )
        else:
            uPER = 0
        player_totals.update({'uPER':uPER})

    return season_stats


print('***** SEASON TOTALS *****')
season_totals = client.players_season_totals(season_end_year=2019)
season_totals = getMoreStats(season_totals)
leagueTotals = getLeagueTotals(season_totals)
teamTotals = getTeamTotals(season_totals)
season_totals = getAdvancedStats(season_totals, leagueTotals, teamTotals)



print(season_totals)


# newlist = sorted(season_totals, key=itemgetter('points_per_game'))
# for total in newlist:
#     print(str(total['name']) + " " + str(total['points_per_game']))
