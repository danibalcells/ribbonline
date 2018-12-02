import datetime

import twint


class TwitterCrawler(object):

    def __init__(self):
        self.config = twint.Config()

    def _get_filename(self, query, since, until):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return (f'crawls/'
                f'crawl_{timestamp}_'
                f'{since}_{until}_{query}')

    def crawl(self, query, since, until, limit, language):

        filename = self._get_filename(query, since, until)
        self.config.Search = query
        self.config.Output = filename
        self.config.Since = since
        self.config.Until = until
        self.config.Lang = language
        self.config.Store_csv = True
        self.config.User_full = True

        twint.run.Search(self.config)

