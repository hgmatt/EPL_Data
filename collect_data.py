import requests, cPickle, shutil, time, os
import StringIO
import pprint
import sys
from bs4 import BeautifulSoup

def Collect_Current_Fantasy():
	date_text = time.strftime("%Y_%m_%d")
	all_data_file = date_text + '_all_data.p'
	all_data_file_exists = os.path.exists(all_data_file)

	if all_data_file_exists:
		all_data = cPickle.load(open(all_data_file, 'rb'))
	else:
		players = {}
		all_data_url = 'https://fantasy.premierleague.com/drf/elements/'
		r_all = requests.get(all_data_url)
		all_data = r_all.json()
		for i in range(490): #486
			playerurl = 'https://fantasy.premierleague.com/drf/element-summary/%s'
			r = requests.get(playerurl % i)
			# skip non-existent players
			if r.status_code != 200: continue
		
			players[i] = r.json()
			all_data[i-1]['history_past'] = players[i]['history_past']
			all_data[i-1]['fixtures'] = players[i]['fixtures']
		print date_text
	cPickle.dump(all_data, open(all_data_file,'wb'))


	position_title = ['Goalkeeper', 'Defender', 'Forward', 'Midfielder']
	teams = {1: 'Arsenal',
    	     91: 'Bournmouth',
        	 3: 'Burnley',
	         4: 'Chelsea',
    	     5: 'Crystal Palace',
        	 6: 'Everton',
	         7: 'Hull City',
    	     8: 'Leicester City',
        	 9: 'Liverpool',
	         10: 'Manchester City',
    	     11: 'Manchester United',
        	 25: 'Middlesbrough',
	         13: 'Southampton',
    	     14: 'Stoke City',
        	 15: 'Sunderland',
	         16: 'Swansea',
    	     17: 'Tottenham',
        	 18: 'Watford',
	         19: 'West Brom',
    	     20: 'West Ham'}
	teams_short = {1: 'ARS', 2:'BOU', 3:'BUR', 4:'CHE', 5:'CRY', 6:'EVE', 7:'HUL', 8:'LEI', 9:'LIV', 10:'MCI', 11:'MUN', 
             	  12:'MID', 13:'SOU', 14:'STK', 15:'SUN', 16:'SWA', 17:'TOT', 18:'WAT', 19:'WBA', 20:'WHU'}
	return teams_short, teams, all_data         
def Collect_Player_Stats(year):
	date_text = time.strftime("%Y_%m_%d")
	player_file = date_text + '_' + year +'_all_players_data.p'
	player_file_exists = os.path.exists(player_file)
	if player_file_exists:
		team_players = cPickle.load(open(player_file, 'rb'))
	else:
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
		team_players = {}
		for teams in teams_espnfc.iterkeys():
			r = requests.get(teams_espnfc[teams])
			soup = BeautifulSoup(r.text, "html.parser")
			squads = soup.find_all("td", class_="pla")
			roster = {}
			for i in squads:
				link = ''
				try:
					name = i.text.strip()
					link = i.a['href'] + '?season=' + year
				except:
					link = 'N/A'
				finally:
					url = 'url'
					roster[name] = {url: link}
			team_players[teams] = roster
			time.sleep(1)
		for team in team_players:
			print team
			for player in team_players[team]:
				if team_players[team][player][url] != 'N/A':
					r = requests.get(team_players[team][player][url])
					soup = BeautifulSoup(r.text, "html.parser")
					team_name = soup.select("div#player-appearances .team")
					oppo_name = soup.select('div#player-appearances .oppo')
					game_date = soup.select('div#player-appearances .date')
					comp = soup.select('div#player-appearances .comp')
					res = soup.select('div#player-appearances .res')
					appear = soup.select('div#player-appearances .appear')
					sv = soup.select('div#player-appearances .sv')
					fc = soup.select('div#player-appearances .fc')
					fs = soup.select('div#player-appearances .fs')
					yc = soup.select('div#player-appearances .yc')
					rc = soup.select('div#player-appearances .rc')
					g = soup.select('div#player-appearances .g')
					a = soup.select('div#player-appearances .a')
					sh = soup.select('div#player-appearances .sh')
					sg = soup.select('div#player-appearances .sg')
					new_tag = BeautifulSoup('<b>0</b>', "html.parser")
					if len(sv) == 0:
						sv = [new_tag]*len(team_name)
					if len(g) == 0:
						g = [new_tag]*len(team_name)
					if len(a) == 0:
						a = [new_tag]*len(team_name)
					if len(sh) == 0:
						sh = [new_tag]*len(team_name)
					if len(sg) == 0:
						sg = [new_tag]*len(team_name)
				#fantasy_points [g, a, sv, minutes, 
					player_games = {}
					
					for game in range(len(game_date)):
						if game == 0: continue
						#calculate home or away
						home_away = oppo_name[game].text
						home_away = home_away.split()
						#calculate minutes played
						game_appear = appear[game].text
						game_appear = game_appear.replace(';','')
						game_appear = game_appear.split()
						if game_appear[0] == 'Started':
							minutes = 90
						elif game_appear[0] == 'Sub-On':
							if len(game_appear) > 3:
								print len(game_appear)
								minutes = int(game_appear[3]) - int(game_appear[1])
							else:
								minutes = 90 - int(game_appear[1])
						elif game_appear[0] == 'Sub-Off':
							minutes = int(game_appear[1])
						else:
							minutes = 0
						#home_away = home_away[0].split()
						game_stats = {'team_name': team_name[game].text,
									  'oppo_name': home_away[2],
									  'home_away': home_away[0],
									  'comp': comp[game].text,
									  'game_date': game_date[game].text,
									  'res': res[game].text,
									  'appear': appear[game].text,
									  'minutes': minutes,
									  'sv': sv[game].text,
									  'fc': fc[game].text,
									  'fs': fs[game].text,
									  'yc': yc[game].text,
									  'rc': rc[game].text,
									  'g': g[game].text,
									  'a': a[game].text,
									  'sh': sh[game].text,
									  'sg': sg[game].text}
						player_games[game] = game_stats
					team_players[team][player]['game_stats'] = player_games
					time.sleep(1)
	
		cPickle.dump(team_players, open(player_file,'wb'))
	return team_players