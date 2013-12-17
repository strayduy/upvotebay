#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Entry point for all things, to avoid circular imports.
'''

# Standard libs
import os

# Our libs
from .app import create_app
from .settings import DevConfig, ProdConfig

env = os.getenv('UPVOTEBAY_ENV', 'dev')

if env.lower() == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)
