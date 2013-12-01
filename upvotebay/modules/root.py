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
from upvotebay.utils import reddit_client

blueprint = Blueprint('root',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@reddit_client
def index(reddit=None):
    if not session.get('username'):
        return landing(reddit)

    return home(reddit)

def landing(reddit):
    config = flask.current_app.config

    # Generate a unique key for the authorization URL. We'll check for a
    # matching key in the oauth callback, to protect against cross-site request
    # forgery.
    auth_key = str(uuid.uuid4())
    session['auth_key'] = auth_key
    auth_url = reddit.get_authorize_url(auth_key,
                                        scope=config['REDDIT_OAUTH_SCOPES'],
                                        refreshable=True)
    return render_template('landing.html',
                           auth_url=auth_url)

def home(reddit):
    return render_template('home.html')

@blueprint.route('/u/')
@blueprint.route('/u/<path:extra_path>')
@reddit_client
def user(extra_path=None, reddit=None):
    return render_template('home.html')

# Logging out via POST request only
# http://stackoverflow.com/a/14587231
@blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('oauth_refresh_token', None)
    return redirect(url_for('root.index'))

@blueprint.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@blueprint.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
