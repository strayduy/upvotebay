#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Entry point for all things, to avoid circular imports.
'''

# Standard libs
import os

# Our libs
from .app import create_app

env = os.getenv('UPVOTEBAY_ENV', 'dev')
config_object = 'upvotebay.settings.{env}Config'.format(env=env.capitalize())
app = create_app(config_object, env)
