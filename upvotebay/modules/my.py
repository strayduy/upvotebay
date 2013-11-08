# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import json
from flask import Response
from flask import session
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import login_required
from upvotebay.utils import reddit_client
from upvotebay.utils import PrawEncoder

blueprint = Blueprint('my',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@blueprint.route('/profile/')
@login_required
def profile():
    username = session['username']
    return render_template('my/profile.html',
                           username=username)

@blueprint.route('/likes.json')
@login_required
@reddit_client
def get_likes(reddit=None):
    # Set credentials
    reddit.set_access_credentials(scope=set(session['access_info']['scope']),
                                  access_token=session['access_info']['access_token'],
                                  refresh_token=session['access_info']['refresh_token'])

    # Get likes
    user = reddit.get_me()
    data = { 'likes' : [l for l in user.get_liked()] }

    return Response(json.dumps(data, cls=PrawEncoder),
                    mimetype='application/json')
