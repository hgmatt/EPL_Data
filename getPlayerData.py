from bs4 import BeautifulSoup
import requests, time

def Collect_Player_Stats(year):
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
		soup = BeautifulSoup(r.text)
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
		for player in team_players[team]:
			if team_players[team][player][url] != 'N/A':
				r = requests.get(team_players[team][player][url])
				soup = BeautifulSoup(r.text)
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
				new_tag = BeautifulSoup('<b>0</b>')
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
				player_games = {}
				for game in range(len(game_date)):
					game_stats = {'team_name': team_name[game].text,
								  'oppo_name': oppo_name[game].text,
								  'comp': comp[game].text,
								  'game_date': game_date[game].text,
								  'res': res[game].text,
								  'appear': appear[game].text,
								  'sv': sv[game].text,
								  'fc': fc[game].text,
								  'fs': fs[game].text,
								  'yc': yc[game].text,
								  'rc': rc[game].text,
								  'g': g[game].text,
								  'a': a[game].text,
								  'sh': sh[game].text,
								  'sg': sg[game].text}
					player_games[game_date[game].text] = game_stats
				team_players[team][player]['game_stats'] = player_games
	return team_players