# -*- coding: utf-8 -*-

# Standard libs
import uuid

# Third party libs
import flask
from flask import Blueprint
from flask import redirect
from flask import session
from flask import url_for
from flask.ext.mako import render_template

# Our libs
from upvotebay.utils import redirect_logged_in_users_to_profile

blueprint = Blueprint('public',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@redirect_logged_in_users_to_profile
def index():
    # Generate a unique key for the authorization URL. We'll check for a
    # matching key in the oauth callback, to protect against cross-site request
    # forgery.
    auth_key = str(uuid.uuid4())
    session['auth_key'] = auth_key
    reddit = flask.current_app.reddit
    auth_url = reddit.get_authorize_url(auth_key,
                                        scope=['identity', 'read'],
                                        refreshable=True)
    return render_template('index.html',
                           auth_url=auth_url)

# Logging out via POST request only
# http://stackoverflow.com/a/14587231
@blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('oauth_refresh_token', None)
    return redirect(url_for('public.index'))
