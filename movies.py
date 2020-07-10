import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

%%time 

from sqlalchemy import create_engine
conn_string_imdb = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    user='student', 
    password='dwdstudent2015', 
    host = 'db.ipeirotis.org', 
    port=3306, 
    db='imdb',
    encoding = 'utf-8'
)
engine_imdb = create_engine(conn_string_imdb)


query = ''' SELECT * FROM movies '''
basic = pd.read_sql(query, con=engine_imdb)

#Goal: analyze the number of movies over time
#Approach 1. Fetch all data from the table, analyze in Pandas 

# Counting movie ids returns all the movies within the year
# Counting movie ranks returns all the movies that have a non-empty "rank" value (i.e., they have been rated)
pivot = basic.pivot_table(
    index = 'year',
    aggfunc = 'count',
    values = ['id', 'rank']
)
# Rename the columns
pivot.columns = ['all_movies', 'rated_movies']
pivot.plot.line(y=['all_movies', 'rated_movies']);
plt.show() # this line, combined with importing matplotlib.pyplot as plt gets rid of the pandas df error: <matplotlib.axes._subplots.AxesSubplot>
<img src="https://github.com/jj1787/sql-practice/blob/master/images/Graph.png">

%%time

#Approach 2 is 80% FASTER, completed in about 300 ms. First, aggregate selected data in SQL, then analyze in pandas.

query = '''
SELECT year, COUNT(*) AS all_movies, COUNT(rank) AS rated_movies
FROM movies 
GROUP BY year
ORDER BY year
'''
df_movies = pd.read_sql(query, con=engine_imdb)



