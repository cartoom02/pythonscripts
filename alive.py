import httplib


import pickle, os, sys, logging
from httplib import HTTPConnection, socket
from smtplib import SMTP



from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urlparse import urlsplit
from collections import deque
import re
import pandas as pd
import tldextract

df=pd.read_csv('urls_alive.csv')

new_urls = deque(['placeholder'])
#print new_urls

for index, row in df.iterrows():
    #print row['url']
    new_urls.append(str(row['url']))

#print new_urls

myarray = []




while len(new_urls):

    url = new_urls.popleft()
    print url

    try:

        # move next url from the queue to the set of processed urls

        conn = httplib.HTTPConnection(url, timeout=3)
        print conn
        conn.request("HEAD", "/")
        r1 = conn.getresponse()
        print r1.status, r1.reason



        myarray.append([url,r1.status, r1.reason])


    except:
        print 'pass'


mydf=pd.DataFrame(myarray, columns=['url','email','sdas'])

mydf.to_csv('emails2123.csv', index=False, encoding='utf-8')
