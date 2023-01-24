#!/usr/bin/env python
# coding: utf-8

# ## Scaning and parsing news from newswire website:

# In[9]:


#importing libraries
import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
from datetime import timedelta
from datetime import datetime

#fetching current date
now = datetime.now()
print('Current DateTime:', now)
current_date = now.date()
year= now.year
month=now.month
day=now.day
today = date(year, month, day)

#fetching previous date
prevdate=today - timedelta(days=7)
x=str(prevdate).split("-")
year=x[0]
month=x[1]
day=x[2]

#fetching news from the given url
pageinc=1
upperframe=[]  
for page in range(1,pageinc+1):
    
    url = 'https://www.prnewswire.com/news-releases/news-releases-list/?month='+str(month)+'&day='+str(day)+'&year='+str(year)+'&hour=12'
    print(url)
    
    try:
        
        page=requests.get(url)                            
    
    except Exception as e:
        print(e)
        continue                                              
    time.sleep(2)   
    soup=BeautifulSoup(page.text,'html.parser')
    #print(soup)
    
    frames = []
    
#fetching data using BeautifulSoup
    for a in soup.findAll('a',href=True, attrs={'class':"newsreleaseconsolidatelink display-outline"}):
      if a.img: 
        Date=a.find('div',attrs={'class':'col-sm-8 col-lg-9 pull-left card'}).find('h3').find('small')
        Date=str(Date).split('</small>')
        Date=Date[0].replace('<small>','')
       
        Title = a.img['title'] # Title of article
        summary = a.find('p', attrs={"class":"remove-outline"}) # Summary of article stored in 'p' tag
       
        # Storing Date,title and summary in dictionary
        article_dict = {
        'Date': Date,
        'title': Title ,
        'summary': summary.text
        }
    
        # Appending dictionary to empty list    
        frames.append(article_dict)  
        
df = pd.DataFrame(frames) 
#df.head()

#searching for stock symbol from all stock split news 
import re

url1="https://www.prnewswire.com/news-releases/financial-services-latest-news/stock-split-list/?"
print(url1)
    
try:
        
      page=requests.get(url1)                            
    
except Exception as e:
        print(e)
                                                      
time.sleep(2)   
soup=BeautifulSoup(page.text,'html.parser')
#print(soup)
s=[]
for a in soup.findAll('a',href=True, attrs={'class':"newsreleaseconsolidatelink display-outline"}):
      if a.img: 
       
        Title = a.img['title'] # Title of article
        summary1= a.find('p', attrs={"class":"remove-outline"})
        
        dict2= {
        'Title':Title,
        'summary': summary1.text
        }
    
        # Appending dictionary to empty list    
        s.append(dict2)  
        print(s)

stocks=[]
df = pd.DataFrame(s) 
for i in range(len(df)):
    
    stocks = stocks + re.findall(r'\b[A-Z]{2,}\b', df.iloc[i]['summary']) 
   
 # Removing duplicates, by converting into set
stocks = list(set(stocks))

# printing to check the stock codes
print('Stock Codes ', stocks)


# ## storing the news to csv file:

# In[17]:


df.to_csv("stocks.csv")


# ## Retrieved stock symbols are :
# ['SPCB', 'IM', 'CNS', 'NYAX', 'NYSE', 'SNES', 'TECH', 'TASE', 'PEYE', 'IMC', 'ONCS', 'KTRA', 'AMPE', 'TA', 'AG', 'AI', 'BHRB', 'IMCC', 'EPA', 'CNSP', 'CSE', 'MMM', 'OTCPK', 'MYSZ', 'OTCQB', 'NASDAQ', 'OTC']
# 

# ## Searching yahoo finance page for the stock symbols:

# In[18]:


#installing yfinance library
get_ipython().system('pip install yfinance --user')


# In[19]:


#Using yfinance module,retrieving data for the fetched stock symbols
import yfinance as yf

data =['CNSP', 'AG', 'TASE', 'SPCB', 'IM', 'BHRB', 'OTCQB', 'MMED', 'PEYE', 'NEO', 
       'CSE', 'NASDAQ', 'SNES', 'CNS', 'IMC', 'EPA', 'AMPE', 'NYSE', 'MNMD', 'MMM',
       'OTC', 'NYAX', 'KTRA', 'OTCPK', 'ONCS', 'TECH', 'IMCC']
