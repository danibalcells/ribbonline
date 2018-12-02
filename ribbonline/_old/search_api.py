import datetime

import TwitterSearch as tw

from .tweet import Tweet
from .collection import TweetCollection


class SearchController(object):

    def __init__(self, credentials):
        self.ts = tw.TwitterSearch(
            consumer_key = credentials['api_key'],
            consumer_secret = credentials['api_secret_key'],
            access_token = credentials['access_token'],
            access_token_secret = credentials['access_token_secret']
        )
        self.authenticate()
        
    def authenticate(self, verify=True):
        self.ts.authenticate(verify)

    def get_tweets_in_interval(self, since, until, keywords,
                               keywords_or_operator=True,
                               include_entities=False):
        tso = tw.TwitterSearchOrder()
        if keywords:
            tso.set_keywords(keywords,
                             or_operator=keywords_or_operator)
        tso.set_include_entities(include_entities)
        tso.set_since(since)
        tso.set_until(until)

        tweets = TweetCollection([])
        for tweet_data in self.ts.search_tweets_iterable(tso):
            tweets.append(Tweet(tweet_data))

        return tweets
