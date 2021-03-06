
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urlparse import urlsplit
from collections import deque
import re
import pandas as pd
import tldextract

df=pd.read_csv('urls.csv')
#print df

#new_urls = deque(dfa)

# a queue of urls to be crawled
#ew_urls = deque(['http://www.hungryharvest.net/','http://www.themoscowtimes.com/contact_us/index.php'])
new_urls = deque(['placeholder'])
#print new_urls


for index, row in df.iterrows():
    print row['url']
    new_urls.append(str(row['url']))

print new_urls


# a set of urls that we have already crawled
processed_urls = set()

# a set of crawled emails
emails = set()

myarray = []

# process urls one by one until we exhaust the queue
while len(new_urls):

    # move next url from the queue to the set of processed urls
    url = new_urls.popleft()
    processed_urls.add(url)

    print url


    print "New URL count" ,len(new_urls)
    print "Processed URL count" ,len(processed_urls)
    # extract base url to resolve relative links
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    #print 'base_url - ' + base_url
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    #print 'path - '+ path

    ext = tldextract.extract(url)
    domain = ext.domain
    rdomain = ext.registered_domain

    #print domain
    #print "url: " + url
    #print "rdomain: "+rdomain

    # get url's content
    #print("Processing %s" % url)
    try:
        response = requests.get(url)
    except:
    #except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        continue

    # extract all email addresses and add them into the resulting set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    emails.update(new_emails)
    #print new_emails

    for emails1 in new_emails:
        print "Email Found:", emails1
        myarray.append([url,emails1])

    #emails = set()

    # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text,"lxml")

    # find and process all the anchors in the document
    for anchor in soup.find_all("a"):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''

        #print 'link - ' + link

        # resolve relative links
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link

        #if domain in link:
        #    print 'yep'

        #if link.find('hungry'):
         #   print 'yep'

        # add the new url to the queue if it was not enqueued nor processed yet
        if not link in new_urls and not link in processed_urls and rdomain in link and len(processed_urls) < 30 and len(new_urls) < 30:
            new_urls.append(link)
        #print new_urls

#print emails
print "Array:", myarray

mydf=pd.DataFrame(myarray, columns=['url','email'])

mydf.to_csv('emails.csv', index=False, encoding='utf-8')