data = yf.download("CNSP AG TASE SPCB IM BHRB OTCQB MMED PEYE NEO CSE NASDAQ SNES CNS IMC EPA AMPE NYSE MNMD MMM OTC NYAX KTRA OTCPK ONCS TECH IMCC", period="6m",
        group_by='ticker', actions=False)


# In[20]:


#since there were no data for the above 11 stock symbols, fetched the data for the other stock symbols for a period of 1 year
data = yf.download("CNSP AG SPCB BHRB NEO SNES CNS AMPE MNMD MMM NYAX KTRA ONCS TECH IMCC", period="1y",
        group_by='ticker', actions=False)


# In[21]:


data


# ## Time series plot for volume of the stocks

# In[42]:


import warnings
warnings.filterwarnings("ignore")
stocks=["CNSP","AG", "SPCB", "BHRB", "NEO", "SNES", "CNS", "AMPE", "MNMD", "MMM", "NYAX", "KTRA", "ONCS", "TECH","IMCC"]
import matplotlib.pyplot as plt
plt.style.use("dark_background")
fig, axes = plt.subplots(nrows=5,ncols=3,figsize=(20,30),dpi=200)
plt.subplots_adjust(hspace=0.3,wspace=0.3)
for i in range(5):
    for j in range(3):
        stock=stocks[:].pop()
        axes[i][j].plot(data.index,data[stock]['Volume'])
        axes[i][j].set_xlabel("Date")
        axes[i][j].set_ylabel("Volume")
        
for ax,stock in zip(axes.flat,stocks):
    ax.set_title(f"VOLUME FOR {stock}",color="Green",fontsize=20)

fig.show()


# ## Time series plot for adjusted close

# In[44]:


fig, axes = plt.subplots(nrows=5,ncols=3,figsize=(20,25),dpi=200)
plt.subplots_adjust(hspace=0.3,wspace=0.3)
for i in range(5):
  for j in range(3):
      stock = stocks[i+j]
      axes[i][j].plot(data.index,data[stock]['Adj Close'])
      axes[i][j].set_xlabel("Date")
      axes[i][j].set_ylabel("Adj close")
        
for ax,stock in zip(axes.flat,stocks):
    ax.set_title(f"Adj. Close for {stock}",color="Green",fontsize=20)

fig.show()


# # Analyzing trend for NEO
# 
# 

# In[61]:


neo_data=data["NEO"]
neo_data


# ## Checking trend for stock "NEO" using TA-Lib

# In[50]:


# installing ta lib- python's technical analysis library
get_ipython().system('pip install TA-Lib')


# ## simple moving average:

# In[143]:


#calulating simple moving average for last 50 days
import talib as ta
neo_data["SMA"]=ta.SMA(neo_data['Adj Close'],50)


# In[144]:


#plotting the trend
plt.figure(figsize=(20,7))
plt.plot(neo_data.index,neo_data['Adj Close'])
plt.plot(neo_data.index,neo_data["SMA"])
plt.show()


# ## exponential moving average

# In[145]:


#calculating exponential moving average
neo_data["EMA"]=ta.EMA(neo_data['Adj Close'],50)


# In[146]:


#checking the trend in ema
plt.figure(figsize=(20,7))
plt.plot(neo_data.index,neo_data['Adj Close'])
plt.plot(neo_data.index,neo_data["EMA"])
plt.show()


# ## RSI-relative strength indicator which will tell us whether to buy or sell the stock

# In[147]:


neo_data["RSI"]=ta.RSI(neo_data['Adj Close'])
neo_data


# In[148]:


# plot price
plt.figure(figsize=(15,5))
plt.plot(neo_data.index, neo_data['Adj Close'])
plt.title('RSI graph for NEO stock- Adj Close')
plt.show()


# plot correspondingRSI values and significant levels
plt.figure(figsize=(15,5))
plt.title('RSI graph')
plt.plot(neo_data.index, neo_data['RSI'])
plt.axhline(30, linestyle='--',color="green",label="buy the stock") # RSI below this means you should buy this stock

plt.axhline(70, linestyle='--',color="red",label="sell the stock")# RSI above this means you should sell this stock
plt.legend()
plt.show()


# ## conclusion:
# As per the above graph, the stock neo was good to be bought in early 2022 but currently it should be sold if already bought.

# In[ ]:




