import requests
import json
from urllib.parse import parse_qs
from time import sleep
from datetime import datetime
import sqlalchemy as db
import logging
from selenium import webdriver




def parse_tweet(tweet):

    id_str = int(tweet.get('id_str'))
    id = tweet.get('id')
    created_at = datetime.strptime(tweet.get('created_at'),'%a %b %d %H:%M:%S %z %Y')
    if created_at.timestamp() < 0:
        created_at = None
    text = tweet['full_text'] if tweet.get('full_text') else tweet['text']
    source = tweet.get('source')
    truncated = tweet.get('truncated')
    in_reply_to_status_id = tweet.get('in_reply_to_status_id')
    in_reply_to_user_id = tweet.get('in_reply_to_user_id')
    in_reply_to_screen_name = tweet.get('in_reply_to_screen_name')
    quoted_status_id = tweet.get('quoted_status_id')
    is_quote_status = tweet.get('is_quote_status')
    quote_count = tweet.get('quote_count')
    reply_count = tweet.get('reply_count')
    retweet_count = tweet.get('retweet_count')
    favorite_count = tweet.get('favorite_count')
    favorited = tweet.get('favorited')
    retweeted = tweet.get('retweeted')
    possibly_sensitive = tweet.get('possibly_sensitive')
    filter_level = tweet.get('filter_level')
    lang = tweet.get('lang')
    retweeted_status_id = int(tweet['retweeted_status'].get('id_str')) if tweet.get('retweeted_status') else None # if


    return [id_str, id, created_at, text, source, truncated, in_reply_to_status_id, in_reply_to_user_id, in_reply_to_screen_name, quoted_status_id,
            is_quote_status, quote_count, reply_count, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive, filter_level, lang,
            retweeted_status_id]


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
    if created_at.timestamp() < 0:
        created_at = None
    profile_banner_url = user.get('profile_banner_url')
    profile_image_url_https = user.get('profile_image_url_https')
    default_profile = user.get('default_profile')
    default_profile_image = user.get('default_profile_image')
    withheld_in_countries = ', '.join((user.get('withheld_in_countries'))) if user.get('withheld_in_countries') else None
    withheld_scope = user.get('withheld_scope')

    return [id, id_str, name, screen_name, location, url, description, protected, verified, followers_count, friends_count, listed_count, favourites_count,
            statuses_count, created_at, profile_banner_url, profile_image_url_https, default_profile, default_profile_image, withheld_in_countries, withheld_scope]


def parse_coordinates(coordinate):
    return [str(coordinate.get('coordinates')).strip('[]'), coordinate.get('type')]


def parse_place(place):
    id = place.get('id')
    url = place.get('url')
    place_type = place.get('place_type')
    name = place.get('name')
    full_name = place.get('full_name')
    country_code = place.get('country_code')
    country = place.get('country')
    bounding_box = str(place.get('bounding_box')) # convert to simple str.

    return [id, url, place_type, name, full_name, country_code, country, bounding_box]


def parse_hashtag(hashtag):

    result = list()

    for hash in hashtag:
        result.append([str(hash.get('indices')).strip('[]'), hash.get('text')])

    return result

def parse_media(media):
    result = list()

    for media_ in media:
        display_url = media_.get('display_url')
        expanded_url = media_.get('expanded_url')
        id = media_.get('id')
        indices = str(media_.get('indices')).strip('[]')
        media_url = media_.get('media_url')
        media_url_https = media_.get('media_url_https')
        source_status_id = media_.get('source_status_id')
        type = media_.get('type')
        url = media_.get('url')

        data_retry_count=0
        while data_retry_count<5:
            try:
                headers = {
                    'authority': 'pbs.twimg.com',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                    'sec-fetch-dest': 'document',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
                }
                data = requests.get(media_url,headers=headers).content
                break
            except:
                data_retry_count+=1
                sleep(60)
                logging.warning('Failed to get media data. wait for 60 secs... [{0}]'.format(data_retry_count+1))


        result.append([display_url, expanded_url, id, indices, media_url, media_url_https, source_status_id, type, url, data])

    return result

def parse_url(url):
    result = list()

    for url_ in url:
        result.append([url_.get('display_url'), url_.get('expanded_url'), str(url_.get('indices')).strip('[]'), url_.get('url')])

    return result

def parse_user_mention(mention):
    result = list()

    for mention_ in mention:
        result.append([mention_.get('id'), str(mention_.get('indices')).strip('[]'), mention_.get('name'), mention_.get('screen_name')])

    return result

def parse_symbol(symbol):
    result = list()

    for symbol_ in symbol:
        result.append([str(symbol_.get('indices')).strip('[]'), symbol_.get('text')])

    return result



