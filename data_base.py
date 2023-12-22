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

def save_ligue_tornament_info(dict_ligue_tornament):
	print("Info ligue tournament info save")
	for field, value in dict_ligue_tornament.items():
		print(field, value, end ='-')

	query = "INSERT INTO league VALUES(%(league_id)s, %(league_country)s, %(league_logo)s, %(league_name)s, %(league_name_i18n)s)"     	 
	cur = con.cursor()																			 
	cur.execute(query, dict_ligue_tornament)														 
	con.commit()																					 

def save_sport_database(sport_dict):
	try:
		query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
										 %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s)"
		cur = con.cursor()
		cur.execute(query, sport_dict)
		con.commit
	except:
		con.rollback()

def create_sports_selected_in_db():
	CONFIG_M1 = load_json('check_points/CONFIG_M1.json')
	for sport, enable_mode in CONFIG_M1['SPORTS'].items():
		sport_dict = {'sport_id' : '', 'is_active' : True, 'desc_i18n' : '', 'logo' : '', 'sport_mode' : '', 'name_i18n' : '', 'point_name': ''}
		print(enable_mode['enable'])
		if enable_mode['enable']:
			print(sport, "Save in data base:")
			sport_dict[sport] = sport_dict
			sport_dict['sport_mode'] = enable_mode['mode']
			if database_enable:
				save_sport_database(sport_dict)

def save_season_database(season_dict):
	query = "INSERT INTO season VALUES(%(season_id)s, %(season_name)s, %(season_end)s,\
									 %(season_start)s, %(league_id)s)"
	cur = con.cursor()
	cur.execute(query, sport_dict)
	con.commit

if database_enable:
	con = getdb()