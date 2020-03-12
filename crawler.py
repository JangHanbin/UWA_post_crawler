import requests
from selenium import webdriver
import argparse
import logging
import configparser
from time import sleep
from reddit_crawler import Reddit
from twitter_crawler import Twitter
from youtube_craweler import Youtube


logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[ %(levelname)s | %(filename)s: %(lineno)s] %(asctime)s > %(message)s')
file_handler = logging.FileHandler('log.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def chrome_header_to_dict(headers):
    return dict([[h.partition(':')[0].strip(), h.partition(':')[2].strip()] for h in headers.split('\n')])


if __name__=='__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--keyword', dest='keyword', type=str, default='', required=True)
    parser.add_argument('--target', dest='target', type=str, default='', required=True)
    parser.add_argument('--auth-id', dest='account', type=str, default='')
    parser.add_argument('--auth-pw', dest='password', type=str, default='')
    parser.add_argument('--headers', dest='headers', type=str, default='')

    args = parser.parse_args()
    target = args.target.lower()

    config = configparser.ConfigParser()
    config.read('dbconfig.ini')

    host = config['DEFAULT']['HOST']
    id = config['DEFAULT']['ID']
    passwd = config['DEFAULT']['PASSWD']

    API_config = configparser.ConfigParser()
    API_config.read('API_Keys.ini')


    if target == 'twitter':
        if not args.account or not args.password or not args.headers:
            raise ValueError('Twitter must be given id, password, headers information.')

        twitter = Twitter(args.account, args.password)

        db = config[target]['DATABASE']
        twitter.connect_to_db(id,passwd,host,db)
        user_headers = configparser.ConfigParser()
        user_headers.read('headers.ini')

        twitter.set_request_headers(dict(user_headers._sections[args.headers]))
        twitter.search(args.keyword)

    elif target == 'reddit':

        # if not (args.account or args.password):
        #     raise ValueError('Reddit needs to ID and PW for access API')

        # DB connection
        db = config[target]['DATABASE']

        # API connection
        reddit = Reddit()
        reddit.connect_to_db(id,passwd,host,db)

        after = ''
        while True:
            after = reddit.search(args.keyword, after)

            if not after:
                reddit.logger.info('Reached end of the Searching. Wait 600 Secs...')
                sleep(600)

        # reddit.extract_comments('3g1jfi')

    elif target == 'youtube':
        youtube = Youtube()
        db = config[target]['DATABASE']


    else:
        raise ValueError('Target not supported.')





