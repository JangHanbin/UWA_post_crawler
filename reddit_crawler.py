import requests
from datetime import datetime
import sqlalchemy as db
import logging
from time import sleep

def get_content(url):

    content = None
    retry_count = 0
    while retry_count < 5:
        try:
            content = requests.get(url, timeout=30).content
            break
        except Exception as e:
            retry_count += 1
            logging.getLogger('logger').warning('Failed to get content data. wait for 60 secs... [{0}]'.format(retry_count))
            sleep(60)


    return content


def parse_post(post):

    id = post['id']
    num_comments = post['numComments']
    created = datetime.fromtimestamp(post['created']/1000.0)
    score = post['score']
    distinguish_type = post['distinguishType']
    is_locked  = post['isLocked']
    is_stickied = post['isStickied']
    thumbnail = get_content(post['thumbnail']['url']) if post['thumbnail']['url'].endswith('.jpg') else None
    title = post['title']
    author = post['author']
    author_id = post['authorId']
    domain = post['domain']
    view_count = post['viewCount']
    gold_count = post['goldCount']
    is_archived = post['isArchived']
    contest_mod = post['contestMode']
    suggested_sort = post['suggestedSort']
    hidden = post['hidden']
    saved = post['saved']
    is_gildable = post['isGildable']
    is_media_only = post['isMediaOnly']
    is_sponsored = post['isSponsored']
    is_NSFW = post['isNSFW']
    is_meta = post['isMeta']
    is_spoiler = post['isSpoiler']
    is_blank = post['isBlank']
    send_replies = post['sendReplies']
    vote_state = post['voteState']
    permalink = post['permalink']
    preview = post['preview']['url'] if post.get('preview') else None
    num_crossports = post['numCrossposts']
    is_crossportable = post['isCrosspostable']
    live_comments_websocket = post['liveCommentsWebsocket']
    is_original_content = post['isOriginalContent']
    is_score_hidden = post['isScoreHidden']

    return [id, num_comments, created, score, distinguish_type, is_locked, is_stickied, thumbnail, title, author, author_id, domain, view_count,
            gold_count, is_archived, contest_mod, suggested_sort, hidden, saved, is_gildable, is_media_only, is_sponsored, is_NSFW, is_meta,
            is_spoiler, is_blank, send_replies, vote_state, permalink, preview, num_crossports, is_crossportable, live_comments_websocket,
            is_original_content, is_score_hidden]


def parse_subreddit(subreddit):
    id = subreddit['id']
    allow_chat_post_creation = subreddit['allowChatPostCreation']
    is_chat_post_feature_enabled = subreddit['isChatPostFeatureEnabled']
    display_text = subreddit['displayText']
    type = subreddit['type']
    is_quarantined = subreddit['isQuarantined']
    is_NSFW = subreddit['isNSFW']
    name = subreddit['name']
    url = subreddit['url']
    title = subreddit['title']
    whitelist_status = subreddit['whitelistStatus']
    wls = subreddit['wls']
    community_icon = get_content(subreddit['communityIcon']) if subreddit['communityIcon'] else None
    subscribers = subreddit['subscribers']
    free_form_reports = subreddit['freeFormReports'] if subreddit.get('freeFormReports') else None


    return [id, allow_chat_post_creation, is_chat_post_feature_enabled, display_text, type, is_quarantined, is_NSFW, name, url,
            title, whitelist_status, wls, community_icon, subscribers, free_form_reports]


def parse_awarding(awards):

    award_type = awards['awardType']
    award_sub_type = awards['awardSubType']
    coin_price = awards['coinPrice']
    coin_reward = awards['coinReward']
    days_of_drip_extension = awards['daysOfDripExtension']
    days_of_premium = awards['daysOfPremium']
    description = awards['description']
    icon = get_content(awards['iconUrl']) if awards['iconUrl'] else None
    icon_width = awards['iconWidth']
    icon_height = awards['iconHeight']
    id = awards['id']
    is_enabled = awards['isEnabled']
    is_new = awards['isNew']
    name = awards['name']
    subreddit_count_reward = awards['subredditCoinReward']
    subreddit_id = awards['subredditId']
    count = awards['count']

    return [award_type, award_sub_type, coin_price, coin_reward, days_of_drip_extension, days_of_premium, description, icon, icon_width, icon_height,
            id, is_enabled, is_new, name, subreddit_count_reward, subreddit_id, count]


