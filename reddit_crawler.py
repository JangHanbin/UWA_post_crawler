import praw
from praw.models import MoreComments
class Reddit:
    def __init__(self,client_id, reddit_id, reddit_pw, api_key):
        self.reddit = praw.Reddit(client_id=client_id,
                     client_secret=api_key,
                     user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 by /u/d0rk94',
                     username=reddit_id,
                     password=reddit_pw)


    def login(self,id, pw):
        pass

    def extract_comments(self,submission_id):
        submission = self.reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            print(comment.body)
        # for top_level_comment in submission.comments:
        #     if isinstance(top_level_comment, MoreComments):
        #         continue
        #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        #     print(top_level_comment.body)
        #     # print(top_level_comment.replies.list())
        #     # exit(10)
        #     for second_level_comment in top_level_comment.replies.list():
        #         if isinstance(second_level_comment, MoreComments):
        #             continue
        #         print('\t>',end='')
        #         print(second_level_comment.body)
        #
        #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n\n\n')
    def search(self):
        pass
