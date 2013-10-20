# -*- coding: utf-8 -*-

# Standard libs
import os

# Third party libs
from flask import Flask
from flask.ext.mako import MakoTemplates
import praw

def create_app(config_object, env):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['ENV'] = env

    # Use Mako instead of Jinja
    mako = MakoTemplates(app)

    # Initialize reddit client
    reddit = praw.Reddit(app.config['REDDIT_USER_AGENT'])
    reddit.set_oauth_app_info(app.config['REDDIT_CLIENT_ID'],
                              app.config['REDDIT_CLIENT_SECRET'],
                              app.config['REDDIT_REDIRECT_URI'])
    app.reddit = reddit

    # Register blueprints
    from .modules import root
    from .modules import oauth
    from .modules import my
    app.register_blueprint(root.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(my.blueprint, url_prefix='/my')

    return app
