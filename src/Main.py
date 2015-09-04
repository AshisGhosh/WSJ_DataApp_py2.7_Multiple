'''
Created on Sep 2, 2015

@author: Ashis
'''

#include the 2 below exports for .exe creation with pyinstaller
import Tkinter
import FileDialog

from lxml import html
import requests
import time
import re
import calendar
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.pyplot import flag
import datetime
import pandas as pd
import pandas.tseries.offsets
from time import strftime


#class Month(OrderedEnum):
        
#months = ['January', 'February', 'March', 'Apriil','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#list(enumerate(months, start=1))

searchterms = []
pagetotal = []

searchnum = raw_input('How many queries do you wish to make?')

for i in range(int(searchnum)):
    print('Enter for your #' + str(i+1) + " WSJ search:")
    searchterms.append(raw_input())

    page = (requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' +  searchterms[i] +'&isAdvanced=true&min-date=1911/09/03&max-date=' + time.strftime("%Y/%m/%d") + '&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch'))

    #page = requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' + searchterms + '&isAdvanced=true&min-date=1911/09/03&max-date=2015/09/03&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch')

    tree = html.fromstring(page.text)

    totalpages = str(tree.xpath('//div[@class="results-menu-wrapper bottom"]//menu[@class="results"]//li[@class="results-count"]/text()'))

    totalpages = re.sub(r"[\D]", "", totalpages)

    print('There are a total of ' + totalpages + ' pages enter the number of pages you\'d like to search (max 50):')

    pagetotal.append(raw_input())   

    print('Searching ' + searchterms[i] + ' for ' + pagetotal[i] + ' pages.')

print('Please wait, the web scraping has begun!')

pagetotal = [int(x) for x in pagetotal]

oldest_date = time.strptime(time.strftime("%B %Y"), "%B %Y")

tabl = []

for i in range(int(searchnum)):
    dates_raw = []
    for j in range(1,pagetotal[i]+1): 
        page = requests.get('http://www.wsj.com/search/term.html?KEYWORDS=+' + searchterms[i] +'&isAdvanced=true&min-date=1911/09/03&max-date=' + time.strftime("%Y/%m/%d") + '&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,sitesearch&page=' + str(j))
        tree = html.fromstring(page.text)
        dates_raw.append(tree.xpath('//div[@class="headline-container"]//time/text()'))
        
    #print(dates_raw)
    dates_raw = list(itertools.chain(*dates_raw))

    dates = [re.sub(r"[.,]|\W\d*:(.*)","", dates_raw[x]) for x in range(len(dates_raw))]


    for y in range(len(dates)):
        try:
            try:
                dates[y] = time.strptime(dates[y], "%b %d %Y")
            except:
                dates[y] = time.strptime(dates[y], "%B %d %Y")
            if (dates[y]<oldest_date):
                oldest_date = dates[y]
            dates[y] = time.strftime("%B %Y", dates[y])    
        except:
            dates[y] = time.strftime("%B %Y")
        
                
    
    ps = pd.Series(dates)
    
    #df = ps.str.split(" ").apply(pd.Series)
      
    #df.columns = ['Month', 'Year']
    
    df = pd.DataFrame({'Date':dates})
    
    #size = df.groupby(['Month', 'Year'], sort=False).size()
    size = df.groupby(['Date'], sort=False).size()

    tabl.append(pd.Series(size.values, index = ps.unique()))

#print(tabl)

#for num in range(int(searchnum)):
 #   print(tabl[num])
  #  print(type(tabl[num]))
   # print(tabl[num].index)
    
#print(oldest_date)

oldest_date = time.strftime("%B %Y", oldest_date)

end_date = datetime.datetime.now() + pandas.tseries.offsets.DateOffset(months=1)
datesrange = pd.date_range(oldest_date, end_date, freq='M')
#print(datesrange)
datesrange = [calendar.month_name[datesrange[x].month] + " " + str(datesrange[x].year) for x in range(len(datesrange))]
#print(datesrange)

#print(type(tabl[0]))
#print(tabl[0].values)

df_tabl =[]

for x in range(int(searchnum)):
    df_tabl.append(pd.DataFrame({searchterms[x]:tabl[x].values}, index = tabl[x].index))

#print(df_tabl)

df_result = pd.DataFrame({'hold':range(len(datesrange))}, index = datesrange)



for x in range(int(searchnum)):
    df_result = pd.concat([df_result,df_tabl[x]], axis=1)    

df_result.sort('hold', inplace=True)
del df_result['hold']
print(df_result)


df_result.plot(kind = "bar")
plt.show()

#plt.gca().invert_xaxis()

#plt.show()

#df = pd.DataFrame({'Count':ps.value_counts(sort=False)})

#print(ps.value_counts(sort=False).index)

#df.reindex([""])
#print(df.axes)

#df.plot(kind = "bar")
#plt.show()

#df = pd.DataFrame({'Date':dates})
#print(list(df.columns.values))
#print(df.values)
#date_sum = df.groupby('Date').size()


#date_groups = df.groupby('Date').groups

#print(date_sum)
#print(df.groupby('Date').)

#date_sum.plot(kind = "bar")

#plt.show()



