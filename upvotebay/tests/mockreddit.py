# -*- coding: utf-8 -*-

# Standard libs
from collections import namedtuple

# Third party libs
from flask import url_for

class MockReddit(object):
    def __init__(self):
        self.user = None
        self.scope = []
        self.refreshable = False

    def get_me(self):
        return self.user

    def get_redditor(self, username):
        redditor = MockRedditUser(username)
        return redditor

    def get_authorize_url(self, state, scope=False, refreshable=False):
        self.scope = scope
        self.refreshable = refreshable
        return url_for('oauth.oauth_callback', state=state)

    def get_access_information(self, code, update_session=True):
        self.user = MockRedditUser('mock_user')
        access_info = {
            'scope': self.scope,
            'access_token': '',
            'refresh_token': '',
        }
        return access_info

    def set_access_credentials(self, scope, access_token, refresh_token=None,
                               update_user=True):
        self.user = MockRedditUser('mock_user')

class MockRedditUser(object):
    def __init__(self, name):
        self.name = name

    def get_liked(self, sort='new', time='all'):
        subreddit = namedtuple('Subreddit', 'display_name')
        subreddit.display_name = 'mockIAma'
        return [MockRedditSubmission('IAmA fake submission. AMA!',
                                     'http://www.example.com',
                                     MockRedditUser('mock_user'),
                                     subreddit)]

class MockRedditSubmission(object):
    def __init__(self, title, url, author, subreddit):
        self.title = title
        self.url = url
        self.author = author
        self.subreddit = subreddit
