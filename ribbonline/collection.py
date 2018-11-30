from .tweet import Tweet
import numpy as np


class TweetCollection(object):

    def __init__(self, tweets):
        self.tweets = tweets

    def __add__(self, other):
        if isinstance(other, TweetCollection):
            return TweetCollection(self.tweets+other.tweets)
        else:
            raise ValueError(f'{other} is not a TweetCollection')

    def __getitem__(self, idx):
        return self.tweets[idx]

    def __setitem__(self, idx, tweet):
        if isinstance(tweet, Tweet):
            self.tweets[idx] = tweet
        else:
            raise ValueError(f'{tweet} is not a Tweet')

    def append(self, tweet):
        if isinstance(tweet, Tweet):
            self.tweets.append(tweet)
        else:
            raise ValueError(f'{tweet} is not a Tweet')

    def filter_by_property(self, property_name):
        return TweetCollection(
            [t for t in self.tweets if t.__getattribute__(property_name)])

    @property
    def length(self):
        return len(self.tweets)

    @property
    def text_has_ribbon(self):
        return self.filter_by_property('text_has_ribbon')

    @property
    def username_has_ribbon(self):
        return self.filter_by_property('username_has_ribbon')

    @property
    def user_description_has_ribbon(self):
        return self.filter_by_property('user_description_has_ribbon')

    @property
    def text_has_flag(self):
        return self.filter_by_property('text_has_flag')

    @property
    def username_has_flag(self):
        return self.filter_by_property('username_has_flag')

    @property
    def user_description_has_flag(self):
        return self.filter_by_property('user_description_has_flag')
