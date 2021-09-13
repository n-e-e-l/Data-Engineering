
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline


#Establishing connection with POSTGRES
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

from urllib.request import urlopen
from bs4 import BeautifulSoup

#Website Scraping
url = "https://www.lucernefestival.ch/en/program/forward-festival-21"
html = urlopen(url)


soup = BeautifulSoup(html, 'lxml')

#Getting the Price Information
temp_info1 = []
entry = soup.findAll('div', {'class': 'entry'})
for text_info in entry:
    temp_info1.append(text_info.text.strip())


df = pd.DataFrame()
df['price'] = temp_info1

#print(df.shape)

df = pd.DataFrame()
df['price'] = temp_info1

df=df.loc[1:9]

df = df.replace(r'\t',' ', regex=True)
df = df.replace(r'\n',' ', regex=True)

df.reset_index(drop='index',inplace=True)

#print(df.shape)

import re

for index, row in df.iterrows():
    tempp=str(row['price'])
    res=re.search(r'\bForward\b', tempp)
    res1=re.search(r'\d+', str(res)).group()
    res2=tempp[int(res1):]#print(row['price'])
    price = [int(word) for word in res2.split() if word.isdigit()]
    if (len(price)==0):
        price = 0
        temp=str(price)+" "+str(re.findall("\w+", tempp)[-1]) +" " +str(re.findall("\w+", tempp)[-2])+ " "+str(re.findall("\w+", tempp)[-3])
        row['price']=temp
    else:
        temp=str(price[0])+" "+str(re.findall("\w+", tempp)[-2])
        row['price']=temp
        #print("paind down")
        #print(temp)


#Geeting the detials from the website
day_name = []
times = []
concerts = []
months = []
locations = []
festivals = []
artist = []
details = []
link=[]
time = soup.findAll('span', attrs={'class': 'time'})
for text_info in time: 
    times.append(text_info.text.strip()) 
day_names = soup.findAll('span', attrs={'class': 'day'})
for text_info in day_names: 
    day_name.append(text_info.text.strip()) 
concert = soup.findAll('p', attrs={'class': 'surtitle'})
for text_info in concert: 
    concerts.append(text_info.text.strip())
month = soup.findAll('p', attrs={'class': 'month'})
for text_info in month: 
    months.append(text_info.text.strip())
location = soup.findAll('p', attrs={'class': 'location'})
for text_info in location: 
    locations.append(text_info.text.strip())
festival = soup.findAll('p', attrs={'class': 'status corall-violet'})
for text_info in festival: 
    festivals.append(text_info.text.strip())
subtitle = soup.findAll('p', attrs={'class': 'subtitle'})
for text_info in subtitle: 
    artist.append(text_info.text.strip())
det = soup.findAll('p', attrs={'class': 'title'})
for text_info in det: 
    details.append(text_info.text.strip()) 
del details[0:3]
entry = soup.findAll('div', {'class': 'entry'})

det = soup.findAll('div', attrs={'class': 'image'})
for text_info in det: 
    link.append(text_info.get('style'))



#df = pd.DataFrame()
#Details in dataframe
df['day_name'] = day_name
df['times'] = times
df['concerts'] = concerts
df['months'] = months
df['locations'] = locations  
#df['festival'] = festival
df['artist'] = artist
df['detail'] = details
df['image_link'] = link



print(df.shape)
print(df)

#Inserting the dataframe into 'concert_tabel' tabel
df.to_sql('concert_table', db)
print("insert done")



#Executing Query
result_set = db.execute("SELECT day_name FROM concert_table")  

print(type(result_set))

#for r in result_set:  
#    print(r)
#    print(type(r))

result = [r for r, in result_set]
#print(type(result))
#print(result)
#print("working")
#ress = df.day_name.value_counts().rename_axis('unique_values').reset_index(name='counts')


df_postgres = pd.DataFrame(result,columns =['days'])
ress=df_postgres.days.value_counts().rename_axis('unique_values').reset_index(name='counts')

days = ress.unique_values.values
values = ress.counts.values


#Plotting the result
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(days, values, color ='maroon',
        width = 0.4)
# 
plt.xlabel("Days of the week")
plt.ylabel("Days")
plt.title("Number of Events Each Day")
plt.savefig('show.jpg')
print("GRAPH SAVED IN DOCKER")