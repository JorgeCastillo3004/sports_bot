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

con = getdb()
print("Connections stablished")
con.close()
# save_news_database(con, dict_news)


# con.close()



# ALTER TABLE news
# ALTER COLUMN news_content TYPE VARCHAR(12578);
# COMMIT;

# ALTER TABLE news
# ALTER COLUMN news_summary TYPE VARCHAR(4196);
# COMMIT;

# ALTER TABLE news
# ALTER COLUMN news_tags TYPE VARCHAR(255);
# COMMIT;

# ALTER TABLE news
# ALTER COLUMN title TYPE VARCHAR(255);
# COMMIT;

# COMMIT;


# create table news
# (
#     news_id      varchar(40) not null
#         primary key,
#     news_content varchar(8392),
#     image        varchar(255),
#     published    timestamp(6),
#     news_summary varchar(4196),
#     news_tags    varchar(255),
#     title        varchar(255)
# );