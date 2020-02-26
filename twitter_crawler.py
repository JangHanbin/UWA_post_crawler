import twitter as tw
import requests
import json
from urllib.parse import parse_qs
from time import sleep
from datetime import datetime
import sqlalchemy as db

def parse_tweet(tweet):

    id_str = int(tweet.get('id_str'))
    id = tweet.get('id')
    create_at = datetime.strptime(tweet.get('created_at'),'%a %b %d %H:%M:%S %z %Y')
    text = tweet['full_text'] if tweet.get('full_text') else tweet['text']
    source = tweet.get('source')
    truncated = tweet.get('truncated')
    in_reply_to_status_id = tweet.get('in_reply_to_status_id')
    in_reply_to_user_id = tweet.get('in_reply_to_user_id')
    in_reply_to_screen_name = tweet.get('in_reply_to_screen_name')
    quoted_status_id = tweet.get('quoted_status_id')
    is_quote_status = tweet.get('is_quote_staus')
    qoute_count = tweet.get('quote_count')
    reply_count = tweet.get('reply_count')
    retweet_count = tweet.get('retweet_count')
    favorite_count = tweet.get('favorite_count')
    favorited = tweet.get('favorited')
    retweeted = tweet.get('retweeted')
    possibly_sensitive = tweet.get('possibly_sensitive')
    filter_level = tweet.get('filter_level')
    lang = tweet.get('lang')

    return [id_str, id, create_at, text, source, truncated, in_reply_to_status_id, in_reply_to_user_id, in_reply_to_screen_name, quoted_status_id,
            is_quote_status, qoute_count, reply_count, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive, filter_level, lang]


def parse_user(user):
    pass

def parse_coordinates(coordinate):
    pass

def parse_place(place):
    pass

def parse_hashtag(hashtag):
    pass

def parse_media(media):
    pass

def parse_url(url):
    pass

def parse_user_mention(mention):
    pass

def parse_symbol(symbol):
    pass


def parse_response(res):

    tweet = parse_tweet(res)

    return tweet


    # if .get('full_text'):
    #     print(i.get('full_text'))
    # elif i.get('text'):
    #     print(i.get('text'))
    # else:
    #     print('Something wrong')


class Twitter:
    # Will use Twitter APIs
    def __init__(self, key, secret_key, token,token_secret):
        self.api= tw.Api(key,secret_key,token,token_secret)

    def connect_to_db(self, id,password, host, db_name):
        self.engine = db.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(id,password,host,db_name))
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

        # tables
        self.tweets = db.Table('tweets', self.metadata, autoload=True, autoload_with=self.engine)
        self.users = db.Table('users', self.metadata, autoload=True, autoload_with=self.engine)
        self.media = db.Table('media', self.metadata, autoload=True, autoload_with=self.engine)
        self.place = db.Table('place', self.metadata, autoload=True, autoload_with=self.engine)
        self.url = db.Table('url', self.metadata, autoload=True, autoload_with=self.engine)
        self.hashtag = db.Table('hashtag', self.metadata, autoload=True, autoload_with=self.engine)
        self.coordinates = db.Table('coordinates', self.metadata, autoload=True, autoload_with=self.engine)
        self.symbol = db.Table('symbol', self.metadata, autoload=True, autoload_with=self.engine)
        self.user_mention = db.Table('user_mention', self.metadata, autoload=True, autoload_with=self.engine)



    def login(self,id, pw):
        pass

    def search(self, keyword):

        if keyword[0]!='#':
            keyword = '#'+keyword

        headers = {
            'authority': 'api.twitter.com',
            'x-twitter-client-language': 'en',
            'x-csrf-token': '4e41cb616906d561145e31b16a741bb0',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'sec-fetch-dest': 'empty',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'accept': '*/*',
            'origin': 'https://twitter.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://twitter.com/search?q=fdfd&src=typed_query',
            'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
            'cookie': '_ga=GA1.2.999650139.1529006038; personalization_id="v1_r5JOCwCltq+bTv6pA/cVuA=="; guest_id=v1%3A158064888176703553; kdt=hMKhExUoshMcQMm8rSm8dsQmQrnMLflLHqFd8PDF; auth_token=e3ee3c00afc206891c70afb7db86cae3233b46e1; dnt=1; csrf_same_site_set=1; rweb_optin=side_no_out; csrf_same_site=1; twid=u%3D1223956457223159813; _gid=GA1.2.1492470375.1582183405; tfw_exp=0; ct0=4e41cb616906d561145e31b16a741bb0; _gat=1',
        }


        params = {'q': keyword, 'tweet_mode': 'extended', 'result_type': 'mixed', 'count': 200}


        while True:

            res = requests.get('https://api.twitter.com/1.1/search/tweets.json', headers=headers, params=params)
            # print(res.text)
            if res.status_code != 200:
                sleep(60)
                continue

            for tweet in json.loads(res.text)['statuses']:
                self.insert_tweet(parse_tweet(tweet))


                # self.insert_tweet(test)

            # Next
            next_qs = res.json()['search_metadata'].get('next_results')
            if next_qs:
                next_params = parse_qs(next_qs[1:])  # to delete param string '?'
                next_params.update({'tweet_mode': 'extended'}) # set mode to extended to get full text
            else:
                # End of the query
                break

            params = next_params


    def insert_tweet(self, tweet):
        query = db.insert(self.tweets).values(tweet)
        result_proxy = self.connection.execute(query)
        # print(result_proxy)
        # exit(199)