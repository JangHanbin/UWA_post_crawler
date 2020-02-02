import requests
from selenium import webdriver
import argparse
import logging
import configparser
from dbconfig import MysqlController
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

    args = parser.parse_args()
    target = args.target.lower()

    config = configparser.ConfigParser()
    config.read('dbconfig.ini')

    host = config['DEFAULT']['HOST']
    id = config['DEFAULT']['ID']
    passwd = config['DEFAULT']['PASSWD']

    if target == 'twitter':
        twitter = Twitter()
        db = config[target]['DATABASE']
        mysqlController = MysqlController(host, id, passwd, db)

    elif target == 'reddit':
        reddit = Reddit()
        db = config[target]['DATABASE']
        mysqlController = MysqlController(host, id, passwd, db)

    elif target == 'youtube':
        youtube = Youtube()
        db = config[target]['DATABASE']
        mysqlController = MysqlController(host, id, passwd, db)

    else:
        raise ValueError('Target not supported.')





