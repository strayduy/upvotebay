# -*- coding: utf-8 -*-

# Standard libs
import uuid

# Third party libs
import flask
from flask import Blueprint
from flask import session
from flask.ext.mako import render_template

blueprint = Blueprint('public',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

@blueprint.route('/')
def index():
    # Generate a unique key for the authorization URL. We'll check for a
    # matching key in the oauth callback, to protect against cross-site request
    # forgery.
    auth_key = str(uuid.uuid4())
    session['auth_key'] = auth_key
    auth_url = flask.current_app.reddit.get_authorize_url(auth_key)
    return render_template('index.html',
                           auth_url=auth_url)
