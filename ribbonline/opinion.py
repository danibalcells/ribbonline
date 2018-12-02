import datetime

from .util import assert_is_instance


class DailyOpinionSplit(object):

    def __init__(self, date, tweet_collection):
        self.date = date
        self.tweet_collection = tweet_collection
        self.text_has_ribbon = \
            self.tweet_collection.text_has_ribbon.length
        self.username_has_ribbon = \
            self.tweet_collection.username_has_ribbon.length
        #  self.user_description_has_ribbon = \
            #  self.tweet_collection.user_description_has_ribbon.length
        self.text_has_flag = \
            self.tweet_collection.text_has_flag.length
        self.username_has_flag = \
            self.tweet_collection.username_has_flag.length
        #  self.user_description_has_flag = \
            #  self.tweet_collection.user_description_has_flag.length
        self.neutral = (self.tweet_collection.length -
                        self.text_has_ribbon -
                        self.username_has_ribbon -
                        #  self.user_description_has_ribbon -
                        self.text_has_flag -
                        self.username_has_flag
                        #  self.user_description_has_flag
                        )

    @property
    def list(self):
        return [
            self.text_has_ribbon,
            self.username_has_ribbon,
            #  self.user_description_has_ribbon,
            self.neutral,
            #  self.user_description_has_flag,
            self.username_has_flag,
            self.text_has_flag,
        ]


class OpinionTimeline(object):

    def __init__(self, daily_opinions):
        self.daily_opinions = daily_opinions
        self._sort()

    def append(self, daily_opinion, sort=True):
        self.daily_opinions.append(daily_opinion)
        if sort:
            self._sort()

    def __iter__(self):
        for opinion in self.daily_opinions:
            yield opinion

    def _sort(self):
        self.daily_opinions.sort(key=lambda x: x.date)

    @property
    def list(self):
        return [opinion.list for opinion in self.daily_opinions]

    def filter_by_dates(self, since=None, until=None)
        if since and until:
            return OpinionTimeline(
                [o for o in self.daily_opinions
                 if o.date >= since and o.date < until])
        elif since:
            return OpinionTimeline(
                [o for o in self.daily_opinions
                 if o.date >= since])
        elif until:
            return OpinionTimeline(
                [o for o in self.daily_opinions
                 if o.date < until])


class OpinionController(object):

    def __init__(self):
        pass

    def create_timeline(self, tweets, start_date=None, end_date=None):
        if not start_date:
            start_date = tweets.start_date
        if not end_date:
            end_date = tweets.end_date
        timeline = OpinionTimeline([])
        since = start_date
        while since < end_date:
            until = since + datetime.timedelta(1)
            daily_tweets = tweets.filter_by_dates(since, until)
            timeline.append(DailyOpinionSplit(until, daily_tweets), sort=False)
            since += datetime.timedelta(1)
        return timeline
