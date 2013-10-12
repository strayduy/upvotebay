# -*- coding: utf-8 -*-

# Standard libs
import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'lulz')
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # reddit oauth credentials
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI', '')

class ProdConfig(Config):
    DEBUG = False

class DevConfig(Config):
    DEBUG = True
