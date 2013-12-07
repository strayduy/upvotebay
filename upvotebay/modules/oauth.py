# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import reddit_client

blueprint = Blueprint('oauth',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/oauth/callback')
@reddit_client
def oauth_callback(reddit=None):
    # Verify that the provided auth key matches the one that we used to
    # initiate the oauth exchange
    auth_key = request.args.get('state', '')
    if auth_key != session.get('auth_key'):
        # Unauthorized
        abort(401)

    # Retrieve access info
    access_code = request.args.get('code', '')
    access_info = reddit.get_access_information(access_code)
    session['access_info'] = {
            'scope'         : list(access_info['scope']),
            'access_token'  : access_info['access_token'],
            'refresh_token' : access_info['refresh_token'],
    }

    # Retrieve username
    user = reddit.get_me()
    session['username'] = user.name

    return redirect(url_for('root.index'))
