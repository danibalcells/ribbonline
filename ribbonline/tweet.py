import dateparser

from . import constants
from .util import has_emoji, assert_is_instance


class Tweet(object):

    def __init__(self, raw_data):
        # self.raw_data = raw_data
        self.id = raw_data['id']
        self.text = raw_data['tweet']
        self.username = raw_data['name']
        self.user_description = ''  # For now
        self.user_id = raw_data['user_id']
        self.date = dateparser.parse(raw_data['date'])

    @property
    def text_has_ribbon(self):
        return has_emoji(self.text, constants.EMOJI_RIBBON)

    @property
    def username_has_ribbon(self):
        return has_emoji(self.username, constants.EMOJI_RIBBON)

    @property
    def user_description_has_ribbon(self):
        return has_emoji(self.user_description, constants.EMOJI_RIBBON)

    @property
    def text_has_flag(self):
        return has_emoji(self.text, constants.EMOJI_FLAG)

    @property
    def username_has_flag(self):
        return has_emoji(self.username, constants.EMOJI_FLAG)

    @property
    def user_description_has_flag(self):
        return has_emoji(self.user_description, constants.EMOJI_FLAG)


class TweetCollection(object):

    def __init__(self, tweets):
        self.tweets = tweets

    def __add__(self, other):
        assert_is_instance(other, TweetCollection)
        return TweetCollection(self.tweets + other.tweets)

    def __getitem__(self, idx):
        return self.tweets[idx]

    def __setitem__(self, idx, tweet):
        assert_is_instance(tweet, Tweet)
        self.tweets[idx] = tweet

    def append(self, tweet):
        assert_is_instance(tweet, Tweet)
        self.tweets.append(tweet)

    def extend(self, tweet_collection):
        assert_is_instance(other, TweetCollection)
        self.tweets.extend(tweet_collection.tweets)

    def filter_by_property(self, property_name):
        return TweetCollection(
            [t for t in self.tweets if t.__getattribute__(property_name)])

    def filter_by_dates(self, since, until):
        return TweetCollection(
            [t for t in self.tweets if t.date >= since and t.date < until])

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
