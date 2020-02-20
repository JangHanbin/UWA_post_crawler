import twitter as tw
import json

class Twitter:
    # Will use Twitter APIs
    def __init__(self, key, secret_key, token,token_secret):
        self.api= tw.Api(key,secret_key,token,token_secret)


    def login(self,id, pw):
        pass

    def search(self, keyword):

        if keyword[0]!='#':
            keyword = '#'+keyword

        result = self.api.GetSearch(raw_query='q=test&tweet_mode=extended&result_type=mixed&count=1'.format(keyword))
        for r in result:
            print(r)


