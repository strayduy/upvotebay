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

blueprint = Blueprint('oauth',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/oauth/callback')
def index():
    # Verify that the provided auth key matches the one that we used to
    # initiate the oauth exchange
    auth_key = request.args.get('state', '')
    if auth_key != session.get('auth_key'):
        # Unauthorized
        abort(401)

    # Retrieve access info
    reddit = flask.current_app.reddit
    access_code = request.args.get('code', '')
    access_info = reddit.get_access_information(access_code)

    # Store oauth refresh token and username
    session['oauth_refresh_token'] = access_info['refresh_token']
    user = reddit.get_me()
    session['username'] = user.name

    return redirect(url_for('my.profile'))
