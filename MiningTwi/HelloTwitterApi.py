__author__ = 'ccuulinay'

import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

# Magic!
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

#import urllib2
#print urllib2.urlopen('http://www.twitter.com').read()

import twitter
import json
import pandas as pd
from pandas import Series, DataFrame
from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np


CONSUMER_KEY = 'CfuBdRkXfgHBpqFp4kbCfIaPV'
CONSUMER_SECRET = 'xNYkjJyF9yWcEuVIdzIKPIcm1CjSjimzXzb3Zzfw5EopbvRnBM'
OAUTH_TOKEN = '501488845-NG2mECd1NejqzZpebacXU6WeDLN1o3GjmWReSZ7J'
OAUTH_TOKEN_SECRET = 'bH0uaC9K9rJPlkAChzRYyeeNXMUu3G6ku3DHuHk8uT66w'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

WORLD_WOE_ID = 1
US_WOE_ID = 23424977

def getTrends():
    # Prefix ID with the underscore for query string parameterization.
    # Without the underscore, the twitter package appends the ID value
    # to the URL itself as a special case keyword argument.
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    us_trends = twitter_api.trends.place(_id=US_WOE_ID)
    #print json.dumps(world_trends, indent=1)
    #print
    #print json.dumps(us_trends, indent=1)

    world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
    us_trends_set = set([trend['name'] for trend in us_trends[0]['trends']])

    common_trends = world_trends_set.intersection(us_trends_set)

    print common_trends


def getTweetStatuses():
    q = "#SongsThatTouchMyHeart"
    count = 100

    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']



    for _ in range(5):
        print "Length of statuses", len(statuses)
        try:
            next_results = search_results['search_metadata']['next_results']
            print "Length of next results", len(next_results)
        except KeyError, e:
            break

        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

        #print kwargs

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    return statuses
    #print len(statuses)
    #print json.dumps(statuses[0], indent=1)


def getEntities(statuses):
    status_texts = [ status['text'] for status in statuses]
    screen_names = [user_mention['screen_name'] for status in statuses for user_mention in status['entities']['user_mentions']]
    hashtags = [hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags']]

    words = [w for t in status_texts for w in t.split()]

    print status_texts[0:5]
    print screen_names[0:5]
    print hashtags[0:5]
    print words[0:5]

    for item in [words, screen_names, hashtags]:
        c = Counter(item)
        print c.most_common()[:10] # Get top 10
        print

    for label, data in (('Word', words),('Screen Name', screen_names),('Hashtag', hashtags)):
        pt = PrettyTable(field_names=[label, 'Count'])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:10]]
        pt.align[label], pt.align['Count'] = 'l', 'r'
        print pt

    print
    print lexical_diversity(words)
    print lexical_diversity(screen_names)
    print lexical_diversity(hashtags)
    print average_words(status_texts)

    #plotFreqOfWords(words)
    histWordsScreenNamesAndHashtags(words, screen_names, hashtags)



def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)


def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)


def findMostPopularRetweets(statuses):
    retweets = [
        # Store out a tuple of these three values ...
        (status['retweet_count'],
         status['retweeted_status']['user']['screen_name'],
         status['retweeted_status']['id'],
         status['text'])


        for status in statuses

        # ... so long as the status meets this condition.
        if status.has_key('retweeted_status')
    ]

    # Slice off the first 5 from the sorted results and display each item in the tuple

    pt = PrettyTable(field_names=['Count', 'Screen Name','ID', 'Text'])
    [ pt.add_row(row) for row in sorted(retweets, reverse=True)[:5] ]
    pt.max_width['Text'] = 50
    pt.align= 'l'
    print pt

    return retweets




def lookupUserRetweetAStatus(status_id):
    _retweets = twitter_api.statuses.retweets(id=status_id)
    print [r['user']['screen_name'] for r in _retweets]


def plotFreqOfWords(words):
    word_counts = sorted(Counter(words).values(), reverse=True)

    plt.loglog(word_counts)
    plt.ylabel("Freq")
    plt.xlabel("Word Rank")
    plt.show()


def histWordsScreenNamesAndHashtags(words, screen_names, hashtags):
    for label, data in (('Words', words),
                    ('Screen Names', screen_names),
                    ('Hashtags', hashtags)):

        # Build a frequency map for each set of data
        # and plot the values
        c = Counter(data)
        plt.hist(c.values())

        # Add a title and y-label ...
        plt.title(label)
        plt.ylabel("Number of items in bin")
        plt.xlabel("Bins (number of times an item appeared)")

        # ... and display as a new figure
        plt.figure()
        plt.show()


def histRetweetCounts(retweets):
    # Using underscores while unpacking values in
    # a tuple is idiomatic for discarding them

    counts = [count for count, _, _, _ in retweets]

    plt.hist(counts)
    plt.title("Retweets")
    plt.xlabel('Bins (number of times retweeted)')
    plt.ylabel('Number of tweets in bin')
    plt.show()
    print counts
    #print np.log(counts)




getTrends()
#getTweetStatuses()
#getEntities(getTweetStatuses())
#findMostPopularRetweets(getTweetStatuses())
histRetweetCounts(findMostPopularRetweets(getTweetStatuses()))
#lookupUserRetweetAStatus(715756656936792064)



