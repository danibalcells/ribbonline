import datetime

from .util import assert_is_instance


class DailyOpinionSplit(object):

    def __init__(self, date, tweets):
        self.date = date
        self.tweets = tweets
        self.text_has_ribbon = \
            self.tweets.text_has_ribbon.length
        self.username_has_ribbon = \
            self.tweets.username_has_ribbon.length
        #  self.user_description_has_ribbon = \
            #  self.tweets.user_description_has_ribbon.length
        self.text_has_flag = \
            self.tweets.text_has_flag.length
        self.username_has_flag = \
            self.tweets.username_has_flag.length
        #  self.user_description_has_flag = \
            #  self.tweets.user_description_has_flag.length
        self.neutral = (self.tweets.length -
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
            #  self.neutral,
            #  self.user_description_has_flag,
            self.username_has_flag,
            self.text_has_flag,
        ]

    def sample(self):
        return [
            self.tweets.text_has_ribbon[0],
            self.tweets.username_has_ribbon[1],
            self.tweets.username_has_flag[1],
            self.tweets.text_has_flag[0]
        ]


class OpinionTimeline(object):

    def __init__(self, opinions):
        self.opinions = opinions
        self._sort()

    def append(self, opinion, sort=True):
        self.opinions.append(opinion)
        if sort:
            self._sort()

    def __iter__(self):
        for opinion in self.opinions:
            yield opinion

    def _sort(self):
        self.opinions.sort(key=lambda x: x.date)

    @property
    def tweets(self):
        return [o.tweets for o in self.opinions]

    @property
    def dates(self):
        return [o.date for o in self.opinions]

    @property
    def start_date(self):
        return min(self.dates)

    @property
    def end_date(self):
        return max(self.dates)

    @property
    def list(self):
        return [opinion.list for opinion in self.opinions]

    def filter_by_dates(self, since=None, until=None):
        if since and until:
            return OpinionTimeline(
                [o for o in self.opinions
                 if o.date >= since and o.date < until])
        elif since:
            return OpinionTimeline(
                [o for o in self.opinions
                 if o.date >= since])
        elif until:
            return OpinionTimeline(
                [o for o in self.opinions
                 if o.date < until])

    def sample_tweets(self):
        return [o.sample() for o in self.opinions]


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
            timeline.append(DailyOpinionSplit(since, daily_tweets), sort=False)
            since += datetime.timedelta(1)
        return timeline