def parse_source(src):

    display_text = src['displayText']
    url = src['url']
    outbound_url = src['outboundUrl']

    outbound_expiration = datetime.fromtimestamp(src['outboundUrlExpiration'] / 1000.0) if src['outboundUrlExpiration'] else None
    outbound_created = datetime.fromtimestamp(src['outboundUrlCreated'] / 1000.0) if src['outboundUrlCreated'] else None

    return [display_text, url, outbound_url, outbound_expiration, outbound_created]

def parse_media(media):

    result = list()
    type = media['type']

    if type =='rtjson':
        result = parse_richtext(media['richtextContent']['document'])

    elif type == 'gifvideo':
        result = parse_gifvideo(media)

    elif type == 'embed':
        result = parse_embed(media)

    elif type =='image':
        result = parse_image(media)

    else:
        logging.getLogger('logger').warning('Not defined type : {0}'.format(type))

    return [type, result]


def parse_rtjson(line, document):

    converted_text = str()

    for words in line:
        # print('WORDS : {0}'.format(words))
        try:
            if words.get('c'):
                converted_text+= '\t' + parse_rtjson(words['c']) # recursive
        except:
            logging.getLogger('logger').exception('@@@@@@@ {0}'.format(document))
            exit(11)

        else:
            if words['e'] == 'text':
                converted_text += words['t']
            if words['e'] == 'link':
                converted_text += '{0} ({1})'.format(words['t'], words['u'])
            if words['e'] == 'r/':
                if words['l']:
                    converted_text += 'r/{0} (https://reddit.com/r/{0})'.format(words['t'])
                else:
                    converted_text += 'r/{0}'.format(words['t'])

    return converted_text


def parse_richtext(document):

    origin_json = str(document)
    converted_text = str()

    for line in document:
        if line.get('c'):
            converted_text += parse_rtjson(line['c'], document) + '\n'

    return [origin_json, converted_text]


def parse_gifvideo(media):

    content_url = media['content']
    content =  get_content(media['content']) if media['content'] else None
    width = media['width']
    height = media['height']

    return [content_url, content, width, height]


def parse_embed(media):

    content = media['content']
    width = media['width']
    height = media['height']
    provider = media['provider']

    return [content, width, height, provider]


def parse_image(media):

    content_url = media['content']
    content  = get_content(media['content']) if media['content'] else None
    width = media['width']
    height = media['height']

    return [content_url, content, width, height]


