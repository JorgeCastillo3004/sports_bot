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

if database_enable:
	con = getdb()