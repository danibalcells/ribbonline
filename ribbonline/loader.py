import csv
import logging

from ribbonline.tweet import Tweet, TweetCollection


logger = logging.getLogger(__name__)

class TweetCSVLoader(object):

    def __init__(self):
        self.tweet_ids = []
        self.tweets = TweetCollection([])

    def _load(self, filename, one_in=None):
        logger.info(f'Loading {filename}')
        with open(filename) as f:
            reader = csv.DictReader(f)
            i = 0
            for line in reader:
                if line['id'] not in self.tweet_ids:
                    i += 1
                    if i == one_in:
                        i = 0
                        self.tweet_ids.append(line['id'])
                        self.tweets.append(Tweet(line))

    def load_multiple(self, filenames, one_in=1):
        for filename in filenames:
            self._load(filename, one_in)
        return self.tweets