class Reddit:
    def __init__(self):
        self.logger = logging.getLogger('logger')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('[ %(levelname)s | %(filename)s: %(lineno)s] %(asctime)s > %(message)s')
            file_handler = logging.FileHandler('log.log')
            file_handler.setFormatter(formatter)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)


    def connect_to_db(self, id,password, host, db_name):
        self.engine = db.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(id,password,host,db_name),  pool_pre_ping=True)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

        # tables
        self.posts = db.Table('posts', self.metadata, autoload=True, autoload_with=self.engine)
        self.subreddits = db.Table('subreddits', self.metadata, autoload=True, autoload_with=self.engine)
        self.awardings = db.Table('awardings', self.metadata, autoload=True, autoload_with=self.engine)
        self.sources = db.Table('sources', self.metadata, autoload=True, autoload_with=self.engine)
        self.media = db.Table('media', self.metadata, autoload=True, autoload_with=self.engine)
        self.richtext = db.Table('richtext', self.metadata, autoload=True, autoload_with=self.engine)
        self.gifvideo = db.Table('gifvideo', self.metadata, autoload=True, autoload_with=self.engine)
        self.embed = db.Table('embed', self.metadata, autoload=True, autoload_with=self.engine)
        self.image = db.Table('image', self.metadata, autoload=True, autoload_with=self.engine)



    def search(self, keyword, after):
        headers = {
            'authority': 'gateway.reddit.com',
            'x-reddaid': '7DC6PV6WWLDIIJAA',
            'sec-fetch-dest': 'empty',
            'x-reddit-loid': '00000000004996r65y.2.1580651318371.Z0FBQUFBQmVYNjdzai1zek1NMG9pZ2lscjdiOW85dWR2WHFsVHRWMDNqRWxsS1FkbXplN0NqbWtKQnRuQlBUOHRBNW1tSmY5eDQwUzJwX0IzUlp5LUcxa2VxQWJNOXhKTEk5QkRFUEM4c2cxRUZvRXFnYXFtQW53ekxhZHdTc1NrY2ZhZkJ6dlhEMGw',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'x-reddit-session': '8TwZWE9qZ6TEC0oXBu.0.1583329180964.Z0FBQUFBQmVYNi1kVEZmSk84Tmo2MUNoRWt1QXQ4aGtQc0dQWFloQ1EtcUVlazBtems1TmY2Uzc3TWpHNG1yOERNbWhSaVQyaFhUbnducTRRekNXVVVkVGlSd0hxM3BCcENhbFFDVE9IZVZGNFdXZFBWalpBVzNFcEZNUHRzX3NJOUxUMlJxVDNFQnA',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://www.reddit.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.reddit.com/',
            'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
        }

        params = (
            ('rtj', 'only'),
            ('allow_over18', ''),
            ('include', 'structuredStyles,prefsSubreddit'),
            ('q', keyword),
            ('sort', 'relevance'),
            ('t', 'all'),
            ('after', after),
            ('type', 'link'),
            ('b', 'true'),
            # ('limit', 1)
            # ('search_correlation_id', 'b63eef90-3c97-4231-8b0c-ec64eec628a8'),
        )

        res = requests.get('https://gateway.reddit.com/desktopapi/v1/search', headers=headers, params=params)

        for post_id, post_content in res.json()['posts'].items():

            post = parse_post(post_content)
            row_count = self.insert_post(post)

            if row_count ==0:
                self.logger.exception('tried to Insert Duplicate entry in post')
                continue
            self.logger.info('Success to insert : {0}'.format(post))



            post_subreddit = res.json()['subreddits'][post_content['belongsTo']['id']]
            subreddit = parse_subreddit(post_subreddit)
            subreddit.insert(0, post_id)  # add pk
            self.insert_subreddit(subreddit)
            self.logger.info('Success to insert : {0}'.format(subreddit))

            if post_content.get('allAwardings'):
                for award in post_content['allAwardings']:
                    award_ = parse_awarding(award)
                    award_.insert(0, post_id)
                    self.insert_awarding(award_)
                    self.logger.info('Success to insert : {0}'.format(award_))

            if post_content.get('source'):
                source = parse_source(post_content['source'])
                source.insert(0, post_id)
                self.insert_source(source)
                self.logger.info('Success to insert : {0}'.format(source))


            if post_content.get('media'):
                media = parse_media(post_content['media'])
                type = media[0]
                self.insert_media([post_id, type])
                self.logger.info('Success to insert : {0}'.format([post_id, type]))

                if type == 'rtjson':
                    richtext = media[1]
                    richtext.insert(0, post_id)
                    self.insert_richtext(richtext)
                    self.logger.info('Success to insert : {0}'.format(richtext))

                elif type == 'gifvideo':
                    gifvideo = media[1]
                    gifvideo.insert(0, post_id)
                    self.insert_gifvideo(gifvideo)
                    self.logger.info('Success to insert : {0}'.format(gifvideo))

                elif type == 'embed':
                    embed = media[1]
                    embed.insert(0, post_id)
                    self.insert_embed(embed)
                    self.logger.info('Success to insert : {0}'.format(embed))

                elif type == 'image':
                    image = media[1]
                    image.insert(0, post_id)
                    self.insert_image(image)
                    self.logger.info('Success to insert : {0}'.format(image))

        return res.json()['tokens']['posts']

    def insert_post(self, post):
        query = db.insert(self.posts).values(post).prefix_with('IGNORE')
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_subreddit(self, subreddit):
        query = db.insert(self.subreddits).values(subreddit)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_awarding(self, awarding):
        query = db.insert(self.awardings).values(awarding)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_source(self, source):
        query = db.insert(self.sources).values(source)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_media(self, media):
        query = db.insert(self.media).values(media)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_richtext(self, richtext):
        query = db.insert(self.richtext).values(richtext)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_gifvideo(self, gifvideo):
        query = db.insert(self.gifvideo).values(gifvideo)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_embed(self, embed):
        query = db.insert(self.embed).values(embed)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

    def insert_image(self, image):
        query = db.insert(self.image).values(image)
        result_proxy = self.connection.execute(query)
        return result_proxy.rowcount

