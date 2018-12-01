import datetime
import logging

from twitterscraper import query_tweets
from bs4 import BeautifulSoup

from .tweet import Tweet
from .collection import TweetCollection


class SearchController(object):

    def __init__(self):
        pass

    def _get_query_string(self, keywords, or_operator=True):
        if or_operator:
            return ' OR '.join(keywords)
        else:
            return ' AND '.join(keywords)

    def _query(self, since, until, query,
               limit=None, poolsize=20):
        raw_tweets = query_tweets(query,
                                  begindate=since,
                                  enddate=until,
                                  limit=limit,
                                  poolsize=poolsize)
        tweets = TweetCollection([])
        for raw_tweet in raw_tweets:
            tweets.append(Tweet(raw_tweet.__dict__))
        return tweets

    def get_tweets_in_interval(self, since, until, keywords,
                               subperiod=None,
                               keywords_or_operator=True,
                               limit=None,
                               poolsize=20):
        query_string = self._get_query_string(keywords,
                                              keywords_or_operator)
        logging.info(f'Getting tweets for query {query_string} in period '
                     f'{since} to {until}')
        if subperiod:
            tweets = TweetCollection([])
            subperiod_since = since
            while subperiod_since < until:
                subperiod_until = subperiod_since + subperiod
                logging.info(f'Getting tweets for query {query_string} in '
                             f'subperiod {subperiod_since} to '
                             f'{subperiod_until}')
                subperiod_tweets = self._query(subperiod_since,
                                               subperiod_until,
                                               query_string,
                                               limit,
                                               poolsize)
                tweets.extend(subperiod_tweets)
                subperiod_since += subperiod
            return tweets
        else:
            return self._query(since, until, query_string, limit, poolsize)
