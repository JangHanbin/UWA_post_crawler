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
    id = user.get('id')
    id_str = user.get('id_str')
    name = user.get('name')
    screen_name = user.get('screen_name')
    location = user.get('location')
    url = user.get('url')
    description = user.get('description')
    protected = user.get('protected')
    verified = user.get('verified')
    followers_count = user.get('followers_count')
    friends_count = user.get('friends_count')
    listed_count = user.get('listed_count')
    favourites_count = user.get('favourites_count')
    statuses_count = user.get('status_count')
    created_at = datetime.strptime(user.get('created_at'), '%a %b %d %H:%M:%S %z %Y')
    profile_banner_url = user.get('profile_banner_url')
    profile_image_url_https = user.get('profile_image_url_https')
    default_profile = user.get('default_profile')
    default_profile_image = user.get('default_profile_image')
    withheld_in_countries = ', '.join((user.get('withheld_in_countires'))) if user.get('withheld_in_countires') else None
    withheld_scope = user.get('withheld_scope')

    return [id, id_str, name, screen_name, location, url, description, protected, verified, followers_count, friends_count, listed_count, favourites_count,
            statuses_count, created_at, profile_banner_url, profile_image_url_https, default_profile, default_profile_image, withheld_in_countries, withheld_scope]


def parse_coordinates(coordinate):


def parse_place(place):
    pass

def parse_hashtag(hashtag):

    result = list()

    for hash in hashtag:
        result.append([str(hash.get('indices')).strip('[]'), hash.get('text')])

    return result

def parse_media(media):
    pass

def parse_url(url):
    result = list()

    for url_ in url:
        result.append([url_.get('display_url'), url_.get('expanded_url'), str(url_.get('indices')).strip('[]'), url_.get('url')])

def parse_user_mention(mention):
    result = list()

    for mention_ in mention:
        result.append([mention_.get('id'), str(mention_.get('indices')).strip('[]'), mention_.get('name'), mention_.get('screen_name')])

    return result

def parse_symbol(symbol):
    result = list()

    for symbol_ in symbol:
        result([str(symbol_.get('indices')).strip('[]'), symbol_.get('text')])

    return result



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

                primary_key = int(tweet['id_str'])
                try:
                    tweet_ = parse_tweet(tweet)
                    tweet_.append(keyword)
                    tweet_.append(datetime.now())
                    self.insert_tweet(tweet_)

                except Exception as e:
                    # logger
                    print(e)

                    user = parse_user(tweet['user'])
                    user.insert(0,primary_key)

                if tweet.get('entities'):
                    if tweet['entities'].get('hashtags'):
                        hashs= parse_hashtag(tweet['entities'].get('hashtags'))
                        for hash in hashs:
                            hash.insert(0, primary_key)
                            self.insert_hashtag(hash)

                    if tweet['entities'].get('symbols'):
                        symbols = parse_symbol(tweet['entities'].get('symbols'))
                        for symbol in symbols:
                            symbol.insert(0, primary_key)
                            self.insert_symbol(symbol)


                    if tweet['entities'].get('user_mentions'):
                        mentions = parse_user_mention(tweet['entities'].get('user_mentions'))
                        for mention in mentions:
                            mention.insert(0, primary_key)
                            self.insert_user_mention(mention)


                    if tweet['entities'].get('urls'):
                        urls = parse_url(tweet['entities'].get('urls'))
                        for url in urls:
                            url.insert(0, primary_key)
                            self.insert_url(url)





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

    def insert_users(self, users):
        query = db.insert(self.users).values(users)
        result_proxy = self.connection.execute(query)

    def insert_media(self, media):
        query = db.insert(self.media).values(media)
        result_proxy = self.connection.execute(query)

    def insert_place(self, place):
        query = db.insert(self.place).values(place)
        result_proxy = self.connection.execute(query)

    def insert_url(self, url):
        query = db.insert(self.url).values(url)
        result_proxy = self.connection.execute(query)

    def insert_hashtag(self, hashtag):
        query = db.insert(self.hashtag).values(hashtag)
        result_proxy = self.connection.execute(query)

    def insert_coordinates(self, coorinates):
        query = db.insert(self.coordinates).values(coorinates)
        result_proxy = self.connection.execute(query)

    def insert_symbol(self, symbol):
        query = db.insert(self.symbol).values(symbol)
        result_proxy = self.connection.execute(query)

    def insert_user_mention(self, mention):
        query = db.insert(self.user_mention).values(mention)
        result_proxy = self.connection.execute(query)

