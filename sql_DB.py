#Store as a SQLITE3 DB
import sqlite3
import os, sys


datafile = 'epldata.db'
datafile_exists = os.path.exists(datafile)
if datafile_exists:
	os.remove(datafile)

def create_EPL_DB(datafile):
	conn = sqlite3.connect(datafile)
	c = conn.cursor()
	
	#Players Table Schema
	players_table_column_name = ['second_name', 'squad_number', 'team_name', 'team_code',
					             'web_name', 'ea_index', 'position', 'first_name']
	players_table_column_type = ['TEXT', 'INT', 'TEXT', 'INT', 'TEXT', 'REAL', 'TEXT','TEXT']
	
	#Player Weekly Stats Table Schema
	player_weekly_stats_column_name = ['ict_index','in_dreamteam','influence','loaned_in',
								 'loaned_out','loans_in','loans_out','minutes','news','now_cost',
								 'own_goals','penalties_missed','penalties_saved','points_per_game',
								 'red_cards','saves','selected_by_percent','special','status','threat',
								 'total_points','transfers_in','transfers_in_event','transfers_out',
								 'transfers_out_event','value_form','value_season','yellow_cards',
								 'form','goals_conceded','goals_scored','assists','bonus','bps',
								 'chance_of_playing_next_round','chance_of_playing_this_round',
								 'clean_sheets','cost_change_event','cost_change_event_fall',
								 'cost_change_start','cost_change_start_fall','creativity',
								 'dreamteam_count','ep_next','ep_this','event_points','code','date_collected']
	player_weekly_stats_column_type = ['REAL','INT','REAL','INT',
									   'INT','INT','INT','INT','BLOB','INT',
									   'INT','INT','INT','REAL',
									   'INT','INT','REAL','TEXT','TEXT','REAL',
									   'INT','INT','INT','INT',
									   'INT','REAL','REAL','INT',
									   'REAL','INT','INT','INT','INT','INT',
									   'TEXT','TEXT',
									   'INT','INT','INT',
									   'INT','INT','REAL',
									   'INT','REAL','TEXT','INT','INT','TEXT']
	
	#Teams Table Schema
	teams_table_column_name = ['team_name','team_short_name','team_url']
	teams_table_column_type = ['TEXT','TEXT','TEXT']
	
	#Game_Stats Table Schema
	game_stats_table_column_name = ['player_id','team_code','team_name','a','appear','comp','fc',
									'fs','g','game_date','home_away','minutes','oppo_name','rc',
									'res','sg','sh','sv','yc','season']
	game_stats_table_column_type = ['INT','INT','TEXT','INT','TEXT','TEXT','INT',
									'INT','INT','TEXT','TEXT','INT','TEXT','INT',
									'TEXT','INT','INT','INT','INT','TEXT']
									
	#2016_Fixtures Table Schema
	fixtures_table_column_name = ['difficulty','event','event_name','finished',
									'finished_provisional','id','is_home','kickoff_time',
									'kickoff_time_formatted','minutes','opponent_name',
									'opponent_short_name','provisional_start_time','team_a',
									'team_a_score','team_h','team_h_score','player_id','team_code']
	fixtures_table_column_type = ['INT','INT','TEXT','TEXT',
									   'TEXT','INT','TEXT','TEXT',
									   'TEXT','INT','TEXT',
									   'TEXT','TEXT','INT',
									   'TEXT','INT','TEXT','INT','INT']
									   
	#CREATE players TABLE
	c.execute('CREATE TABLE players(player_id INT PRIMARY KEY)')
	
	for n in range(len(players_table_column_name)):
		c.execute("ALTER TABLE players ADD COLUMN '{cn}' {ct}"\
		         .format(cn = players_table_column_name[n], ct = players_table_column_type[n]))

	#CREATE players_weekly_stats TABLE
	c.execute('CREATE TABLE player_weekly_stats (player_id INT PRIMARY KEY)')
	
	for n in range(len(player_weekly_stats_column_name)):
		c.execute("ALTER TABLE player_weekly_stats ADD COLUMN '{cn}' {ct}"\
				 .format(cn = player_weekly_stats_column_name[n], ct = player_weekly_stats_column_type[n]))

	#for loop to add columns

	#CREATE teams TABLE
	c.execute('CREATE TABLE teams (team_code TEXT PRIMARY KEY)')

	#for loop to add columns
	for n in range(len(teams_table_column_name)):
		c.execute("ALTER TABLE teams ADD COLUMN '{cn}' {ct}"\
				  .format(cn = teams_table_column_name[n], ct = teams_table_column_type[n]))
				  	
	#CREATE game_stats TABLE
	c.execute('CREATE TABLE game_stats (playerid_game INT PRIMARY KEY)')
	
	#for loop to add columns
	for n in range(len(game_stats_table_column_name)):
		c.execute("ALTER TABLE game_stats ADD COLUMN '{cn}' {ct}"\
				  .format(cn = game_stats_table_column_name[n], ct = game_stats_table_column_type[n]))
	#CREATE 2016_fixtures TABLE
	c.execute('CREATE TABLE fixtures (code INT PRIMARY KEY)')
	
	#for loop to add columns
	for n in range(len(fixtures_table_column_name)):
		c.execute("ALTER TABLE fixtures ADD COLUMN '{cn}' {ct}"\
				  .format(cn = fixtures_table_column_name[n], ct = fixtures_table_column_type[n]))
	
	conn.commit()
	conn.close
	
