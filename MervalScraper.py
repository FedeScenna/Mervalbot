# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 19:20:45 2018

@author: federico.i.scenna
"""
from secrets import *
from bs4 import BeautifulSoup
import urllib.request as urllib
import time, datetime
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

 #Construct the API instance
api = tweepy.API(auth) # create an API object

try:
     api.update_status("Cierre de las acciones del índice Merval al día "+str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year))
except tweepy.error.TweepError:
     pass
time.sleep(3)
for index, accion in merval.iterrows():
     try:
          api.update_status(str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)+": "+accion['stock'] + " cierra en "+ accion['close']+". Variación diaria: " + accion['var'])
     except tweepy.error.TweepError:
          pass
     time.sleep(3)