# -*- coding: utf-8 -*-

# Standard libs
from functools import wraps

# Third party libs
import flask
from flask import json
import praw

def reddit_client(view):
    '''Decorator that initializes a reddit client and passes it to the view.'''
    @wraps(view)
    def wrap(*args, **kwargs):
        config = flask.current_app.config

        # Initialize reddit client
        reddit = praw.Reddit(config['REDDIT_USER_AGENT'])
        reddit.set_oauth_app_info(config['REDDIT_CLIENT_ID'],
                                  config['REDDIT_CLIENT_SECRET'],
                                  config['REDDIT_REDIRECT_URI'])
        kwargs['reddit'] = reddit

        return view(*args, **kwargs)
    return wrap

class PrawEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, praw.objects.Submission):
            return {'title'     : obj.title,
                    'url'       : obj.url,
                    'author'    : obj.author.name,
                    'subreddit' : obj.subreddit.display_name}
        return json.JSONEncoder.default(self, obj)
