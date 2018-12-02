import csv

from ribbonline.tweet import Tweet, TweetCollection


class TweetCSVLoader(object):

    def __init__(self):
        self.tweet_ids = []
        self.tweets = TweetCollection([])

    def _load(filename):
        with open(filename) as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['id'] not in self.tweet_ids:
                    self.tweet_ids.append(line['id'])
                    self.tweets.append(Tweet(line))

    def load_multiple(filenames):
        for filename in filenames:
            self._load(filename)
        return self.tweets
