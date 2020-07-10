# Connect to the Facebook database, and use the MemberSince variable from the Profiles table to plot the growth of Facebook users.
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from sqlalchemy import create_engine

conn_string_facebook = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    user='student', 
    password='dwdstudent2015', 
    host = 'db.ipeirotis.org', 
    port=3306, 
    db='facebook',
    encoding = 'utf-8'
)
engine_facebook = create_engine(conn_string_facebook)
con_facebook = engine_facebook.connect()
descrip = con_facebook.execute("DESCRIBE Profiles")
for i in descrip:
    print(i)

# Former approach
#query= '''SELECT * FROM Profiles''' 
#df_members = pd.read_sql(query,con=engine_facebook)
#pivot_table = df_members.pivot_table(index = 'MemberSince',
#                             values = 'ProfileID',
#                             aggfunc = 'count')
#weekly_signups = pivot_table.resample('1W').sum()
#weekly_signups = weekly_signups.cumsum()
#weekly_signups.plot();

query= '''SELECT MemberSince, COUNT(ProfileID) as Signups FROM Profiles GROUP BY MemberSince ORDER BY MemberSince''' # Because there can be multiple rows with the same "MemberSince" date, we use "ProfileID" as an identifier.
df_members = pd.read_sql(query,con=engine_facebook)
df_members.set_index("MemberSince", inplace=True)

#Make the graphs a bit prettier, and bigger
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
plt.rcParams['figure.figsize'] = (15, 7)

weekly_signups = df_members.resample('1W').sum() #to resample time-series data
weekly_signups.cumsum().plot();

myImage = Image.open("Graph2.png"); #View image in sql-practice directory
myImage.show();
