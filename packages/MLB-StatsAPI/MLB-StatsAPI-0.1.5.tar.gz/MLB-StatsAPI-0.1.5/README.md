# MLB-StatsAPI

Python wrapper for MLB Stats API

Created by Todd Roberts

https://pypi.org/project/MLB-StatsAPI/

https://github.com/toddrob99/MLB-StatsAPI

Documentation: https://toddrob99.github.io/MLB-StatsAPI/

## Installation
MLB-StatsAPI is listed on the [Python Package Index](https://pypi.org/project/MLB-StatsAPI/), 
and the preferred installation method is pip for all platforms. 
If you install manually, be sure to also install requests.

```pip install MLB-StatsAPI```

## Available Functions

* `statsapi.get()` - make calls directly to MLB StatsAPI endpoints; supports the most flexibility in request parameters, and returns raw json data

* `statsapi.meta()` - retrieve available values from StatsAPI for use in other queries, or look up descriptions for values found in API results

* `statsapi.notes()` - retrieve notes for a given endpoint, including a list of required parameters, as well as hints for some endpoints

* `statsapi.lookup_player()` - get a list of player data based on first, last, or full name, jersey number, current team Id, position, etc.

* `statsapi.lookup_team()` - get a list of teams' info based on the team name, city, abbreviation, or file code

* `statsapi.schedule()` - retrieve a list of games on a given date/range and/or team/opponent

* `statsapi.boxscore()` - generate a formatted boxscore for a given game

* `statsapi.boxscore_data()` - generate a dict containing boxscore data for a given game

* `statsapi.linescore()` - generate a formatted linescore for a given game

* `statsapi.roster()` - generate a formatted list of players on a team's roster

* `statsapi.standings()` - generate a formatted list of standings for a given league/date

* `statsapi.standings_data()` - returns a python list of standings data for a given league/date

* `statsapi.team_leaders()` - generate a formatted list of a team's leaders for a given stat

* `statsapi.team_leader_data()` - returns a python list of a team's leader data for a given stat

* `statsapi.league_leaders()` - generate a formatted list of stat leaders for current or specified season

* `statsapi.league_leader_data()` - returns python list of stat leader data for current or specified season

* `statsapi.player_stats()` - generate a formatted list of a player's career or season stats

* `statsapi.player_stat_data()` - returns a python dict of a player's career or season stats, along with some biographical information

* `statsapi.last_game()` - get the game id for the given team's most recent game

* `statsapi.next_game()` - get the game id for the given team's next game

* `statsapi.game_highlights()` - generate a formatted list of highlights with video links for a given game

* `statsapi.game_highlight_data()` - returns a python list of highlight data, including video links, for a given game

* `statsapi.game_pace()` - generate a formatted list of pace of game information for a given season (back to 1999)

* `statsapi.game_pace_data()` - returns a python dict of pace of game information for a given season (back to 1999)

* `statsapi.game_scoring_plays()` - generate a formatted list of scoring plays for a given game

* `statsapi.game_scoring_play_data()` - returns a python dict of scoring play data for a given game

## Example Use

### Print the number of games won by the Oakland Athletics in 2018

Use `statsapi.schedule()` to retrieve all A's games for 2018,
and use `sum()` to count records in the resultset where the A's were the winning_team.

```
print('The A\'s won %s games in 2018.' % sum(1 for x in statsapi.schedule(team=133,start_date='01/01/2018',end_date='12/31/2018') if x.get('winning_team','')=='Oakland Athletics'))
```

### Print the linescore for all games the Phillies won in July 2008

Use `statsapi.schedule()` to retrieve all games for July 2018,
run the resulting dict through a list comprehension
to iterate over the records where the Phillies are the winning team,
and feed the `game_id` into `statsapi_linescore()`.

```
for x in [y for y in statsapi.schedule(team=143,start_date='07/01/2008',end_date='07/31/2008') if y.get('winning_team','')=='Philadelphia Phillies']:
    print('%s\nWinner: %s, Loser: %s\n%s\n\n' % (x['game_date'], x['winning_team'], x['losing_team'], statsapi.linescore(x['game_id'])))
```

### Print the Phillies 40-man Roster on opening day of the 2018 season

Use `statsapi.get('season')` to retrieve the dates for the 2018 season,
feed the opening day date into `statsapi.roster()`.

```
print('Phillies 40-man roster on opening day of the 2018 season:\n%s' % statsapi.roster(143,'40Man',date=statsapi.get('season',{'seasonId':2018,'sportId':1})['seasons'][0]['regularSeasonStartDate']))
```

### Print the boxscore and linescore from the A's most recent game (which may be in progress or may not have started yet based on MLB response to 'last game' request)

Use `statsapi.last_game()` to retrieve the most recent A's game
and feed the gamePk into `statsapi.boxscore()` and `statsapi.linescore()`.

```
most_recent_game_id = statsapi.last_game(133)
print(statsapi.boxscore(most_recent_game_id))
print(statsapi.linescore(most_recent_game_id))
```

### Find the team with the longest name

Use `statsapi.get('teams')` to retrieve all active team names,
then feed into max() to find the longest value and its length

```
longest_team_name = max([x['name'] for x in statsapi.get('teams',{'sportIds':1,'activeStatus':'Yes','fields':'teams,name'})['teams']],key=len)
print('The team with the longest name is %s, at %s characters.' % (longest_team_name, len(longest_team_name)))
```

### Print the standings from July 4, 2018

Use `statsapi.standings()` with the `date` parameters

```
print(statsapi.standings(date='07/04/2018'))
```

### Print the top 5 team leaders in walks for the 2008 Phillies

Use `statsapi.team_leaders()`

```
print(statsapi.team_leaders(143,'walks',limit=5,season=2008))
```

### Print the top 10 all time career leaders in doubles (NOTE: The extra 8949 records come back in the data from MLB)

use `statsapi.league_leaders()`

```
print(statsapi.league_leaders('doubles',statGroup='hitting',statType='career',limit=10))
```

### Print Chase Utley's career hitting stats

use `statsapi.get()` to call the sports_players endpoint for the 2008 World Series,
lookup Chase Utley's person id from the results, and pass it into `statsapi.player_stats()`
using `type='hitting'` and `group='career'`

```
print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2008,'gameType':'W'})['people'] if x['fullName']=='Chase Utley'), 'hitting', 'career') )
```

### Print a list of scoring plays from the 4/28/2019 Marlins @ Phillies game

```
print( statsapi.game_scoring_plays(567074) )
```

## Copyright Notice

This package and its author are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.
