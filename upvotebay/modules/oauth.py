# -*- coding: utf-8 -*-

# Third party libs
import flask
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.ext.login import login_user

# Our libs
from upvotebay.extensions import db
from upvotebay.models import User
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

    # Retrieve access info and reddit user from API
    access_code = request.args.get('code', '')
    access_info = reddit.get_access_information(access_code)
    reddit_user = reddit.get_me()

    # Retrieve User model from DB
    user = User.query.filter_by(username=reddit_user.name).first()

    # If we don't have a record for this user, create one on the spot
    if not user:
        user = User(username=reddit_user.name)
        db.session.add(user)

    # Save access info to User model and update the DB record
    user.set_access_info(access_info)
    db.session.commit()

    # Log in through Flask-Login interface
    login_user(user)

    return redirect(url_for('root.index'))
