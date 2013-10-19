# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import Blueprint
from flask import session
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import login_required

blueprint = Blueprint('my',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@blueprint.route('/profile/')
@login_required
def profile():
    reddit = flask.current_app.reddit

    # Retrieve access info
    oauth_refresh_token = session['oauth_refresh_token']
    access_info = reddit.refresh_access_information(oauth_refresh_token)

    # Get user info
    user = reddit.get_me()
    try:
        liked = user.get_liked()
    except:
        liked = []

    username = session['username']
    return render_template('my/profile.html',
                           user=user,
                           liked=liked)
