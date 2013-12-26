# -*- coding: utf-8 -*-

# Standard libs
import os

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # reddit client settings
    REDDIT_USER_AGENT = 'upvotebay/0.1 by /u/strayharbor'
    REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_REDIRECT_URI = os.environ['REDDIT_REDIRECT_URI']
    REDDIT_OAUTH_SCOPES = ['identity', 'history', 'read', 'mysubreddits']

class ProdConfig(Config):
    DEBUG = False

class TestConfig(Config):
    DEBUG = False
    USE_MOCK_REDDIT_CLIENT = True

class DevConfig(Config):
    DEBUG = True

    # Database settings
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

    # Test settings
    USE_MOCK_REDDIT_CLIENT = (True if os.getenv('USE_MOCK_REDDIT_CLIENT', '').lower()
                                   in ['true', '1']
                                   else False)
