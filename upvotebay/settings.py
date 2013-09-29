# -*- coding: utf-8 -*-

# Standard libs
import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'lulz')
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

class ProdConfig(Config):
    DEBUG = False

class DevConfig(Config):
    DEBUG = True
