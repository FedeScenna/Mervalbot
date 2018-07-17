# -*- coding: utf-8 -*-
from secrets import *
from bs4 import BeautifulSoup
import urllib.request as urllib
import time
from datetime import datetime
import pandas as pd
import tweepy


site="http://www.merval.sba.com.ar/default.aspx"
query_site = urllib.urlopen(site)

soup = BeautifulSoup(query_site, 'html.parser')
stocks_soup = soup.find_all('td',class_='celdaPanelTablaContenido')
stocks_soup = soup.find_all('a', class_='linkPanel')
stocks=[]

for stock in stocks_soup:
     if len(stock.get_text())>1:
          stocks.append(stock.get_text())

data=[]
data_soup= soup.find_all('span',class_='txtPanelContenido')
data_soup = data_soup[-len(stocks)*3:]

for d in data_soup:
     data.append(d.get_text())

merval = pd.DataFrame({'stock':stocks,
                       'close':data[0::3],
                       'var':data[1::3],
                       'vol':data[2::3]})

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

auth.set_access_token(access_token, access_secret)
now = datetime.now()
 #Construct the API instance
api = tweepy.API(auth) # create an API object

if now.strftime("%A") != ("Saturday" or "Sunday"):  
    for index, accion in merval.iterrows():
         try:
              api.update_status(str(now.day)+"/"+str(now.month)+"/"+str(now.year)+":  "+ "$"+accion['stock'] + " cierra en "+ accion['close']+". Variación diaria: " + accion['var'])
         except tweepy.error.TweepError:
              pass