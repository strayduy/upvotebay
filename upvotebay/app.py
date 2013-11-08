# -*- coding: utf-8 -*-

# Standard libs
import os

# Third party libs
from flask import Flask
from flask.ext.mako import MakoTemplates
import praw

def create_app(config_object, env):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['ENV'] = env

    # Use Mako instead of Jinja
    mako = MakoTemplates(app)

    # Register blueprints
    from .modules import public
    from .modules import oauth
    from .modules import my
    app.register_blueprint(public.blueprint)
    app.register_blueprint(oauth.blueprint)
    app.register_blueprint(my.blueprint, url_prefix='/my')

    return app
