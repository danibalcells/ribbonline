from optparse import OptionParser
import logging

from ribbonline.crawl import TwitterCrawler


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():

    parser = OptionParser()

    parser.add_option('-q', '--query', dest='query', type='string',
                      default='#catalunya',
                      help='Query string', metavar='QUERY')
    parser.add_option('-s', '--since', dest='since', default='2017-09-01',
                      help='Period start date', type='string',
                      metavar='START_DATE')
    parser.add_option('-u', '--until', dest='until', default='2018-11-30',
                      help='Period end date', type='string',
                      metavar='END_DATE')
    parser.add_option('-l', '--limit', dest='limit', default=None,
                      help='Limit number of tweets', type='int',
                      metavar='LIMIT')
    parser.add_option('-L', '--language', dest='language', default=None,
                      help='Language of the tweet', type='string',
                      metavar='LANGUAGE')

    options, args = parser.parse_args()
    crawler = TwitterCrawler()
    crawler.crawl(query=options.query,
                  since=options.since,
                  until=options.until,
                  limit=options.limit,
                  language=options.language)


if __name__ == '__main__':
    main()
