import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse

from common_functions import load_json
parser = argparse.ArgumentParser()
parser.add_argument('--option', type=int, default=1)
parser.add_argument('--table', type=str, default='news')
parser.add_argument('--column', type=str, default='title')

# parser.add_argument('--option', type=int, default=1, '--table', type=str, default='news')

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
		con.commit

def save_sport_database(sport_dict):

	query = "INSERT INTO sport VALUES(%(sport_id)s, %(is_active)s, %(desc_i18n)s,\
					 %(logo)s, %(sport_mode)s, %(name_i18n)s, %(point_name)s)"
	cur = con.cursor()
	cur.execute(query, sport_dict)
	con.commit



def create_sports_selected():
	CONFIG_M1 = load_json('check_points/CONFIG_M1.json')
	for sport, enable_flag in CONFIG_M1['SPORTS'].items():
		sport_dict = {'sport_id' : '', 'is_active' : True, 'desc_i18n' : '', 'logo' : '', 'sport_mode' : '', 'name_i18n' : '', 'point_name': ''}
		if enable_flag:
			print(sport, "Save in data base:")
			sport_dict[sport] = sport_dict
			sport_dict['sport_mode'] = sport_dict[sport]['mode']
			try:
				save_sport_database(sport_dict)
			except:
				print("Previously created ")

args = parser.parse_args()
option = args.option
table = args.table
column = args.column
print("Option: ", option)
print("Table: ", table)
con = getdb()
print("Connections stablished")
create_sports_selected()
# dict_news = dict_news = {'news_id':"asd223ddsf13", 'title':"insert new news" ,'news_summary':"summary.text",\
#                                  'news_content':"body_html", 'image':"image_path",\
#                                 'published':datetime.now(),'news_tags': "mentions"}     

if option  == 1:
	print("Select all from news")
	query = "SELECT {} FROM {};".format(column, table)

if option == 2:
	print("Cound duplicates")
	query = "SELECT title, COUNT(*) as count\
	FROM news\
	GROUP BY title\
	HAVING COUNT(*) > 1;"

if option == 3:
	print("Delete all")
	input_user = input("Type Y to continue")
	query = "DELETE FROM {};".format(table)

cur = con.cursor()
cur.execute(query)

if option != 3:
	results = cur.fetchall()   

	for result in results:
		print(result)
	print("Total results: ", len(results))
else:
	if input_user == 'Y':
		con.commit()

cur.close()