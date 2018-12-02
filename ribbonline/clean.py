from .tweet import TweetCollection


class OnePerUserCleaner(object):

    def __init__(self, dirty_tweets):
        self.dirty_tweets = dirty_tweets
        self.clean_tweets = TweetCollection([])
        self._unique_keys = []

    def clean(self):
        for tweet in self.dirty_tweets:
            key = self._get_key(tweet)
            if key not in self._unique_keys:
                self._unique_keys.append(key)
                self.clean_tweets.append(tweet)
        return self.clean_tweets

    def _get_key(self, tweet):
        text_has_ribbon = 'RT'
        username_has_ribbon = 'RU'
        neutral = 'NU'
        username_has_flag = 'FU'
        text_has_flag = 'FT'
        other = 'OT'

        flags = [
            tweet.text_has_ribbon,
            tweet.username_has_ribbon,
            tweet.username_has_flag,
            tweet.text_has_flag
        ]

        if sum(flags) > 1:
            return self._format_key(tweet, other)
        elif flags[0]:
            return self._format_key(tweet, text_has_ribbon)
        elif flags[1]:
            return self._format_key(tweet, username_has_ribbon)
        elif flags[2]:
            return self._format_key(tweet, username_has_flag)
        elif flags[3]:
            return self._format_key(tweet, text_has_flag)
        else:
            return self._format_key(tweet, neutral)


    def _format_key(self, tweet, category):
        return f'{tweet.user_id}_{tweet.date.date()}_{category}'
