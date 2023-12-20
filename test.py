import psycopg2
from datetime import date, timedelta
from datetime import datetime
import sys

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

print("Connections stablished")

con = getdb()
dict_news = dict_news = {'news_id':"asd223ddsf13", 'title':"insert new news" ,'news_summary':"summary.text",\
                                 'news_content':"body_html", 'image':"image_path",\
                                'published':datetime.now(),'news_tags': "mentions"}     
#save_news_database(dict_news)

option = int(sys.argv[1])
if option  == 1:
    print("Select all from news")
    query = "SELECT title FROM news;"

if option == 2:
    print("Cound duplicates")
    query = "SELECT title, COUNT(*) as count\
    FROM news\
    GROUP BY title\
    HAVING COUNT(*) > 1;"

if option == 3:
    print("Delete all")
    input_user = input("Type Y to continue")
    query = "DELETE FROM news;"

cur = con.cursor()
cur.execute(query)

if option != 3:
    results = cur.fetchall()
    print(len(results))

    for result in results:
        print(result)
else:
    if input_user == 'Y':
        con.commit()

cur.close()

