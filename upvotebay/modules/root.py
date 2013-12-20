# -*- coding: utf-8 -*-

# Standard libs
import uuid

# Third party libs
import flask
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

# Our libs
from upvotebay.utils import reddit_client

blueprint = Blueprint('root',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@reddit_client
def index(reddit=None):
    if not is_logged_in():
        return landing(reddit)

    return home(reddit)

def landing(reddit):
    oauth_scopes = flask.current_app.config['REDDIT_OAUTH_SCOPES']
    session['auth_key'], auth_url = generate_auth_key_and_auth_url(reddit,
                                                                   oauth_scopes)

    return render_template('landing.html',
                           auth_url=auth_url)

def home(reddit):
    return render_template('home.html')

@blueprint.route('/u/')
@blueprint.route('/u/<path:extra_path>')
@reddit_client
def user(extra_path=None, reddit=None):
    auth_url = ''

    if not is_logged_in():
        oauth_scopes = flask.current_app.config['REDDIT_OAUTH_SCOPES']
        session['auth_key'], auth_url = generate_auth_key_and_auth_url(reddit,
                                                                       oauth_scopes)

    return render_template('home.html',
                           auth_url=auth_url)

def generate_auth_key_and_auth_url(reddit, scopes, refreshable=True):
    # Generate a unique key for the authorization URL. We'll check for a
    # matching key in the oauth callback, to protect against cross-site request
    # forgery.
    auth_key = str(uuid.uuid4())

    auth_url = reddit.get_authorize_url(auth_key,
                                        scope=scopes,
                                        refreshable=refreshable)

    return auth_key, auth_url

# Logging out via POST request only
# http://stackoverflow.com/a/14587231
@blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('oauth_refresh_token', None)
    return redirect(url_for('root.index'))

def is_logged_in():
    return bool(session.get('username'))

@blueprint.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@blueprint.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
