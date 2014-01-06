# -*- coding: utf-8 -*-

# Standard libs
import uuid

# Third party libs
import flask
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import logout_user
import requests

# Our libs
from upvotebay.extensions import db
from upvotebay.models import User
from upvotebay.utils import reddit_client

blueprint = Blueprint('root',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
@reddit_client
def index(reddit=None):
    if current_user.is_active():
        if current_user.has_confirmed_signup:
            return home()

        return redirect(url_for('root.signup'))

    return landing(reddit)

def landing(reddit):
    oauth_scopes = flask.current_app.config['REDDIT_OAUTH_SCOPES']
    session['auth_key'], auth_url = generate_auth_key_and_auth_url(reddit,
                                                                   oauth_scopes)

    return render_template('landing.html',
                           auth_url=auth_url)

def home():
    return render_template('home.html')

@blueprint.route('/signup')
@login_required
def signup():
    if current_user.is_active() and not current_user.has_confirmed_signup:
        return render_template('signup.html')

    return redirect(url_for('root.index'))

@blueprint.route('/confirm-signup', methods=['POST'])
@reddit_client
@login_required
def confirm_signup(reddit=None):
    reddit.set_access_credentials(scope=set(current_user.oauth_scope.split(',')),
                                  access_token=current_user.oauth_access_token,
                                  refresh_token=current_user.oauth_refresh_token)

    # Check that we can access the user's upvotes
    try:
        user = reddit.get_me()
        likes = [l for l in user.get_liked()]
    except requests.exceptions.HTTPError:
        # If we can't, redirect back to the signup page with an error message
        flash("Sorry, we weren't able to access your upvotes."
              "Could you double-check that they're public?")
        return redirect(url_for('root.signup'))

    # If we can access their upvotes, mark the user as having confirmed signup
    current_user.has_confirmed_signup = True
    db.session.commit()

    return redirect(url_for('root.index'))

@blueprint.route('/u/')
@blueprint.route('/u/<path:extra_path>')
@reddit_client
def user(extra_path=None, reddit=None):
    auth_url = ''

    if not current_user.is_active():
        oauth_scopes = flask.current_app.config['REDDIT_OAUTH_SCOPES']
        session['auth_key'], auth_url = generate_auth_key_and_auth_url(reddit,
                                                                       oauth_scopes)

    return render_template('home.html',
                           current_user=current_user,
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
    logout_user()
    return redirect(url_for('root.index'))
