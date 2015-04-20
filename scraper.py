import urllib2
import tweepy
import time
from bs4 import BeautifulSoup

CONSUMER_KEY = 'vq4ePtpnNODPQAOpuIYE4FwEg'
CONSUMER_SECRET = 'pksbOZE4pft0eE1gl0MwqeTwtXrVOMW6FK78ESkTYXaahxHgKN'
ACCESS_TOKEN = '3165849229-tzLiXEZSjWORyjZt4a420YecMN5zMkIoPLFzWkN'
ACCESS_TOKEN_SECRET = 'jawWauNnQAjx2QPvGYJ8BTcxfkUtM8PygOVnVToz2l6yx'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


infile = open('RFPList.txt', 'r')
RFPS = infile.read()

outfile = open('RFPList.txt', 'a')
soup = BeautifulSoup(urllib2.urlopen('http://nau.edu/Contracting-Purchasing-Services/NAU-Bid-Board/').read())

for row in soup('table', {'class': 'table table-striped table-bordered'})[0].tbody('tr'):
    tds = row('td')
    new = 0
    count = 0
    tweet = ""
    # check if we've logged this particular entry before
    if tds[0].string not in RFPS:
        print "New RFP #{0}, Adding to index".format(tds[0].string)
        new = 1
        outfile.write(tds[0].string + "\n")

    # if new entry, tweet that ish
    if new:
        tweet += tds[0].string + "\n"
        tweet += "Req: " + tds[1].string + "\n"
        tweet += "Link: " + "http://nau.edu" + tds[2].find('a').get('href') + "\n"
        tweet += "Due: " + tds[3].string.replace("Arizona Local Time", "") + "\n"

    # regardless if new, echo out the contents of the entry to console
    print tds[0].string
    print "Req: " + tds[1].string
    print "Link: " + "http://nau.edu" + tds[2].find('a').get('href')
    print "Due: " + tds[3].string
    print "\n"
    #flag that keeps track of whether we're making a new tweet or not

    if new:
        print "Posting tweet for " + tds[0].string + "\n"
        print tweet
        api.update_status(status=tweet)

