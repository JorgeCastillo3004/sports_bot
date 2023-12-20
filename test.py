import psycopg2
from datetime import date, timedelta
from datetime import datetime
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--option')
# parser.add_argument('--table')
parser = argparse.ArgumentParser()
parser.add_argument('--option', type=int, default=1)
parser.add_argument('--table', type=str, default='news')

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


args = parser.parse_args()



option = args.option
table = args.table
print("Option: ", option)
print("Table: ", table)

con = getdb()
print("Connections stablished")
dict_news = dict_news = {'news_id':"asd223ddsf13", 'title':"insert new news" ,'news_summary':"summary.text",\
                                 'news_content':"body_html", 'image':"image_path",\
                                'published':datetime.now(),'news_tags': "mentions"}     
#save_news_database(dict_news)



if option  == 1:
    print("Select all from news")
    query = "SELECT {} FROM news;".format(table)

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