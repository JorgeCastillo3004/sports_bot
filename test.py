import psycopg2
from datetime import date, timedelta
from datetime import datetime

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
save_news_database(dict_news)

query = "SELECT * FROM news;"
cur = con.cursor()
cur.execute(query)
results = cur.fetchall()
for result in results:
    print(result)

con.close()

