# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import json
from flask import Response
from flask.ext.login import current_user
from flask.ext.login import login_required

# Our libs
from upvotebay.utils import reddit_client
from upvotebay.utils import PrawEncoder

blueprint = Blueprint('api',
                      __name__,
                      url_prefix='/api',
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/v1/users/<username>/likes.json')
@reddit_client
def user_likes(username, reddit=None):
    user = reddit.get_redditor(username)
    data = {'likes': [l for l in user.get_liked()]}

    return Response(json.dumps(data, cls=PrawEncoder),
                    mimetype='application/json')

@blueprint.route('/v1/my/likes.json')
@reddit_client
@login_required
def my_likes(reddit=None):
    # Set credentials
    reddit.set_access_credentials(scope=set(current_user.oauth_scope.split(',')),
                                  access_token=current_user.oauth_access_token,
                                  refresh_token=current_user.oauth_refresh_token)

    # Get likes
    user = reddit.get_me()
    data = {'likes': [l for l in user.get_liked()]}

    return Response(json.dumps(data, cls=PrawEncoder),
                    mimetype='application/json')