class Twitter:
    # Will use Twitter APIs
    def __init__(self,id, passwd):
        # self.api= tw.Api(key,secret_key,token,token_secret)
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[ %(levelname)s | %(filename)s: %(lineno)s] %(asctime)s > %(message)s')
        file_handler = logging.FileHandler('log.log')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.id = id
        self.passwd = passwd
        self.cookies = dict()
        self.login(id,passwd)

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

        # to be defined
        # options = webdriver.ChromeOptions()
        # # options.add_argument('headless')
        #
        # with webdriver.Chrome('./chromedriver', options=options) as driver:
        #     driver.implicitly_wait(60)
        #     driver.get('https://www.twitter.com')
        #     driver.find_element_by_name('session[username_or_email]').send_keys(id)
        #     driver.find_element_by_name('session[password]').send_keys(pw)
        #     driver.find_element_by_name('session[password]').submit()
        #
        #     for i in driver.find_elements_by_tag_name('input'):
        #         i.send_keys('corona')
        #         i.submit()
        #
        #
        #
        #     for cookie in driver.get_cookies():
        #         self.cookies.update({cookie['name']:cookie['value']})




    def search(self, keyword):

        # if keyword[0]!='#':
        #     keyword = '#'+keyword

        headers = {
            'authority': 'api.twitter.com',
            'x-twitter-client-language': 'en',
            'x-csrf-token': '03dffd0f47d95b4c57ebe4febb5eb608',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'sec-fetch-dest': 'empty',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'accept': '*/*',
            'origin': 'https://twitter.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://twitter.com/home',
            'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
            'cookie': 'ct0=03dffd0f47d95b4c57ebe4febb5eb608; personalization_id="v1_j0AZi1zx8Du6rp1cuVy9gg=="; guest_id=v1%3A158282257475598345; _ga=GA1.2.1910892442.1582822576; _gid=GA1.2.1352091348.1582822576; gt=1233073366342356993; dnt=1; ads_prefs="HBESAAA="; kdt=im9KJgxfQbiqzkMzfUXZXH5tLURXD2uyq24CCNuz; remember_checked_on=1; auth_token=baa0aa64bb45cc004c9f3461dd369923b97950ce; csrf_same_site_set=1; rweb_optin=side_no_out; csrf_same_site=1; twid=u%3D1223956457223159813; _gat=1',
        }


        params = {'q': keyword, 'tweet_mode': 'extended', 'result_type': 'mixed', 'count': 200}
        # print(headers['x-csrf-token'])
        # print(self.cookies)
        # headers['x-csrf-token'] = self.cookies['csrf']
        # print(headers['x-csrf-token'])

        while True:

            res = requests.get('https://api.twitter.com/1.1/search/tweets.json', headers=headers, params=params)
            # print(res.text)
            if res.status_code != 200:
                for error in res.json()['errors']:
                    if error['code']==32:
                        # re login to update tokens
                        self.login(self.id, self.passwd)
                        headers['x-csrf-token']=self.cookies['csrf']
                        continue
                self.logger.warning('Failed to access to api. wait 60 secs....')
                print(res.text)
                sleep(60)

                continue

            for tweet in json.loads(res.text)['statuses']:

                primary_key = int(tweet['id_str'])
                try:
                    tweet_ = parse_tweet(tweet)
                    tweet_.append(keyword)
                    tweet_.append(datetime.now())
                    self.insert_tweet(tweet_)
                    self.logger.info('Success to insert : {0}'.format(tweet_))

                except Exception as e:
                    self.logger.exception('Tweet Insert Err')
                    self.logger.exception(e)
                    continue

                user = parse_user(tweet['user'])
                user.insert(0,primary_key)

                if tweet.get('place'):
                    place = parse_place(tweet.get('place'))
                    place.insert(0,primary_key)
                    self.insert_place(place)
                    self.logger.info('Success to insert : {0}'.format(place))

                if tweet.get('user'):
                    user = parse_user(tweet.get('user'))
                    user.insert(0,primary_key)
                    self.insert_users(user)
                    self.logger.info('Success to insert : {0}'.format(user))

                if tweet.get('coordinates'):
                    coordinates = parse_coordinates(tweet.get('coordinates'))
                    coordinates.insert(0, primary_key)
                    self.insert_coordinates(coordinates)
                    self.logger.info('Success to insert : {0}'.format(coordinates))

                if tweet.get('entities'):
                    if tweet['entities'].get('hashtags'):
                        hashs= parse_hashtag(tweet['entities'].get('hashtags'))
                        for hash in hashs:
                            hash.insert(0, primary_key)
                            self.insert_hashtag(hash)
                            self.logger.info('Success to insert : {0}'.format(hash))

                    if tweet['entities'].get('symbols'):
                        symbols = parse_symbol(tweet['entities'].get('symbols'))
                        for symbol in symbols:
                            symbol.insert(0, primary_key)
                            self.insert_symbol(symbol)
                            self.logger.info('Success to insert : {0}'.format(symbol))

                    if tweet['entities'].get('user_mentions'):
                        mentions = parse_user_mention(tweet['entities'].get('user_mentions'))
                        for mention in mentions:
                            mention.insert(0, primary_key)
                            self.insert_user_mention(mention)
                            self.logger.info('Success to insert : {0}'.format(mention))


                    if tweet['entities'].get('urls'):
                        urls = parse_url(tweet['entities'].get('urls'))
                        for url in urls:
                            url.insert(0, primary_key)
                            self.insert_url(url)
                            self.logger.info('Success to insert : {0}'.format(url))

                    if tweet['entities'].get('media'):
                        media = parse_media(tweet['entities'].get('media'))
                        for media_ in media:
                            media_.insert(0,primary_key)
                            self.insert_media(media_)
                            self.logger.info('Success to insert : {0}'.format(media_[:-1])) # except binary data

                if tweet.get('extended_entities'):
                    if tweet['extended_entities'].get('media'):
                        media = parse_media(tweet['extended_entities'].get('media'))
                        for media_ in media:
                            media_.insert(0, primary_key)
                            self.insert_media(media_)
                            self.logger.info('Success to insert : {0}'.format(media_[:-1]))  # except binary data



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

