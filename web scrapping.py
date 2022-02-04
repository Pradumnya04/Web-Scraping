''' Import packages
'''
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPError
from datetime import datetime, timedelta
import operator
from functools import reduce
import pandas as p
import csv

''' reading the url from page no 1 to 10.
    save the urls in list s
    due to slow computation of system , set the range upto page 9
'''
base_url = 'https://www.rapid7.com/db/?q=&type=nexpose&page='
url_list = ["{}{}".format(base_url, str(page)) for page in range(1, 10)]
s=[]
for url in url_list:
    s.append(url)
    
   
''' with the help of BeautifulSoup , 
    parse the html file and save the required div in seperate list ls and ls1 
    according to the div class name
''' 
data = []
data1= []
for pg in s:
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(pg)
    try:
        search_response = urllib.request.urlopen(pg)
    except urllib.request.HTTPError:
        pass
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value
    ls = [x.get_text(strip=True) for x in soup.find_all("div", {"class": "resultblock__info-title"})]
    ls1=  [x.get_text(strip=True) for x in soup.find_all("div", {"class": "resultblock__info-meta"})]
    # save the data 
    data.append((ls))
    data1.append(ls1)
 
 
''' with the help of reduce function,Flatten a List of Lists 
    data and data1
'''   
col1 =reduce(operator.concat, data)
col2 =reduce(operator.concat, data1)

 
''' with help of pandas, create a dataframe with required columns name
    and the col1 ,col2 list data
'''   
df=p.DataFrame(col1,columns=['Topic of vulnarability'])
df['Published Date']=col2


'''data cleaning and data processing on the dataframe

'''

#remove the  " ' "
df.applymap(lambda x: x.replace("'", ""))
#  strip the published from the column
df['Published Date'] = df['Published Date'].map(lambda x: x.lstrip('Published: '))
#  replace \r\n with empty string
df['Published Date'] = df['Published Date'].map(lambda x: x.replace("\r\n", ""))
#create a new column 
df['Severity'] = df['Published Date'][0][-1]
# with the help of slicing take remove unwanted space
df['Published Date']= df['Published Date'][0][0:16]
#save to csv file
df.to_csv('vulnarability list1.csv')