def build_EPL_DB(datafile, all_data):
	#Building data for the Teams Table
	teams = {1: 'Arsenal',2: 'Bournmouth',3: 'Burnley',4: 'Chelsea',5: 'Crystal Palace',
        	 6: 'Everton',7: 'Hull City',8: 'Leicester City',9: 'Liverpool',10: 'Manchester City',
    	     11: 'Manchester United',12: 'Middlesbrough',13: 'Southampton',14: 'Stoke City',
        	 15: 'Sunderland',16: 'Swansea',17: 'Tottenham',18: 'Watford',19: 'West Brom',
    	     20: 'West Ham'}
	teams_short = {1: 'ARS', 2:'BOU', 3:'BUR', 4:'CHE', 5:'CRY', 6:'EVE', 7:'HUL', 8:'LEI', 9:'LIV', 10:'MCI', 11:'MUN', 
             	  12:'MID', 13:'SOU', 14:'STK', 15:'SUN', 16:'SWA', 17:'TOT', 18:'WAT', 19:'WBA', 20:'WHU'}
	teams_espnfc = {'BOU':'http://www.espnfc.us/club/afc-bournemouth/349/squad',
						'ARS':'http://www.espnfc.us/club/arsenal/359/squad',
						'BUR':'http://www.espnfc.us/club/burnley/379/squad',
						'CHE':'http://www.espnfc.us/club/chelsea/363/squad',
						'CRY':'http://www.espnfc.us/club/crystal-palace/384/squad',
						'EVE':'http://www.espnfc.us/club/everton/368/squad',
						'HUL':'http://www.espnfc.us/club/hull-city/306/squad',
						'LEI':'http://www.espnfc.us/club/leicester-city/375/squad',
						'LIV':'http://www.espnfc.us/club/liverpool/364/squad',
						'MCI':'http://www.espnfc.us/club/manchester-city/382/squad',
						'MUN':'http://www.espnfc.us/club/manchester-united/360/squad',
						'MID':'http://www.espnfc.us/club/middlesbrough/369/squad',
						'SOU':'http://www.espnfc.us/club/southampton/376/squad',
						'STK':'http://www.espnfc.us/club/stoke-city/336/squad',
						'SUN':'http://www.espnfc.us/club/sunderland/366/squad',
						'SWA':'http://www.espnfc.us/club/swansea-city/318/squad',
						'TOT':'http://www.espnfc.us/club/tottenham-hotspur/367/squad',
						'WAT':'http://www.espnfc.us/club/watford/395/squad',
						'WBA':'http://www.espnfc.us/club/west-bromwich-albion/383/squad',
						'WHU':'http://www.espnfc.us/club/west-ham-united/371/squad'}
	conn = sqlite3.connect(datafile)
	c = conn.cursor()
# Add data to the teams table
	for n in teams.iterkeys():
		c.execute("INSERT INTO teams (team_code,team_name,team_short_name,team_url) VALUES ('{tc}','{tn}','{tsn}','{tu}')"\
				.format(tc = int(n), tn = teams[n], tsn = teams_short[n], tu = teams_espnfc[teams_short[n]]))
# Add data to the players table
	for n in range(len(all_data)):
		dict = {}
		dict = all_data[n]
		pi = dict['id']
		sn = dict['second_name']#.encode('utf-8')
		sqn = dict['squad_number']
		t = teams[dict['team']]
		tc = dict['team_code']
		wn = dict['web_name']#.encode('utf-8')
		ea = dict['ea_index']
		pn = dict['element_type']
		fn = dict['first_name']#.encode('utf-8')
		c.execute("INSERT INTO players (player_id, second_name, squad_number, team_name, team_code, web_name, ea_index, position, first_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (pi, sn, sqn, t, tc, wn, ea, pn, fn))

# Add data to the game_stats table

# Add data to the players_weekly_stats table

# Add data to the 2016_fixtures table	
	
	conn.commit()
	conn.close()