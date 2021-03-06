# -*- coding: utf-8 -*-

# Standard libs
import calendar
from collections import namedtuple
from datetime import datetime, timedelta
import random

# Third party libs
from flask import url_for

class MockReddit(object):
    DEFAULT_USERNAME = 'mock_user'

    def __init__(self, config):
        self.config = config
        self.user = None
        self.refreshable = False

    def get_me(self):
        return self.user

    def get_redditor(self, username):
        redditor = MockRedditUser(username)
        return redditor

    def get_authorize_url(self, state, scope='identity', refreshable=False):
        self.refreshable = refreshable
        return url_for('oauth.oauth_callback', state=state)

    def get_access_information(self, code, update_session=True):
        self.user = MockRedditUser(self.__class__.get_username())
        access_info = {
            'scope': self.config['REDDIT_OAUTH_SCOPES'],
            'access_token': '',
            'refresh_token': '',
        }
        return access_info

    def set_access_credentials(self, scope, access_token, refresh_token=None,
                               update_user=True):
        self.user = MockRedditUser(self.__class__.get_username())

    @classmethod
    def get_username(cls):
        return cls.DEFAULT_USERNAME

class MockRedditUser(object):
    def __init__(self, name):
        self.name = name

    def get_liked(self, sort='new', time='all'):
        liked = [MockRedditSubmission('IAmA fake submission. AMA!',
                                      'http://www.example.com',
                                      MockRedditUser('mock_user_1'),
                                      'mock_IAmA'),
                 MockRedditSubmission('ELI5: Creating a fake submission',
                                      'http://www.example.com',
                                      MockRedditUser('mock_user_2'),
                                      'mock_explainlikeimfive'),
                 MockRedditSubmission('TIL you can submit fake links',
                                      'http://www.example.com',
                                      MockRedditUser('mock_user_3'),
                                      'mock_todayilearned'),
                 MockRedditSubmission('DAE ask questions?',
                                      'http://www.example.com',
                                      MockRedditUser('mock_user_4'),
                                      'mock_AskReddit'),
                 MockRedditSubmission('A cat',
                                      'http://www.example.com',
                                      MockRedditUser('mock_user_5'),
                                      'mock_awww')]
        random.shuffle(liked)
        return liked

class MockRedditSubmission(object):
    def __init__(self, title, url, author, subreddit):
        self.title = title
        self.url = url
        self.author = author
        self.thumbnail = ''
        self.num_comments = random.randint(0, 1000)
        self.permalink = '#'

        self.subreddit = namedtuple('Subreddit', 'display_name')
        self.subreddit.display_name = subreddit

        created_utc = datetime.now() - timedelta(minutes=random.randint(1, 1000))
        self.created_utc = calendar.timegm(created_utc.utctimetuple())
