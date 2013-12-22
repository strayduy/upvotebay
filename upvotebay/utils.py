# -*- coding: utf-8 -*-

# Standard libs
from functools import wraps

# Third party libs
import flask
from flask import abort
from flask import json
from flask import session
import praw

# Our libs
from .tests.mockreddit import MockReddit
from .tests.mockreddit import MockRedditSubmission

def reddit_client(view):
    # Instantiates a reddit client
    # A new reddit client is instantiated for each view for thread safety
    @wraps(view)
    def wrap(*args, **kwargs):
        config = flask.current_app.config

        if config.get('USE_MOCK_REDDIT_CLIENT'):
            # Initialize mock reddit client
            reddit = MockReddit(config)
        else:
            # Initialize reddit client
            reddit = praw.Reddit(config['REDDIT_USER_AGENT'])
            reddit.set_oauth_app_info(config['REDDIT_CLIENT_ID'],
                                      config['REDDIT_CLIENT_SECRET'],
                                      config['REDDIT_REDIRECT_URI'])
        kwargs['reddit'] = reddit

        return view(*args, **kwargs)
    return wrap

def login_required(view):
    # Raises a 401 HTTP error if the user is not logged in
    @wraps(view)
    def wrap(*args, **kwargs):
        if session.get('username'):
            return view(*args, **kwargs)

        abort(401)
    return wrap

class PrawEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, praw.objects.Submission) or
            isinstance(obj, MockRedditSubmission)):
            return {'title'     : obj.title,
                    'url'       : obj.url,
                    'author'    : obj.author.name,
                    'subreddit' : obj.subreddit.display_name}
        return json.JSONEncoder.default(self, obj)
