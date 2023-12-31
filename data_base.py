import psycopg2
from common_functions import load_json
CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']

def getdb():
	return psycopg2.connect(
				host="localhost",
				user="wohhu",
				password="caracas123",
		dbname='sports_db',
		)

def save_news_database(dict_news):	
	query = "INSERT INTO news VALUES(%(news_id)s, %(news_content)s, %(image)s,\
			 %(published)s, %(news_summary)s, %(news_tags)s, %(title)s)"
	cur = con.cursor()
	cur.execute(query, dict_news)
	con.commit()

def save_ligue_info(dict_ligue_tornament):
	for field, value in dict_ligue_tornament.items():
		print(field, value, end ='-')

	query = "INSERT INTO league VALUES(%(league_id)s, %(league_country)s, %(league_logo)s, %(league_name)s, %(league_name_i18n)s)"     	 
	cur = con.cursor()																			 
	cur.execute(query, dict_ligue_tornament)														 
	con.commit()																					 

def save_season_database(season_dict):
	query = "INSERT INTO season VALUES(%(season_id)s, %(season_name)s, %(season_end)s,\
									 %(season_start)s, %(league_id)s)"
	cur = con.cursor()
	cur.execute(query, season_dict)
	con.commit

def save_tournament(dict_tournament):
	query = "INSERT INTO tournament VALUES(%(tournament_id)s, %(team_country)s, %(desc_i18n)s,\
									 %(end_date)s, %(logo)s, %(name_i18n)s, %(season)s, %(start_date)s, %(tournament_year)s)"
	cur = con.cursor()
	cur.execute(query, dict_tournament)
	con.commit

def save_team_info(dict_team):
	query = "INSERT INTO team VALUES(%(team_id)s, %(team_country)s, %(team_desc)s,\
	 %(team_logo)s, %(team_name)s, %(sport_id)s, %(tournament_id)s)"
	cur = con.cursor()																			 
	cur.execute(query, dict_team)														 
	con.commit()

def save_league_team_entity(dict_team):
	query = "INSERT INTO league_team VALUES(%(instance_id)s, %(team_meta)s, %(team_position)s, %(league_id)s, %(season_id)s, %(team_id)s)"	
	cur = con.cursor()
	cur.execute(query, dict_team)
	con.commit()

def save_player_info(dict_team):	
	query = "INSERT INTO player VALUES(%(player_id)s, %(player_country)s, %(player_dob)s,\
	 %(player_name)s, %(player_photo)s, %(player_position)s)"
	cur = con.cursor()
	cur.execute(query, dict_team)
	con.commit()

# def save_team_info(dict_team):
# 	print("dict_team: ", dict_team)
# 	query = "INSERT INTO league_team VALUES(%(instance_id)s, %(team_meta)s, %(team_position)s, %(league_id)s, %(season_id)s, %(team_id)s)"
# 	cur = con.cursor()
# 	cur.execute(query, dict_team)
# 	con.commit()

def create_sport_dict(sport, sport_mode):
	sport_dict = {'sport_id' : sport, 'is_active' : True, 'desc_i18n' : '', 'logo' : '',\
	'sport_mode' : sport_mode, 'name_i18n' : '', 'point_name': ''}
	return sport_dict

def save_sport_database(sport_dict):
	try:
		query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
										 %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s)"
		cur = con.cursor()
		cur.execute(query, sport_dict)
		con.commit()
	except:
		con.rollback()

if database_enable:
	con = getdb()