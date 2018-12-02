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

    def __repr__(self):
        return (f'<Tweet by "{self.username}" on {self.date.date()}: '
                f'"{self.text[:30]}...">')

    def __str__(self):
        return f'{self.date.date()} "{self.username}": "{self.text[:30]}..."'

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

    def __iter__(self):
        for tweet in self.tweets:
            yield tweet

    def __add__(self, other):
        return TweetCollection(self.tweets + other.tweets)

    def __getitem__(self, idx):
        return self.tweets[idx]

    def __setitem__(self, idx, tweet):
        self.tweets[idx] = tweet

    def append(self, tweet):
        self.tweets.append(tweet)

    def extend(self, tweet_collection):
        self.tweets.extend(tweet_collection.tweets)

    def filter_by_property(self, property_name):
        return TweetCollection(
            [t for t in self.tweets if t.__getattribute__(property_name)])

    def filter_by_dates(self, since=None, until=None):
        if since and until:
            return TweetCollection(
                [t for t in self.tweets
                 if t.date >= since and t.date < until])
        elif since:
            return TweetCollection(
                [t for t in self.tweets
                 if t.date >= since])
        elif until:
            return TweetCollection(
                [t for t in self.tweets
                 if t.date < until])

    @property
    def length(self):
        return len(self.tweets)

    @property
    def start_date(self):
        return min([t.date for t in self.tweets])

    @property
    def end_date(self):
        return max([t.date for t in self.tweets])

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
